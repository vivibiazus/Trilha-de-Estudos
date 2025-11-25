from datetime import datetime
from .TarefaEstudo import TarefaEstudo
from .StatusTarefa import StatusTarefa


class TarefaLeitura(TarefaEstudo):
    def __init__(
        self,
        titulo,
        total_paginas,
        paginas_lidas=0,
        descricao=None,
        data_realizacao=None,
        status=StatusTarefa.A_FAZER
    ):
        # inicializa parte comum da tarefa de estudo
        super().__init__(
            titulo=titulo,
            descricao=descricao,
            data_realizacao=data_realizacao,
            status=status
        )
        # ordem importa: primeiro define total_paginas, depois paginas_lidas
        self.total_paginas = total_paginas
        self.paginas_lidas = paginas_lidas

    # --- getters e setters ---

    @property
    def total_paginas(self):
        return self.__total_paginas

    @total_paginas.setter
    def total_paginas(self, valor):
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 1

        if valor_temporario < 1:
            valor_temporario = 1

        self.__total_paginas = valor_temporario

        # ao reduzir total_paginas, garante que paginas_lidas continue válido
        if hasattr(self, "_TarefaLeitura__paginas_lidas"):
            if self.__paginas_lidas > self.__total_paginas:
                self.__paginas_lidas = self.__total_paginas

    @property
    def paginas_lidas(self):
        return self.__paginas_lidas

    @paginas_lidas.setter
    def paginas_lidas(self, valor):
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 0

        if valor_temporario < 0:
            valor_temporario = 0

        # clamp entre 0 e total_paginas
        if valor_temporario > self.__total_paginas:
            valor_temporario = self.__total_paginas

        self.__paginas_lidas = valor_temporario

    # --- regra de progresso ---

    def progresso(self):
        """
        Retorna o progresso da leitura entre 0.0 e 1.0.
        Ex.: 0.5 significa 50% das páginas lidas.
        """
        if self.total_paginas <= 0:
            return 0.0
        return self.paginas_lidas / self.total_paginas

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
        """
        Ao concluir, define a data de realização como a data/hora atual.
        O status é marcado como CONCLUÍDA em TarefaEstudo.concluir().
        """
        self.data_realizacao = datetime.now()
