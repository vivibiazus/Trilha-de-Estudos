from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa


class TarefaComPrazo(TarefaEstudo):
    """
    Decorator = Envolve uma tarefa base 
    e aplica uma penalidade no progresso
    caso ela seja concluída após o prazo definido.
    """

    def __init__(self, tarefa_base, prazo=None, penalidade=0.0):
        """
        Parâmetros:
            tarefa_base:
                Instância concreta de TarefaEstudo (Leitura, Quiz, Prática, Projeto, ...).
            prazo:
                Objeto datetime OU string no formato 'dd-mm-YYYY HH:MM' (opcional).

            penalidade:
                Fração entre 0.0 e 1.0 que será descontada do progresso
                caso a tarefa seja concluída depois do prazo.
        """
        if not isinstance(tarefa_base, TarefaEstudo):
            raise TypeError("tarefa_base deve ser uma instância de TarefaEstudo.")

        # Reaproveita os dados da tarefa base
        super().__init__(
            titulo=tarefa_base.titulo,
            descricao=tarefa_base.descricao,
            data_realizacao=tarefa_base.data_realizacao,
            status=tarefa_base.status,
        )

        self.__tarefa_base = tarefa_base

        self.__prazo = None
        self.prazo = prazo  # usa o setter

        self.__penalidade = 0.0
        self.penalidade = penalidade  # usa o setter

    # --- campos adicionais ---

    @property
    def prazo(self):
        """Retorna o prazo limite da tarefa (datetime ou None)."""
        return self.__prazo

    @prazo.setter
    def prazo(self, valor):
        """
        Define o prazo limite da tarefa.

        Aceita:
            - None → sem prazo;
            - datetime;
            - string 'dd-mm-YYYY HH:MM'.

        Em formato inválido, mantém None e exibe uma mensagem.
        """
        self.__prazo = None

        if valor is None:
            return

        if isinstance(valor, datetime):
            self.__prazo = valor
            return

        if isinstance(valor, str):
            try:
                self.__prazo = datetime.strptime(valor, "%d-%m-%Y %H:%M")
            except ValueError as erro:
                print(f"Prazo em formato inválido: {erro}")
            return

        print("Prazo inválido. Use datetime ou string 'dd-mm-YYYY HH:MM'.")

    @property
    def penalidade(self):
        """Retorna a penalidade aplicada em caso de atraso (entre 0.0 e 1.0)."""
        return self.__penalidade

    @penalidade.setter
    def penalidade(self, valor):
        """
        Define a penalidade para atraso como número entre 0.0 e 1.0.

        - Valores inválidos viram 0.0;
        - menor que 0 → 0.0;
        - maior que 1 → 1.0.
        """
        try:
            valor_convertido = float(valor)
        except (TypeError, ValueError):
            valor_convertido = 0.0

        if valor_convertido < 0.0:
            valor_convertido = 0.0
        if valor_convertido > 1.0:
            valor_convertido = 1.0

        self.__penalidade = valor_convertido

    # --- comportamento ---

    def progresso(self):
        """
        Calcula o progresso considerando o prazo.
        - usa o progresso da tarefa base;
        - se houver prazo e a tarefa estiver concluída depois dele,
          aplica a penalidade;
        - o resultado final é mantido entre 0.0 e 1.0.
        """
        progresso_base = self.__tarefa_base.progresso()

        if (
            self.__prazo is not None
            and self.status == StatusTarefa.CONCLUIDA
            and self.data_realizacao is not None
            and self.data_realizacao > self.__prazo
        ):
            fator = 1.0 - self.__penalidade
            if fator < 0.0:
                fator = 0.0
            progresso_base *= fator

        if progresso_base < 0.0:
            progresso_base = 0.0
        if progresso_base > 1.0:
            progresso_base = 1.0

        return progresso_base

    def concluir(self):
        """
        Conclui a tarefa base e registra a conclusão também no decorator.
        """
        self.__tarefa_base.concluir()
        self.data_realizacao = datetime.now()
        self.status = StatusTarefa.CONCLUIDA
        # Não há regra extra de término além da tarefa base.

    def definir_termino(self):
        """Decorator não adiciona regra extra de término além da tarefa base."""
        # Aqui não mudamos nada em relação à tarefa base.
        pass

    def exibir_dados(self):
        """
        Exibe os dados da tarefa base + informações de prazo e penalidade.
        """
        texto_base = self.__tarefa_base.exibir_dados()
        prazo_formatado = (
            self.__prazo.strftime("%d-%m-%Y %H:%M") if self.__prazo else "Sem prazo"
        )

        linhas = [
            texto_base,
            "Decorator: Tarefa com prazo",
            f"Prazo: {prazo_formatado}",
            f"Penalidade se atrasar: {int(self.__penalidade * 100)}%",
            f"Progresso (com prazo): {self.progresso() * 100:.0f}%",
        ]
        return "\n".join(linhas)
