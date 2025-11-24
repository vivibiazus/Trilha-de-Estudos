from .TarefaLeitura import TarefaLeitura
from .TarefaQuiz import TarefaQuiz
from .TarefaPratica import TarefaPratica
from .TarefaProjeto import TarefaProjeto

class TarefaFactory:
    @staticmethod
    def criar(tipo, **dados):
        """
        Cria uma tarefa de estudo de acordo com o 'tipo'.
        Aceita:
          - string: "leitura", "quiz", "pratica", "projeto"

        Parâmetros esperados por tipo:
          leitura -> titulo, total_paginas, (paginas_lidas=0), descricao, data_realizacao
          quiz    -> titulo, nota, (nota_max=10), descricao, data_realizacao
          pratica -> titulo, total_etapas, (etapas_concluidas=0), descricao, data_realizacao
          projeto -> titulo, total_entregas, (entregas_aprovadas=0), descricao, data_realizacao
        """
        if not tipo:
            raise ValueError("Tipo de tarefa não informado.")

        chave = str(tipo).strip().lower()

        # --- LEITURA ---
        if chave == "leitura":
            total_paginas = dados.get("total_paginas")
            if total_paginas is None:
                raise ValueError("Para 'leitura', informe 'total_paginas'.")
            titulo = dados.get("titulo") or "Leitura"
            paginas_lidas = dados.get("paginas_lidas", 0)
            return TarefaLeitura(
                titulo=titulo,
                total_paginas=total_paginas,
                paginas_lidas=paginas_lidas,
                descricao=dados.get("descricao"),
                data_realizacao=dados.get("data_realizacao"),
            )

        # --- QUIZ ---
        if chave == "quiz":
            nota = dados.get("nota")
            if nota is None:
                raise ValueError("Para 'quiz', informe 'nota'.")
            titulo = dados.get("titulo") or "Quiz"
            nota_max = dados.get("nota_max", 10)
            return TarefaQuiz(
                titulo=titulo,
                nota=nota,
                nota_max=nota_max,
                descricao=dados.get("descricao"),
                data_realizacao=dados.get("data_realizacao"),
            )

        # --- PRÁTICA ---
        if chave == "pratica":
            total_etapas = dados.get("total_etapas")
            if total_etapas is None:
                raise ValueError("Para 'pratica', informe 'total_etapas'.")
            titulo = dados.get("titulo") or "Prática"
            etapas_concluidas = dados.get("etapas_concluidas", 0)
            return TarefaPratica(
                titulo=titulo,
                total_etapas=total_etapas,
                etapas_concluidas=etapas_concluidas,
                descricao=dados.get("descricao"),
                data_realizacao=dados.get("data_realizacao"),
            )

        # --- PROJETO ---
        if chave == "projeto":
            total_entregas = dados.get("total_entregas")
            if total_entregas is None:
                raise ValueError("Para 'projeto', informe 'total_entregas'.")
            titulo = dados.get("titulo") or "Projeto"
            entregas_aprovadas = dados.get("entregas_aprovadas", 0)
            return TarefaProjeto(
                titulo=titulo,
                total_entregas=total_entregas,
                entregas_aprovadas=entregas_aprovadas,
                descricao=dados.get("descricao"),
                data_realizacao=dados.get("data_realizacao"),
            )

        # --- tipo inválido ---
        raise ValueError("Tipo de tarefa inválido. Use: leitura, quiz, pratica ou projeto.")
