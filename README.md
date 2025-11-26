# Gerenciador de Estudos e Trilhas de Aprendizagem

Projeto em Python que organiza **Trilhas → Cursos → Aulas → Tarefas** e aplica POO com padrões de projeto (**Factory**, **Strategy** e **Decorator**).

> **Objetivo:** acompanhar a evolução do estudante em trilhas de aprendizagem, permitindo trocar o algoritmo de cálculo de progresso sem modificar as classes de domínio.

---

## Visão geral da modelagem

- Uma **Trilha** reúne vários **Cursos**.
- Cada **Curso** possui uma lista de **Aulas**.
- Cada **Aula** contém uma lista de **Tarefas de estudo** polimórficas:
  - `TarefaLeitura`
  - `TarefaPratica`
  - `TarefaQuiz`
  - `TarefaProjeto`
- As tarefas herdam da classe abstrata `TarefaEstudo` e usam o `Enum StatusTarefa` para controlar o ciclo de vida (**A_FAZER**, **EM_ANDAMENTO**, **CONCLUIDA**).
- O cálculo do **progresso da trilha** é delegado a objetos `EstrategiaProgresso` (padrão **Strategy**).
- A classe `TarefaComPrazo` envolve uma tarefa existente para aplicar penalidade em caso de atraso (padrão **Decorator**).
- A criação das tarefas concretas é centralizada em `TarefaFactory`, que recebe o tipo em formato de texto (`"leitura"`, `"quiz"`, `"pratica"`, `"projeto"`).

---

## Padrões e pilares de POO utilizados

### Abstração e Polimorfismo

- `TarefaEstudo` é uma **classe abstrata** que define a interface comum das tarefas de estudo:

```python
from abc import ABC, abstractmethod
from .StatusTarefa import StatusTarefa

class TarefaEstudo(ABC):
    @abstractmethod
    def progresso(self):
        """Retorna o progresso da tarefa entre 0.0 e 1.0."""
        pass

    @abstractmethod
    def definir_termino(self):
        """Ações específicas ao concluir a tarefa."""
        pass
```
As classes concretas (`TarefaLeitura`, `TarefaPratica`, `TarefaQuiz`, `TarefaProjeto`) implementam `progresso()` de formas diferentes, mas a assinatura do método é a mesma.

Dessa forma, `Aula`, `Curso` e `Trilha` podem tratar qualquer tarefa apenas como `TarefaEstudo` e chamar `progresso()` de forma polimórfica, sem precisar saber qual é o subtipo exato de tarefa.

### Encapsulamento

- Cada classe de tarefa valida e protege seus próprios dados usando `@property`, garantindo consistência interna.
```python
# src/model/TarefaLeitura.py (trecho)

@property
def total_paginas(self):
    return self.__total_paginas

@total_paginas.setter
def total_paginas(self, valor):
    # garante inteiro >= 1
    ...
```
Isso evita estados inválidos, como número de páginas igual a 0, valores negativos ou configurações inconsistentes em relação às regras de cada tarefa.

### Herança

- As classes de tarefas concretas herdam de TarefaEstudo:
```python
class TarefaLeitura(TarefaEstudo): ...
class TarefaPratica(TarefaEstudo): ...
class TarefaQuiz(TarefaEstudo): ...
class TarefaProjeto(TarefaEstudo): ...
```
`TarefaComPrazo` também herda de `TarefaEstudo`, mas funciona como um **Decorator**, reaproveitando e estendendo o comportamento da tarefa base que ela envolve.

### Factory

- A classe `TarefaFactory` centraliza a criação das tarefas concretas.  
  Ela recebe o tipo da tarefa em formato de texto (`"leitura"`, `"quiz"`, `"pratica"`, `"projeto"`)
  e devolve uma instância da subclasse correta de `TarefaEstudo`.

```python
# src/model/TarefaFactory.py (exemplo de uso)

from model.TarefaFactory import TarefaFactory

tarefa_quiz = TarefaFactory.criar(
    tipo_tarefa="quiz",
    titulo="Prova 1 de POO",
    nota=8,
    nota_max=10,
)

tarefa_leitura = TarefaFactory.criar(
    tipo_tarefa="leitura",
    titulo="Cap. 1",
    total_paginas=50,
    paginas_lidas=20,
)

print(tarefa_quiz.progresso())    # usa regra de TarefaQuiz
print(tarefa_leitura.progresso()) # usa regra de TarefaLeitura
```
Dessa forma, o código que usa a fábrica não precisa conhecer diretamente
as classes concretas (`TarefaLeitura`, `TarefaPratica`, `TarefaQuiz`, `TarefaProjeto`):
basta informar o tipo em texto e os parâmetros necessários.

### Strategy

- `EstrategiaProgresso` é uma **classe abstrata** que funciona como uma **interface de estratégia**:  
  ela define o método `calcular(trilha)` que todas as estratégias concretas precisam implementar.

```python
# src/model/EstrategiaProgresso.py (trecho)
from abc import ABC, abstractmethod

class EstrategiaProgresso(ABC):
    @abstractmethod
    def calcular(self, trilha) -> float:
        """Recebe uma Trilha e devolve um número entre 0.0 e 1.0."""
        pass
```
- **Implementações concretas:**
 ```python
# src/model/MediaSimplesEstrategia.py (trecho)
from .EstrategiaProgresso import EstrategiaProgresso

class MediaSimplesEstrategia(EstrategiaProgresso):
    def calcular(self, trilha):
        cursos = trilha.cursos
        if not cursos:
            return 0.0
        soma_progresso = sum(curso.progresso() for curso in cursos)
        return soma_progresso / len(cursos)


# src/model/MediaPonderadaPorCargaEstrategia.py (trecho)
from .EstrategiaProgresso import EstrategiaProgresso

class MediaPonderadaPorCargaEstrategia(EstrategiaProgresso):
    def calcular(self, trilha):
        cursos = trilha.cursos
        if not cursos:
            return 0.0

        soma_progresso_ponderado = 0.0
        soma_pesos = 0

        for curso in cursos:
            peso_curso = curso.carga_horas or 1
            soma_progresso_ponderado += curso.progresso() * peso_curso
            soma_pesos += peso_curso

        if soma_pesos == 0:
            return 0.0

        return soma_progresso_ponderado / soma_pesos
```
- A classe `Trilha` apenas **usa** a estratégia recebida: ela chama `estrategia.calcular(self)` sem precisar conhecer os detalhes de cada implementação concreta.
```python
def progresso(self, estrategia):
    if estrategia is None:
        return 0.0
    return estrategia.calcular(self)
```

### Decorator

- `TarefaComPrazo` envolve uma tarefa base (`TarefaEstudo`) e aplica uma penalidade no progresso se a conclusão ocorrer depois do prazo:
```python
# src/model/TarefaComPrazo.py (trecho)

def progresso(self):
    progresso_base = self.__tarefa_base.progresso()

    if (
        self.__prazo is not None
        and self.status == StatusTarefa.CONCLUIDA
        and self.data_realizacao is not None
        and self.data_realizacao > self.__prazo
    ):
        fator = 1.0 - self.__penalidade
        if fator < 0.0:
            fator = 0.0
        progresso_base *= fator

    # garante que o resultado fique entre 0.0 e 1.0
    if progresso_base < 0.0:
        progresso_base = 0.0
    if progresso_base > 1.0:
        progresso_base = 1.0

    return progresso_base
```
Dessa forma, o comportamento da tarefa original é reutilizado e apenas **estendido** com a lógica de prazo e penalidade, garantindo que o resultado final permaneça entre `0.0` e `1.0`.

### Resumo das classes principais

- **Trilha**: agrega vários cursos e calcula o progresso usando uma estratégia (Strategy).
- **Curso**: agrupa aulas e calcula o progresso médio das aulas.
- **Aula**: contém uma lista de tarefas de estudo polimórficas.
- **TarefaEstudo** (abstrata): define a interface comum (`progresso`, `definir_termino`, `exibir_dados`) e o ciclo de vida (`status`).
- **TarefaLeitura / TarefaPratica / TarefaQuiz / TarefaProjeto**: implementam regras específicas de progresso.
- **TarefaComPrazo** (Decorator): envolve uma tarefa e adiciona a lógica de prazo + penalidade.
- **StatusTarefa** (Enum): controla o ciclo de vida da tarefa (`A_FAZER`, `EM_ANDAMENTO`, `CONCLUIDA`).
- **EstrategiaProgresso** + `MediaSimplesEstrategia` / `MediaPonderadaPorCargaEstrategia`: aplicam o padrão Strategy para o cálculo do progresso da trilha.
- **TarefaFactory**: centraliza a criação das tarefas concretas a partir de um tipo textual.

--- 
# Estrutura do projeto, pilares de POO e padrões
```text
gerenciador-trilhas-estudo/
├─ README.md
└─ src/
   ├─ model/
   │  ├─ Aula.py
   │  ├─ Curso.py
   │  ├─ EstrategiaProgresso.py
   │  ├─ MediaPonderadaPorCargaEstrategia.py
   │  ├─ MediaSimplesEstrategia.py
   │  ├─ StatusTarefa.py
   │  ├─ TarefaComPrazo.py
   │  ├─ TarefaEstudo.py
   │  ├─ TarefaFactory.py
   │  ├─ TarefaLeitura.py
   │  ├─ TarefaPratica.py
   │  ├─ TarefaProjeto.py
   │  ├─ TarefaQuiz.py
   │  ├─ Trilha.py
   │  └─ __init__.py
   ├─ testes/
   │  ├─ __init__.py
   │  ├─ guia_como_rodar_local.py
   │  ├─ teste_aula_curso_trilha.py
   │  ├─ teste_decorator_prazo.py
   │  ├─ teste_factory.py
   │  └─ teste_tarefas.py
   └─ diagrama_uml    
```
---
## Testes
Dentro da pasta `src`, execute:
```python
# Tarefas concretas (Leitura, Prática, Quiz, Projeto)
python -m testes.teste_tarefas

# Decorator (TarefaComPrazo)
python -m testes.teste_decorator_prazo

# Aula, Curso, Trilha e Strategy
python -m testes.teste_aula_curso_trilha

# Factory (TarefaFactory)
python -m testes.teste_factory
```
###Teste das tarefas concretas 

**(teste_tarefas.py)**

Comando:
```python
python -m testes.teste_tarefas
```

**O que esse teste faz**

- Cria exemplos de: `TarefaLeitura`, `TarefaPratica`, `TarefaQuiz`, `TarefaProjeto`.
- Atualiza o estado de cada tarefa (páginas lidas, etapas concluídas, nota, entregas aprovadas) e chama `concluir()`.
- Mostra a evolução do progresso antes e depois de concluir.

**Como cada tipo de tarefa calcula o progresso**

- **Leitura** → `paginas_lidas / total_paginas`
- **Prática** → `etapas_concluidas / total_etapas`
- **Quiz** → `nota / nota_max`
- **Projeto** → `entregas_aprovadas / total_entregas`

É montada uma lista de `TarefaEstudo` com tarefas de tipos diferentes, e o código percorre a lista chamando apenas `progresso()`.
**polimorfismo**: o código não precisa saber se é leitura, prática, quiz ou projeto; ele só chama `progresso()`.

**Exemplo de saída**

```text
=== TAREFA LEITURA ===
Antes de concluir:
Status: A FAZER
Progresso: 0.30

Depois de concluir:
Status: CONCLUIDA
Progresso: 1.00
```

**Decorator de prazo (teste_decorator_prazo.py)**

Comando:
```python
python -m testes.teste_decorator_prazo
```

**O que esse teste faz**

- Usa a classe `TarefaComPrazo` como **Decorator** em cima de uma tarefa base.
- Testa dois cenários:
  - **Sem atraso** → prazo no futuro, nenhuma penalidade aplicada.
  - **Com atraso** → prazo no passado, aplica penalidade no progresso.

**Pontos importantes do código**

- `TarefaComPrazo` recebe uma `TarefaEstudo` interna (composição) e:
  - Reaproveita o progresso original da tarefa.
  - Ajusta o valor final de `progresso()` aplicando a penalidade se estiver atrasada.
- Mostra o padrão **Decorator**: altera o comportamento da tarefa sem modificar o código das classes concretas.

**Exemplo de saída**

```text
=== DECORATOR - CASO SEM ATRASO ===
Progresso (sem atraso): 1.00

=== DECORATOR - CASO COM ATRASO ===
Progresso (com atraso): 0.50
````

**Trilha, cursos, aulas e Strategy (teste_aula_curso_trilha.py)**

Comando:
```python
python -m testes.teste_aula_curso_trilha
```

**O que esse teste faz**

- Cria uma trilha de estudos com:
  - Curso de **POO em Python** com duas aulas e várias tarefas.
  - Curso de **Estruturas de Dados** com uma aula prática.
- Associa esses cursos a uma `Trilha`.
- Depois, calcula o progresso da trilha com duas estratégias diferentes:
  - `MediaSimplesEstrategia` → média simples dos progressos dos cursos.
  - `MediaPonderadaPorCargaEstrategia` → média ponderada usando a carga horária de cada curso como peso.

- A classe `Trilha` recebe um objeto que implementa `EstrategiaProgresso`.
- A trilha chama  `estrategia.calcular(self)` para obter o progresso.
- Isso demonstra o padrão **Strategy**: O algoritmo de cálculo do progresso da trilha muda trocando apenas o objeto estratégia, sem alterar o código de `Trilha`.

**Exemplo de saída**

```text
=== DETALHES DOS CURSOS DA TRILHA ===
Curso: Poo Em Python
Progresso do curso: 55%

Curso: Estruturas De Dados
Progresso do curso: 50%

=== PROGRESSO DA TRILHA ===
(Strategy: Média simples)   -> 0.5250
(Strategy: Média ponderada) -> 0.5200
```

**Factory de tarefas (teste_factory.py)**

Comando:
```python
python -m testes.teste_factory
```

**O que esse teste faz**

- Usa `TarefaFactory` para centralizar a criação das tarefas.
- O método estático `criar(tipo_tarefa, **args)`:
  - Recebe uma string (`"leitura"`, `"pratica"`, `"quiz"`, `"projeto"`).
  - Valida os parâmetros obrigatórios (`total_paginas`, `nota_max`, etc.).
  - Retorna a instância da subclasse correta.

**Pontos importantes do código**

- Demonstra o padrão **Factory**:
  - O código que usa as tarefas não precisa saber qual classe concreta instanciar.
  - A lógica de criação fica isolada dentro da `TarefaFactory`.

**Exemplo**

```python
t1 = TarefaFactory.criar(
    tipo_tarefa="leitura",
    titulo="Capítulo 1 - POO",
    total_paginas=100
)

t2 = TarefaFactory.criar(
    tipo_tarefa="quiz",
    titulo="Quiz de Herança",
    nota_max=10
)
````

### Resumo dos conceitos de POO e padrões usados

- `Trilha` → `Curso` → `Aula` → `TarefaEstudo` (`TarefaLeitura`, `TarefaPratica`, `TarefaQuiz`, `TarefaProjeto`)

##### Pilares de POO no código

**Abstração**

- `TarefaEstudo` como classe base abstrata.
- `EstrategiaProgresso` como contrato para as estratégias de cálculo.

**Herança**

- `TarefaLeitura`, `TarefaPratica`, `TarefaQuiz`, `TarefaProjeto` herdam de `TarefaEstudo`.

**Encapsulamento**

- Uso de `@property` para validar atributos (nota, páginas, etapas, prazos).

**Polimorfismo**

- Lista de `TarefaEstudo` tratada de forma genérica, chamando `progresso()` em qualquer tipo de tarefa.
- Diferentes estratégias de progresso tratadas como `EstrategiaProgresso`.

##### Padrões de projeto aplicados

- **Strategy**: cálculo do progresso da trilha com estratégias flexíveis.
- **Decorator**: `TarefaComPrazo` alterando o comportamento da tarefa base.
- **Factory**: `TarefaFactory` centralizando a criação das tarefas concretas(recebe um `tipo_tarefa`, ex.: `"leitura"`, `"pratica"`, `"quiz"`, `"projeto"`) e retorna a instância da subclasse correspondente.







