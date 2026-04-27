def extract_entities(question: str) -> list[str]:
    text = question.lower()
    entities = []

    if "passaporte" in text:
        entities.append("passaporte")

    if "residência" in text or "residencia" in text or "endereço" in text or "endereco" in text:
        entities.append("comprovante_residencia")

    if "financeiro" in text or "renda" in text or "banco" in text:
        entities.append("comprovante_financeiro")

    if "formulário" in text or "formulario" in text:
        entities.append("formulario")

    return entities