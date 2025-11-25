from .EstrategiaProgresso import EstrategiaProgresso


class MediaPonderadaPorCargaEstrategia(EstrategiaProgresso):
    def calcular(self, trilha):
        """
        Calcula o progresso da trilha usando média ponderada
        pela carga horária de cada curso.
        Retorna:
            Número entre 0.0 e 1.0 representando o progresso total.
        """
        cursos_da_trilha = trilha.cursos
        if not cursos_da_trilha:
            return 0.0

        soma_progresso_ponderado = 0.0
        soma_pesos = 0

        for curso in cursos_da_trilha: # Se carga_horas for 0, considera peso 1 para não descartar o curso.
            peso_curso = curso.carga_horas or 1
            soma_progresso_ponderado += curso.progresso() * peso_curso
            soma_pesos += peso_curso

        if soma_pesos == 0:
            return 0.0

        return soma_progresso_ponderado / soma_pesos
