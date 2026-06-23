# 🤖 Agente de Portfólio — Pedro Aiello

Assistente de IA conversacional embutido no meu portfólio pessoal. Responde perguntas sobre meus projetos, habilidades, experiências e certificados com base em uma base de conhecimento própria — sem inventar dados.

🔗 **Live:** [pedro-portfolio no Render](https://pedro-portfolio-9bpd.onrender.com)

---

## ✨ Como Funciona

O visitante do site pode conversar com um assistente que conhece o meu portfólio por inteiro. O agente responde apenas com informações reais do meu perfil, sem alucinações — se não souber, diz que não sabe.

Exemplos de perguntas que ele responde:
- *"Quais projetos você já fez?"*
- *"Você tem experiência com LangGraph?"*
- *"Quais são suas certificações?"*

---

## 🏗️ Arquitetura

```
Visitante → index.html (chat)
                 │
                 ▼
         FastAPI /chat (POST)
                 │
                 ▼
      LangGraph StateGraph
       │
       ├── carregar_historico   ← busca memória da sessão (últimas 5 trocas)
       ├── responder            ← Groq Llama-3.3-70b gera resposta com contexto
       └── salvar_historico     ← persiste turno na memória in-memory
                 │
                 ▼
        Resposta para o frontend
```

O contexto do portfólio é carregado de arquivos `.md` na pasta `rag/` — basta editar esses arquivos para atualizar o que o agente sabe sobre mim.

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| **Agente / Orquestração** | [LangGraph](https://langchain-ai.github.io/langgraph/) (`StateGraph`) |
| **LLM** | [Groq](https://groq.com/) — `llama-3.3-70b-versatile` com rotação de 2 chaves |
| **Servidor** | [FastAPI](https://fastapi.tiangolo.com/) (async) |
| **Frontend** | HTML/CSS/JS puro (chat embutido no portfólio) |
| **Deploy** | [Render](https://render.com/) |
| **Gerenciador de pacotes** | [uv](https://github.com/astral-sh/uv) |

---

## 🧠 Detalhes Técnicos

**Memória de curto prazo:** O agente mantém até 5 turnos de histórico por `session_id` em memória. Cada aba/visitante tem sua própria sessão isolada.

**Base de conhecimento:** Arquivos `.md` dentro de `rag/` são concatenados e injetados no system prompt. Sem banco de dados, sem vetores — contexto direto no prompt.

**Rotação de chaves Groq:** Se a chave principal atingir rate limit (429), o sistema tenta automaticamente a segunda chave sem interromper a conversa.

**Grafo linear:** O fluxo é simples e determinístico — sem roteamento condicional, sem loops. Entrada → resposta → saída.

---

## 🚀 Rodando Localmente

### Pré-requisitos

- Python 3.11+
- `uv` instalado (`pip install uv`)
- Uma chave de API do [Groq](https://console.groq.com/)

### Instalação

```bash
git clone https://github.com/PedroAiello/pedro-portfolio.git
cd pedro-portfolio

# Cria ambiente virtual e instala dependências
uv sync

# Configura variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves Groq
```

### Personalizando o Conteúdo

Edite ou crie arquivos `.md` dentro da pasta `rag/`:

```
rag/
└── sobre_mim.md    ← coloque aqui seus projetos, habilidades, experiências
```

O agente carrega todos os `.md` automaticamente ao iniciar.

### Rodando

```bash
uv run uvicorn server:app --reload --port 8000
```

Acesse `http://localhost:8000/docs` para ver a documentação da API.

---

## 📁 Estrutura do Projeto

```
├── main.py           # Agente LangGraph — lógica, memória, rotação de chaves
├── server.py         # Servidor FastAPI — endpoints /chat e /health
├── index.html        # Frontend do portfólio com chat integrado
├── rag/
│   └── sobre_mim.md  # Base de conhecimento (NÃO commitar dados sensíveis)
├── .env.example      # Variáveis de ambiente necessárias
└── pyproject.toml    # Dependências (uv)
```

---

## 🔑 Variáveis de Ambiente

```env
GROQ_API_KEY=sua_chave_principal
GROQ_API_KEY2=sua_chave_secundaria_opcional
```

---

## 📄 Licença

MIT
