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
VIDEOS_DIR = Path("/tmp/mssp_videos")
AUDIOS_DIR = Path("/tmp/mssp_audios")

IMAGENS_DIR.mkdir(exist_ok=True)
VIDEOS_DIR.mkdir(exist_ok=True)
AUDIOS_DIR.mkdir(exist_ok=True)

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
def ia_mssp_responder(mensagem_usuario="", tem_imagem=False, tem_video=False, tem_audio=False, historico_recente=None):
    """
    Responde como a MSSP — sem API, sem token, 100% local.
    Simula inteligência com base em palavras-chave e contexto.
    """
    msg_lower = mensagem_usuario.strip().lower()

    # Contexto: verificar se há mídia recente
    contexto_tem_midia = (
        tem_imagem or
        tem_video or
        tem_audio or
        (
            historico_recente and any(
                item.get("tipo") in ["usuario_imagem", "usuario_video", "usuario_audio"]
                for item in historico_recente[-3:]
            )
        )
    )

    if not msg_lower:
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires), sua assistente pessoal para criação de apps.\n\n"
            "Posso te ajudar com:\n"
            "- Criar apps simples e editáveis\n"
            "- Receber e armazenar imagens, vídeos e áudios\n"
            "- Manter todo o histórico da nossa conversa\n"
            "- Guiar passo a passo cada implementação\n\n"
            "Digite algo ou envie uma mídia para começarmos!"
        )

    # Saudações
    if any(palavra in msg_lower for palavra in ["oi", "olá", "ola", "eai", "salve"]):
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires)!\n\n"
            "Fico feliz em te ver! Como posso te ajudar hoje?\n\n"
            "Você pode:\n"
            "- Pedir ajuda para criar um app\n"
            "- Enviar uma imagem, vídeo ou áudio para análise futura\n"
            "- Perguntar sobre o histórico salvo\n\n"
            "Estou aqui para construir junto com você! 💙"
        )

    # Ajuda para criar apps
    if any(palavra in msg_lower for palavra in ["ajudar", "criar", "app", "aplicativo", "fazer", "construir"]):
        return (
            "🛠️ Claro! Vamos criar um app juntos.\n\n"
            "Para começar, me diga:\n"
            "1. Qual é o objetivo do app? (ex: lista de tarefas, cadastro de produtos)\n"
            "2. Quais funcionalidades ele precisa ter? (ex: formulário, gráficos, upload de mídias)\n"
            "3. Você já tem algum código ou ideia?\n\n"
            "Com essas informações, posso te guiar passo a passo com código editável no GitHub."
        )

    # Perguntas sobre histórico
    if any(palavra in msg_lower for palavra in ["histórico", "conversa", "salvo", "mensagem", "anterior"]):
        return (
            "📁 Seu histórico está sendo salvo automaticamente!\n\n"
            "- Mensagens e mídias ficam em `st.session_state`\n"
            "- Tudo é persistido em `historico.json`\n"
            "- Imagens, vídeos e áudios são armazenados em `/tmp/mssp_*/`\n\n"
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

    # Perguntas sobre mídias
    if contexto_tem_midia:
        return (
            "🖼️🎤🎧 Recebi sua mídia! \n\n"
            "Por enquanto, estou apenas armazenando-a no histórico. "
            "No futuro, poderei analisá-la e descrever seu conteúdo, identificar objetos, transcrever áudio ou responder perguntas sobre ela.\n\n"
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
def adicionar_ao_historico(tipo, conteudo, caminho_midia=None, eh_resposta_ia=False):
    item = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        "data_hora": datetime.now().isoformat(),
        "tipo": tipo,
        "conteudo": conteudo,
        "caminho_midia": str(caminho_midia) if caminho_midia else None,
        "eh_resposta_ia": eh_resposta_ia
    }
    st.session_state.historico.append(item)
    salvar_historico(st.session_state.historico)

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP — Menu")

# Botões de navegação
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Criador de Apps", "Chat da MSSP", "Histórico de Conversas", "Histórico de Imagens", "Configurações"),
    index=2
)

# ==============================
# Chat da MSSP
# ==============================
if pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.caption("Converse com a Marie Sophie Souza Pires — sua assistente pessoal para criação de apps.")

    # Exibir histórico de conversas (apenas as últimas 5 mensagens)
    if st.session_state.historico:
        st.subheader("Últimas mensagens:")
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )[:5]  # Mostrar apenas as 5 mais recentes
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m %H:%M")
            if item["tipo"] == "usuario_texto":
                st.markdown(f"**👤 Você** • {data_fmt}")
                st.code(item["conteudo"], language=None)
            elif item["tipo"] == "ia_resposta":
                st.markdown(f"**🤖 MSSP** • {data_fmt}")
                st.info(item["conteudo"])
            st.markdown("---")

    # Campo de texto e botões
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])

    with col1:
        mensagem_usuario = st.text_input(
            label="Sua mensagem:",
            placeholder="Ex: Olá MSSP! Quero criar um app de tarefas.",
            help="Digite sua mensagem e clique em 'Enviar'."
        )

    with col2:
        btn_enviar = st.button("📤 Enviar")

    with col3:
        uploaded_image = st.file_uploader(
            "🖼️ Imagem",
            type=["jpg", "png", "jpeg"],
            label_visibility="collapsed"
        )

    with col4:
        uploaded_video = st.file_uploader(
            "🎥 Vídeo",
            type=["mp4", "avi", "mov"],
            label_visibility="collapsed"
        )

    # Processar mensagem
    if btn_enviar and mensagem_usuario.strip():
        # Salvar mensagem do usuário
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        
        # Gerar resposta da IA
        with st.spinner("🧠 A MSSP está pensando..."):
            resposta = ia_mssp_responder(
                mensagem_usuario=mensagem_usuario,
                historico_recente=st.session_state.historico
            )
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        
        # Mostrar pergunta e resposta na tela
        st.markdown("---")
        st.subheader("Sua mensagem:")
        st.code(mensagem_usuario, language=None)
        st.subheader("Resposta da MSSP:")
        st.info(resposta)
        
        st.rerun()

    # Processar imagem
    if uploaded_image is not None:
        ext = uploaded_image.name.split(".")[-1].lower()
        nome_arquivo = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        caminho_imagem = IMAGENS_DIR / nome_arquivo
        with open(caminho_imagem, "wb") as f:
            f.write(uploaded_image.getbuffer())
        adicionar_ao_historico("usuario_imagem", "Imagem enviada pelo usuário", caminho_imagem)
        
        # Gerar resposta da IA
        with st.spinner("🧠 Analisando imagem..."):
            resposta = ia_mssp_responder(tem_imagem=True)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        
        # Mostrar imagem e resposta
        st.success("✅ Imagem recebida!")
        st.image(str(caminho_imagem), caption="Imagem recebida", use_column_width=True)
        st.subheader("Resposta da MSSP:")
        st.info(resposta)
        
        st.rerun()

    # Processar vídeo
    if uploaded_video is not None:
        ext = uploaded_video.name.split(".")[-1].lower()
        nome_arquivo = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        caminho_video = VIDEOS_DIR / nome_arquivo
        with open(caminho_video, "wb") as f:
            f.write(uploaded_video.getbuffer())
        adicionar_ao_historico("usuario_video", "Vídeo enviado pelo usuário", caminho_video)
        
        # Gerar resposta da IA
        with st.spinner("🧠 Analisando vídeo..."):
            resposta = ia_mssp_responder(tem_video=True)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        
        # Mostrar vídeo e resposta
        st.success("✅ Vídeo recebido!")
        st.video(str(caminho_video))
        st.subheader("Resposta da MSSP:")
        st.info(resposta)
        
        st.rerun()

# ==============================
# Histórico de Conversas
# ==============================
elif pagina == "Histórico de Conversas":
    st.title("📜 Histórico de Conversas")
    st.caption("Veja todas as mensagens trocadas com a MSSP.")

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
            elif item["tipo"] == "ia_resposta":
                st.markdown(f"**🤖 MSSP** • {data_fmt}")
                st.info(item["conteudo"])
            st.markdown("---")
    else:
        st.info("Nenhuma conversa ainda. Envie uma mensagem no Chat da MSSP para começar!")

# ==============================
# Histórico de Imagens
# ==============================
elif pagina == "Histórico de Imagens":
    st.title("🖼️ Histórico de Imagens")
    st.caption("Veja todas as imagens enviadas e suas respostas associadas.")

    if st.session_state.historico:
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m/%Y %H:%M:%S")
            if item["tipo"] == "usuario_imagem":
                st.markdown(f"**🖼️ Você (imagem)** • {data_fmt}")
                if item["caminho_midia"] and os.path.exists(item["caminho_midia"]):
                    st.image(item["caminho_midia"], use_column_width=True)
                else:
                    st.text("[Imagem não disponível]")
                # Mostrar resposta da IA associada
                if len(st.session_state.historico) > st.session_state.historico.index(item) + 1:
                    proximo_item = st.session_state.historico[st.session_state.historico.index(item) + 1]
                    if proximo_item["tipo"] == "ia_resposta":
                        st.markdown(f"**🤖 MSSP (resposta)** • {proximo_item['data_hora']}")
                        st.info(proximo_item["conteudo"])
            st.markdown("---")
    else:
        st.info("Nenhuma imagem enviada ainda. Envie uma no Chat da MSSP para começar!")

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
