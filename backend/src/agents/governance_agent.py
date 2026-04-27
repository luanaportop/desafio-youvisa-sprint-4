def is_safe_question(question: str) -> bool:
    text = question.lower()

    blocked_terms = [
        "ignore as instruções",
        "ignore as instrucoes",
        "revele o prompt",
        "mostre suas regras",
        "finja que",
        "desconsidere o contexto"
    ]

    return not any(term in text for term in blocked_terms)