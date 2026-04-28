import os
import requests
from google import genai
from dotenv import load_dotenv

# Garante a leitura do .env mesmo em subpastas
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# --- MOCK DA FUNÇÃO DE LOG (Governança) ---
def log_ai_interaction(pergunta: str, resposta: str):
    """Simula o registro de auditoria exigido pela governança"""
    print(f"\n[AUDITORIA IA] Pergunta: {pergunta[:30]}... | Resposta: {resposta[:30]}...")

SYSTEM_PROMPT = """
Você é o assistente da plataforma YOUVISA.
Responda sempre em português do Brasil de forma cordial.

Regras de Governança:
- Use apenas o contexto fornecido.
- Não invente status ou documentos.
- Caso o usuário forneça senhas ou CPFs, oriente-o a não compartilhar dados sensíveis no chat.
"""

def extrair_status_do_contexto(contexto: str) -> str:
    try:
        for linha in contexto.split('\n'):
            if "Status global" in linha:
                return linha.split(':')[-1].strip()
    except Exception:
        pass
    return "em processamento"

def gerar_resposta_com_fonte(pergunta: str, contexto: str) -> tuple[str, str]:
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")

        # Verificação de segurança para API Key
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no ambiente.")

        client = genai.Client(api_key=api_key)
        prompt = f"{SYSTEM_PROMPT}\n\nContexto: {contexto}\n\nPergunta: {pergunta}"

        # Ajustado para modelo estável (2.0 Flash)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        
        ai_response = response.text
        
        # Agora a função existe e não causará erro
        log_ai_interaction(pergunta, ai_response)

        return ai_response, "gemini"

    except Exception as gemini_error:
        print(f"❌ Erro na IA (Gemini): {gemini_error}")
        try:
            return gerar_resposta_llama_local(pergunta, contexto), "llama_local"
        except Exception as llama_error:
            print(f"❌ Erro na IA (Llama local): {llama_error}")
            raise gemini_error


def gerar_resposta(pergunta: str, contexto: str) -> str:
    resposta, _ = gerar_resposta_com_fonte(pergunta, contexto)
    return resposta


def gerar_resposta_llama_local(pergunta: str, contexto: str) -> str:
    """
    Tenta gerar resposta via modelo local (ex.: Ollama).
    Configuracao por variaveis de ambiente:
    - LLAMA_BASE_URL (default: http://127.0.0.1:11434)
    - LLAMA_MODEL (default: llama3.2)
    """
    base_url = os.environ.get("LLAMA_BASE_URL", "http://127.0.0.1:11434")
    model = os.environ.get("LLAMA_MODEL", "llama3.2")
    prompt = f"{SYSTEM_PROMPT}\n\nContexto: {contexto}\n\nPergunta: {pergunta}"

    response = requests.post(
        f"{base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=25
    )
    response.raise_for_status()
    data = response.json()
    ai_response = data.get("response", "").strip()
    if not ai_response:
        raise ValueError("Resposta vazia do Llama local.")

    log_ai_interaction(pergunta, ai_response)
    return ai_response
    
def formatar_status(status: str) -> str:
    mapa = {
        "AGUARDANDO_DOCUMENTOS": "Aguardando envio de documentos",
        "EM_ANALISE": "Em análise",
        "APROVADO": "Aprovado",
        "REJEITADO": "Rejeitado",
        "DOCUMENTO_REJEITADO": "Documento rejeitado",
        "FINALIZADO": "Processo finalizado"
    }

    return mapa.get(status, status.replace("_", " ").capitalize())
