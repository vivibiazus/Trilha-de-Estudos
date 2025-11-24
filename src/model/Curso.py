class Curso:
    def __init__(self, titulo, carga_horas=0):
        self.__titulo = str(titulo) if titulo else "Curso"
        self.__carga_horas = 0
        self.carga_horas = carga_horas  # usa o setter
        self.__aulas = []

    # --- encapsulamento ---

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        self.__titulo = str(valor).strip().title() if valor else "Curso"

    @property
    def carga_horas(self):
        return self.__carga_horas

    @carga_horas.setter
    def carga_horas(self, valor):
        try:
            v = int(valor)
        except (TypeError, ValueError):
            v = 0
        if v < 0:
            v = 0
        self.__carga_horas = v

    @property
    def aulas(self):
        # devolve CÓPIA para manter encapsulamento
        return self.__aulas

    # --- composição ---

    def adicionar_aula(self, aula):
        # espera uma instância de Aula
        if aula is not None:
            self.__aulas.append(aula)

    # --- progresso do curso ---

    def progresso(self):
        if not self.__aulas:
            return 0.0
        soma = 0.0
        for a in self.__aulas:
            soma += a.progresso()
        return soma / len(self.__aulas)

    # --- apresentação ---

    def __str__(self):
        return f"Curso: {self.__titulo} ({len(self.__aulas)} aulas, {self.__carga_horas}h)"

    def exibir_dados(self):
        linhas = [
            f"Curso: {self.__titulo}",
            f"Carga horária: {self.__carga_horas}h",
            f"Quantidade de aulas: {len(self.__aulas)}",
            f"Progresso do curso: {self.progresso()*100:.0f}%",
        ]
        return "\n".join(linhas)
