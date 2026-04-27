import json
from datetime import datetime
from src.database.db import get_connection


def save_chat_interaction(
    session_id: str,
    user_question: str,
    intent: str,
    entities: list[str],
    ai_response: str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_interactions (
            session_id,
            user_question,
            intent,
            entities,
            ai_response,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        user_question,
        intent,
        json.dumps(entities, ensure_ascii=False),
        ai_response,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()