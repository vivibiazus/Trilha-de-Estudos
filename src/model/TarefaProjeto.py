from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa


class TarefaProjeto(TarefaEstudo):
    def __init__(
        self,
        titulo,
        total_entregas,
        entregas_aprovadas=0,
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
# define o total de entregas antes, pois entregas_aprovadas não pode ultrapassar esse valor
        self.total_entregas = total_entregas
        self.entregas_aprovadas = entregas_aprovadas

    # --- getters e setters ---

    @property
    def total_entregas(self):
        return self.__total_entregas

    @total_entregas.setter
    def total_entregas(self, valor):
        """
        Define o total de entregas como um inteiro >= 1.
        Se o valor for inválido, assume 1.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 1

        if valor_temporario < 1:
            valor_temporario = 1

        self.__total_entregas = valor_temporario

        # revalida entregas_aprovadas se já existir e estiver fora do limite
        try:
            if self.__entregas_aprovadas > self.__total_entregas:
                self.__entregas_aprovadas = self.__total_entregas
        except AttributeError:
            pass

    @property
    def entregas_aprovadas(self):
        return self.__entregas_aprovadas

    @entregas_aprovadas.setter
    def entregas_aprovadas(self, valor):
        """
        Define entregas aprovadas como inteiro entre 0 e total_entregas.
        Se o valor for inválido, assume 0.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 0

        if valor_temporario < 0:
            valor_temporario = 0

        try:
            if valor_temporario > self.__total_entregas:
                valor_temporario = self.__total_entregas
        except AttributeError:
            # total ainda não setado; apenas garante não-negativo
            pass

        self.__entregas_aprovadas = valor_temporario

    # --- obrigatórios da hierarquia ---

    def progresso(self):
        """
        Retorna a fração de entregas aprovadas entre 0.0 e 1.0.
        """
        return self.entregas_aprovadas / self.total_entregas

    def definir_termino(self):
        """
        Ao concluir, registra a data de realização como a data/hora atual.
        O status é definido como CONCLUÍDA em TarefaEstudo.concluir().
        """
        self.data_realizacao = datetime.now()

    # --- apresentação ---

    def __str__(self):
        return f"[Projeto] {super().__str__()}"

    def exibir_dados(self):
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Projeto",
            f"Entregas aprovadas: {self.entregas_aprovadas}/{self.total_entregas}",
        ]
        return "\n".join(linhas)

