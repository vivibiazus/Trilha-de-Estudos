from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa

class TarefaPratica(TarefaEstudo):
    def __init__(self, titulo, total_etapas, etapas_concluidas=0, descricao=None,
                 data_realizacao=None, status=StatusTarefa.A_FAZER):
        super().__init__(titulo=titulo, descricao=descricao,
                         data_realizacao=data_realizacao, status=status)
        # defina o total antes (o clamp de etapas usa esse valor)
        self.total_etapas = total_etapas
        self.etapas_concluidas = etapas_concluidas

    # --- getters e setters ---

    @property
    def total_etapas(self):
        return self.__total_etapas

    @total_etapas.setter
    def total_etapas(self, valor):
        # inteiro >= 1
        try:
            v = int(valor)
        except (TypeError, ValueError):
            v = 1
        if v < 1:
            v = 1
        self.__total_etapas = v
        # readequar etapas_concluidas ao novo total (sem hasattr)
        try:
            if self.__etapas_concluidas > v:
                self.__etapas_concluidas = v
        except AttributeError:
            # ainda não foi definido (antes do __init__ terminar)
            pass

    @property
    def etapas_concluidas(self):
        return self.__etapas_concluidas

    @etapas_concluidas.setter
    def etapas_concluidas(self, valor):
        # inteiro entre 0 e total_etapas
        try:
            v = int(valor)
        except (TypeError, ValueError):
            v = 0
        if v < 0:
            v = 0
        if v > self.__total_etapas:
            v = self.__total_etapas
        self.__etapas_concluidas = v

    # --- regra de negócio ---

    def progresso(self):
        # fração concluída (0.0 a 1.0)
        return self.etapas_concluidas / float(self.total_etapas) if self.total_etapas else 0.0

    def definir_termino(self):
        # ao concluir, registra data e status
        self.data_realizacao = datetime.now()
        self.status = StatusTarefa.CONCLUIDA

    # --- apresentação ---

    def __str__(self):
        return f"[Prática] {super().__str__()}"

    def exibir_dados(self):
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Prática",
            f"Etapas: {self.etapas_concluidas}/{self.total_etapas}",
        ]
        return "\n".join(linhas)
