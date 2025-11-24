from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa

class TarefaComPrazo(TarefaEstudo):
    """
    Decorator = envolve uma TarefaEstudo e aplica penalidade no progresso
    se a conclusão ocorrer após o prazo definido.
    """

    def __init__(self, base, prazo=None, penalidade=0.0):
        status_base = base.status if base.status in (
            StatusTarefa.A_FAZER, StatusTarefa.EM_ANDAMENTO, StatusTarefa.CONCLUIDA
        ) else StatusTarefa.A_FAZER

        super().__init__(
            titulo=base.titulo,
            descricao=base.descricao,
            data_realizacao=base.data_realizacao,
            status=status_base
        )

        self.__base = base
        self.__prazo = None
        self.prazo = prazo  # usa o setter

        try:
            valor = float(penalidade)
        except (TypeError, ValueError):
            valor = 0.0
        if valor < 0.0:
            valor = 0.0
        if valor > 1.0:
            valor = 1.0
        self.__penalidade = valor

    # --- propriedades do decorator ---

    @property
    def prazo(self):
        return self.__prazo

    @prazo.setter
    def prazo(self, valor):
        """
        Aceita string 'dd-mm-YYYY HH:MM' ou objeto com .strftime (ex.: datetime).
        Sem isinstance: tenta strptime; se falhar, tenta usar .strftime; senão mantém None.
        """
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
        except (TypeError, ValueError):
            p = 0.0
        if p < 0.0:
            p = 0.0
        if p > 1.0:
            p = 1.0
        self.__penalidade = p

    # --- comportamento ---

    def progresso(self):
        """
        Se houver prazo e a tarefa estiver concluída após o prazo,
        aplica a penalidade ao progresso da tarefa base.
        """
        progresso_base = self.__base.progresso()

        if self.__prazo and self.status == StatusTarefa.CONCLUIDA and self.data_realizacao:
            if self.data_realizacao > self.__prazo:
                fator_penalidade = 1.0 - self.__penalidade
                if fator_penalidade < 0.0:
                    fator_penalidade = 0.0
                progresso_base = progresso_base * fator_penalidade

        if progresso_base < 0.0:
            progresso_base = 0.0
        if progresso_base > 1.0:
            progresso_base = 1.0
        return progresso_base

    def concluir(self):
        """
        Conclui a base e o decorator.
        """
        self.__base.concluir()
        self.data_realizacao = datetime.now()
        self.status = StatusTarefa.CONCLUIDA
        self.definir_termino()

    def definir_termino(self):
        # Mantém simples (estilo da prof). Nada específico adicional aqui.
        pass

    def exibir_dados(self):
        texto_base = self.__base.exibir_dados()
        texto_prazo = self.__prazo.strftime("%d-%m-%Y %H:%M") if self.__prazo else "Sem prazo"
        texto = "\n".join([
            texto_base,
            "Decorator: Prazo",
            f"Prazo: {texto_prazo}",
            f"Penalidade se atrasar: {int(self.__penalidade * 100)}%",
            f"Progresso (com prazo): {self.progresso()*100:.0f}%"
        ])
        return texto
