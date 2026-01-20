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
AGENDAMENTOS_ARQUIVO = "agendamentos.json"

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
# Função para carregar agendamentos
# ==============================
def carregar_agendamentos():
    if os.path.exists(AGENDAMENTOS_ARQUIVO):
        try:
            with open(AGENDAMENTOS_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

# ==============================
# Função para salvar agendamentos
# ==============================
def salvar_agendamentos(agendamentos):
    with open(AGENDAMENTOS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, ensure_ascii=False, indent=2)

# ==============================
# 🔍 FUNÇÃO PARA DETECTAR INTENÇÃO DO USUÁRIO
# ==============================
def detectar_intencao(mensagem_usuario):
    """
    Detecta a intenção do usuário com base em palavras-chave.
    Retorna uma das intenções pré-definidas.
    """
    msg = mensagem_usuario.strip().lower()
    
    # Intenção: criar_app
    if any(palavra in msg for palavra in ["criar app", "fazer app", "construir app", "app de", "aplicativo"]):
        return "criar_app"
    
    # Intenção: agendar_postagem
    if any(palavra in msg for palavra in ["agendar", "postagem", "postar", "redes sociais", "instagram", "tiktok", "facebook", "horário", "agenda"]):
        return "agendar_postagem"
    
    # Intenção: monetizacao (afiliados, vendas, ganhar dinheiro)
    if any(palavra in msg for palavra in ["monetizar", "ganhar dinheiro", "vender", "afiliado", "comissão", "clickbank", "hotmart", "lucro", "receita", "vendas"]):
        return "monetizacao"
    
    # Intenção: ajuda
    if any(palavra in msg for palavra in ["ajuda", "como fazer", "não sei", "me ajuda", "duvida", "dúvida", "orientação"]):
        return "ajuda"
    
    # Intenção: configuracoes
    if any(palavra in msg for palavra in ["configuração", "configurar", "ajustar", "preferência", "opção", "config"]):
        return "configuracoes"
    
    # Intenção padrão
    return "conversa_geral"


# ==============================
# 💬 FUNÇÃO PARA RESPONDER COM BASE NA INTENÇÃO
# ==============================
def responder_mssp(mensagem_usuario, historico_recente=None):
    """
    Gera respostas específicas com base na intenção detectada.
    Tudo em português, sem promessas irreais.
    """
    intencao = detectar_intencao(mensagem_usuario)
    
    if intencao == "criar_app":
        return (
            "✅ **Vamos criar um app!**\n\n"
            "Para começar, me diga:\n"
            "- Qual é o objetivo do app? (ex: lista de tarefas, cadastro de clientes)\n"
            "- Quais funcionalidades ele precisa ter?\n"
            "- Você já tem algum código ou ideia?\n\n"
            "Com essas informações, posso te guiar passo a passo com código editável no GitHub."
        )
    
    elif intencao == "agendar_postagem":
        return (
            "📅 **Agendamento de postagens**\n\n"
            "Use a página **'Agendador de Postagens'** no menu lateral para:\n"
            "- Escolher a plataforma (Instagram, TikTok, Facebook, Shopify Blog)\n"
            "- Definir o tipo de conteúdo\n"
            "- Selecionar os horários (09:00, 15:00, 21:00)\n\n"
            "⚠️ Lembre-se: este é um agendamento lógico. A execução automática real exige um servidor ativo 24/7."
        )
    
    elif intencao == "monetizacao":
        return (
            "💰 **Monetização e afiliados**\n\n"
            "Você pode integrar estas plataformas ao seu funil:\n"
            "- **ClickBank**: produtos digitais internacionais\n"
            "- **Hotmart**: cursos e e-books (disponível em Portugal)\n"
            "- **Digistore24**: foco na Europa (Alemanha)\n\n"
            "Quer que eu mostre como criar uma página de recomendações no Shopify com links de afiliado?"
        )
    
    elif intencao == "ajuda":
        return (
            "🆘 **Ajuda prática**\n\n"
            "Estou aqui para orientar com soluções reais. Por favor, especifique:\n"
            "- O que você está tentando fazer?\n"
            "- Onde está travando?\n"
            "- Qual é o resultado esperado?\n\n"
            "Exemplo: 'Minha taxa de checkout no Shopify é baixa — o que ajustar?'"
        )
    
    elif intencao == "configuracoes":
        return (
            "⚙️ **Configurações**\n\n"
            "A página de configurações está em desenvolvimento.\n\n"
            "Por enquanto, você pode:\n"
            "- Editar o código diretamente no GitHub\n"
            "- Salvar agendamentos na página dedicada\n"
            "- Gerenciar seu histórico de conversas\n\n"
            "O que você gostaria de configurar?"
        )
    
    else:  # conversa_geral
        return (
            "Olá! Sou a **MSSP**, sua consultora técnica em Shopify, dropshipping e automações.\n\n"
            "Fale diretamente o que precisa:\n"
            "- Criar um app\n"
            "- Agendar postagens\n"
            "- Monetizar com afiliados\n"
            "- Resolver um problema técnico\n\n"
            "Estou aqui para entregar orientação clara e aplicável."
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
    ("Início", "Criador de Apps", "Chat da MSSP", "Agendador de Postagens", "Histórico de Conversas", "Histórico de Imagens", "Configurações"),
    index=2
)

# ==============================
# Chat da MSSP
# ==============================
if pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.caption("Sua consultora técnica em Shopify, dropshipping e automações.")

    # Caixa de entrada fixa no topo
    st.markdown('<div class="fixed-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([9, 1])
    with col1:
        mensagem_usuario = st.text_input(
            label="Sua mensagem:",
            placeholder="Ex: Como integrar ClickBank ao meu funil?",
            label_visibility="collapsed",
            key="input_fixo"
        )
    with col2:
        btn_enviar = st.button("📤 Enviar", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Botão de WhatsApp fixo abaixo do input
    st.markdown(
        '[💬 Falar comigo no WhatsApp](https://wa.me/351927245410?text=Olá!%20Vim%20do%20app%20MSSP)',
        unsafe_allow_html=True
    )

    # Processar envio de texto
    if btn_enviar and mensagem_usuario.strip():
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        with st.spinner("🧠 A MSSP está analisando..."):
            resposta = responder_mssp(mensagem_usuario=mensagem_usuario, historico_recente=st.session_state.historico)
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
# Agendador de Postagens
# ==============================
elif pagina == "Agendador de Postagens":
    st.title("📅 Agendador de Postagens")
    st.caption("Simule o agendamento de postagens em redes sociais e blog.")

    # Carregar agendamentos existentes
    agendamentos = carregar_agendamentos()

    # Formulário de agendamento
    st.subheader("Novo Agendamento")

    plataforma = st.selectbox(
        "Plataforma:",
        ["Instagram", "TikTok", "Facebook", "Shopify Blog"]
    )

    tipo_conteudo = st.text_input(
        "Tipo de conteúdo:",
        placeholder="Ex: produto, oferta, dica, vídeo curto"
    )

    # Horários padrão
    horarios_padrao = ["09:00", "15:00", "21:00"]
    horarios_escolhidos = st.multiselect(
        "Horários de postagem (selecione até 3):",
        options=["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00",
                 "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                 "20:00", "21:00", "22:00", "23:00"],
        default=horarios_padrao
    )

    if st.button("💾 Salvar Agendamento"):
        if not tipo_conteudo.strip():
            st.warning("⚠️ Por favor, preencha o tipo de conteúdo.")
        elif len(horarios_escolhidos) == 0:
            st.warning("⚠️ Selecione pelo menos um horário.")
        else:
            novo_agendamento = {
                "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
                "data_criacao": datetime.now().isoformat(),
                "plataforma": plataforma,
                "tipo_conteudo": tipo_conteudo.strip(),
                "horarios": sorted(horarios_escolhidos)
            }
            agendamentos.append(novo_agendamento)
            salvar_agendamentos(agendamentos)
            st.success("✅ Agendamento salvo com sucesso!")
            st.rerun()

    # Mostrar agendamentos salvos
    st.markdown("---")
    st.subheader("Agendamentos Salvos")

    if agendamentos:
        agendamentos_ordenados = sorted(agendamentos, key=lambda x: x["data_criacao"], reverse=True)
        for ag in agendamentos_ordenados:
            data_fmt = datetime.fromisoformat(ag["data_criacao"]).strftime("%d/%m/%Y %H:%M")
            st.markdown(f"**{ag['plataforma']}** • {data_fmt}")
            st.write(f"**Conteúdo:** {ag['tipo_conteudo']}")
            st.write(f"**Horários:** {', '.join(ag['horarios'])}")
            st.markdown("---")
    else:
        st.info("Nenhum agendamento salvo ainda.")

    # Aviso importante
    st.info(
        "ℹ️ Este agendamento é lógico. A execução automática depende de um servidor ativo 24/7. "
        "No Streamlit Cloud gratuito, o app dorme após inatividade, então não é possível executar postagens reais automaticamente."
    )

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
