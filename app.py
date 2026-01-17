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
def ia_mssp_responder(mensagem_usuario="", historico_recente=None):
    msg_lower = mensagem_usuario.strip().lower()

    if not msg_lower:
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires), sua assistente pessoal para criação de apps.\n\n"
            "Posso te ajudar com:\n"
            "- Criar apps simples e editáveis\n"
            "- Manter todo o histórico da nossa conversa\n"
            "- Guiar passo a passo cada implementação\n\n"
            "Digite algo para começarmos!"
        )

    if any(palavra in msg_lower for palavra in ["oi", "olá", "ola", "eai", "salve"]):
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires)!\n\n"
            "Fico feliz em te ver! Como posso te ajudar hoje?\n\n"
            "Você pode:\n"
            "- Pedir ajuda para criar um app\n"
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

    if any(palavra in msg_lower for palavra in ["histórico", "conversa", "salvo", "mensagem", "anterior"]):
        return (
            "📁 Seu histórico está sendo salvo automaticamente!\n\n"
            "- Mensagens ficam em `st.session_state`\n"
            "- Tudo é persistido em `historico.json`\n\n"
            "Isso garante que, mesmo após atualizar a página, você não perde nada (durante a sessão ativa).\n\n"
            "Quer que eu mostre algo específico do histórico?"
        )

    if any(palavra in msg_lower for palavra in ["quem é você", "o que você faz", "qual sua função", "sua identidade"]):
        return (
            "🧠 Sou a **MSSP** (Marie Sophie Souza Pires) — sua assistente pessoal para criação de apps.\n\n"
            "Minha função é:\n"
            "- Ajudar você a criar aplicativos simples, seguros e totalmente editáveis\n"
            "- Manter todo o histórico da nossa conversa\n"
            "- Preparar a estrutura para integrar IA avançada quando você quiser\n\n"
            "No momento, minhas respostas são simuladas, mas minha estrutura já está pronta para evoluir.\n\n"
            "Como posso te ajudar agora? 😊"
        )

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
def adicionar_ao_historico(tipo, conteudo, eh_resposta_ia=False):
    item = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        "data_hora": datetime.now().isoformat(),
        "tipo": tipo,
        "conteudo": conteudo,
        "eh_resposta_ia": eh_resposta_ia
    }
    st.session_state.historico.append(item)
    salvar_historico(st.session_state.historico)

# ==============================
# Estilo CSS para fixar caixa no topo
# ==============================
st.markdown("""
<style>
/* Fixar container do input no topo */
.fixed-input-container {
    position: sticky;
    top: 0;
    background-color: white;
    z-index: 100;
    padding: 1rem 0;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

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

    # Caixa de entrada fixa no topo
    st.markdown('<div class="fixed-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([9, 1])
    with col1:
        mensagem_usuario = st.text_input(
            label="Sua mensagem:",
            placeholder="Digite sua mensagem...",
            label_visibility="collapsed",
            key="input_fixo"
        )
    with col2:
        btn_enviar = st.button("📤 Enviar", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Processar envio de texto
    if btn_enviar and mensagem_usuario.strip():
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        with st.spinner("🧠 A MSSP está pensando..."):
            resposta = ia_mssp_responder(mensagem_usuario=mensagem_usuario)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        st.rerun()

    # Área do histórico (rola para baixo)
    if st.session_state.historico:
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m %H:%M")
            if item["tipo"] == "usuario_texto":
                titulo = item["conteudo"][:50] + "..." if len(item["conteudo"]) > 50 else item["conteudo"]
                col1, col2 = st.columns([9, 1])
                with col1:
                    st.markdown(f"**👤 {titulo}** • {data_fmt}")
                with col2:
                    if st.button("🗑️", key=f"del_{item['id']}"):
                        st.session_state.historico.remove(item)
                        salvar_historico(st.session_state.historico)
                        st.rerun()
            elif item["tipo"] == "ia_resposta":
                st.markdown(f"**🤖 MSSP** • {data_fmt}")
                st.info(item["conteudo"])
            st.markdown("---")
    else:
        st.info("Nenhuma conversa ainda. Envie uma mensagem para começar!")

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
    st.info("Nenhuma imagem enviada ainda. Envie uma no Chat da MSSP para começar!")

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
