class Trilha:
    def __init__(self, nome):
        """
        Representa uma trilha de estudos.
        Uma trilha = por vários cursos 
        e é usada pelas estratégias de progresso para calcular um valor agregado.
        """
       # Usa o setter de nome (self.nome = ...) porque ele já:
       # - converte o valor para string;
       # - remove espaços extras;
       # - aplica .title();
       # - define "Trilha" se nada for informado.
        self.nome = nome

        # Lista de cursos que fazem parte desta trilha.
        self.__cursos = []

    # --- encapsulamento ---

    @property
    def nome(self):
        """Retorna o nome da trilha."""
        return self.__nome

    @nome.setter
    def nome(self, valor):
        """
        Define o nome da trilha.
        - Converte para string;
        - remove espaços extras;
        - aplica .title();
        - se vier vazio/None, usa 'Trilha' como padrão.
        """
        self.__nome = str(valor).strip().title() if valor else "Trilha"

    @property
    def cursos(self):
        """
        Retorna a lista de cursos associados à trilha.

        A inclusão de novos cursos deve ser feita pelo método adicionar_curso().
        """
        return self.__cursos

    # --- composição ---

    def adicionar_curso(self, curso):
        """
        Adiciona um curso à trilha.

        Espera receber um objeto da classe Curso (ou compatível).
        """
        if curso is not None:
            self.__cursos.append(curso)

    # --- cálculo de progresso com Strategy ---

    def progresso(self, estrategia):
        """
        Calcula o progresso da trilha utilizando uma estratégia.

        Parâmetros:
            estrategia: objeto que implementa o método calcular(trilha),
            como MediaSimplesEstrategia ou MediaPonderadaPorCargaEstrategia.

                       
        Retorna:
            Número entre 0.0 e 1.0 representando o progresso total.
            Se nenhuma estratégia for informada, retorna 0.0.
        """
        if estrategia is None:
            return 0.0

        return estrategia.calcular(self)

    # --- apresentação ---

    def __str__(self):
        """Retorna um resumo curto da trilha."""
        return f"Trilha: {self.__nome} ({len(self.__cursos)} cursos)"

    def exibir_dados(self, estrategia=None):
        """
        Monta um texto com as informações principais da trilha.
        Se uma estratégia for fornecida, inclui também o percentual
        de progresso calculado por ela.
        """
        linhas = [
            f"Trilha: {self.__nome}",
            f"Quantidade de cursos: {len(self.__cursos)}",
        ]

        if estrategia is not None:
            progresso_trilha = self.progresso(estrategia) * 100
            linhas.append(f"Progresso da trilha: {progresso_trilha:.0f}%")

        return "\n".join(linhas)

