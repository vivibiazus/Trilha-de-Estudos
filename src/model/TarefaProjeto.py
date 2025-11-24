from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa


class TarefaProjeto(TarefaEstudo):
    def __init__(self, titulo, total_entregas, entregas_aprovadas=0, descricao=None,
                 data_realizacao=None, status=StatusTarefa.A_FAZER):
        super().__init__(titulo=titulo, descricao=descricao,
                         data_realizacao=data_realizacao, status=status)
        # defina o total antes para que o clamp funcione ao setar aprovadas
        self.total_entregas = total_entregas
        self.entregas_aprovadas = entregas_aprovadas

    # --- getters e setters ---

    @property
    def total_entregas(self):
        return self.__total_entregas

    @total_entregas.setter
    def total_entregas(self, v):
        try:
            v = int(v)
        except (TypeError, ValueError):
            v = 1
        if v < 1:
            v = 1
        self.__total_entregas = v
        # revalida aprovadas se já existir e estiver fora do limite
        try:
            if self.__entregas_aprovadas > v:
                self.__entregas_aprovadas = v
        except AttributeError:
            # ainda não foi definido, ignore
            pass

    @property
    def entregas_aprovadas(self):
        return self.__entregas_aprovadas

    @entregas_aprovadas.setter
    def entregas_aprovadas(self, v):
        try:
            v = int(v)
        except (TypeError, ValueError):
            v = 0
        if v < 0:
            v = 0
        try:
            if v > self.__total_entregas:
                v = self.__total_entregas
        except AttributeError:
            # total ainda não setado; apenas garante não-negativo
            pass
        self.__entregas_aprovadas = v

    # --- obrigatórios da hierarquia ---

    def progresso(self):
        """Retorna fração 0..1 baseada em entregas aprovadas."""
        if not self.total_entregas:
            return 0.0
        return self.entregas_aprovadas / float(self.total_entregas)

    def definir_termino(self):
        """Conclui o projeto marcando data e status."""
        self.data_realizacao = datetime.now()
        self.status = StatusTarefa.CONCLUIDA

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
