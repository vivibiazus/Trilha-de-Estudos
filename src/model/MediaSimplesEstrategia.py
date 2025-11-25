from .EstrategiaProgresso import EstrategiaProgresso


class MediaSimplesEstrategia(EstrategiaProgresso):
    def calcular(self, trilha):
        """
        Calcula o progresso (média simples) da trilha.
        - Pega a lista de cursos da trilha;
        - soma o progresso de cada curso;
        - divide pela quantidade total de cursos.

        Retorna:
            Número entre 0.0 e 1.0.
            Se a trilha não tiver cursos, retorna 0.0.
        """
        cursos = trilha.cursos

        # Se a trilha ainda não tiver cursos cadastrados, considera progresso 0.0.
        if not cursos:
            return 0.0

        soma_progresso = 0.0
        for curso in cursos:
            # Cada curso sabe calcular o próprio progresso().
            soma_progresso += curso.progresso()

        return soma_progresso / len(cursos)
