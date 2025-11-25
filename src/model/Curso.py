class Curso:
    def __init__(self, titulo, carga_horas=0):
        """
        Representa um curso dentro da trilha.

        Aqui guardamos:
        - título do curso;
        - carga horária total;
        - lista de aulas que fazem parte desse curso.
        """
        # Inicializa o título usando o setter, que já trata espaços,
        # formatação (.title()) e define "Curso" quando não for informado.
        self.titulo = titulo

        # Inicializa carga horária com valor seguro
        self.__carga_horas = 0
        # Usa o setter para validar a carga informada.
        self.carga_horas = carga_horas

        # Lista de aulas pertencentes a este curso.
        self.__aulas = []

    # --- encapsulamento ---

    @property
    def titulo(self):
        """Retorna o título do curso."""
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        """
        Define o título do curso.

        - Converte para string;
        - remove espaços extras;
        - aplica .title();
        - se vier vazio/None, usa 'Curso' como padrão.
        """
        self.__titulo = str(valor).strip().title() if valor else "Curso"

    @property
    def carga_horas(self):
        """Retorna a carga horária total do curso (em horas)."""
        return self.__carga_horas

    @carga_horas.setter
    def carga_horas(self, valor):
        """
        Define a carga horária do curso.

        - Tenta converter para inteiro;
        - valores inválidos viram 0;
        - não permite valor negativo.
        """
        try:
            carga_convertida = int(valor)
        except (TypeError, ValueError):
            carga_convertida = 0

        if carga_convertida < 0:
            carga_convertida = 0

        self.__carga_horas = carga_convertida

    @property
    def aulas(self):
        """
        Retorna a lista de aulas associadas ao curso.

        A inclusão de novas aulas deve ser feita pelo método adicionar_aula().
        """
        return self.__aulas

    # --- composição ---

    def adicionar_aula(self, aula):
        """
        Adiciona uma aula ao curso.

        Espera receber um objeto da classe Aula (ou compatível).
        """
        if aula is not None:
            self.__aulas.append(aula)

    # --- progresso do curso ---

    def progresso(self):
        """
        Calcula o progresso médio do curso com base nas aulas.

        - Se não houver aulas cadastradas, o progresso é 0.0.
        - Caso existam aulas, faz a média dos progressos de cada aula.
        """
        if not self.__aulas:
            return 0.0

        soma_progresso = 0.0
        for aula in self.__aulas:
            soma_progresso += aula.progresso()

        return soma_progresso / len(self.__aulas)

    # --- apresentação ---

    def __str__(self):
        """Retorna um resumo curto do curso."""
        return f"Curso: {self.__titulo} ({len(self.__aulas)} aulas, {self.__carga_horas}h)"

    def exibir_dados(self):
        """
        Monta um texto com as informações principais do curso:
        título, carga horária, quantidade de aulas e progresso.
        """
        linhas = [
            f"Curso: {self.__titulo}",
            f"Carga horária: {self.__carga_horas}h",
            f"Quantidade de aulas: {len(self.__aulas)}",
            f"Progresso do curso: {self.progresso() * 100:.0f}%",
        ]
        return "\n".join(linhas)
