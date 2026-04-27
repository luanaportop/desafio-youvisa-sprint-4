from src.nlp.gemini_service import gerar_resposta


def generate_response(question: str, context: str, intent: str, entities: list[str]) -> str:
    prompt_context = f"""
    Você é o assistente virtual da plataforma YOUVISA.

    Responda apenas dúvidas relacionadas a:
    - status do processo
    - documentos necessários
    - documentos faltantes
    - correção de documentos
    - prazos e andamento da solicitação

    Intenção identificada: {intent}
    Entidades identificadas: {entities}

    Contexto atual:
    {context}
    """

    try:
        return gerar_resposta(question, prompt_context)

    except Exception as e:
        print(f"❌ Erro na IA: {e}")

        return gerar_resposta_fallback(intent, context, entities)


def gerar_resposta_fallback(intent: str, context: str, entities: list[str]) -> str:
    if intent == "status_processo":
        return f"Consultei o sistema da YOUVISA e o status atual do seu processo é: {context}"

    if intent == "documentos_faltantes":
        return f"Consultei o sistema da YOUVISA e identifiquei os seguintes documentos pendentes: {context}"

    if intent == "documentos_necessarios":
        return "Para continuar o processo, envie os documentos solicitados pela plataforma, como passaporte, comprovantes e formulários exigidos."

    if intent == "correcao_documento":
        return "Para corrigir um documento recusado, envie uma nova versão com boa iluminação, sem cortes e com todas as informações legíveis."

    if intent == "prazo":
        return "O prazo pode variar conforme a análise dos documentos. Acompanhe o status atualizado diretamente pela plataforma."

    return "Posso ajudar com status do processo, documentos necessários, documentos faltantes, correção de documentos e prazos."