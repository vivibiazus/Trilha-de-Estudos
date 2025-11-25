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
Como executar os testes de exemplo

No VS Code: 

Abra o terminal integrado (Terminal → New Terminal).

Navegue até a pasta src:

cd src


Execute os arquivos de teste desejados:

# Tarefas concretas (Leitura, Prática, Quiz, Projeto)
python testes/teste_tarefas.py

# Decorator (TarefaComPrazo)
python testes/teste_decorator_prazo.py

# Aula, Curso, Trilha e Strategy
python testes/teste_aula_curso_trilha.py

# Factory + Enum TipoTarefaEstudo
python testes/teste_factory.py

---
