from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa


class TarefaQuiz(TarefaEstudo):
    def __init__(self, titulo, nota, nota_max=10, descricao=None,
                 data_realizacao=None, status=StatusTarefa.A_FAZER):
        super().__init__(titulo=titulo, descricao=descricao,
                         data_realizacao=data_realizacao, status=status)
        self.nota_max = nota_max
        self.nota = nota

    # --- getters e setters ---

    @property
    def nota_max(self):
        return self.__nota_max

    @nota_max.setter
    def nota_max(self, v):
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = 10.0
        if v < 1.0:
            v = 1.0
        self.__nota_max = v
        # revalida nota se já existir
        try:
            if self.__nota < 0.0:
                self.__nota = 0.0
            if self.__nota > self.__nota_max:
                self.__nota = self.__nota_max
        except AttributeError:
            pass

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, v):
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = 0.0
        if v < 0.0:
            v = 0.0
        # limita ao máximo se já definido
        try:
            if v > self.__nota_max:
                v = self.__nota_max
        except AttributeError:
            pass
        self.__nota = v

    # --- métodos especiais/auxiliares ---

    def __str__(self):
        return f"[Quiz] {super().__str__()}"

    def exibir_dados(self):
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Quiz",
            f"Nota: {self.nota}/{self.nota_max}",
        ]
        return "\n".join(linhas)

    def definir_termino(self):
        """Conclui o quiz marcando data e status."""
        self.data_realizacao = datetime.now()
        self.status = StatusTarefa.CONCLUIDA
