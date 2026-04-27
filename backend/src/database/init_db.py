from src.database.db import get_connection
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        filename TEXT,
        type TEXT,
        status TEXT,
        created_at TEXT,
        validation_reason TEXT,
        file_path TEXT
    )
    """)

    # Migração: adiciona file_path se a tabela já existia sem a coluna
    try:
        cursor.execute("ALTER TABLE documents ADD COLUMN file_path TEXT")
    except Exception:
        pass

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS status_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id TEXT,
        status_anterior TEXT,
        status_novo TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_question TEXT NOT NULL,
        intent TEXT,
        entities TEXT,
        ai_response TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()