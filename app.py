import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="MSSP",
    page_icon="🎯",
    layout="centered"
)

# Título principal
st.title("Marie Sophie Souza Pires")
st.subheader("Projeto MSSP – Simples, funcional e editável")

# Texto explicativo
st.write("Este é o primeiro app Streamlit do projeto MSSP.")
st.write("Você pode editar este código diretamente no GitHub.")

# Exemplo de interação
if st.button("Clique aqui para testar"):
    st.success("Funcionou! 👏")
