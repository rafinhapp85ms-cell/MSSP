import streamlit as st
import json
import os
import requests
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
# 🧠 IA REAL com modelo PÚBLICO (sem restrições)
# ==============================
def ia_mssp_responder(mensagem_usuario="", tem_imagem=False, historico_recente=None):
    HF_TOKEN = "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"

    if tem_imagem:
        prompt = (
            "Você é a MSSP (Marie Sophie Souza Pires). O usuário enviou uma imagem. "
            "Como você não pode vê-la ainda, responda de forma útil: agradeça, diga que no futuro poderá analisá-la, "
            "e pergunte como pode ajudar agora. Responda em português do Brasil, de forma curta."
        )
        user_msg = "Enviei uma imagem. O que você pode fazer?"
    else:
        prompt = (
            "Você é a MSSP (Marie Sophie Souza Pires), assistente pessoal que ajuda a criar apps. "
            "Responda sempre em português do Brasil, de forma clara, útil e orientadora. "
            "Nunca diga que é uma IA. Seja a Marie Sophie Souza Pires."
        )
        user_msg = mensagem_usuario

    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"<|system|>\n{prompt}</s>\n<|user|>\n{user_msg}</s>\n<|assistant|>",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7, "return_full_text": False}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                texto = result[0].get("generated_text", "").strip()
                return texto if texto else "Desculpe, não entendi."
            else:
                return "Erro: resposta inesperada."
        elif response.status_code == 429:
            return "⚠️ Limite atingido. Tente mais tarde."
        else:
            return f"Erro {response.status_code}."
    except Exception as e:
        return f"❌ Erro: {str(e)}"

# ==============================
# Inicializar histórico
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

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
pagina = st.sidebar.radio("Navegue:", ("Início", "Criador de Apps", "Chat da MSSP", "Configurações"), index=2)

# ==============================
# Chat da MSSP
# ==============================
if pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.caption("Sua assistente pessoal para criação de apps.")

    mensagem = st.text_input("Sua mensagem:", placeholder="Ex: Olá! Quero criar um app.")
    if st.button("📤 Enviar") and mensagem.strip():
        adicionar_ao_historico("usuario_texto", mensagem)
        with st.spinner("🧠 A MSSP está pensando..."):
            resp = ia_mssp_responder(mensagem_usuario=mensagem)
        adicionar_ao_historico("ia_resposta", resp, eh_resposta_ia=True)
        st.rerun()

    st.markdown("---")
    st.subheader("Ou envie uma imagem")
    uploaded_file = st.file_uploader("Escolha uma imagem (jpg, png, jpeg):", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()
        nome = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        caminho = IMAGENS_DIR / nome
        with open(caminho, "wb") as f:
            f.write(uploaded_file.getbuffer())
        adicionar_ao_historico("usuario_imagem", "Imagem enviada", caminho)
        with st.spinner("🧠 Analisando imagem..."):
            resp = ia_mssp_responder(tem_imagem=True)
        adicionar_ao_historico("ia_resposta", resp, eh_resposta_ia=True)
        st.success("✅ Imagem recebida!")
        st.rerun()

    st.markdown("---")
    st.subheader("📜 Histórico")
    if st.session_state.historico:
        for item in sorted(st.session_state.historico, key=lambda x: x["data_hora"], reverse=True):
            data = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m %H:%M")
            if item["tipo"] == "usuario_texto":
                st.markdown(f"**👤 Você** • {data}")
                st.code(item["conteudo"], language=None)
            elif item["tipo"] == "usuario_imagem":
                st.markdown(f"**🖼️ Você (imagem)** • {data}")
                if item["caminho_imagem"] and os.path.exists(item["caminho_imagem"]):
                    st.image(item["caminho_imagem"], use_column_width=True)
            elif item["tipo"] == "ia_resposta":
                st.markdown(f"**🤖 MSSP** • {data}")
                st.info(item["conteudo"])
            st.markdown("---")
    else:
        st.info("Nenhuma conversa ainda.")

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
