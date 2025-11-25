from model.Aula import Aula
from model.Curso import Curso
from model.Trilha import Trilha
from model.TarefaLeitura import TarefaLeitura
from model.TarefaPratica import TarefaPratica
from model.TarefaQuiz import TarefaQuiz
from model.MediaSimplesEstrategia import MediaSimplesEstrategia
from model.MediaPonderadaPorCargaEstrategia import MediaPonderadaPorCargaEstrategia


def montar_trilha_exemplo():
    """
    Cria uma trilha de exemplo com:
    - 2 cursos
    - várias aulas
    - tarefas de tipos diferentes em cada aula.
    """
    # --- Curso 1: POO em Python ---
    aula_poo_1 = Aula("Introdução à POO")
    aula_poo_1.adicionar_tarefa(
        TarefaLeitura("Apostila POO", total_paginas=40, paginas_lidas=20)
    )
    aula_poo_1.adicionar_tarefa(
        TarefaQuiz("Quiz POO básico", nota=8, nota_max=10)
    )

    aula_poo_2 = Aula("Padrões de Projeto")
    aula_poo_2.adicionar_tarefa(
        TarefaLeitura("Capítulo Strategy", total_paginas=30, paginas_lidas=15)
    )
    aula_poo_2.adicionar_tarefa(
        TarefaPratica("Exercícios Strategy", total_etapas=5, etapas_concluidas=2)
    )

    curso_poo = Curso(titulo="POO em Python", carga_horas=40)
    curso_poo.adicionar_aula(aula_poo_1)
    curso_poo.adicionar_aula(aula_poo_2)

    # --- Curso 2: Estruturas de Dados ---
    aula_ed_1 = Aula("Listas e Dicionários")
    aula_ed_1.adicionar_tarefa(
        TarefaPratica("Lista de exercícios ED", total_etapas=8, etapas_concluidas=4)
    )

    curso_ed = Curso(titulo="Estruturas de Dados", carga_horas=60)
    curso_ed.adicionar_aula(aula_ed_1)

    # --- Trilha completa ---
    trilha_python = Trilha("Trilha Python Completa")
    trilha_python.adicionar_curso(curso_poo)
    trilha_python.adicionar_curso(curso_ed)

    return trilha_python


def mostrar_detalhes_trilha(trilha):
    print("\n=== DETALHES DOS CURSOS DA TRILHA ===")
    for curso in trilha.cursos:
        print("\n------------------------------")
        print(curso.exibir_dados())


def testar_strategies():
    trilha = montar_trilha_exemplo()
    mostrar_detalhes_trilha(trilha)

    estrategia_simples = MediaSimplesEstrategia()
    estrategia_ponderada = MediaPonderadaPorCargaEstrategia()

    progresso_simples = trilha.progresso(estrategia_simples)
    progresso_ponderado = trilha.progresso(estrategia_ponderada)

    print("\n=== PROGRESSO DA TRILHA ===")
    print(trilha.exibir_dados(estrategia_simples))
    print(f"(Strategy: Média simples)  -> {progresso_simples:.4f}")

    print("\n" + "-" * 40)
    print(trilha.exibir_dados(estrategia_ponderada))
    print(f"(Strategy: Média ponderada)-> {progresso_ponderado:.4f}")


if __name__ == "__main__":
    testar_strategies()

"""
Mostra:
- composição Aula -> Tarefas
- composição Curso -> Aulas
- composição Trilha -> Cursos
- uso das estratégias MediaSimplesEstrategia e MediaPonderadaPorCargaEstrategia.
"""
