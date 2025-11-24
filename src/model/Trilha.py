class Trilha:
    def __init__(self, nome):
        self.__nome = str(nome).strip().title() if nome else "Trilha"
        self.__cursos = []

    # --- encapsulamento ---

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = str(valor).strip().title() if valor else "Trilha"

    @property
    def cursos(self):
        # estilo da prof: retorna a lista interna (sem cópia)
        return self.__cursos

    # --- composição ---

    def adicionar_curso(self, curso):
        # espera instância de Curso
        if curso is not None:
            self.__cursos.append(curso)

    # --- cálculo de progresso com Strategy ---

    def progresso(self, estrategia):
        """
        Recebe um objeto que implementa EstrategiaProgresso
        e delega o cálculo do progresso da trilha.
        """
        if estrategia is None:
            return 0.0
        return estrategia.calcular(self)

    # --- apresentação ---

    def __str__(self):
        return f"Trilha: {self.__nome} ({len(self.__cursos)} cursos)"

    def exibir_dados(self, estrategia=None):
        linhas = [
            f"Trilha: {self.__nome}",
            f"Quantidade de cursos: {len(self.__cursos)}",
        ]
        if estrategia is not None:
            linhas.append(f"Progresso da trilha: {self.progresso(estrategia)*100:.0f}%")
        return "\n".join(linhas)
