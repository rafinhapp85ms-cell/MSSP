import streamlit as st

# ==============================
# Configuração inicial da página
# ==============================
st.set_page_config(
    page_title="MSSP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Menu lateral (sidebar)
# ==============================
st.sidebar.title("MSSP — Menu")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Criador de Apps", "Chat da MSSP", "Configurações"),
    index=0  # Página inicial por padrão
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

    # ==============================
    # 🔧 FORMULÁRIO DE ENTRADA DE DADOS
    # ==============================
    st.markdown("---")  # Linha divisória
    st.subheader("📝 Formulário de Entrada")

    # Campo de texto
    entrada = st.text_input(
        label="Digite algo aqui:",
        placeholder="Ex: Meu primeiro app, Ideia de projeto, etc.",
        help="Este campo coleta um texto simples. Será exibido após o envio."
    )

    # Campo de seleção (dropdown)
    tipo_app = st.selectbox(
        label="Escolha o tipo de app:",
        options=["App Simples", "App com Gráficos", "App com IA"],
        help="Selecione o tipo de aplicativo que deseja criar."
    )

    # Botão de envio
    if st.button("Enviar"):
        if entrada.strip():  # Verifica se o campo não está vazio
            st.success("✅ Dados enviados com sucesso!")
            st.markdown("### Você digitou:")
            st.code(entrada, language=None)  # Exibe o texto digitado
            st.markdown("### Tipo de app selecionado:")
            st.code(tipo_app, language=None)  # Exibe o tipo de app selecionado
        else:
            st.warning("⚠️ Por favor, digite algo antes de enviar.")

# ==============================
# Conteúdo principal: Chat da MSSP
# ==============================
elif pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.write("""
    Esta seção será usada no futuro para:

    - Conversar com uma IA integrada ao projeto
    - Fazer perguntas sobre o código ou o projeto
    - Receber sugestões de melhorias automáticas

    Por enquanto, esta é apenas uma estrutura — nenhuma IA conectada ainda.
    """)

    # ==============================
    # 🖼️ UPLOAD DE IMAGENS (ETAPA 5)
    # ==============================
    st.markdown("---")  # Linha divisória
    st.subheader("🖼️ Envie uma imagem para análise")

    # Campo de upload de imagem
    uploaded_file = st.file_uploader(
        label="Escolha uma imagem (jpg, png, jpeg):",
        type=["jpg", "png", "jpeg"],
        help="Faça upload de uma imagem para que a IA possa analisá-la. Apenas formatos JPG, PNG e JPEG são suportados."
    )

    # Se uma imagem for enviada, mostrar na tela
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Imagem recebida", use_column_width=True)
        st.success("✅ Imagem carregada com sucesso!")

        # Placeholder para futura análise de IA
        st.info("""
        🔍 **Análise da imagem (futuro):**
        
        Nesta etapa, a IA ainda não está conectada — mas a estrutura já está pronta!
        
        Futuramente, você poderá:
        - Analisar o conteúdo da imagem
        - Responder perguntas sobre ela
        - Conectar isso ao chat principal
        
        Por enquanto, a imagem é apenas exibida na tela.
        """)

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
