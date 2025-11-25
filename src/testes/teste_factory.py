from model.TarefaFactory import TarefaFactory


def testar_factory_leitura_quiz():
    print("\n=== FACTORY COM STRINGS (LEITURA E QUIZ) ===")

    tarefa_leitura = TarefaFactory.criar(
        tipo_tarefa="leitura",
        titulo="Capítulo 2 - Factory",
        total_paginas=50,
        paginas_lidas=10,
        descricao="Leitura sobre o padrão Factory",
    )

    tarefa_quiz = TarefaFactory.criar(
        tipo_tarefa="quiz",
        titulo="Quiz Factory",
        nota=9,
        nota_max=10,
    )

    print("\nTarefa criada (LEITURA via string):")
    print(tarefa_leitura)
    print(tarefa_leitura.exibir_dados())

    print("\nTarefa criada (QUIZ via string):")
    print(tarefa_quiz)
    print(tarefa_quiz.exibir_dados())


def testar_factory_pratica_projeto():
    print("\n=== FACTORY COM STRINGS (PRÁTICA E PROJETO) ===")

    tarefa_pratica = TarefaFactory.criar(
        tipo_tarefa="pratica",
        titulo="Exercícios de Factory",
        total_etapas=5,
        etapas_concluidas=1,
    )

    tarefa_projeto = TarefaFactory.criar(
        tipo_tarefa="projeto",
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
    testar_factory_leitura_quiz()
    testar_factory_pratica_projeto()

"""
Mostra:
- criação de tarefas usando a TarefaFactory a partir de strings:
  "leitura", "quiz", "pratica", "projeto".
- cada tipo concreto aplica sua própria regra de progresso().
"""
