# ==============================================================================
# Agente de Portfólio — Pedro Aiello
# Stack: Groq Llama-3.3-70b | LangGraph | contexto completo (sem FAISS)
# ==============================================================================

import os
from pathlib import Path
from typing import TypedDict, Any, List

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

load_dotenv()

SCRIPT_DIR = Path(__file__).parent.resolve()
RAG_DIR = SCRIPT_DIR / "rag"

GROQ_KEY1 = os.getenv("GROQ_API_KEY", "")
GROQ_KEY2 = os.getenv("GROQ_API_KEY2", "")
MODEL_NAME = "llama-3.3-70b-versatile"

MAX_TURNS = 5


# ==============================================================================
# LLM — rotação de 2 chaves Groq
# ==============================================================================

def invocar_com_rotacao(mensagens: list) -> str:
    for key in [GROQ_KEY1, GROQ_KEY2]:
        if not key:
            continue
        try:
            llm = ChatGroq(model=MODEL_NAME, temperature=0, api_key=key)
            return llm.invoke(mensagens).content
        except Exception as e:
            err = str(e).lower()
            if "rate" in err or "429" in err or "limit" in err:
                continue
            raise
    raise RuntimeError("Ambas as chaves Groq estão em rate limit ou inválidas.")


# ==============================================================================
# Contexto do portfólio — lê todos os .md da pasta rag/ em memória
# ==============================================================================

def carregar_contexto_portfolio() -> str:
    partes = []
    if RAG_DIR.exists():
        for md_file in sorted(RAG_DIR.glob("*.md")):
            partes.append(md_file.read_text(encoding="utf-8"))
    if not partes:
        raise RuntimeError(f"Nenhum .md encontrado em {RAG_DIR}. Adicione seu arquivo de contexto.")
    return "\n\n---\n\n".join(partes)


_contexto_portfolio: str | None = None


def obter_contexto() -> str:
    global _contexto_portfolio
    if _contexto_portfolio is None:
        _contexto_portfolio = carregar_contexto_portfolio()
        print(f"Contexto carregado: {len(_contexto_portfolio)} chars.")
    return _contexto_portfolio


# ==============================================================================
# Memória por session_id (in-memory)
# ==============================================================================

_memorias: dict[str, list[dict]] = {}


def obter_historico(session_id: str) -> list[dict]:
    return list(_memorias.get(session_id, []))


def salvar_turno(session_id: str, pergunta: str, resposta: str) -> None:
    if session_id not in _memorias:
        _memorias[session_id] = []
    _memorias[session_id].append({"pergunta": pergunta, "resposta": resposta})
    _memorias[session_id] = _memorias[session_id][-MAX_TURNS:]


def formatar_historico(historico: list[dict]) -> str:
    return "\n".join(
        f"Usuário: {t['pergunta']}\nAssistente: {t['resposta']}"
        for t in historico
    )


# ==============================================================================
# Prompt
# ==============================================================================

SYSTEM_PROMPT_TEMPLATE = (
    "Você é o assistente de portfólio do Pedro Aiello.\n\n"
    "REGRAS ABSOLUTAS:\n"
    "1. Responda usando SOMENTE as informações abaixo. Cite dados reais: projetos, "
    "tecnologias, certificados, experiências — exatamente como aparecem no documento.\n"
    "2. NUNCA faça inferências ou invente dados. Se a informação não estiver abaixo, "
    "diga: 'Essa informação não está nos meus arquivos.'\n"
    "3. Seja direto e assertivo. Proibido usar 'parece', 'sugere que', 'provavelmente'.\n"
    "4. Quando a base de conhecimento tiver detalhes (sub-itens, rotas, destaques técnicos), "
    "INCLUA TODOS esses detalhes na resposta — não resuma nem omita sub-componentes.\n"
    "5. Para perguntas fora do portfólio (receitas, política, etc.), redirecione brevemente.\n"
    "6. Responda em português, de forma clara. Use listas quando houver múltiplos itens.\n"
    "7. Para saudações, seja amigável e ofereça exemplos do que pode responder.\n\n"
    "== BASE DE CONHECIMENTO DO PEDRO ==\n\n"
    "{contexto}"
)


# ==============================================================================
# AgentState
# ==============================================================================

class AgentState(TypedDict, total=False):
    mensagem_usuario: str
    session_id: str
    historico: List[dict]
    resposta_final: str


# ==============================================================================
# Nós do grafo
# ==============================================================================

def node_carregar_historico(state: AgentState) -> dict:
    session_id = state.get("session_id", "default")
    return {"historico": obter_historico(session_id)}


def node_responder(state: AgentState) -> dict:
    contexto = obter_contexto()
    system_content = SYSTEM_PROMPT_TEMPLATE.format(contexto=contexto)

    historico = state.get("historico", [])
    if historico:
        system_content += f"\n\n== HISTÓRICO DA CONVERSA ==\n{formatar_historico(historico)}"

    resposta = invocar_com_rotacao([
        SystemMessage(content=system_content),
        HumanMessage(content=state["mensagem_usuario"]),
    ])
    return {"resposta_final": resposta}


def node_salvar_historico(state: AgentState) -> dict:
    session_id = state.get("session_id", "default")
    resposta = state.get("resposta_final", "")
    if resposta:
        salvar_turno(session_id, state["mensagem_usuario"], resposta)
    return {}


# ==============================================================================
# Construção e singleton do grafo
# ==============================================================================

_grafo_agente: Any = None


def criar_grafo_agente():
    workflow = StateGraph(AgentState)

    workflow.add_node("carregar_historico", node_carregar_historico)
    workflow.add_node("responder", node_responder)
    workflow.add_node("salvar_historico", node_salvar_historico)

    workflow.set_entry_point("carregar_historico")
    workflow.add_edge("carregar_historico", "responder")
    workflow.add_edge("responder", "salvar_historico")
    workflow.add_edge("salvar_historico", END)

    return workflow.compile()


def obter_grafo_agente():
    global _grafo_agente
    if _grafo_agente is None:
        print("Compilando grafo do agente de portfólio...")
        _grafo_agente = criar_grafo_agente()
        print("Grafo compilado.")
    return _grafo_agente


# ==============================================================================
# Execução direta (teste manual)
# ==============================================================================

if __name__ == "__main__":
    print("Carregando contexto do portfólio...")
    obter_contexto()
    grafo = obter_grafo_agente()

    session = "cli_test"
    print("\nAgente de portfólio do Pedro pronto. Digite 'sair' para encerrar.\n")
    while True:
        try:
            pergunta = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not pergunta or pergunta.lower() == "sair":
            break
        resultado = grafo.invoke({"mensagem_usuario": pergunta, "session_id": session})
        print(f"\nAssistente: {resultado['resposta_final']}\n")
