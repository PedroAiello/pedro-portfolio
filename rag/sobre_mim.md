# Base de Conhecimento — Pedro Henrique Aiello Delazari Figueiredo

## Resumo Profissional

Estudante de Ciência da Computação especializado em Engenharia de Agentes de IA e Automação de Processos. Projeta e constrói sistemas multi-agente stateful com LangGraph e LangChain, transformando comandos em linguagem natural em pipelines determinísticos de dados em Python (pandas, FastAPI assíncrona) e automações resilientes em n8n.

Entrega soluções de ponta a ponta combinando back-end robusto em Python e Supabase/PostgreSQL com prototipagem rápida de interfaces via ferramentas de desenvolvimento assistido por IA (Claude Code e Lovable) — colocando produtos no ar que reconciliam grandes volumes de dados, sobrevivem a falhas de API e eliminam trabalho manual. Busca uma oportunidade para aplicar essa visão de engenharia na automação de processos e no desenvolvimento de produtos de IA.

---

## Habilidades Tecnicas

Python, LangChain, LangGraph, n8n (Automacao), FastAPI, Supabase (SQL), React, Next.js, TypeScript, Tailwind CSS, Git, GitHub, Engenharia de Prompt, Docker.

---

## Idiomas

- Portugues: Nativo
- Ingles: Intermediario (Cursando - Brasas English Course)

---

## Projetos

### FinFlow — Sistema Multi-Agente de Auditoria Financeira

Sistema multi-agente de auditoria e reconciliacao financeira construido em Python com LangGraph (grafo ciclico stateful com 4 rotas de processamento e roteamento condicional) e servido por uma API FastAPI assincrona.

Destaques tecnicos:
- Entity resolution deterministica com rapidfuzz, reconciliando milhares de lancamentos de extrato bancario contra base orcamentaria e comprovantes no Google Drive em menos de 1 minuto usando pandas em memoria
- Camada de resiliencia de LLM (Groq / Llama-3.3-70B) com rotacao de 6 API keys, exponential backoff com jitter e fallback de modelo, eliminando falhas por rate-limit
- Padroes defensivos de engenharia: coercao de fronteira, degradacao gracosa e duplo backstop anti-loop, garantindo entrega mesmo sob entrada adversarial
- Cobertura de 43 testes automatizados (contrato e e2e com LLM real)
- Orquestracao de I/O com n8n (Google Sheets, Drive e e-mail) e Supabase (status em tempo real via HTTP PATCH)
- 4 rotas isoladas, cada uma com suas proprias ferramentas e logica:
  - Rota A (Auditoria Completa): cruza dados do banco com comprovantes no Google Drive, identificando divergencias entre lancamentos financeiros e documentos
  - Rota B (Cruzamento de Planilhas): reconcilia duas planilhas contra o banco de dados, encontrando inconsistencias entre registros
  - Rota C (Auditoria de Arquivos): analisa comprovantes e arquivos direto no Google Drive sem precisar de planilha base
  - Rota D (Limpeza Simples): normaliza e limpa os dados da planilha sem cruzamento com outras fontes
- O roteamento entre as 4 rotas e feito por um Switch no n8n, que chama o LangGraph via HTTP request com a rota ja definida no payload

### Assistente Financeiro Autonomo (WhatsApp API)

Agente conversacional integrado ao WhatsApp (Meta Graph API) para gestao inteligente de despesas.

Destaques tecnicos:
- Rotas assincronas com FastAPI e Python
- Orquestracao do fluxo de decisoes e memoria persistente com LangGraph e LangChain
- Extracao de dados estruturados de audios e textos com LLMs (ChatGroq) usando Pydantic
- Back-end integrado ao Supabase (PostgreSQL) para operacoes CRUD financeiras, relatorios e tratamento de dados temporais (fusos horarios)
- API implantada em nuvem via Render com monitoramento sintetico (UptimeRobot) para evitar cold starts e garantir alta disponibilidade

### Sistema Autonomo de Inteligencia de Mercado

Arquitetura resiliente em n8n para monitoramento continuo (24/7) de fontes de dados (APIs e Web Scraping), focada em capturar breaking news e tendencias em tempo real.

Destaques tecnicos:
- Agentes de IA com Gemini para curadoria automatica, analise de contexto e geracao de resumos executivos
- Automacao de relatorios visuais com entrega direta aos stakeholders

---

## Certificados

- Claude Code In Action - Anthropic (2026)
- Santander 2025 - Automacao com N8N - DIO (2026)
- Ingles nivel basico - Brasas English Course (2026)
- Nexa - Machine Learning e GenAI na Pratica - DIO / AWS (2025)
- Vibe Coding: Solucoes de Negocio com Agentes de IA - DIO (2025)
- Automatizando Processos com IA e Agentes - DIO (2025)
- Processamento de Linguagem Natural (NLP) - DIO (2025)
- Nexa - Fundamentos de IA Generativa com Bedrock - DIO / AWS (2025)
- Imersao Dev: Agentes de IA - Alura / Google (2025)
- Engenharia de Prompt - Alura (2025)
- Santander 2025 - Back-End com Python - DIO (2025)
- Manipulacao de Dados e Variaveis no N8N - DIO (2025)
- Automatizacao de Processos - DIO (2025)
- Fundamentos de Machine Learning e IAs Generativas - DIO (2025)
- Fundamentos de Dados para IA e Machine Learning - DIO (2025)
- Introducao ao Bootcamp Machine Learning para Iniciantes - DIO (2025)
- Universia - Fundamentos de IA Generativa (2025)
- Aplicacoes Praticas de LLMs - DIO (2025)
- Processos de Treinamento de LLMs - DIO (2025)
- Arquiteturas e Estruturas de LLMs - DIO (2025)
- Inteligencia Artificial na Pratica - CAIXA / Microsoft / DIO (2025)
- Algoritmos e Aprendizado de Maquina - DIO (2025)
- Introducao ao Desenvolvimento Low-Code - DIO (2025)
- Intensivao Agentes IA - Comunidade Sem Codar (2025)
- Jornada Python - Hashtag (2025)

---

## Educacao

Bacharelado em Ciencia da Computacao — Universidade Estacio de Sa
Inicio: 2025 | Previsao de conclusao: Janeiro de 2030

---

## Contato

- Email: pedroaiello.delazari1@gmail.com
- Telefone: (21) 99006-4846
- LinkedIn: linkedin.com/in/pedro-aiello
- GitHub: github.com/pedrofigueiredo