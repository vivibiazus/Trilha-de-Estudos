from datetime import datetime
from abc import ABC, abstractmethod
from .StatusTarefa import StatusTarefa


class TarefaEstudo(ABC):
    def __init__(self, titulo, descricao=None, data_realizacao=None, status=StatusTarefa.A_FAZER):
        self.__titulo = str(titulo).strip().title() if titulo else "Tarefa"
        self.__descricao = descricao
        self.__data_realizacao = None
        if data_realizacao is not None:
            self.data_realizacao = data_realizacao  # usa o setter
        self.status = status  # valida pelo setter

    # --- encapsulamento ---

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        self.__titulo = str(valor).strip().title() if valor else "Tarefa"

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, valor):
        self.__descricao = valor

    @property
    def data_realizacao(self):
        return self.__data_realizacao

    @data_realizacao.setter
    def data_realizacao(self, data):
        """
        Aceita string 'dd-mm-YYYY' ou datetime.
        tenta como string; se falhar, tenta usar .strftime;
        se não der, mantém None e avisa.
        """
        self.__data_realizacao = None
        if data is None:
            return         # tenta como string 'dd-mm-YYYY'
        try:
            self.__data_realizacao = datetime.strptime(str(data), "%d-%m-%Y")
            return
        except Exception:
            pass         # tenta como objeto com .strftime (ex.: datetime)
        try:
            _ = data.strftime("%d-%m-%Y")
            self.__data_realizacao = data
        except Exception:
            print("Data em formato inválido. Use 'dd-mm-YYYY' ou um datetime.")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status):
        if novo_status in (StatusTarefa.A_FAZER, StatusTarefa.EM_ANDAMENTO, StatusTarefa.CONCLUIDA):
            self.__status = novo_status
        else:
            self.__status = StatusTarefa.A_FAZER

  # --- derivado do status (sem flag duplicada) ---
    @property
    def concluida(self):
        """True se o status está como CONCLUÍDA."""
        return self.status == StatusTarefa.CONCLUIDA
    
    # --- ciclo de vida ---

    def concluir(self):
        self.__concluida = True
        self.status = StatusTarefa.CONCLUIDA
        self.definir_termino()

    def iniciar_estudo(self):
        self.status = StatusTarefa.EM_ANDAMENTO

    # --- apresentação / comparação ---

    def __str__(self):
        return f"{self.__class__.__name__}: {self.__titulo} [{self.status.value}]"

    def __eq__(self, outro):
        try:
            return (self.titulo == outro.titulo) and (self.data_realizacao == outro.data_realizacao)
        except Exception:
            return False

    # --- contrato das subclasses ---

    @abstractmethod
    def progresso(self):
        """Retorna número entre 0.0 e 1.0."""
        pass

    @abstractmethod
    def definir_termino(self):
        """Ações específicas ao concluir (se necessário na subclasse)."""
        pass

    # --- exibição genérica (subclasse pode sobrescrever) ---

    def exibir_dados(self):
        linhas = [f"Tarefa: {self.titulo}"]
        if self.descricao:
            linhas.append(f"Descrição: {self.descricao}")
        linhas.append(f"Status: {self.status.value}")
        data = self.data_realizacao.strftime("%d-%m-%Y") if self.data_realizacao else "Sem data definida"
        linhas.append(f"Data Realização: {data}")
        return "\n".join(linhas)
