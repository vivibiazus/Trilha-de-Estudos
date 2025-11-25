from .TarefaLeitura import TarefaLeitura
from .TarefaQuiz import TarefaQuiz
from .TarefaPratica import TarefaPratica
from .TarefaProjeto import TarefaProjeto


class TarefaFactory:
    @staticmethod
    def criar(tipo_tarefa: str, **args):
        """
        Cria e retorna uma tarefa de estudo.
        """
        # leitura:
        #   precisa: total_paginas
        #   opcionais: titulo, paginas_lidas, descricao, data_realizacao
        # quiz:
        #   precisa: nota
        #   opcionais: titulo, nota_max, descricao, data_realizacao
        # pratica:
        #   precisa: total_etapas
        #   opcionais: titulo, etapas_concluidas, descricao, data_realizacao
        # projeto:
        #   precisa: total_entregas
        #   opcionais: titulo, entregas_aprovadas, descricao, data_realizacao

        if not tipo_tarefa:
            raise ValueError("Tipo de tarefa não informado.")

        tipo_normalizado = str(tipo_tarefa).strip().lower()

        # --- LEITURA ---
        if tipo_normalizado == "leitura":
            total_paginas = args.get("total_paginas")
            if total_paginas is None:
                raise ValueError("Para 'leitura', informe 'total_paginas'.")

            titulo = args.get("titulo", "Leitura")
            paginas_lidas = args.get("paginas_lidas", 0)

            return TarefaLeitura(
                titulo=titulo,
                total_paginas=total_paginas,
                paginas_lidas=paginas_lidas,
                descricao=args.get("descricao"),
                data_realizacao=args.get("data_realizacao"),
            )

        # --- QUIZ ---
        if tipo_normalizado == "quiz":
            nota = args.get("nota")
            if nota is None:
                raise ValueError("Para 'quiz', informe 'nota'.")

            titulo = args.get("titulo", "Quiz")
            nota_max = args.get("nota_max", 10)

            return TarefaQuiz(
                titulo=titulo,
                nota=nota,
                nota_max=nota_max,
                descricao=args.get("descricao"),
                data_realizacao=args.get("data_realizacao"),
            )

        # --- PRÁTICA ---
        if tipo_normalizado == "pratica":
            total_etapas = args.get("total_etapas")
            if total_etapas is None:
                raise ValueError("Para 'pratica', informe 'total_etapas'.")

            titulo = args.get("titulo", "Prática")
            etapas_concluidas = args.get("etapas_concluidas", 0)

            return TarefaPratica(
                titulo=titulo,
                total_etapas=total_etapas,
                etapas_concluidas=etapas_concluidas,
                descricao=args.get("descricao"),
                data_realizacao=args.get("data_realizacao"),
            )

        # --- PROJETO ---
        if tipo_normalizado == "projeto":
            total_entregas = args.get("total_entregas")
            if total_entregas is None:
                raise ValueError("Para 'projeto', informe 'total_entregas'.")

            titulo = args.get("titulo", "Projeto")
            entregas_aprovadas = args.get("entregas_aprovadas", 0)

            return TarefaProjeto(
                titulo=titulo,
                total_entregas=total_entregas,
                entregas_aprovadas=entregas_aprovadas,
                descricao=args.get("descricao"),
                data_realizacao=args.get("data_realizacao"),
            )

        # --- tipo inválido ---
        raise ValueError(
            "Tipo de tarefa inválido. Use: 'leitura', 'quiz', 'pratica' ou 'projeto'."
        )

