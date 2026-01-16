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
# 🧠 FUNÇÃO DA IA REAL – MSSP com Hugging Face
# ==============================
def ia_mssp_responder(mensagem_usuario="", tem_imagem=False, historico_recente=None):
    """
    Conecta à IA real via Hugging Face Inference API (gratuita).
    Responde em português, com personalidade da MSSP.
    """
    # Substitua YOUR_HF_TOKEN pelo seu token real do Hugging Face
    HF_TOKEN = "YOUR_HF_TOKEN"  # ← ALTERE ESTA LINHA!

    if not HF_TOKEN or HF_TOKEN == "YOUR_HF_TOKEN":
        return (
            "⚠️ **Chave de API não configurada!**\n\n"
            "Para ativar a IA real:\n"
            "1. Crie uma conta grátis em https://huggingface.co\n"
            "2. Gere um token em Settings > Access Tokens\n"
            "3. Cole o token no código (linha 45 do app.py)\n"
            "4. Salve e atualize o app."
        )

    if tem_imagem:
        system_prompt = (
            "Você é a MSSP (Marie Sophie Souza Pires), uma assistente pessoal amigável que ajuda a criar apps. "
            "O usuário enviou uma imagem. Como você não pode vê-la ainda, responda de forma útil: "
            "agradeça, diga que no futuro poderá analisá-la, e pergunte como pode ajudar agora. "
            "Responda em português do Brasil, de forma curta e acolhedora."
        )
        user_message = "Enviei uma imagem. O que você pode fazer?"
    else:
        system_prompt = (
            "Você é a MSSP (Marie Sophie Souza Pires), uma assistente pessoal amigável e útil, que ajuda a criar e gerenciar aplicativos. "
            "Responda sempre em português do Brasil, de forma clara, completa e orientadora. "
            "Nunca mencione que é uma IA. Assuma que é a Marie Sophie Souza Pires. "
            "Seja prática, evite jargões técnicos desnecessários, e sempre ofereça ajuda concreta."
        )
        user_message = mensagem_usuario

    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n",
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                texto = result[0].get("generated_text", "").strip()
                if "<|eot_id|>" in texto:
                    texto = texto.split("<|eot_id|>")[0]
                return texto if texto else "Desculpe, não entendi. Pode reformular?"
            else:
                return "Erro: resposta inesperada da IA."
        elif response.status_code == 429:
            return "⚠️ Limite de uso atingido. Tente novamente mais tarde."
        else:
            return f"Erro {response.status_code}: falha na conexão com a IA."
    except Exception as e:
        return f"❌ Erro de conexão: {str(e)}"

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
        with st.spinner("🧠 A MSSP está pensando..."):
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
        with st.spinner("🧠 A MSSP está analisando a imagem..."):
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

    st.markdown("---")
    st.subheader("📝 Formulário de Entrada")

    entrada = st.text_input(
        label="Digite algo aqui:",
        placeholder="Ex: Meu primeiro app, Ideia de projeto, etc.",
        help="Este campo coleta um texto simples. Será exibido após o envio."
    )

    tipo_app = st.selectbox(
        label="Escolha o tipo de app:",
        options=["App Simples", "App com Gráficos", "App com IA"],
        help="Selecione o tipo de aplicativo que deseja criar."
    )

    if st.button("Enviar"):
        if entrada.strip():
            st.success("✅ Dados enviados com sucesso!")
            st.markdown("### Você digitou:")
            st.code(entrada, language=None)
            st.markdown("### Tipo de app selecionado:")
            st.code(tipo_app, language=None)
        else:
            st.warning("⚠️ Por favor, digite algo antes de enviar.")

elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("""
    Esta seção será usada no futuro para:

    - Ajustar temas, cores e layouts
    - Gerenciar conexões com APIs
    - Controlar permissões e segurança

    Por enquanto, esta é apenas uma estrutura — nenhuma configuração real ainda.
    """)
