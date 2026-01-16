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
# 🧠 IA SIMULADA — MSSP
# ==============================
def ia_mssp_responder(mensagem_usuario="", tem_imagem=False, tem_video=False, tem_audio=False, historico_recente=None):
    msg_lower = mensagem_usuario.strip().lower()

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

    if any(palavra in msg_lower for palavra in ["oi", "olá", "ola", "eai", "salve"]):
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires)!\n\n"
            "Fico feliz em te ver! Como posso te ajudar hoje?\n\n"
            "Você pode:\n"
            "- Pedir ajuda para criar um app\n"
            "- Enviar uma imagem, vídeo ou áudio\n"
            "- Perguntar sobre o histórico salvo\n\n"
            "Estou aqui para construir junto com você! 💙"
        )

    if any(palavra in msg_lower for palavra in ["ajudar", "criar", "app", "aplicativo", "fazer", "construir"]):
        return (
            "🛠️ Claro! Vamos criar um app juntos.\n\n"
            "Para começar, me diga:\n"
            "1. Qual é o objetivo do app?\n"
            "2. Quais funcionalidades ele precisa ter?\n"
            "3. Você já tem algum código ou ideia?\n\n"
            "Com essas informações, posso te guiar passo a passo com código editável no GitHub."
        )

    if tem_imagem or tem_video or tem_audio:
        return (
            "✅ Mídia recebida! \n\n"
            "Por enquanto, estou apenas armazenando-a no histórico. "
            "No futuro, poderei analisá-la e responder perguntas sobre ela.\n\n"
            "Como posso te ajudar agora?"
        )

    return (
        "Entendi! Sou a **MSSP** (Marie Sophie Souza Pires) 👋\n\n"
        "Minha função é te ajudar a criar e gerenciar aplicativos de forma simples e totalmente editável.\n\n"
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

    # Exibir últimas mensagens (opcional, leve)
    if st.session_state.historico:
        st.subheader("Últimas mensagens:")
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )[:5]
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m %H:%M")
            if item["tipo"] == "usuario_texto":
                st.markdown(f"**👤 Você** • {data_fmt}")
                st.code(item["conteudo"], language=None)
            elif item["tipo"] == "ia_resposta":
                st.markdown(f"**🤖 MSSP** • {data_fmt}")
                st.info(item["conteudo"])
        st.markdown("---")

    # Caixa de texto
    mensagem_usuario = st.text_input(
        label="Sua mensagem:",
        placeholder="Digite sua mensagem...",
        label_visibility="collapsed"
    )

    # Botões: Enviar + Anexar
    col1, col2 = st.columns(2)
    with col1:
        btn_enviar = st.button("📤 Enviar", use_container_width=True)
    with col2:
        btn_anexar = st.button("📎 Anexar", use_container_width=True)

    # Menu de anexos (só aparece ao clicar em "Anexar")
    if btn_anexar:
        st.markdown("---")
        st.subheader("Selecione o tipo de arquivo:")

        # Opções de mídia
        col_img, col_vid, col_aud = st.columns(3)
        with col_img:
            uploaded_image = st.file_uploader("Imagem", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
            if uploaded_image is not None:
                ext = uploaded_image.name.split(".")[-1].lower()
                nome = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                caminho = IMAGENS_DIR / nome
                with open(caminho, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                adicionar_ao_historico("usuario_imagem", "Imagem enviada", caminho)
                with st.spinner("🧠 Analisando imagem..."):
                    resposta = ia_mssp_responder(tem_imagem=True)
                adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
                st.success("✅ Imagem recebida!")
                st.image(str(caminho), use_column_width=True)
                st.subheader("Resposta da MSSP:")
                st.info(resposta)
                st.rerun()

        with col_vid:
            uploaded_video = st.file_uploader("Vídeo", type=["mp4", "avi", "mov"], label_visibility="collapsed")
            if uploaded_video is not None:
                ext = uploaded_video.name.split(".")[-1].lower()
                nome = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                caminho = VIDEOS_DIR / nome
                with open(caminho, "wb") as f:
                    f.write(uploaded_video.getbuffer())
                adicionar_ao_historico("usuario_video", "Vídeo enviado", caminho)
                with st.spinner("🧠 Analisando vídeo..."):
                    resposta = ia_mssp_responder(tem_video=True)
                adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
                st.success("✅ Vídeo recebido!")
                st.video(str(caminho))
                st.subheader("Resposta da MSSP:")
                st.info(resposta)
                st.rerun()

        with col_aud:
            uploaded_audio = st.file_uploader("Áudio", type=["mp3", "wav", "ogg"], label_visibility="collapsed")
            if uploaded_audio is not None:
                ext = uploaded_audio.name.split(".")[-1].lower()
                nome = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                caminho = AUDIOS_DIR / nome
                with open(caminho, "wb") as f:
                    f.write(uploaded_audio.getbuffer())
                adicionar_ao_historico("usuario_audio", "Áudio enviado", caminho)
                with st.spinner("🧠 Analisando áudio..."):
                    resposta = ia_mssp_responder(tem_audio=True)
                adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
                st.success("✅ Áudio recebido!")
                st.audio(str(caminho))
                st.subheader("Resposta da MSSP:")
                st.info(resposta)
                st.rerun()

    # Processar envio de texto
    if btn_enviar and mensagem_usuario.strip():
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        with st.spinner("🧠 A MSSP está pensando..."):
            resposta = ia_mssp_responder(mensagem_usuario=mensagem_usuario)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        st.markdown("---")
        st.subheader("Sua mensagem:")
        st.code(mensagem_usuario, language=None)
        st.subheader("Resposta da MSSP:")
        st.info(resposta)
        st.rerun()

# ==============================
# Histórico de Conversas
# ==============================
elif pagina == "Histórico de Conversas":
    st.title("📜 Histórico de Conversas")
    if st.session_state.historico:
        for item in sorted(st.session_state.historico, key=lambda x: x["data_hora"], reverse=True):
            data = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m %H:%M")
            if item["tipo"] == "usuario_texto":
                st.markdown(f"**👤 Você** • {data}")
                st.code(item["conteudo"], language=None)
            elif item["tipo"] == "ia_resposta":
                st.markdown(f"**🤖 MSSP** • {data}")
                st.info(item["conteudo"])
            st.markdown("---")
    else:
        st.info("Nenhuma conversa ainda.")

# ==============================
# Histórico de Imagens
# ==============================
elif pagina == "Histórico de Imagens":
    st.title("🖼️ Histórico de Imagens")
    if st.session_state.historico:
        for item in sorted(st.session_state.historico, key=lambda x: x["data_hora"], reverse=True):
            if item["tipo"] == "usuario_imagem":
                data = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m %H:%M")
                st.markdown(f"**🖼️ Você (imagem)** • {data}")
                if item["caminho_midia"] and os.path.exists(item["caminho_midia"]):
                    st.image(item["caminho_midia"], use_column_width=True)
                else:
                    st.text("[Imagem não disponível]")
                st.markdown("---")
    else:
        st.info("Nenhuma imagem enviada ainda.")

# ==============================
# Outras páginas
# ==============================
elif pagina == "Início":
    st.title("Marie Sophie Souza Pires")
    st.write("Bem-vindo ao projeto MSSP.")
elif pagina == "Criador de Apps":
    st.title("🛠️ Criador de Apps")
    st.write("Formulário funcional já implementado.")
elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("Em desenvolvimento.")
