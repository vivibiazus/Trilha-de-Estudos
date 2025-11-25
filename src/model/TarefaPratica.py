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
        """
        Representa uma tarefa prática
        Controla o total de etapas e quantas já foram concluídas.
        """
        # Inicializa os atributos comuns de uma tarefa de estudo.
        super().__init__(
            titulo=titulo,
            descricao=descricao,
            data_realizacao=data_realizacao,
            status=status
        )

        # Define o total de etapas antes, pois etapas_concluidas não pode ultrapassar esse valor.
        self.total_etapas = total_etapas
        self.etapas_concluidas = etapas_concluidas

    # --- Atributos específicos da tarefa prática ---

    @property
    def total_etapas(self):
        """Retorna o total de etapas previstas para a tarefa prática."""
        return self.__total_etapas

    @total_etapas.setter
    def total_etapas(self, valor):
        """
        Define o total de etapas da tarefa prática como um inteiro maior ou igual a 1.
        Em caso de valor inválido, assume 1 como padrão.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 1

        if valor_temporario < 1:
            valor_temporario = 1

        self.__total_etapas = valor_temporario

        # Se etapas_concluidas já foi definido, garante que não ultrapasse o novo total de etapas.
        try:
            if self.__etapas_concluidas > self.__total_etapas:
                self.__etapas_concluidas = self.__total_etapas
        except AttributeError:
            # Caso etapas_concluidas ainda não tenha sido definido, não há ajuste a fazer.
            pass

    @property
    def etapas_concluidas(self):
        """Retorna a quantidade de etapas já concluídas na tarefa prática."""
        return self.__etapas_concluidas

    @etapas_concluidas.setter
    def etapas_concluidas(self, valor):
        """
        Define a quantidade de etapas concluídas como um inteiro entre 0 e total_etapas.
        Em caso de valor inválido, assume 0 como padrão.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 0

        if valor_temporario < 0:
            valor_temporario = 0

        # Garante que etapas concluidas não ultrapasse o total de etapas.
        if valor_temporario > self.__total_etapas:
            valor_temporario = self.__total_etapas

        self.__etapas_concluidas = valor_temporario

    # --- Regra de progresso ---

    def progresso(self):
        """
        Calcula o progresso da tarefa prática como uma fração entre 0.0 e 1.0.

        Exemplo:
            Se total_etapas = 10 e etapas_concluidas = 5,
            o método retornará 0.5 (50% de progresso).
        """
        return self.etapas_concluidas / self.total_etapas

    def definir_termino(self):
        """
        Ao concluir a tarefa, registra a data de realização como a data/hora atual.

        A mudança de status para CONCLUIDA é realizada pelo método concluir()
        definido na classe TarefaEstudo.
        """
        self.data_realizacao = datetime.now()

    # --- Apresentação ---

    def __str__(self):
        """Retorna uma representação textual indicando que se trata de uma tarefa prática."""
        return f"[Prática] {super().__str__()}"

    def exibir_dados(self):
        """
        Retorna uma string com as informações da tarefa prática,
        incluindo os dados básicos da tarefa e o controle de etapas.
        """
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Prática",
            f"Etapas: {self.etapas_concluidas}/{self.total_etapas}",
        ]
        return "\n".join(linhas)



