# Gerenciador de Estudos e Trilhas de Aprendizagem

Projeto em Python que organiza **Trilhas --> Cursos --> Aulas --> Tarefas** e aplica POO com padrões de projeto (**Factory**, **Strategy** e **Decorator**).

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
- A criação das tarefas concretas é centralizada em `TarefaFactory`, usando o `Enum TipoTarefaEstudo` (padrão **Factory**).

---
## Padrões e pilares de POO utilizados

### Abstração e Polimorfismo

- `TarefaEstudo` é uma **classe abstrata** que define a interface comum:

  ```python
  # src/model/TarefaEstudo.py (trecho)
  from abc import ABC, abstractmethod
  from .StatusTarefa import StatusTarefa

  class TarefaEstudo(ABC):
      @abstractmethod
      def progresso(self) -> float:
          """Retorna o progresso da tarefa entre 0.0 e 1.0."""
          pass

      @abstractmethod
      def definir_termino(self):
          """Ações específicas ao concluir a tarefa."""
          pass
  
As classes concretas (`TarefaLeitura`, `TarefaPratica``, TarefaQuiz, TarefaProjeto) implementam progresso() de formas diferentes, mas a interface é a mesma.
Assim, Aula, Curso e Trilha podem tratar qualquer tarefa apenas como TarefaEstudo e chamar progresso() de forma polimórfica.

### Encapsulamento

- Cada classe valida seus próprios dados via @property
```
# src/model/TarefaLeitura.py (trecho)

@property
def total_paginas(self):
    return self.__total_paginas

@total_paginas.setter
def total_paginas(self, valor):
    # garante inteiro >= 1
    ...
```
Isso evita estados inválidos (por exemplo, número de páginas igual a 0, etapas negativas, nota maior que a nota máxima).

###Herança

- As classes de tarefas concretas herdam de TarefaEstudo:
```python
class TarefaLeitura(TarefaEstudo): ...
class TarefaPratica(TarefaEstudo): ...
class TarefaQuiz(TarefaEstudo): ...
class TarefaProjeto(TarefaEstudo): ...
```
TarefaComPrazo também herda de TarefaEstudo, mas funciona como um Decorator, reaproveitando e estendendo o comportamento da tarefa base.

### Enum + Factory

- TipoTarefaEstudo padroniza os tipos de tarefa e evita erros de digitação:
```python

# src/model/TipoTarefaEstudo.py (trecho)
from enum import Enum

class TipoTarefaEstudo(Enum):
    LEITURA = "Leitura"
    QUIZ    = "Quiz"
    PRATICA = "Prática"
    PROJETO = "Projeto"
```
TarefaFactory centraliza a criação das tarefas concretas:
```python
# src/model/TarefaFactory.py (exemplo de uso)
from model.TarefaFactory import TarefaFactory
from model.TipoTarefaEstudo import TipoTarefaEstudo

tarefa_quiz = TarefaFactory.criar(
    tipo=TipoTarefaEstudo.QUIZ,
    titulo="Prova 1 de POO",
    nota=8,
    nota_max=10,
)
```

### Strategy

- EstrategiaProgresso é uma interface para estratégias de cálculo de progresso da Trilha:
```python
# src/model/EstrategiaProgresso.py (trecho)
from abc import ABC, abstractmethod

class EstrategiaProgresso(ABC):
    @abstractmethod
    def calcular(self, trilha) -> float:
        """Recebe uma Trilha e devolve um número entre 0.0 e 1.0."""
        pass
```
Implementações concretas:
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
A Trilha apenas usa a estratégia recebida:
```python
# src/model/Trilha.py (trecho)

def progresso(self, estrategia):
    if estrategia is None:
        return 0.0
    return estrategia.calcular(self)
```

### Decorator

- TarefaComPrazo envolve uma tarefa base (TarefaEstudo) e aplica penalidade se a conclusão ocorrer depois do prazo:
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

    ...
    return progresso_base
```
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
   │  ├─ TipoTarefaEstudo.py
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
## Como executar os testes de exemplo

No VS Code:

1. Abra o terminal integrado  
   **Menu**: `Terminal → New Terminal`.

2. Navegue até a pasta `src` do projeto:

   ```bash
   cd src

Execute os arquivos de teste desejados:

# Tarefas concretas (Leitura, Prática, Quiz, Projeto)
python testes/teste_tarefas.py

# Decorator (TarefaComPrazo)
python testes/teste_decorator_prazo.py

# Aula, Curso, Trilha e Strategy
python testes/teste_aula_curso_trilha.py

# Factory (TarefaFactory)
python testes/teste_factory.py

E se o comando python não funcionar?

Instale o Python no site oficial (https://www.python.org) e marque a opção
“Add Python to PATH” durante a instalação.

Feche e abra o VS Code novamente.

No terminal, teste:
```bash
python --version
```
Se o comando for python3 em vez de python, use:
```bash
python3 testes/teste_tarefas.py
```
Instale a extensão “Python” (Microsoft) para ter: 
realce de sintaxe, lint básico, e integração com terminal/debug.
---

### . Abstração e Polimorfismo

- `TarefaEstudo` é uma **classe abstrata** que define a interface comum das tarefas de estudo:

  ```python
  # src/model/TarefaEstudo.py (trecho)
  from abc import ABC, abstractmethod
  from .StatusTarefa import StatusTarefa

  class TarefaEstudo(ABC):
      @abstractmethod
      def progresso(self) -> float:
          """Retorna o progresso da tarefa entre 0.0 e 1.0."""
          pass

      @abstractmethod
      def definir_termino(self):
          """Ações específicas ao concluir a tarefa."""
          pass

As classes concretas (TarefaLeitura, TarefaPratica, TarefaQuiz, TarefaProjeto) implementam progresso() de formas diferentes, mas a interface é a mesma.

Assim, Aula, Curso e Trilha podem tratar qualquer tarefa apenas como TarefaEstudo e chamar progresso() de forma polimórfica.

---

### Encapsulamento

- Cada classe valida seus próprios dados usando `@property`, garantindo consistência interna.

  ```python
  # src/model/TarefaLeitura.py (trecho)

  @property
  def total_paginas(self):
      return self.__total_paginas

  @total_paginas.setter
  def total_paginas(self, valor):
      # garante inteiro >= 1
      try:
          valor_temporario = int(valor)
      except (TypeError, ValueError):
          valor_temporario = 1

      if valor_temporario < 1:
          valor_temporario = 1

      self.__total_paginas = valor_temporario


Isso evita estados inválidos (por exemplo, número de páginas igual a 0, etapas negativas, nota maior que a nota máxima, etc.).

---

### Herança
- As classes de tarefas concretas **herdam** de `TarefaEstudo`:

  ```python
  class TarefaLeitura(TarefaEstudo):
      ...
  class TarefaPratica(TarefaEstudo):
      ...
  class TarefaQuiz(TarefaEstudo):
      ...
  class TarefaProjeto(TarefaEstudo):
      ...

TarefaComPrazo também herda de TarefaEstudo, mas funciona como um Decorator, reaproveitando e estendendo o comportamento da tarefa base que ela envolve.
---

### Factory 

### Factory

- A classe `TarefaFactory` centraliza a criação das tarefas concretas, recebendo um tipo de tarefa   em formato de texto (`"leitura"`, `"quiz"`, `"pratica"`, `"projeto"`) e os parâmetros específicos:

  ```python
  # src/model/TarefaFactory.py (trecho)
  from .TarefaLeitura import TarefaLeitura
  from .TarefaQuiz import TarefaQuiz
  from .TarefaPratica import TarefaPratica
  from .TarefaProjeto import TarefaProjeto

  class TarefaFactory:
      @staticmethod
      def criar(tipo_tarefa: str, **args):
          if not tipo_tarefa:
              raise ValueError("Tipo de tarefa não informado.")

          tipo_normalizado = str(tipo_tarefa).strip().lower()

          if tipo_normalizado == "leitura":
              return TarefaLeitura(
                  titulo=args.get("titulo", "Leitura"),
                  total_paginas=args["total_paginas"],
                  paginas_lidas=args.get("paginas_lidas", 0),
                  descricao=args.get("descricao"),
                  data_realizacao=args.get("data_realizacao"),
              )

          # Demais tipos: "quiz", "pratica", "projeto"...

---
### Strategy

- `EstrategiaProgresso` é uma interface (classe abstrata) para estratégias de cálculo de progresso da `Trilha`:

  ```python
  # src/model/EstrategiaProgresso.py (trecho)
  from abc import ABC, abstractmethod

  class EstrategiaProgresso(ABC):
      @abstractmethod
      def calcular(self, trilha) -> float:
          """Recebe uma Trilha e devolve um número entre 0.0 e 1.0."""
          pass

Implementações concretas:

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


A Trilha apenas usa a estratégia recebida:

# src/model/Trilha.py (trecho)

def progresso(self, estrategia):
    if estrategia is None:
        return 0.0
    return estrategia.calcular(self)

---
### Decorator

- `TarefaComPrazo` envolve uma tarefa base (`TarefaEstudo`) e aplica penalidade   se a conclusão ocorrer depois do prazo:

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


Dessa forma, o comportamento da tarefa original é reutilizado e apenas estendido com a lógica de prazo e penalidade.

---

## Diagrama de classes UML

    class Trilha {
      - nome: str
      - cursos: List<Curso>
      + adicionar_curso(curso: Curso): None
      + progresso(estrategia: EstrategiaProgresso): float
      + exibir_dados(estrategia: EstrategiaProgresso | None): str
    }

    class Curso {
      - titulo: str
      - carga_horas: int
      - aulas: List<Aula>
      + adicionar_aula(aula: Aula): None
      + progresso(): float
      + exibir_dados(): str
    }

    class Aula {
      - titulo: str
      - tarefas: List<TarefaEstudo>
      + adicionar_tarefa(tarefa: TarefaEstudo): None
      + progresso(): float
      + exibir_dados(): str
    }

    class TarefaEstudo {
      <<abstract>>
      - titulo: str
      - descricao: str | None
      - data_realizacao: datetime | None
      - status: StatusTarefa
      + iniciar_estudo(): None
      + concluir(): None
      + concluida: bool
      + progresso(): float
      + definir_termino(): None
      + exibir_dados(): str
    }

    class TarefaLeitura {
      - total_paginas: int
      - paginas_lidas: int
      + progresso(): float
      + definir_termino(): None
      + exibir_dados(): str
    }

    class TarefaPratica {
      - total_etapas: int
      - etapas_concluidas: int
      + progresso(): float
      + definir_termino(): None
      + exibir_dados(): str
    }

    class TarefaQuiz {
      - nota: float
      - nota_max: float
      + progresso(): float
      + definir_termino(): None
      + exibir_dados(): str
    }

    class TarefaProjeto {
      - total_entregas: int
      - entregas_aprovadas: int
      + progresso(): float
      + definir_termino(): None
      + exibir_dados(): str
    }

    class TarefaComPrazo {
      <<decorator de TarefaEstudo>>
      - prazo: datetime | None
      - penalidade: float
      - tarefa_base: TarefaEstudo
      + progresso(): float
      + concluir(): None
      + definir_termino(): None
      + exibir_dados(): str
    }

    class TarefaFactory {
      + criar(tipo_tarefa: str, **kwargs): TarefaEstudo
    }

    class EstrategiaProgresso {
      <<interface>>
      + calcular(trilha: Trilha): float
    }

    class MediaSimplesEstrategia {
      + calcular(trilha: Trilha): float
    }

    class MediaPonderadaPorCargaEstrategia {
      + calcular(trilha: Trilha): float
    }

    class StatusTarefa {
      <<enumeration>>
      A_FAZER
      EM_ANDAMENTO
      CONCLUIDA
    }

### Relacionamentos

- **Multiplicidade**
  - `Trilha (1)` → `(0..*) Curso`
  - `Curso (1)` → `(0..*) Aula`
  - `Aula (1)` → `(0..*) TarefaEstudo`

- **Herança**
  - `TarefaLeitura`, `TarefaPratica`, `TarefaQuiz`, `TarefaProjeto`, `TarefaComPrazo`
    **herdam** de `TarefaEstudo`.
  - `MediaSimplesEstrategia` e `MediaPonderadaPorCargaEstrategia`
    **implementam** `EstrategiaProgresso`.

- **Dependências**
  - `Trilha` **usa** `EstrategiaProgresso` para calcular o progresso.
  - `Aula` **usa** `TarefaEstudo` (composição).
  - `Curso` **usa** `Aula` (composição).
  - `TarefaComPrazo` **decora** uma `TarefaEstudo`.
  - `TarefaFactory` **cria** instâncias de `TarefaEstudo` concretas.
