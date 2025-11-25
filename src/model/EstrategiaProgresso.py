from abc import ABC, abstractmethod

class EstrategiaProgresso(ABC):
    @abstractmethod
    def calcular(self, trilha):
        """
        Recebe uma Trilha, calcula o progresso e retorna um número entre 0.0 e 1.0
        representando o progresso agregado.
        """
        pass
