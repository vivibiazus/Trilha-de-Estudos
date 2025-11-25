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
        """
        Representa uma tarefa de projeto.

        Aqui vai controlar:
        - quantas entregas o projeto prevê = total_entregas
        - quantas entregas já foram aprovadas = entregas_aprovadas 
        """
        # Inicializa os dados comuns de qualquer TarefaEstudo
        super().__init__(
            titulo=titulo,
            descricao=descricao,
            data_realizacao=data_realizacao,
            status=status
        )

        # Inicializa atributos específicos com valores padrão válidos
        # isso evita problemas de atributo inexistente nos setters
        self.__total_entregas = 1
        self.__entregas_aprovadas = 0

        # aplica as regras de validação dos setters
        self.total_entregas = total_entregas
        self.entregas_aprovadas = entregas_aprovadas

    # --- Atributos específicos do projeto ---

    @property
    def total_entregas(self):
        """Retorna o total de entregas previstas para o projeto."""
        return self.__total_entregas

    @total_entregas.setter
    def total_entregas(self, valor):
        """
        Define o total de entregas do projeto.

        - Converte o valor para inteiro.
        - Garante que seja, no mínimo, 1.
        - Se o valor for inválido, assume 1.
        - Se já existirem entregas aprovadas, ajusta para não ultrapassar o novo total.
        """
        try:
            valor_inteiro = int(valor)
        except (TypeError, ValueError):
            valor_inteiro = 1

        if valor_inteiro < 1:
            valor_inteiro = 1

        self.__total_entregas = valor_inteiro

        # Garante que entregas_aprovadas fique dentro do limite [0, total_entregas]
        if self.__entregas_aprovadas > self.__total_entregas:
            self.__entregas_aprovadas = self.__total_entregas

    @property
    def entregas_aprovadas(self):
        """Retorna a quantidade de entregas já aprovadas no projeto."""
        return self.__entregas_aprovadas

    @entregas_aprovadas.setter
    def entregas_aprovadas(self, valor):
        """
        Define quantas entregas já foram aprovadas.

        - Converte o valor para inteiro.
        - Garante que não seja menor que 0.
        - Garante que não ultrapasse o total de entregas.
        - Se o valor for inválido, assume 0.
        """
        try:
            valor_inteiro = int(valor)
        except (TypeError, ValueError):
            valor_inteiro = 0

        if valor_inteiro < 0:
            valor_inteiro = 0

        if valor_inteiro > self.__total_entregas:
            valor_inteiro = self.__total_entregas

        self.__entregas_aprovadas = valor_inteiro

    # --- Regra de progresso ---

    def progresso(self):
        """
        Calcula o progresso do projeto como fração entre 0.0 e 1.0.

        Exemplo:
            total_entregas = 4  e  entregas_aprovadas = 2  --> progresso = 0.5 (50%)
        """
        return self.entregas_aprovadas / self.total_entregas

    def definir_termino(self):
        """
        Ao concluir o projeto, registra a data de realização como a data/hora atual.

        A mudança de status para CONCLUIDA é feita pelo método concluir() herdado de TarefaEstudo.
        """
        self.data_realizacao = datetime.now()

    # --- Apresentação ---

    def __str__(self):
        """Indica que se trata de uma tarefa de projeto e reutiliza o texto base."""
        return f"[Projeto] {super().__str__()}"

    def exibir_dados(self):
        """
        Devolve um texto com as informações do projeto,
        incluindo dados básicos da tarefa e o resumo das entregas.
        """
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Projeto",
            f"Entregas aprovadas: {self.entregas_aprovadas}/{self.total_entregas}",
        ]
        return "\n".join(linhas)

