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
        """
        Tarefa de leitura (livro, artigo, capítulo, etc.).
        Aqui controlamos quantas páginas existem e quantas já foram lidas.
        """
        # Inicializa primeiro a parte "genérica" da tarefa de estudo.
        super().__init__(
            titulo=titulo,
            descricao=descricao,
            data_realizacao=data_realizacao,
            status=status
        )

        # A ordem importa: primeiro o total de páginas, depois o quanto já foi lido.
        self.total_paginas = total_paginas
        self.paginas_lidas = paginas_lidas

    # --- dados específicos de leitura ---

    @property
    def total_paginas(self):
        """Quantidade total de páginas da leitura."""
        return self.__total_paginas

    @total_paginas.setter
    def total_paginas(self, valor):
        """
        Define o total de páginas.

        - Tenta converter para inteiro.
        - Se der erro ou vier um valor menor que 1, usa 1 como padrão.
        - Se páginas_lidas já existir, garante que ela não fique maior que o novo total.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 1

        if valor_temporario < 1:
            valor_temporario = 1

        self.__total_paginas = valor_temporario

        # Se paginas_lidas já foi definido antes, ajusta caso tenha passado do novo limite.
        try:
            if self.__paginas_lidas > self.__total_paginas:
                self.__paginas_lidas = self.__total_paginas
        except AttributeError:
            # Ainda não temos paginas_lidas definido, então não há nada para ajustar aqui.
            pass

    @property
    def paginas_lidas(self):
        """Quantidade de páginas já lidas até agora."""
        return self.__paginas_lidas

    @paginas_lidas.setter
    def paginas_lidas(self, valor):
        """
        Define quantas páginas já foram lidas.

        - Tenta converter para inteiro.
        - Se der erro, começa em 0.
        - Nunca deixa ficar menor que 0.
        - Também não deixa passar do total de páginas.
        """
        try:
            valor_temporario = int(valor)
        except (TypeError, ValueError):
            valor_temporario = 0

        if valor_temporario < 0:
            valor_temporario = 0

        # Garante que não ultrapasse o total de páginas.
        if valor_temporario > self.__total_paginas:
            valor_temporario = self.__total_paginas

        self.__paginas_lidas = valor_temporario

    # --- regra de progresso ---

    def progresso(self):
        """
        Calcula o progresso da leitura.

        Exemplo:
            total_paginas = 100 e paginas_lidas = 25  →  progresso = 0.25 (25%)
        """
        return self.paginas_lidas / self.total_paginas

    # --- apresentação ---

    def __str__(self):
        """Mostra que é uma tarefa de leitura + representação da tarefa base."""
        return f"[Leitura] {super().__str__()}"

    def exibir_dados(self):
        """
        Monta um texto com os dados da tarefa de leitura,
        incluindo as informações comuns e o resumo de páginas.
        """
        base = super().exibir_dados()
        linhas = [
            base,
            "Tipo: Leitura",
            f"Páginas lidas: {self.paginas_lidas} de {self.total_paginas}",
        ]
        return "\n".join(linhas)

    # --- o que fazer quando a leitura é concluída ---

    def definir_termino(self):
        """
        Quando a leitura é concluída, registra a data/hora de término.

        Obs.: quem muda o status para CONCLUIDA é o método concluir()
        da classe TarefaEstudo.
        """
        self.data_realizacao = datetime.now()

