from datetime import datetime
from abc import ABC, abstractmethod
from .StatusTarefa import StatusTarefa


class TarefaEstudo(ABC):
    def __init__(self, titulo, descricao=None, data_realizacao=None, status=StatusTarefa.A_FAZER):
        """
        Classe base abstrata para representar uma tarefa de estudo.
        Define atributos e comportamentos comuns a todos os tipos de tarefa.
        """
        self.__titulo = str(titulo).strip().title() if titulo else "Tarefa"
        self.__descricao = descricao
        self.__data_realizacao = None

        # Caso uma data inicial seja informada, utiliza o setter para validar/converter.
        if data_realizacao is not None:
            self.data_realizacao = data_realizacao

        # Define o status inicial, validando contra o Enum StatusTarefa.
        self.status = status

    # --- Encapsulamento: título, descrição e data de realização ---

    @property
    def titulo(self):
        """Retorna o título da tarefa."""
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        """
        Define o título da tarefa.
        Aplica strip e title, e utiliza um valor padrão caso o título seja vazio.
        """
        self.__titulo = str(valor).strip().title() if valor else "Tarefa"

    @property
    def descricao(self):
        """Retorna a descrição da tarefa (pode ser None)."""
        return self.__descricao

    @descricao.setter
    def descricao(self, valor):
        """Define a descrição da tarefa."""
        self.__descricao = valor

    @property
    def data_realizacao(self):
        """Retorna a data de realização da tarefa (datetime ou None)."""
        return self.__data_realizacao

    @data_realizacao.setter
    def data_realizacao(self, data):
        """
        Define a data de realização da tarefa.

        Aceita:
        - string no formato 'dd-mm-YYYY'; ou
        - objeto datetime (ou similar, que possua strftime).

        Em caso de formato inválido, mantém None e exibe uma mensagem.
        """
        self.__data_realizacao = None

        if data is None:
            return

        # Tenta converter a partir de uma string no formato 'dd-mm-YYYY'
        try:
            self.__data_realizacao = datetime.strptime(str(data), "%d-%m-%Y")
            return
        except Exception:
            pass

        # Tenta utilizar diretamente um objeto com .strftime (ex.: datetime)
        try:
            _ = data.strftime("%d-%m-%Y")
            self.__data_realizacao = data
        except Exception:
            print("Data em formato inválido. Use 'dd-mm-YYYY' ou um objeto datetime.")

    # --- Encapsulamento: status da tarefa ---

    @property
    def status(self):
        """Retorna o status atual da tarefa (valor do Enum StatusTarefa)."""
        return self.__status

    @status.setter
    def status(self, novo_status):
        """
        Define o status da tarefa, garantindo que seja um valor válido do Enum StatusTarefa.
        Caso contrário, utiliza o status padrão A_FAZER.
        """
        if novo_status in (StatusTarefa.A_FAZER, StatusTarefa.EM_ANDAMENTO, StatusTarefa.CONCLUIDA):
            self.__status = novo_status
        else:
            self.__status = StatusTarefa.A_FAZER

    # --- Propriedade derivada do status ---

    @property
    def concluida(self):
        """
        Indica se a tarefa está concluída.

        Retorna:
            True, se o status for CONCLUIDA;
            False, caso contrário.
        """
        return self.status == StatusTarefa.CONCLUIDA

    # --- Ciclo de vida da tarefa ---

    def concluir(self):
        """
        Marca a tarefa como concluída e delega para definir_termino()
        as ações específicas de cada subtipo de tarefa.
        """
        self.status = StatusTarefa.CONCLUIDA
        self.definir_termino()

    def iniciar_estudo(self):
        """Altera o status da tarefa para EM_ANDAMENTO."""
        self.status = StatusTarefa.EM_ANDAMENTO

    # --- Representação e comparação ---

    def __str__(self):
        """Retorna uma representação textual simples da tarefa, incluindo o status."""
        return f"{self.__class__.__name__}: {self.__titulo} [{self.status.value}]"

    def __eq__(self, outro):
        """
        Compara duas tarefas pelo título e pela data de realização.
        Retorna False caso o objeto comparado não tenha os mesmos atributos.
        """
        try:
            return (self.titulo == outro.titulo) and (self.data_realizacao == outro.data_realizacao)
        except Exception:
            return False

    # --- Contrato das subclasses (abstração e polimorfismo) ---

    @abstractmethod
    def progresso(self):
        """
        Retorna o progresso da tarefa como um número entre 0.0 e 1.0.

        Cada subtipo de tarefa deve implementar sua própria forma de cálculo
        (por exemplo, páginas lidas, etapas concluídas, entregas aprovadas etc.).
        """
        pass

    @abstractmethod
    def definir_termino(self):
        """
        Executa ações específicas ao concluir a tarefa.

        Exemplos:
        - registrar data de conclusão;
        - calcular nota final;
        - atualizar campos derivados.
        """
        pass

    # --- Exibição genérica de dados ---

    def exibir_dados(self):
        """
        Retorna uma string com informações básicas da tarefa:
        título, descrição (se houver), status e data de realização.
        """
        linhas = [f"Tarefa: {self.titulo}"]

        if self.descricao:
            linhas.append(f"Descrição: {self.descricao}")

        linhas.append(f"Status: {self.status.value}")

        data = (
            self.data_realizacao.strftime("%d-%m-%Y")
            if self.data_realizacao
            else "Sem data definida"
        )
        linhas.append(f"Data Realização: {data}")

        return "\n".join(linhas)
