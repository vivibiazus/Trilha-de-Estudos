# Gerenciador de Estudos e Trilhas de Aprendizagem

Organiza **Trilhas → Cursos → Aulas → Tarefas** e aplica POO com padrões (Factory e Strategy) para manter o código coeso e flexível.

**Destaques**
- **Factory**: cria tarefas (quiz, leitura, prática, projeto) a partir de um Enum (`TipoTarefaEstudo`).
- **Strategy**: calcula o **progresso da trilha** por diferentes métodos (média simples e ponderada por carga horária).
- **Decorator**: adiciona comportamento de **prazo** a uma tarefa, aplicando **penalidade** se for concluída após a data/hora definida.
- **Extensões**: espaço para evoluir (lembretes, pré-requisitos, badges).

> **Objetivo**: acompanhar a evolução do estudante em trilhas de aprendizagem, trocando o algoritmo de progresso sem alterar as classes de domínio.
---
## Visão geral

- **Estrutura**: uma **Trilha** reúne **Cursos**; cada **Curso** possui **Aulas**; cada **Aula** contém **Tarefas** polimórficas (*Quiz*, *Leitura*, *Prática*, *Projeto*).
- **Cálculo de progresso**: a **Trilha** recebe uma **Strategy** e delega o cálculo, permitindo alternar o método sem mudar as entidades.
- **Padronização**: a **Factory** centraliza a criação das tarefas usando `TipoTarefaEstudo`, evitando *ifs* espalhados e erros de digitação.
- **Regra de prazo (Decorator)**: `TarefaComPrazo` envolve uma tarefa existente e aplica penalidade ao progresso se houver atraso.


### Conceitos-chave

- **Enum `TipoTarefaEstudo`** — padroniza os tipos de tarefa e evita erros de digitação:
```python
from model.TipoTarefaEstudo import TipoTarefaEstudo

# Opções: LEITURA, QUIZ, PRATICA, PROJETO
tipo = TipoTarefaEstudo.QUIZ
# Exemplo: obter o texto amigável
print(tipo.value)  # "Quiz"
``` 
- **Factory `TarefaFactory`** — centraliza a criação das tarefas corretas a partir do `TipoTarefaEstudo`:
```python
from model.TarefaFactory import TarefaFactory
from model.TipoTarefaEstudo import TipoTarefaEstudo

quiz = TarefaFactory.criar(
    TipoTarefaEstudo.QUIZ,
    titulo="Prova 1",
    nota=8,       # nota obtida
    nota_max=10   # nota máxima
)

# Ex.: também aceita string
# leitura = TarefaFactory.criar("leitura", titulo="Cap. 1", total_paginas=50, paginas_lidas=20)
```
- **Strategy de Progresso** — permite trocar o algoritmo de cálculo sem alterar Trilha/Curso/Aula:
```python
from model.MediaSimplesEstrategia import MediaSimplesEstrategia
from model.MediaPonderadaPorCargaEstrategia import MediaPonderadaPorCargaEstrategia

# média aritmética simples entre cursos
progresso = trilha.progresso(MediaSimplesEstrategia())

# para ponderar por carga horária, troque a estratégia:
# progresso = trilha.progresso(MediaPonderadaPorCargaEstrategia())
```
---
## Diagrama de classes


    class Trilha {
      - nome: str
      - cursos: List<Curso>
      + progresso(estrategia: EstrategiaProgresso): float
      + exibir_dados(estrategia: EstrategiaProgresso): str
    }

    class Curso {
      - titulo: str
      - aulas: List<Aula>
      - carga_horas: int
      + progresso(): float
      + exibir_dados(): str
    }

    class Aula {
      - titulo: str
      - tarefas: List<TarefaEstudo>
      + progresso(): float
      + exibir_dados(): str
    }

    class TarefaEstudo {
      <<abstract>>
      + progresso(): float
      + exibir_dados(): str
      + concluir(): None
    }

    class TarefaQuiz {
      - titulo: str
      - nota: float
      - nota_max: float
      + progresso(): float
      + exibir_dados(): str
    }

    class TarefaLeitura {
      - titulo: str
      - paginas_lidas: int
      - total_paginas: int
      + progresso(): float
      + exibir_dados(): str
    }

    class TarefaPratica {
      - titulo: str
      - etapas_concluidas: int
      - total_etapas: int
      + progresso(): float
      + exibir_dados(): str
    }

    class TarefaProjeto {
      - titulo: str
      - entregas_aprovadas: int
      - total_entregas: int
      + progresso(): float
      + exibir_dados(): str
    }

    class TarefaFactory {
      + criar(tipo: TipoTarefaEstudo, **kwargs): TarefaEstudo
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

    class TipoTarefaEstudo {
      <<enumeration>>
      QUIZ
      LEITURA
      PRATICA
      PROJETO
    }


### Relacionamentos

#### Multiplicidade
- **Trilha (1)** → **(1..*) Curso**
- **Curso (1)** → **(1..*) Aula**
- **Aula (1)** → **(0..*) TarefaEstudo**

#### Herança
- `TarefaQuiz`, `TarefaLeitura`, `TarefaPratica`, `TarefaProjeto` **herdam** de `TarefaEstudo`.
- `MediaSimplesEstrategia` e `MediaPonderadaPorCargaEstrategia` **implementam** `EstrategiaProgresso`.

#### Dependências
- `Trilha` **usa** `EstrategiaProgresso` para calcular o progresso.
- `TarefaFactory` **cria** `TarefaEstudo` e **usa** `TipoTarefaEstudo` para decidir qual classe instanciar.


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
   └─ tests/
      ├─ __init__.py
      ├─ lembrete_como_rodar_local
      ├─ teste_aula_curso_trilha.py
      ├─ teste_factory.py
      ├─ teste_tarefas.py
      └─ teste_decorator_prazo.py    
```

## Onde encontram-se os pilares?

**Abstração**  
`TarefaEstudo` define a interface comum (`progresso`, `exibir_dados`) sem expor detalhes do cálculo:

```python
# --- src/model/TarefaEstudo.py ---
from abc import ABC, abstractmethod

class TarefaEstudo(ABC):
    @abstractmethod
    def progresso(self) -> float: ...
    
    def exibir_dados(self) -> str:
        return f"{self.__class__.__name__}: {self.progresso()*100:.0f}%"
````
**Herança e Polimorfismo**  
Subclasses implementam o cálculo, e Aula/Curso/Trilha usam polimorfismo ao chamar `progresso()`:

```python
# --- src/model/TarefaLeitura.py ---
from .TarefaEstudo import TarefaEstudo

class TarefaLeitura(TarefaEstudo):
    def __init__(self, titulo, total_paginas, paginas_lidas=0, descricao=None, data_realizacao=None):
        self.titulo = titulo or "Leitura"
        self.total_paginas = max(1, int(total_paginas))
        self.paginas_lidas = max(0, int(paginas_lidas))

    def progresso(self) -> float:
        return min(1.0, self.paginas_lidas / self.total_paginas)
```
**Encapsulamento**  
Cada tarefa mantém e valida seus próprios dados (limites e consistência):

```python
# --- src/model/TarefaQuiz.py ---
from .TarefaEstudo import TarefaEstudo

class TarefaQuiz(TarefaEstudo):
    def __init__(self, titulo, nota, nota_max=10, descricao=None, data_realizacao=None):
        self.titulo = titulo or "Quiz"
        self.nota_max = max(1.0, float(nota_max))
        self.nota = max(0.0, min(float(nota), self.nota_max))

    def progresso(self) -> float:
        return self.nota / self.nota_max
```
**Padrões**
Factory: `TarefaFactory`
Strategy: `MediaSimplesEstrategia`, `MediaPonderadaPorCargaEstrategia`
Decorator: `TarefaComPrazo`

`Enum + Factory`
```python
# --- src/model/TipoTarefaEstudo.py ---
from enum import Enum

class TipoTarefaEstudo(Enum):
    LEITURA = "Leitura"
    QUIZ    = "Quiz"
    PRATICA = "Prática"
    PROJETO = "Projeto"


# --- Exemplo de uso da Factory ---
from model.TarefaFactory import TarefaFactory
from model.TipoTarefaEstudo import TipoTarefaEstudo

t1 = TarefaFactory.criar(TipoTarefaEstudo.QUIZ, titulo="Prova 1", nota=8, nota_max=10)
t2 = TarefaFactory.criar("leitura",             titulo="Cap. 1",  total_paginas=50, paginas_lidas=20)

print(round(t1.progresso(), 2))  # 0.80
print(round(t2.progresso(), 2))  # 0.40
```

`Strategy`

```python
# --- src/model/EstrategiaProgresso.py ---
from abc import ABC, abstractmethod

class EstrategiaProgresso(ABC):
    @abstractmethod
    def calcular(self, trilha) -> float: ...
    

# --- src/model/MediaSimplesEstrategia.py ---
from .EstrategiaProgresso import EstrategiaProgresso

class MediaSimplesEstrategia(EstrategiaProgresso):
    def calcular(self, trilha) -> float:
        cursos = trilha.cursos
        return 0.0 if not cursos else sum(c.progresso() for c in cursos) / len(cursos)


# --- Uso rápido (em qualquer parte do projeto) ---
from model.MediaSimplesEstrategia import MediaSimplesEstrategia

progresso = trilha.progresso(MediaSimplesEstrategia())
```

`Composição (Aula → Tarefas, Curso → Aulas, Trilha → Cursos)`

```python
# --- src/model/Aula.py ---
from statistics import mean

class Aula:
    def __init__(self, titulo: str):
        self.titulo = titulo
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def progresso(self) -> float:
        return 0.0 if not self.tarefas else mean(t.progresso() for t in self.tarefas)
