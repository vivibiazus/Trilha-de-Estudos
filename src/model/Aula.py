class Aula:
    def __init__(self, titulo):
# Chama o setter para aplicar as regras do título (strip, title e valor padrão).
        self.titulo = titulo
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
        """
        Retorna a lista de tarefas associadas à aula.
        A inclusão de novas tarefas deve ser feita pelo método adicionar_tarefa().
        """
        return self.__tarefas

    # --- operações de composição ---

    def adicionar_tarefa(self, tarefa):
        """
        Adiciona uma tarefa de estudo à aula.
        Espera um objeto de alguma subclasse de TarefaEstudo.
        """
        if tarefa is not None:
            self.__tarefas.append(tarefa)

    # --- cálculo de progresso da aula ---

    def progresso(self):
        """
        Calcula o progresso médio da aula com base nas tarefas.
        Se não houver tarefas, o progresso é 0.0.
        """
        if not self.__tarefas:
            return 0.0

        soma_progresso = 0.0
        for tarefa in self.__tarefas:
            # cada tarefa concreta sabe calcular o próprio progresso()
            soma_progresso += tarefa.progresso()

        return soma_progresso / len(self.__tarefas)

    # --- apresentação ---

    def __str__(self):
        return f"Aula: {self.__titulo} ({len(self.__tarefas)} tarefas)"

    def exibir_dados(self):
        linhas = [
            f"Aula: {self.__titulo}",
            f"Quantidade de tarefas: {len(self.__tarefas)}",
            f"Progresso da aula: {self.progresso() * 100:.0f}%",
        ]
        return "\n".join(linhas)
