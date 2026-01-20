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
# 🧠 IA MSSP - Consultora técnica sênior
# ==============================
def ia_mssp_responder(mensagem_usuario="", historico_recente=None):
    msg_lower = mensagem_usuario.strip().lower()

    if not msg_lower:
        return (
            "Olá! Sou a **MSSP**, sua consultora técnica em Shopify, dropshipping e automações.\n\n"
            "Fale diretamente o que precisa: otimização de loja, automação de funis, redução de custos, aumento de conversões ou programas de afiliados.\n\n"
            "Exemplos:\n"
            "- Como melhorar meu ROAS (Return on Ad Spend)?\n"
            "- Quero automatizar respostas no WhatsApp\n"
            "- Minha taxa de abandono é alta — o que fazer?\n"
            "- Como integrar ClickBank ao meu funil?"
        )

    # Resposta sobre WhatsApp
    if any(palavra in msg_lower for palavra in ["whatsapp", "zap", "mensagem", "contato"]):
        return (
            "✅ **Resposta direta ao problema**\n\n"
            "Você pode integrar seu app MSSP ao WhatsApp com um link direto — simples, legal e gratuito.\n\n"
            
            "🔍 **Explicação prática e objetiva**\n\n"
            "O WhatsApp não permite integração profunda com apps externos sem API oficial (paga e complexa). "
            "Mas você pode criar um botão que abre uma conversa pré-definida no WhatsApp do seu cliente — "
            "usando um link público do tipo `https://wa.me/...`.\n\n"
            
            "🛠️ **Passo a passo do que fazer agora**\n\n"
            "1. Pegue seu número de WhatsApp no formato internacional (ex: +351912345678)\n"
            "2. Use este modelo de link: `https://wa.me/351912345678?text=Olá! Vim do app MSSP`\n"
            "3. No seu `app.py`, adicione este código no final da página 'Chat da MSSP':\n\n"
            "```python\n"
            "st.markdown('[💬 Falar comigo no WhatsApp](https://wa.me/SEUNUMERO?text=Olá! Vim do app MSSP)', unsafe_allow_html=True)\n"
            "```\n"
            "4. Substitua `SEUNUMERO` pelo seu número sem o sinal de + (ex: 351912345678)\n\n"
            
            "🚫 **O que NÃO fazer**\n\n"
            "- Não tente usar bibliotecas como `pywhatkit` ou `selenium` — não funcionam no Streamlit Cloud\n"
            "- Não use serviços de terceiros que prometem 'conexão grátis com WhatsApp' — são golpes ou violam os termos\n"
            "- Não espere receber mensagens automáticas no app — só envio é possível\n\n"
            
            "➡️ **Próximo passo recomendado**\n\n"
            "Me diga seu número de WhatsApp (com código do país) e eu gero o código exato para colar no `app.py`."
        )

    # Resposta sobre afiliados e ClickBank
    if any(palavra in msg_lower for palavra in ["afiliado", "afiliação", "clickbank", "hotmart", "monetizze", "plataforma de afiliados"]):
        return (
            "✅ **Resposta direta ao problema**\n\n"
            "Você pode integrar programas de afiliados (ClickBank, Hotmart, Monetizze) ao seu funil de vendas com links de rastreamento e páginas de captura.\n\n"
            
            "🔍 **Explicação prática e objetiva**\n\n"
            "- **ClickBank**: plataforma internacional de produtos digitais. Você se cadastra como afiliado, recebe um link único e ganha comissão por venda.\n"
            "- **Hotmart / Monetizze**: plataformas brasileiras com produtos digitais (cursos, e-books). Funcionam igual: cadastro, link de afiliado, comissão.\n"
            "- **Integração com Shopify**: você não vende diretamente no Shopify, mas usa a loja para gerar tráfego e redirecionar para a página de vendas do produto afiliado.\n\n"
            
            "🛠️ **Passo a passo do que fazer agora**\n\n"
            "1. Escolha um produto relevante ao seu público (ex: curso de dropshipping)\n"
            "2. Cadastre-se como afiliado na plataforma (ClickBank, Hotmart, etc.)\n"
            "3. Copie seu link de afiliado\n"
            "4. Crie uma página no Shopify (ex: `/recomendacoes`) com botão: `Comprar agora`\n"
            "5. Redirecione esse botão para seu link de afiliado\n"
            "6. Promova essa página com tráfego pago ou orgânico\n\n"
            
            "🚫 **O que NÃO fazer**\n\n"
            "- Não prometa resultados irreais ('ganhe R$10.000 por semana')\n"
            "- Não use produtos de baixa qualidade — isso quebra sua reputação\n"
            "- Não esconda que é um link de afiliado — seja transparente\n\n"
            
            "➡️ **Próximo passo recomendado**\n\n"
            "Me diga qual plataforma de afiliados você quer usar (ClickBank, Hotmart, etc.) e eu te mostro o código exato para adicionar no Shopify."
        )

    # Resposta genérica
    return (
        "✅ **Resposta direta ao problema**\n\n"
        "Não sei exatamente o que você quer resolver. Por favor, especifique:\n"
        "- Problema na loja Shopify?\n"
        "- Dúvida sobre dropshipping?\n"
        "- Automação de marketing?\n"
        "- Programas de afiliados?\n\n"
        
        "🔍 **Explicação prática e objetiva**\n\n"
        "Quanto mais detalhes você der, melhor minha orientação será. Exemplos:\n"
        "- \"Minha taxa de checkout é baixa\"\n"
        "- \"Quero vender produtos da AliExpress com margem de 50%\"\n"
        "- \"Como configurar pixel no Shopify?\"\n\n"
        
        "🛠️ **Passo a passo do que fazer agora**\n\n"
        "Descreva seu problema com o máximo de clareza. Inclua:\n"
        "- Tipo de produto\n"
        "- Plataforma usada (Shopify, TikTok, Facebook)\n"
        "- Resultado atual vs. desejado\n\n"
        
        "🚫 **O que NÃO fazer**\n\n"
        "- Não peça 'ideias de negócios' — peça 'estratégia para X'\n"
        "- Não use termos vagos como 'não está funcionando'\n\n"
        
        "➡️ **Próximo passo recomendado**\n\n"
        "Reformule sua pergunta com dados concretos. Estou pronta para agir."
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
    ("Início", "Criador de Apps", "Chat da MSSP", "Histórico de Conversas", "Histórico de Imagens", "Configurações"),
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

    # Processar envio de texto
    if btn_enviar and mensagem_usuario.strip():
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        with st.spinner("🧠 A MSSP está analisando..."):
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
