"""
API REST usando FastAPI para expor o agente RAG de portfólio via HTTP.
"""

import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import FastAPI, HTTPException, Request
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
    description="RAG sobre projetos, habilidades e experiências do Pedro. Groq GPT-OSS-120B + LangGraph.",
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
# Protecao contra spam e abuso
# ==============================================================================

LIMITE_POR_MINUTO = 5
LIMITE_POR_HORA = 30
LIMITE_GLOBAL_POR_HORA = 300
TAMANHO_MAX_MENSAGEM = 500

_historico_ip = defaultdict(deque)
_historico_global = deque()
_trava = Lock()


def _obter_ip(req: Request) -> str:
    encaminhado = req.headers.get("x-forwarded-for", "")
    if encaminhado:
        return encaminhado.split(",")[0].strip()
    return req.client.host if req.client else "desconhecido"


def _descartar_antigos(fila: deque, janela: float, agora: float) -> None:
    while fila and agora - fila[0] > janela:
        fila.popleft()


def verificar_limite(req: Request) -> None:
    agora = time.time()
    ip = _obter_ip(req)

    with _trava:
        _descartar_antigos(_historico_global, 3600, agora)
        if len(_historico_global) >= LIMITE_GLOBAL_POR_HORA:
            raise HTTPException(
                status_code=429,
                detail="O assistente atingiu o limite de uso desta hora. Tente novamente mais tarde.",
            )

        fila = _historico_ip[ip]
        _descartar_antigos(fila, 3600, agora)

        if sum(1 for t in fila if agora - t <= 60) >= LIMITE_POR_MINUTO:
            raise HTTPException(
                status_code=429,
                detail="Muitas mensagens seguidas. Aguarde um pouco antes de perguntar de novo.",
            )

        if len(fila) >= LIMITE_POR_HORA:
            raise HTTPException(
                status_code=429,
                detail="Voce atingiu o limite de mensagens por hora. Tente novamente mais tarde.",
            )

        fila.append(agora)
        _historico_global.append(agora)

        if len(_historico_ip) > 5000:
            for chave in [k for k, v in _historico_ip.items() if not v]:
                del _historico_ip[chave]


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


@app.head("/health")
async def health_head():
    return {}


@app.get("/health")
async def health_check():
    try:
        grafo = obter_grafo_agente()
        return {"status": "healthy", "grafo_carregado": grafo is not None}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/chat", response_model=MensagemResponse)
async def chat_endpoint(request: MensagemRequest, req: Request):
    verificar_limite(req)

    if len(request.mensagem or "") > TAMANHO_MAX_MENSAGEM:
        raise HTTPException(
            status_code=413,
            detail=f"Mensagem muito longa (maximo {TAMANHO_MAX_MENSAGEM} caracteres).",
        )

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
