from model.TarefaQuiz import TarefaQuiz
from model.TarefaLeitura import TarefaLeitura
from model.TarefaPratica import TarefaPratica
from model.TarefaProjeto import TarefaProjeto
from model.StatusTarefa import StatusTarefa

print("\n=== Teste das Tarefas (progresso, concluir, exibir) ===")

# --- QUIZ ---
q = TarefaQuiz(titulo="Prova 1", nota=12, nota_max=10)  # deve capar em 10/10
print(q.exibir_dados())
print("Progresso Quiz (esperado 100%):", f"{q.progresso()*100:.0f}%")
q.concluir()
print("Após concluir:", q.status == StatusTarefa.CONCLUIDA, q.data_realizacao is not None)

# --- LEITURA ---
l = TarefaLeitura(titulo="Capítulo 1", total_paginas=50, paginas_lidas=20)
print(l.exibir_dados())
print("Progresso Leitura (esperado 40%):", f"{l.progresso()*100:.0f}%")

# bordas
l.paginas_lidas = -5
print("Lidas negativas → 0:", l.paginas_lidas == 0)
l.paginas_lidas = 999
print("Lidas acima do total → total:", l.paginas_lidas == l.total_paginas)

# --- PRÁTICA ---
p = TarefaPratica(titulo="Lab 1", total_etapas=6, etapas_concluidas=3)
print(p.exibir_dados())
print("Progresso Prática (esperado 50%):", f"{p.progresso()*100:.0f}%")

# bordas
p.etapas_concluidas = -1
print("Concluídas negativas → 0:", p.etapas_concluidas == 0)
p.total_etapas = 2
print("Reduzi total; concluídas capadas:", p.etapas_concluidas <= p.total_etapas)

# --- PROJETO ---
pj = TarefaProjeto(titulo="Projeto Final", total_entregas=4, entregas_aprovadas=1)
print(pj.exibir_dados())
print("Progresso Projeto (esperado 25%):", f"{pj.progresso()*100:.0f}%")

# bordas
pj.entregas_aprovadas = 10
print("Aprovadas acima do total → total:", pj.entregas_aprovadas == pj.total_entregas)
pj.entregas_aprovadas = -3
print("Aprovadas negativas → 0:", pj.entregas_aprovadas == 0)
