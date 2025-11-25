from datetime import datetime, timedelta
from model.TarefaLeitura import TarefaLeitura
from model.TarefaComPrazo import TarefaComPrazo


def testar_sem_atraso():
    print("\n=== DECORATOR - CASO SEM ATRASO ===")

    tarefa_base = TarefaLeitura(
        titulo="Capítulo Decorator",
        total_paginas=30,
        paginas_lidas=30,
        descricao="Leitura obrigatória da disciplina",
    )

    prazo_futuro = datetime.now() + timedelta(days=2)

    tarefa_com_prazo = TarefaComPrazo(
        tarefa_base=tarefa_base,
        prazo=prazo_futuro,
        penalidade=0.3,  # 30% de desconto em caso de atraso (não será aplicado aqui)
    )

    tarefa_com_prazo.concluir()

    print(tarefa_com_prazo.exibir_dados())
    print(f"Progresso (sem atraso): {tarefa_com_prazo.progresso():.2f}")


def testar_com_atraso():
    print("\n=== DECORATOR - CASO COM ATRASO ===")

    tarefa_base = TarefaLeitura(
        titulo="Artigo sobre padrões de projeto",
        total_paginas=10,
        paginas_lidas=10,
    )

    prazo_passado = datetime.now() - timedelta(days=1)

    tarefa_com_prazo = TarefaComPrazo(
        tarefa_base=tarefa_base,
        prazo=prazo_passado,
        penalidade=0.5,  # 50% de desconto se entregar atrasado
    )

    tarefa_com_prazo.concluir()

    print(tarefa_com_prazo.exibir_dados())
    print(f"Progresso (com atraso): {tarefa_com_prazo.progresso():.2f}")


if __name__ == "__main__":
    testar_sem_atraso()
    testar_com_atraso()

"""
Mostra dois cenários:
- tarefa concluída ANTES do prazo (sem penalidade);
- tarefa concluída DEPOIS do prazo (com penalidade aplicada).
"""
