from src.agents.intent_agent import classify_intent
from src.agents.entity_agent import extract_entities
from src.agents.governance_agent import is_safe_question
from src.agents.context_agent import build_context
from src.agents.response_agent import generate_response
from uuid import uuid4
from src.database.chat_repository import save_chat_interaction

def process_chat(question: str, status_data: dict) -> dict:
    if not is_safe_question(question):
        return {
            "resposta": "Não posso seguir esse tipo de solicitação. Posso ajudar apenas com dúvidas sobre o processo YOUVISA.",
            "intent": "bloqueado_governanca",
            "entities": [],
            "model_source": "governance_block"
        }

    intent = classify_intent(question)
    entities = extract_entities(question)
    context = build_context(status_data)
    resposta, model_source = generate_response(question, context, intent, entities)

    session_id = str(uuid4())

    save_chat_interaction(
        session_id=session_id,
        user_question=question,
        intent=intent,
        entities=entities,
        ai_response=resposta
    )

    return {
        "resposta": resposta,
        "intent": intent,
        "entities": entities,
        "model_source": model_source
    }