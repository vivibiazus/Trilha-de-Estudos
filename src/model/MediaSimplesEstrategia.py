from .EstrategiaProgresso import EstrategiaProgresso

class MediaSimplesEstrategia(EstrategiaProgresso):
    def calcular(self, trilha):
        cursos = trilha.cursos
        if not cursos:
            return 0.0
        soma = 0.0
        for c in cursos:
            soma += c.progresso()
        return soma / len(cursos)
