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
