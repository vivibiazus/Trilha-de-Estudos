from .EstrategiaProgresso import EstrategiaProgresso

class MediaPonderadaPorCargaEstrategia(EstrategiaProgresso):
    def calcular(self, trilha):
        cursos = trilha.cursos
        if not cursos:
            return 0.0
            
        soma = 0.0
        soma_pesos = 0
        
        for c in cursos:
            peso = c.carga_horas or 1               # carga_horas já vem normalizada (inteiro >= 0); se for 0, usa 1 como peso mínimo
            soma += c.progresso() * peso
            soma_pesos += peso
            
        if soma_pesos == 0:
            
            return 0.0
        return soma / soma_pesos
