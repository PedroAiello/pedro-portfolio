"""
API REST usando FastAPI para expor o agente RAG de portfólio via HTTP.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv

from main import obter_grafo_agente

load_dotenv()

# ==============================================================================
# Configuração do FastAPI
# ==============================================================================

app = FastAPI(
    title="Agente de Portfólio — Pedro Aiello",
    description="RAG sobre projetos, habilidades e experiências do Pedro. Groq Llama-3.3-70b + FAISS.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# Modelos Pydantic
# ==============================================================================

class MensagemRequest(BaseModel):
    mensagem: str
    session_id: Optional[str] = "default"


class MensagemResponse(BaseModel):
    resposta: str
    status: str = "success"
    mensagem: Optional[str] = None


# ==============================================================================
# Endpoints
# ==============================================================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Agente de portfólio do Pedro Aiello funcionando!",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)",
        },
    }


@app.get("/health")
async def health_check():
    try:
        grafo = obter_grafo_agente()
        return {"status": "healthy", "grafo_carregado": grafo is not None}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/chat", response_model=MensagemResponse)
async def chat_endpoint(request: MensagemRequest):
    if not request.mensagem or not request.mensagem.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    try:
        grafo = obter_grafo_agente()
        resultado = grafo.invoke({
            "mensagem_usuario": request.mensagem.strip(),
            "session_id": request.session_id or "default",
        })
        resposta_texto = resultado.get("resposta_final", "")
        return MensagemResponse(resposta=resposta_texto, status="success")

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar a mensagem: {str(e)}",
        )


# ==============================================================================
# Execução
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Iniciando servidor FastAPI — Agente de Portfólio")
    print("=" * 60)
    print("Docs:   http://localhost:8000/docs")
    print("Chat:   http://localhost:8000/chat")
    print("Health: http://localhost:8000/health")
    print("=" * 60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
