from model.TarefaFactory import TarefaFactory
from model.TipoTarefaEstudo import TipoTarefaEstudo
from model.TarefaLeitura import TarefaLeitura
from model.TarefaQuiz import TarefaQuiz
from model.TarefaPratica import TarefaPratica
from model.TarefaProjeto import TarefaProjeto

def eh_classe(obj, nome_classe: str) -> bool:
    return obj.__class__.__name__ == nome_classe

print("\n=== Teste da TarefaFactory ===")

# 1) Criação por STRING
q = TarefaFactory.criar("quiz", titulo="Prova 1", nota=8, nota_max=10)
print(eh_classe(q, "TarefaQuiz"), q.exibir_dados(), sep="\n")

l = TarefaFactory.criar("leitura", titulo="Capítulo 1", total_paginas=50, paginas_lidas=20)
print(eh_classe(l, "TarefaLeitura"), l.exibir_dados(), sep="\n")

p = TarefaFactory.criar("pratica", titulo="Lab 1", total_etapas=6, etapas_concluidas=3)
print(eh_classe(p, "TarefaPratica"), p.exibir_dados(), sep="\n")

pj = TarefaFactory.criar("projeto", titulo="Projeto Final", total_entregas=4, entregas_aprovadas=1)
print(eh_classe(pj, "TarefaProjeto"), pj.exibir_dados(), sep="\n")

# 2) Criação por ENUM
l2 = TarefaFactory.criar(TipoTarefaEstudo.LEITURA, titulo="Capítulo 2", total_paginas=30, paginas_lidas=15)
print(eh_classe(l2, "TarefaLeitura"), l2.exibir_dados(), sep="\n")

# 3) Erros esperados (campos obrigatórios faltando)
try:
    TarefaFactory.criar("leitura", titulo="Capítulo sem total")
except Exception as e:
    print("Erro (ok - faltou total_paginas):", e)

try:
    TarefaFactory.criar("quiz", titulo="Prova sem nota")
except Exception as e:
    print("Erro (ok - faltou nota):", e)
