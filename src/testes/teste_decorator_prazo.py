from datetime import datetime
from model.TarefaQuiz import TarefaQuiz
from model.TarefaComPrazo import TarefaComPrazo

def iguais_ou_aproximados(valor, esperado, margem=0.000001):
    """
    Compara dois números de ponto flutuante permitindo uma pequena margem de erro.
    A função abs(x) devolve o valor absoluto de x (distância até zero), ignorando o sinal.
    """
    diferenca = valor - esperado
    return abs(diferenca) <= margem

#testes 

# 1) Sem atraso --> mantém progresso em 100%
tarefa_base_sem_atraso = TarefaQuiz(titulo="Prova 1", nota=10, nota_max=10)  # 100%
prazo_no_futuro = datetime(2099, 1, 1, 12, 0)  # prazo bem no futuro
tarefa_com_prazo = TarefaComPrazo(tarefa_base_sem_atraso, prazo=prazo_no_futuro, penalidade=0.20)

print("\nCaso 1: sem atraso e sem data de realização definida")
progresso_1 = tarefa_com_prazo.progresso()
print("Progresso calculado:", f"{progresso_1*100:.0f}%")
print("Confere com 100%? ", iguais_ou_aproximados(progresso_1, 1.0))

# Ainda no caso 1: mesmo concluindo antes do prazo, mantém 100%
tarefa_base_sem_atraso.data_realizacao = datetime(2025, 1, 1, 10, 0)  # antes de 2099
tarefa_com_prazo = TarefaComPrazo(tarefa_base_sem_atraso, prazo=prazo_no_futuro, penalidade=0.20)
print("\nCaso 1 (continuação): concluída antes do prazo")
progresso_1b = tarefa_com_prazo.progresso()
print("Progresso calculado:", f"{progresso_1b*100:.0f}%")
print("Confere com 100%? ", iguais_ou_aproximados(progresso_1b, 1.0))

# 2) Com atraso --> aplica penalidade
tarefa_base_com_atraso = TarefaQuiz(titulo="Prova 2", nota=10, nota_max=10)  # 100%
prazo_no_passado = datetime(2000, 1, 1, 12, 0)                  # prazo já passou
tarefa_base_com_atraso.data_realizacao = datetime(2025, 1, 1, 10, 0)  # conclusão depois do prazo
tarefa_com_prazo_atraso = TarefaComPrazo(
    tarefa_base_com_atraso, prazo=prazo_no_passado, penalidade=0.25  # -25%
)

print("\nCaso 2: com atraso, aplica penalidade de 25%")
progresso_2 = tarefa_com_prazo_atraso.progresso()
print("Progresso calculado:", f"{progresso_2*100:.0f}%")
print("Confere com ~75%? ", iguais_ou_aproximados(progresso_2, 0.75))

# 3) Texto exibido contém informações do prazo e penalidade
tarefa_base_texto = TarefaQuiz(titulo="Prova 3", nota=8, nota_max=10)  # 80%
prazo_para_exibir = datetime(2099, 1, 1, 12, 0)
tarefa_com_prazo_texto = TarefaComPrazo(tarefa_base_texto, prazo=prazo_para_exibir, penalidade=0.20)

print("\nCaso 3: exibir_dados inclui informações do decorator")
texto_saida = tarefa_com_prazo_texto.exibir_dados()
print(texto_saida)
print("Contém 'Prazo:'?                   ", ("Prazo:" in texto_saida))
print("Contém 'Penalidade se atrasar:'?   ", ("Penalidade se atrasar:" in texto_saida))
print("Contém 'Progresso (c/ prazo):'?    ", ("Progresso (c/ prazo):" in texto_saida))


