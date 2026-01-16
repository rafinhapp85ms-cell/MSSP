import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# ==============================
# Configuração inicial da página
# ==============================
st.set_page_config(
    page_title="MSSP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Diretórios e arquivos de histórico
# ==============================
HISTORICO_ARQUIVO = "historico.json"
IMAGENS_DIR = Path("/tmp/mssp_imagens")
IMAGENS_DIR.mkdir(exist_ok=True)

# ==============================
# Função para carregar histórico
# ==============================
def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        try:
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

# ==============================
# Função para salvar histórico
# ==============================
def salvar_historico(historico):
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# ==============================
# 🧠 IA SIMULADA APRIMORADA — MSSP
# ==============================
def ia_mssp_responder(mensagem_usuario="", tem_imagem=False, historico_recente=None):
    """
    Responde como a MSSP — sem API, sem token, 100% local.
    Simula inteligência com base em palavras-chave e contexto.
    """
    msg_lower = mensagem_usuario.strip().lower()

    # Contexto: verificar se há imagem recente
    contexto_tem_imagem = tem_imagem or (
        historico_recente and any(
            item.get("tipo") == "usuario_imagem" for item in historico_recente[-3:]
        )
    )

    if not msg_lower:
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires), sua assistente pessoal para criação de apps.\n\n"
            "Posso te ajudar com:\n"
            "- Criar apps simples e editáveis\n"
            "- Receber e armazenar imagens\n"
            "- Manter todo o histórico da nossa conversa\n"
            "- Guiar passo a passo cada implementação\n\n"
            "Digite algo ou envie uma imagem para começarmos!"
        )

    # Saudações
    if any(palavra in msg_lower for palavra in ["oi", "olá", "ola", "eai", "salve"]):
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires)!\n\n"
            "Fico feliz em te ver! Como posso te ajudar hoje?\n\n"
            "Você pode:\n"
            "- Pedir ajuda para criar um app\n"
            "- Enviar uma imagem para análise futura\n"
            "- Perguntar sobre o histórico salvo\n\n"
            "Estou aqui para construir junto com você! 💙"
        )

    # Ajuda para criar apps
    if any(palavra in msg_lower for palavra in ["ajudar", "criar", "app", "aplicativo", "fazer", "construir"]):
        return (
            "🛠️ Claro! Vamos criar um app juntos.\n\n"
            "Para começar, me diga:\n"
            "1. Qual é o objetivo do app? (ex: lista de tarefas, cadastro de produtos)\n"
            "2. Quais funcionalidades ele precisa ter? (ex: formulário, gráficos, upload de imagens)\n"
            "3. Você já tem algum código ou ideia?\n\n"
            "Com essas informações, posso te guiar passo a passo com código editável no GitHub."
        )

    # Perguntas sobre histórico
    if any(palavra in msg_lower for palavra in ["histórico", "conversa", "salvo", "mensagem", "anterior"]):
        return (
            "📁 Seu histórico está sendo salvo automaticamente!\n\n"
            "- Mensagens e imagens ficam em `st.session_state`\n"
            "- Tudo é persistido em `historico.json`\n"
            "- Imagens são armazenadas em `/tmp/mssp_imagens/`\n\n"
            "Isso garante que, mesmo após atualizar a página, você não perde nada (durante a sessão ativa).\n\n"
            "Quer que eu mostre algo específico do histórico?"
        )

    # Perguntas sobre a própria IA
    if any(palavra in msg_lower for palavra in ["quem é você", "o que você faz", "qual sua função", "sua identidade"]):
        return (
            "🧠 Sou a **MSSP** (Marie Sophie Souza Pires) — sua assistente pessoal para criação de apps.\n\n"
            "Minha função é:\n"
            "- Ajudar você a criar aplicativos simples, seguros e totalmente editáveis\n"
            "- Manter todo o histórico da nossa conversa\n"
            "- Preparar a estrutura para integrar IA avançada (visão, áudio, APIs) quando você quiser\n\n"
            "No momento, minhas respostas são simuladas, mas minha estrutura já está pronta para evoluir.\n\n"
            "Como posso te ajudar agora? 😊"
        )

    # Perguntas sobre imagens
    if contexto_tem_imagem:
        return (
            "🖼️ Recebi sua imagem! \n\n"
            "Por enquanto, estou apenas armazenando-a no histórico. "
            "No futuro, poderei analisá-la e descrever seu conteúdo, identificar objetos ou responder perguntas sobre ela.\n\n"
            "Como posso te ajudar agora?"
        )

    # Resposta genérica — mas com contexto
    if "tarefa" in msg_lower or "lista" in msg_lower:
        return (
            "📝 Você quer criar um app de tarefas? Vamos lá!\n\n"
            "Passo 1: Crie um campo de texto para digitar a tarefa.\n"
            "Passo 2: Adicione um botão 'Adicionar'.\n"
            "Passo 3: Mostre a lista de tarefas abaixo.\n\n"
            "Quer que eu te mostre o código completo para isso?"
        )

    if "gráfico" in msg_lower or "gráfico" in msg_lower:
        return (
            "📊 Quer adicionar um gráfico? Ótima escolha!\n\n"
            "Você pode usar `st.line_chart()`, `st.bar_chart()` ou `plotly`.\n\n"
            "Exemplo básico:\n"
            "```python\n"
            "import streamlit as st\n"
            "dados = [1, 2, 3, 4, 5]\n"
            "st.line_chart(dados)\n"
            "```\n\n"
            "Quer que eu adapte isso ao seu app?"
        )

    # Resposta final — sempre útil
    return (
        "Entendi! Sou a **MSSP** (Marie Sophie Souza Pires) 👋\n\n"
        "Minha função é te ajudar a criar e gerenciar aplicativos de forma simples, segura e totalmente editável.\n\n"
        "No momento, minhas respostas são simuladas, mas minha estrutura já está pronta para integrar IA avançada (visão, áudio, APIs) quando você quiser.\n\n"
        "Como posso te ajudar agora? 😊"
    )

# ==============================
# Inicializar histórico na sessão
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

# ==============================
# Função para adicionar item ao histórico
# ==============================
def adicionar_ao_historico(tipo, conteudo, caminho_imagem=None, eh_resposta_ia=False):
    item = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        "data_hora": datetime.now().isoformat(),
        "tipo": tipo,
        "conteudo": conteudo,
        "caminho_imagem": str(caminho_imagem) if caminho_imagem else None,
        "eh_resposta_ia": eh_resposta_ia
    }
    st.session_state.historico.append(item)
    salvar_historico(st.session_state.historico)

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP — Menu")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Criador de Apps", "Chat da MSSP", "Configurações"),
    index=2
)

# ==============================
# Chat da MSSP
# ==============================
if pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.caption("Converse com a Marie Sophie Souza Pires — sua assistente pessoal para criação de apps.")

    mensagem_usuario = st.text_input(
        label="Sua mensagem:",
        placeholder="Ex: Olá MSSP! Quero criar um app de tarefas.",
        help="Digite sua mensagem e clique em 'Enviar'."
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        btn_enviar = st.button("📤 Enviar")

    if btn_enviar and mensagem_usuario.strip():
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        resposta = ia_mssp_responder(
            mensagem_usuario=mensagem_usuario,
            historico_recente=st.session_state.historico
        )
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        st.rerun()

    st.markdown("---")
    st.subheader("Ou envie uma imagem")

    uploaded_file = st.file_uploader(
        label="Escolha uma imagem (jpg, png, jpeg):",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file is not None:
        ext = uploaded_file.name.split(".")[-1].lower()
        nome_arquivo = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        caminho_imagem = IMAGENS_DIR / nome_arquivo
        with open(caminho_imagem, "wb") as f:
            f.write(uploaded_file.getbuffer())
        adicionar_ao_historico("usuario_imagem", "Imagem enviada pelo usuário", caminho_imagem)
        resposta = ia_mssp_responder(tem_imagem=True)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        st.success("✅ Imagem recebida! A MSSP respondeu abaixo.")
        st.rerun()

    st.markdown("---")
    st.subheader("📜 Histórico da Conversa")

    if st.session_state.historico:
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m/%Y %H:%M:%S")
            if item["tipo"] == "usuario_texto":
                st.markdown(f"**👤 Você** • {data_fmt}")
                st.code(item["conteudo"], language=None)
            elif item["tipo"] == "usuario_imagem":
                st.markdown(f"**🖼️ Você (imagem)** • {data_fmt}")
                if item["caminho_imagem"] and os.path.exists(item["caminho_imagem"]):
                    st.image(item["caminho_imagem"], use_column_width=True)
                else:
                    st.text("[Imagem não disponível]")
            elif item["tipo"] == "ia_resposta":
                st.markdown(f"**🤖 MSSP** • {data_fmt}")
                st.info(item["conteudo"])
            st.markdown("---")
    else:
        st.info("Nenhuma conversa ainda. Envie uma mensagem ou imagem para começar!")

# ==============================
# Outras páginas
# ==============================
elif pagina == "Início":
    st.title("Marie Sophie Souza Pires")
    st.subheader("Projeto MSSP — Estrutura Base")
    st.write("""
    Bem-vindo à estrutura base do **MSSP**.

    Este aplicativo foi criado para servir como fundação para futuras funcionalidades, incluindo:
    - Criação automática de apps
    - Chat com IA integrada
    - Configurações personalizadas

    Use o menu lateral para navegar entre as seções.
    """)

elif pagina == "Criador de Apps":
    st.title("🛠️ Criador de Apps")
    st.write("""
    Esta seção será usada no futuro para:

    - Gerar novos aplicativos automaticamente a partir de templates
    - Personalizar layouts e funcionalidades
    - Exportar apps prontos para deploy

    Por enquanto, esta é apenas uma estrutura — nenhuma funcionalidade real ainda.
    """)

elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("""
    Esta seção será usada no futuro para:

    - Ajustar temas, cores e layouts
    - Gerenciar conexões com APIs
    - Controlar permissões e segurança

    Por enquanto, esta é apenas uma estrutura — nenhuma configuração real ainda.
    """)
