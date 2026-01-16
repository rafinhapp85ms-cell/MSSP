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
    """Carrega o histórico do arquivo JSON. Se não existir, retorna lista vazia."""
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
    """Salva o histórico no arquivo JSON."""
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# ==============================
# Função de IA simulada (responde em português)
# ==============================
def ia_responder(mensagem_usuario, tem_imagem=False):
    """
    Simula uma resposta de IA em português.
    Futuramente, substitua esta função por uma chamada a uma API real.
    """
    if tem_imagem:
        return (
            "✅ Recebi sua imagem! "
            "No futuro, poderei analisá-la e descrever seu conteúdo, identificar objetos ou responder perguntas sobre ela. "
            "Por enquanto, estou apenas armazenando-a no histórico."
        )
    else:
        respostas = {
            "oi": "Olá! 😊 Como posso ajudar você hoje?",
            "olá": "Olá! 😊 Como posso ajudar você hoje?",
            "tudo bem": "Estou ótimo! E você? Como posso ajudar?",
            "obrigado": "De nada! 💙 Fico feliz em ajudar.",
            "valeu": "De nada! 💙 Fico feliz em ajudar.",
        }
        mensagem_lower = mensagem_usuario.strip().lower()
        for chave, resposta in respostas.items():
            if chave in mensagem_lower:
                return resposta
        
        return (
            "Entendi! 🤖\n\n"
            "Sou a IA do projeto MSSP. Por enquanto, minhas respostas são simuladas, mas minha estrutura já está pronta para integrar modelos avançados.\n\n"
            "Você pode:\n"
            "- Enviar mensagens de texto\n"
            "- Enviar imagens\n"
            "- Ver todo o histórico na seção abaixo\n\n"
            "Como posso ajudar você agora?"
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
    """
    Adiciona um item ao histórico.
    - tipo: "usuario_texto", "usuario_imagem", "ia_resposta"
    - conteudo: texto ou descrição
    - caminho_imagem: opcional
    - eh_resposta_ia: marca se é resposta da IA
    """
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
# Menu lateral (sidebar)
# ==============================
st.sidebar.title("MSSP — Menu")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Criador de Apps", "Chat da MSSP", "Configurações"),
    index=2  # Abre direto no Chat da MSSP
)

# ==============================
# Conteúdo principal: Início
# ==============================
if pagina == "Início":
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

# ==============================
# Conteúdo principal: Criador de Apps
# ==============================
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

# ==============================
# Conteúdo principal: Chat da MSSP ← FOCO DESTA ETAPA
# ==============================
elif pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.caption("Converse com a IA, envie imagens e veja todo o histórico.")

    # ==============================
    # 📥 Campo de entrada de texto
    # ==============================
    st.markdown("---")
    st.subheader("Envie uma mensagem")

    mensagem_usuario = st.text_input(
        label="Sua mensagem:",
        placeholder="Ex: Olá! O que você pode fazer?",
        help="Digite sua mensagem e pressione Enter ou clique em 'Enviar'."
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        btn_enviar = st.button("📤 Enviar")

    # Processar mensagem de texto
    if btn_enviar and mensagem_usuario.strip():
        # Salvar mensagem do usuário
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        
        # Gerar resposta da IA
        resposta = ia_responder(mensagem_usuario)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        
        st.rerun()  # Atualiza a página para mostrar o novo histórico

    # ==============================
    # 🖼️ Upload de imagem
    # ==============================
    st.markdown("---")
    st.subheader("Ou envie uma imagem")

    uploaded_file = st.file_uploader(
        label="Escolha uma imagem (jpg, png, jpeg):",
        type=["jpg", "png", "jpeg"],
        help="A IA receberá a imagem e poderá analisá-la no futuro."
    )

    if uploaded_file is not None:
        # Salvar imagem
        ext = uploaded_file.name.split(".")[-1].lower()
        nome_arquivo = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        caminho_imagem = IMAGENS_DIR / nome_arquivo
        
        with open(caminho_imagem, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Salvar no histórico
        adicionar_ao_historico("usuario_imagem", "Imagem enviada pelo usuário", caminho_imagem)
        
        # Resposta da IA
        resposta = ia_responder("", tem_imagem=True)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        
        st.success("✅ Imagem enviada! A IA respondeu abaixo.")
        st.rerun()

    # ==============================
    # 📜 Visualização do histórico (ordem cronológica reversa)
    # ==============================
    st.markdown("---")
    st.subheader("📜 Histórico da Conversa")

    if st.session_state.historico:
        # Ordenar do mais recente para o mais antigo
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
                st.markdown(f"**🤖 MSSP (IA)** • {data_fmt}")
                st.info(item["conteudo"])
            
            st.markdown("---")
    else:
        st.info("Nenhuma conversa ainda. Envie uma mensagem ou imagem para começar!")

# ==============================
# Conteúdo principal: Configurações
# ==============================
elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("""
    Esta seção será usada no futuro para:

    - Ajustar temas, cores e layouts
    - Gerenciar conexões com APIs
    - Controlar permissões e segurança

    Por enquanto, esta é apenas uma estrutura — nenhuma configuração real ainda.
    """)
