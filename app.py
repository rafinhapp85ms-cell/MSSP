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
IMAGENS_DIR.mkdir(exist_ok=True)  # Cria pasta se não existir

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
    with open(HISTORICO_ARQUIVO, "w", encoding=" utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# ==============================
# Inicializar histórico na sessão
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

# ==============================
# Função para adicionar item ao histórico
# ==============================
def adicionar_ao_historico(tipo, conteudo, caminho_imagem=None):
    """
    Adiciona um item ao histórico.
    - tipo: "texto" ou "imagem"
    - conteudo: texto digitado ou descrição da imagem
    - caminho_imagem: opcional, caminho do arquivo salvo
    """
    item = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        "data_hora": datetime.now().isoformat(),
        "tipo": tipo,
        "conteudo": conteudo,
        "caminho_imagem": str(caminho_imagem) if caminho_imagem else None
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
    index=0
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
# Conteúdo principal: Chat da MSSP
# ==============================
elif pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.write("""
    Esta seção permite enviar mensagens e imagens.  
    Todo o histórico é salvo localmente e pode ser revisado abaixo.
    """)

    # ==============================
    # 🖼️ Upload de imagem
    # ==============================
    st.markdown("---")
    st.subheader("🖼️ Envie uma imagem")

    uploaded_file = st.file_uploader(
        label="Escolha uma imagem (jpg, png, jpeg):",
        type=["jpg", "png", "jpeg"],
        help="Apenas formatos JPG, PNG e JPEG são suportados."
    )

    if uploaded_file is not None:
        # Salvar imagem no /tmp/
        ext = uploaded_file.name.split(".")[-1]
        nome_arquivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        caminho_imagem = IMAGENS_DIR / nome_arquivo
        
        with open(caminho_imagem, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Adicionar ao histórico
        adicionar_ao_historico("imagem", "Imagem enviada pelo usuário", caminho_imagem)
        st.image(str(caminho_imagem), caption="Imagem recebida", use_column_width=True)
        st.success("✅ Imagem salva no histórico!")

    # ==============================
    # 💬 Campo de texto
    # ==============================
    st.markdown("---")
    st.subheader("💬 Envie uma mensagem")

    pergunta = st.text_input(
        label="Sua mensagem:",
        placeholder="Ex: O que tem nesta imagem? Como posso melhorar meu app?",
        help="Digite uma pergunta ou comando."
    )

    if st.button("Enviar mensagem"):
        if pergunta.strip():
            adicionar_ao_historico("texto", pergunta)
            st.info("📌 Mensagem salva no histórico!")
        else:
            st.warning("⚠️ Digite algo antes de enviar.")

    # ==============================
    # 📜 Visualização do histórico
    # ==============================
    st.markdown("---")
    st.subheader("📜 Histórico de Conversas")

    if st.session_state.historico:
        # Ordenar do mais recente para o mais antigo
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )
        
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m/%Y %H:%M:%S")
            tipo_icone = "🖼️" if item["tipo"] == "imagem" else "💬"
            
            st.markdown(f"**{tipo_icone} {data_fmt}**")
            
            if item["tipo"] == "imagem" and item["caminho_imagem"]:
                if os.path.exists(item["caminho_imagem"]):
                    st.image(item["caminho_imagem"], use_column_width=True)
                else:
                    st.text("[Imagem não disponível]")
            else:
                st.code(item["conteudo"], language=None)
            
            st.markdown("---")
    else:
        st.info("Nenhum item no histórico ainda.")

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
