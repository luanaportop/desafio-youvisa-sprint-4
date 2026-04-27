import { useEffect, useState } from "react";

type ChatItem = {
  id: number;
  session_id: string;
  user_question: string;
  intent: string;
  entities: string;
  ai_response: string;
  created_at: string;
};

export default function ChatHistory() {
  const [historico, setHistorico] = useState<ChatItem[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/chat/history")
      .then((res) => res.json())
      .then((data: ChatItem[]) => setHistorico(data))
      .catch((err) => console.error("Erro ao buscar histórico:", err));
  }, []);

  return (
    <div className="chat-history">
      {historico.length === 0 ? (
        <p>Nenhuma interação registrada ainda.</p>
      ) : (
        historico.map((item) => (
          <div key={item.id} className="history-card">
            <p><strong>Pergunta:</strong> {item.user_question}</p>
            <p><strong>Resposta:</strong> {item.ai_response}</p>
            <p><strong>Intenção:</strong> {item.intent}</p>
            <p><strong>Entidades:</strong> {item.entities}</p>
            <p><strong>Data:</strong> {new Date(item.created_at).toLocaleString("pt-BR")}</p>
          </div>
        ))
      )}
    </div>
  );
}