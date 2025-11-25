from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa


class TarefaPratica(TarefaEstudo):
    def __init__(
        self,
        titulo,
        total_etapas,
        etapas_concluidas=0,
        descricao=None,
        data_realizacao=None,
        status=StatusTarefa.A_FAZER
    ):
        super().__init__(
            titulo=titulo,
            descricao=descricao,
            data_realizacao=data_realizacao,
            status=status
        )
        # define o total antes
        self.total_etapas = total_etapas
        self.etapas_concluidas = etapas_concluidas

    # --- getters e setters ---

    @property
    def total_etapas(self):
        return self.__total_etapas

    @total_etapas.setter
    def total_etapas(self, valor):
        """
        Define o total de etapas como um inteiro >= 1.
        Se o valor for inválido, assume 1.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 1

        if valor_temporario < 1:
            valor_temporario = 1

        self.__total_etapas = valor_temporario

        # readequar etapas_concluidas ao novo total (se já existir)
        try:
            if self.__etapas_concluidas > self.__total_etapas:
                self.__etapas_concluidas = self.__total_etapas
        except AttributeError:
            # ainda não foi definido (antes de etapas_concluidas ser setado)
            pass

    @property
    def etapas_concluidas(self):
        return self.__etapas_concluidas

    @etapas_concluidas.setter
    def etapas_concluidas(self, valor):
        """
        Define etapas concluídas como inteiro entre 0 e total_etapas.
        Se o valor for inválido, assume 0.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 0

        if valor_temporario < 0:
            valor_temporario = 0

        if valor_temporario > self.__total_etapas:
            valor_temporario = self.__total_etapas

        self.__etapas_concluidas = valor_temporario

    # --- regra de negócio ---

    def progresso(self):
        """
        Retorna o progresso da tarefa prática entre 0.0 e 1.0.
        Ex.: 0.5 significa 50% das etapas concluídas.
        """
        if self.total_etapas <= 0:
            return 0.0
        return self.etapas_concluidas / self.total_etapas

    def definir_termino(self):
        """
        Ao concluir, registra a data de realização como a data/hora atual.
        O status é definido como CONCLUÍDA em TarefaEstudo.concluir().
        """
        self.data_realizacao = datetime.now()

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


