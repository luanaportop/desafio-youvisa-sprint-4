def classify_intent(question: str) -> str:
    text = question.lower()

    if "falta" in text or "faltando" in text or "pendente" in text or "pendentes" in text:
        return "documentos_faltantes"

    if "status" in text or "andamento" in text or "processo" in text:
        return "status_processo"

    if "documento" in text or "documentos" in text or "preciso enviar" in text or "necessário" in text:
        return "documentos_necessarios"

    if "corrigir" in text or "erro" in text or "recusado" in text:
        return "correcao_documento"

    if "prazo" in text or "tempo" in text or "demora" in text:
        return "prazo"

    return "duvida_geral"