from datetime import datetime
from model.StatusTarefa import StatusTarefa
from model.TarefaLeitura import TarefaLeitura
from model.TarefaPratica import TarefaPratica
from model.TarefaQuiz import TarefaQuiz
from model.TarefaProjeto import TarefaProjeto


def testar_tarefa_leitura():
    print("\n=== TAREFA LEITURA ===")
    tarefa_leitura = TarefaLeitura(
        titulo="Capítulo 1 - POO",
        total_paginas=100,
        paginas_lidas=30,
        descricao="Introdução à orientação a objetos",
    )

    print("Antes de concluir:")
    print(tarefa_leitura)
    print(tarefa_leitura.exibir_dados())
    print(f"Progresso inicial: {tarefa_leitura.progresso():.2f}\n")

    # Simula leitura de mais páginas e conclusão
    tarefa_leitura.paginas_lidas = 100
    tarefa_leitura.concluir()

    print("Depois de concluir:")
    print(tarefa_leitura.exibir_dados())
    print(f"Progresso final: {tarefa_leitura.progresso():.2f}")


def testar_tarefa_pratica():
    print("\n=== TAREFA PRÁTICA ===")
    tarefa_pratica = TarefaPratica(
        titulo="Lista de exercícios 01",
        total_etapas=10,
        etapas_concluidas=4,
        descricao="Exercícios sobre variáveis e tipos",
    )

    print("Antes de concluir:")
    print(tarefa_pratica)
    print(tarefa_pratica.exibir_dados())
    print(f"Progresso inicial: {tarefa_pratica.progresso():.2f}\n")

    # Simula avanço das etapas e conclusão
    tarefa_pratica.etapas_concluidas = 10
    tarefa_pratica.concluir()

    print("Depois de concluir:")
    print(tarefa_pratica.exibir_dados())
    print(f"Progresso final: {tarefa_pratica.progresso():.2f}")


def testar_tarefa_quiz():
    print("\n=== TAREFA QUIZ ===")
    tarefa_quiz = TarefaQuiz(
        titulo="Quiz de Herança",
        nota=7.5,
        nota_max=10,
        descricao="Avaliação rápida sobre herança e polimorfismo",
    )

    print("Situação do quiz:")
    print(tarefa_quiz)
    print(tarefa_quiz.exibir_dados())
    print(f"Progresso (nota/nota_max): {tarefa_quiz.progresso():.2f}")

    # Ajusta nota para mostrar validação
    tarefa_quiz.nota = 11  # deve ser limitado a nota_max
    print("\nApós tentar definir nota = 11 (limite em nota_max):")
    print(tarefa_quiz.exibir_dados())
    print(f"Progresso ajustado: {tarefa_quiz.progresso():.2f}")


def testar_tarefa_projeto():
    print("\n=== TAREFA PROJETO ===")
    tarefa_projeto = TarefaProjeto(
        titulo="Projeto de Banco de Dados",
        total_entregas=4,
        entregas_aprovadas=1,
        descricao="Modelagem + scripts SQL + documentação",
    )

    print("Antes de concluir:")
    print(tarefa_projeto)
    print(tarefa_projeto.exibir_dados())
    print(f"Progresso inicial: {tarefa_projeto.progresso():.2f}\n")

    tarefa_projeto.entregas_aprovadas = 4
    tarefa_projeto.concluir()

    print("Depois de concluir:")
    print(tarefa_projeto.exibir_dados())
    print(f"Progresso final: {tarefa_projeto.progresso():.2f}")


def testar_polimorfismo():
    """
    uma lista de TarefaEstudo com diferentes tipos concretos,
    todos expondo progresso().
    """
    print("\n=== POLIMORFISMO COM LISTA DE TAREFAS ===")

    tarefas_estudo = [
        TarefaLeitura("Artigo sobre Strategy", total_paginas=20, paginas_lidas=10),
        TarefaPratica("Exercícios de listas", total_etapas=5, etapas_concluidas=3),
        TarefaQuiz("Quiz de Decorator", nota=8, nota_max=10),
        TarefaProjeto("Projeto POO", total_entregas=3, entregas_aprovadas=1),
    ]

    for tarefa in tarefas_estudo: # Todas respondem a progresso() e exibir_dados()
        print("\n---")
        print(tarefa)
        print(f"Tipo concreto: {tarefa.__class__.__name__}")
        print(f"Progresso: {tarefa.progresso():.2f}")


if __name__ == "__main__":
    testar_tarefa_leitura()
    testar_tarefa_pratica()
    testar_tarefa_quiz()
    testar_tarefa_projeto()
    testar_polimorfismo()

"""
Teste das classes de tarefas de estudo.
- TarefaLeitura
- TarefaPratica
- TarefaQuiz
- TarefaProjeto
"""
