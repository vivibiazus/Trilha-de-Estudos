class Aula:
    def __init__(self, titulo):
        self.__titulo = str(titulo) if titulo else "Aula"
        self.__tarefas = []

    # --- encapsulamento ---

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        self.__titulo = str(valor).strip().title() if valor else "Aula"

    @property
    def tarefas(self):
        # expõe uma CÓPIA para não quebrar o encapsulamento
        return self.__tarefas

    # --- operações de composição ---

    def adicionar_tarefa(self, tarefa):
        # espera uma instância de TarefaEstudo ou subclasse
        if tarefa is not None:
            self.__tarefas.append(tarefa)

    # --- cálculo de progresso da aula ---

    def progresso(self):
        if not self.__tarefas:
            return 0.0
        soma = 0.0
        for t in self.__tarefas:
            soma += t.progresso()   # cada tarefa concreta implementa seu próprio progresso()
        return soma / len(self.__tarefas)

    # --- apresentação ---

    def __str__(self):
        return f"Aula: {self.__titulo} ({len(self.__tarefas)} tarefas)"

    def exibir_dados(self):
        linhas = [
            f"Aula: {self.__titulo}",
            f"Quantidade de tarefas: {len(self.__tarefas)}",
            f"Progresso da aula: {self.progresso()*100:.0f}%",
        ]
        return "\n".join(linhas)
