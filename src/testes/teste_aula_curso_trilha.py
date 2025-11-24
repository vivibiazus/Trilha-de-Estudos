from model.TarefaFactory import TarefaFactory
from model.Aula import Aula
from model.Curso import Curso
from model.Trilha import Trilha
from model.MediaSimplesEstrategia import MediaSimplesEstrategia
from model.MediaPonderadaPorCargaEstrategia import MediaPonderadaPorCargaEstrategia

print("\n=== Teste Aula, Curso, Trilha + Estratégias ===")

# ----- monta tarefas via Factory -----
q1 = TarefaFactory.criar("quiz", titulo="Prova 1", nota=8, nota_max=10)           # 80%
l1 = TarefaFactory.criar("leitura", titulo="Cap. 1", total_paginas=40, paginas_lidas=20)  # 50%
p1 = TarefaFactory.criar("pratica", titulo="Lab 1", total_etapas=5, etapas_concluidas=5)  # 100%

# ----- Aula -----
a1 = Aula("Introdução")
a1.adicionar_tarefa(q1)
a1.adicionar_tarefa(l1)
a1.adicionar_tarefa(p1)
print(a1.exibir_dados())  # média das tarefas: (0.8 + 0.5 + 1.0)/3 = 0.7666...

# ----- Curso -----
c1 = Curso("Python Básico", carga_horas=40)
c1.adicionar_aula(a1)
print(c1.exibir_dados())

# segunda aula do mesmo curso
q2 = TarefaFactory.criar("quiz", titulo="Prova 2", nota=10, nota_max=10)  # 100%
a2 = Aula("Fundamentos")
a2.adicionar_tarefa(q2)
c1.adicionar_aula(a2)
print("Progresso curso (esperado > 80%):", f"{c1.progresso()*100:.1f}%")

# ----- Outro curso -----
c2 = Curso("Algoritmos", carga_horas=20)
l2 = TarefaFactory.criar("leitura", titulo="Cap. 2", total_paginas=30, paginas_lidas=15)  # 50%
a3 = Aula("Estruturas")
a3.adicionar_tarefa(l2)
c2.adicionar_aula(a3)

# ----- Trilha -----
t = Trilha("Trilha de Programação")
t.adicionar_curso(c1)
t.adicionar_curso(c2)

# Estratégia: média simples
estr_simples = MediaSimplesEstrategia()
print("Trilha (média simples):", f"{t.progresso(estr_simples)*100:.1f}%")
print(t.exibir_dados(estr_simples))

# Estratégia: ponderada por carga-horas (c1 pesa 40, c2 pesa 20)
estr_pond = MediaPonderadaPorCargaEstrategia()
print("Trilha (ponderada por carga):", f"{t.progresso(estr_pond)*100:.1f}%")
print(t.exibir_dados(estr_pond))
