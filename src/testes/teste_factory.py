from model.TarefaFactory import TarefaFactory
from model.TipoTarefaEstudo import TipoTarefaEstudo


def testar_com_enum():
    print("\n=== FACTORY COM ENUM ===")

    tarefa_leitura = TarefaFactory.criar(
        tipo=TipoTarefaEstudo.LEITURA,
        titulo="Capítulo 2 - Factory",
        total_paginas=50,
        paginas_lidas=10,
        descricao="Leitura sobre o padrão Factory",
    )

    tarefa_quiz = TarefaFactory.criar(
        tipo=TipoTarefaEstudo.QUIZ,
        titulo="Quiz Factory",
        nota=9,
        nota_max=10,
    )

    print("\nTarefa criada (LEITURA via Enum):")
    print(tarefa_leitura)
    print(tarefa_leitura.exibir_dados())

    print("\nTarefa criada (QUIZ via Enum):")
    print(tarefa_quiz)
    print(tarefa_quiz.exibir_dados())


def testar_com_string():
    print("\n=== FACTORY COM STRING ===")

    tarefa_pratica = TarefaFactory.criar(
        tipo="pratica",  # deve aceitar string, normalizando internamente
        titulo="Exercícios de Factory",
        total_etapas=5,
        etapas_concluidas=1,
    )

    tarefa_projeto = TarefaFactory.criar(
        tipo="projeto",
        titulo="Projeto Final POO",
        total_entregas=3,
        entregas_aprovadas=0,
        descricao="Projeto integrador da disciplina",
    )

    print("\nTarefa criada (PRÁTICA via string):")
    print(tarefa_pratica)
    print(tarefa_pratica.exibir_dados())

    print("\nTarefa criada (PROJETO via string):")
    print(tarefa_projeto)
    print(tarefa_projeto.exibir_dados())


if __name__ == "__main__":
    testar_com_enum()
    testar_com_string()

"""
- criação de tarefas usando o Enum TipoTarefaEstudo; --- não sei se manterei -- verificar
- criação de tarefas usando string (ex.: "leitura").
"""


