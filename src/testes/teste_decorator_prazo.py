import unittest
from datetime import datetime, timedelta

from model.TarefaQuiz import TarefaQuiz
from model.TarefaComPrazo import TarefaComPrazo

class TestDecoratorPrazo(unittest.TestCase):
    def test_quiz_sem_atraso_mantem_progresso(self):
        base = TarefaQuiz(titulo="Prova 1", nota=10, nota_max=10)  # 100%
        prazo = datetime.now() + timedelta(hours=1)  # prazo no futuro
        decorada = TarefaComPrazo(base, prazo=prazo, penalidade=0.2)
        # Sem data_realizacao: não há atraso -> mantém 100%
        self.assertAlmostEqual(decorada.progresso(), 1.0, places=6)

        # Mesmo concluindo antes do prazo, mantém 100%
        base.data_realizacao = datetime.now()
        self.assertAlmostEqual(decorada.progresso(), 1.0, places=6)

    def test_quiz_com_atraso_aplica_penalidade(self):
        base = TarefaQuiz(titulo="Prova 1", nota=10, nota_max=10)  # 100% antes da penalidade
        prazo = datetime.now() - timedelta(hours=1)  # prazo já passou
        base.data_realizacao = datetime.now()       # concluiu agora (atrasado)
        decorada = TarefaComPrazo(base, prazo=prazo, penalidade=0.25)  # -25%

        # 100% com penalidade de 25% -> 75% = 0.75
        self.assertAlmostEqual(decorada.progresso(), 0.75, places=6)

    def test_exibir_dados_traz_info_do_prazo_e_penalidade(self):
        base = TarefaQuiz(titulo="Prova 2", nota=8, nota_max=10)  # 80%
        prazo = datetime(2099, 1, 1, 12, 0)
        decorada = TarefaComPrazo(base, prazo=prazo, penalidade=0.2)

        texto = decorada.exibir_dados()
        self.assertIn("Prazo:", texto)
        self.assertIn("Penalidade se atrasar:", texto)
        # Deve exibir também o progresso “após regra de prazo”
        self.assertIn("Progresso (após regra de prazo):", texto)

if __name__ == "__main__":
    unittest.main()

