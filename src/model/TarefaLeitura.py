from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa

class TarefaLeitura(TarefaEstudo):
    def __init__(self, titulo, total_paginas, paginas_lidas=0, descricao=None,
                 data_realizacao=None, status=StatusTarefa.A_FAZER):
        super().__init__(titulo=titulo, descricao=descricao,
                         data_realizacao=data_realizacao, status=status)
        # ordem importa: primeiro define total_paginas, depois paginas_lidas (clamp usa total_paginas)
        self.total_paginas = total_paginas
        self.paginas_lidas = paginas_lidas

    # --- getters e setters ---

    @property
    def total_paginas(self):
        return self.__total_paginas

    @total_paginas.setter
    def total_paginas(self, valor):
        try:
            v = int(valor)
        except (TypeError, ValueError):
            v = 1
        if v < 1:
            v = 1
        self.__total_paginas = v
        # ao reduzir total_paginas, garanta que paginas_lidas continue válido
        if hasattr(self, "_TarefaLeitura__paginas_lidas"):
            if self.__paginas_lidas > self.__total_paginas:
                self.__paginas_lidas = self.__total_paginas

    @property
    def paginas_lidas(self):
        return self.__paginas_lidas

    @paginas_lidas.setter
    def paginas_lidas(self, valor):
        try:
            v = int(valor)
        except (TypeError, ValueError):
            v = 0
        if v < 0:
            v = 0
        # clamp entre 0 e total_paginas
        if v > self.__total_paginas:
            v = self.__total_paginas
        self.__paginas_lidas = v

    # --- apresentação ---

    def __str__(self):
        return f"[Leitura] {super().__str__()}"

    def exibir_dados(self):
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Leitura",
            f"Páginas lidas: {self.paginas_lidas} de {self.total_paginas}",
        ]
        return "\n".join(linhas)

    # --- regra de término ---

    def definir_termino(self):
        """Ao concluir, define data atual e marca como CONCLUÍDA."""
        self.data_realizacao = datetime.now()
        self.status = StatusTarefa.CONCLUIDA
