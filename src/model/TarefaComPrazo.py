from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa

class TarefaComPrazo(TarefaEstudo):
    """
    Decorator= envolve uma TarefaEstudo e aplica penalidade no progresso
    se a tarefa for concluída após o prazo. Mantém a interface de TarefaEstudo.
    """

    def __init__(self, base, prazo=None, penalidade=0.0):
        # Reaproveita dados da tarefa base; o setter de status já valida
        super().__init__(
            titulo=base.titulo,
            descricao=base.descricao,
            data_realizacao=base.data_realizacao,
            status=base.status
        )
        self.__base = base
        self.__prazo = None
        self.prazo = prazo              # usa setter
        self.__penalidade = 0.0
        self.penalidade = penalidade    # usa setter

    # --- campos adicionais ---

    @property
    def prazo(self):
        return self.__prazo

    @prazo.setter
    def prazo(self, valor):
        # aceita string 'dd-mm-YYYY HH:MM' ou objeto com .strftime (ex.: datetime)
        self.__prazo = None
        if valor is None:
            return
        # tenta como string
        try:
            self.__prazo = datetime.strptime(str(valor), "%d-%m-%Y %H:%M")
            return
        except Exception:
            pass
        # tenta como objeto com .strftime
        try:
            _ = valor.strftime("%d-%m-%Y %H:%M")
            self.__prazo = valor
        except Exception:
            print("Prazo inválido. Use 'dd-mm-YYYY HH:MM' ou um datetime.")

    @property
    def penalidade(self):
        return self.__penalidade

    @penalidade.setter
    def penalidade(self, valor):
        try:
            p = float(valor)
        except Exception:
            p = 0.0
        if p < 0.0:
            p = 0.0
        if p > 1.0:
            p = 1.0
        self.__penalidade = p

    # --- comportamento ---

    def progresso(self):
        """
        Se houver prazo e a tarefa estiver CONCLUÍDA após o prazo,
        aplica a penalidade ao progresso da base.
        """
        progresso_base_tarefa = self.__base.progresso()

        if self.__prazo and self.status == StatusTarefa.CONCLUIDA and self.data_realizacao:
            if self.data_realizacao > self.__prazo:
                fator = 1.0 - self.__penalidade
                if fator < 0.0:
                    fator = 0.0
                progresso_base_tarefa = progresso_base_tarefa * fator

        # garante [0.0, 1.0]
        if progresso_base_tarefa < 0.0:
            progresso_base_tarefa = 0.0
        if progresso_base_tarefa > 1.0:
            progresso_base_tarefa = 1.0
        return progresso_base_tarefa

    def concluir(self):
        """Conclui a base e registra conclusão aqui."""
        self.__base.concluir()
        self.data_realizacao = datetime.now()
        self.status = StatusTarefa.CONCLUIDA
        self.definir_termino()

    def definir_termino(self):
        pass

    def exibir_dados(self):
        data_prazo = self.__prazo.strftime("%d-%m-%Y %H:%M") if self.__prazo else "Sem prazo"
        linhas = [
            self.__base.exibir_dados(),
            "Decorator: Prazo",
            f"Prazo: {data_prazo}",
            f"Penalidade se atrasar: {int(self.__penalidade * 100)}%",
            f"Progresso (c/ prazo): {self.progresso()*100:.0f}%"
        ]
        return "\n".join(linhas)
