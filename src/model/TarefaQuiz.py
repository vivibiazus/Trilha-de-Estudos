from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa


class TarefaQuiz(TarefaEstudo):
    def __init__(
        self,
        titulo,
        nota,
        nota_max=10,
        descricao=None,
        data_realizacao=None,
        status=StatusTarefa.A_FAZER
    ):
        """
        Representa uma tarefa do tipo quiz.

        Aqui controlamos:
        - nota obtida no quiz = nota
        - nota máxima possível = nota_max
        """
        # Inicializa os dados comuns de qualquer TarefaEstudo
        super().__init__(
            titulo=titulo,
            descricao=descricao,
            data_realizacao=data_realizacao,
            status=status
        )

        # Inicializa atributos específicos com valores padrão válidos
        # evita problema de atributo inexistente dentro dos setters
        self.__nota_max = 10.0
        self.__nota = 0.0

        # Aplica as regras de validação dos setters
        self.nota_max = nota_max
        self.nota = nota

    # --- Atributos específicos do quiz ---

    @property
    def nota_max(self):
        """Retorna a nota máxima possível para o quiz."""
        return self.__nota_max

    @nota_max.setter
    def nota_max(self, valor):
        """
        Define a nota máxima do quiz.

        - Converte o valor para float.
        - Se for inválido, usa 10.0 como padrão.
        - Garante que seja, no mínimo, 1.0.
        - Após definir a nota máxima, ajusta a nota atual
          para não ultrapassar esse limite.
        """
        try:
            valor_float = float(valor)
        except (TypeError, ValueError):
            valor_float = 10.0

        if valor_float < 1.0:
            valor_float = 1.0

        self.__nota_max = valor_float

        # Garante que a nota fique dentro do intervalo [0, nota_max]
        if self.__nota < 0.0:
            self.__nota = 0.0
        if self.__nota > self.__nota_max:
            self.__nota = self.__nota_max

    @property
    def nota(self):
        """Retorna a nota obtida no quiz."""
        return self.__nota

    @nota.setter
    def nota(self, valor):
        """
        Define a nota obtida no quiz.

        - Converte o valor para float.
        - Se for inválido, usa 0.0 como padrão.
        - Garante que não seja negativa.
        - Garante que não ultrapasse a nota máxima configurada.
        """
        try:
            valor_float = float(valor)
        except (TypeError, ValueError):
            valor_float = 0.0

        if valor_float < 0.0:
            valor_float = 0.0

        if valor_float > self.__nota_max:
            valor_float = self.__nota_max

        self.__nota = valor_float

    # --- Regra de progresso ---

    def progresso(self):
        """
        Calcula o progresso do quiz como fração entre 0.0 e 1.0.

        Exemplo:
            nota_max = 10  e  nota = 7  -->  progresso = 0.7 (70%)
        """
        return self.nota / self.nota_max

    # --- Ações ao término ---

    def definir_termino(self):
        """
        Ao concluir o quiz, registra a data de realização como a data/hora atual.

        A mudança de status para CONCLUIDA é feita pelo método concluir()
        herdado de TarefaEstudo.
        """
        self.data_realizacao = datetime.now()

    # --- Apresentação ---

    def __str__(self):
        """Indica que se trata de uma tarefa do tipo Quiz + texto base."""
        return f"[Quiz] {super().__str__()}"

    def exibir_dados(self):
        """
        Devolve um texto com as informações do quiz,
        incluindo os dados básicos da tarefa e a nota obtida.
        """
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Quiz",
            f"Nota: {self.nota}/{self.nota_max}",
        ]
        return "\n".join(linhas)

