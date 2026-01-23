import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# ==============================
# Configuração inicial da página
# ==============================
st.set_page_config(
    page_title="MSSP — Salão de Cabelo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Diretórios e arquivos
# ==============================
AGENDAMENTOS_ARQUIVO = "agendamentos_salao.json"
CREDENCIAIS_ARQUIVO = "credenciais.json"

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
# Função para carregar credenciais (sem senhas)
# ==============================
def carregar_credenciais():
    if os.path.exists(CREDENCIAIS_ARQUIVO):
        try:
            with open(CREDENCIAIS_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

# ==============================
# Função para salvar credenciais (sem senhas)
# ==============================
def salvar_credenciais(credenciais):
    # Remover senhas antes de salvar
    credenciais_sem_senha = [
        {k: v for k, v in cred.items() if k != "senha"}
        for cred in credenciais
    ]
    with open(CREDENCIAIS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(credenciais_sem_senha, f, ensure_ascii=False, indent=2)

# ==============================
# Função para obter horários disponíveis
# ==============================
def obter_horarios_disponiveis(data_selecionada, profissional_selecionado, agendamentos):
    horarios_padrao = [
        "09:00", "10:00", "11:00", "12:00",
        "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"
    ]
    agendamentos_filtrados = [
        ag for ag in agendamentos
        if ag["data"] == data_selecionada and ag["profissional"] == profissional_selecionado
    ]
    horarios_ocupados = {ag["horario"] for ag in agendamentos_filtrados}
    horarios_disponiveis = [h for h in horarios_padrao if h not in horarios_ocupados]
    return horarios_disponiveis

# ==============================
# 🔒 FUNÇÃO PARA USAR CREDENCIAL (simulada)
# ==============================
def usar_credencial(plataforma):
    """
    Simula o uso de uma credencial.
    Na versão futura, isso poderá acionar automações reais.
    Por enquanto, apenas confirma que a credencial existe.
    """
    # Verifica se a variável de ambiente existe
    senha = os.environ.get(f"SENHA_{plataforma.upper().replace(' ', '_')}")
    if senha:
        return f"✅ Credencial para **{plataforma}** está pronta para uso (aprovada manualmente)."
    else:
        return f"⚠️ Credencial para **{plataforma}** não configurada nas variáveis de ambiente."

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP — Menu")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Criador de Apps", "Chat da MSS P", "Agendador de Postagens", "Credenciais", "Produtos Afiliados (Europa)", "Histórico de Conversas", "Histórico de Imagens", "Configurações"),
    index=1
)

# ==============================
# Página: Produtos Afiliados (Europa)
# ==============================
if pagina == "Produtos Afiliados (Europa)":
    st.title("🛒 Produtos Afiliados (Europa)")
    st.caption("Encontre produtos para promover na Europa — com dados simulados e anúncios prontos.")

    # Inicializar estado da sessão para anúncios gerados
    if "anuncios_gerados" not in st.session_state:
        st.session_state.anuncios_gerados = {}

    # Formulário de busca
    st.subheader("🔍 Buscar Produtos")

    palavra_chave = st.text_input("Palavra-chave do produto:", placeholder="Ex: fone bluetooth, relógio smart")

    pais = st.selectbox(
        "País:",
        ["Portugal", "Espanha", "França", "Alemanha", "Itália"]
    )

    plataforma = st.selectbox(
        "Plataforma:",
        ["Amazon EU", "AliExpress EU", "Awin", "CJ Affiliate"]
    )

    if st.button("🔍 Buscar produtos"):
        if not palavra_chave.strip():
            st.warning("⚠️ Por favor, digite uma palavra-chave.")
        else:
            # Simular resultados de busca
            produtos_simulados = [
                {
                    "nome": f"{palavra_chave.title()} Pro - Edição Europa",
                    "preco": "€49,99",
                    "comissao": "€7,50",
                    "pais": pais,
                    "plataforma": plataforma
                },
                {
                    "nome": f"{palavra_chave.title()} Premium com Garantia",
                    "preco": "€64,90",
                    "comissao": "€9,75",
                    "pais": pais,
                    "plataforma": plataforma
                },
                {
                    "nome": f"{palavra_chave.title()} Básico - Frete Grátis",
                    "preco": "€29,99",
                    "comissao": "€4,50",
                    "pais": pais,
                    "plataforma": plataforma
                }
            ]

            st.session_state.produtos_encontrados = produtos_simulados
            st.session_state.ultima_busca = {
                "palavra_chave": palavra_chave,
                "pais": pais,
                "plataforma": plataforma
            }

    # Mostrar resultados da busca
    if "produtos_encontrados" in st.session_state:
        st.markdown("---")
        st.subheader("📦 Produtos Encontrados")

        for i, prod in enumerate(st.session_state.produtos_encontrados):
            with st.container():
                st.markdown(f"**{prod['nome']}**")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"💰 {prod['preco']}")
                with col2:
                    st.write(f"💶 {prod['comissao']}")
                with col3:
                    st.write(f"🌍 {prod['pais']}")
                with col4:
                    st.write(f"🔗 {prod['plataforma']}")
                
                if st.button("✍️ Gerar anúncio", key=f"gerar_{i}"):
                    anuncio = (
                        f"🔥 **Oferta imperdível!**\n\n"
                        f"Acabei de encontrar este **{prod['nome'].lower()}** por apenas **{prod['preco']}**!\n\n"
                        f"✅ Frete rápido para {prod['pais']}\n"
                        f"✅ Garantia de satisfação\n"
                        f"✅ Comissão justa para quem indica 😊\n\n"
                        f"👉 **Clique no link abaixo para garantir o seu!**\n"
                        f"[LINK DE AFILIADO AQUI]\n\n"
                        f"#afiliado #{prod['pais'].replace(' ', '').lower()}"
                    )
                    st.session_state.anuncios_gerados[i] = anuncio
                
                # Mostrar anúncio se já foi gerado
                if i in st.session_state.anuncios_gerados:
                    st.text_area(
                        "Seu anúncio pronto:",
                        value=st.session_state.anuncios_gerados[i],
                        height=180,
                        key=f"anuncio_{i}"
                    )
                
                st.markdown("---")

# ==============================
# Criador de Apps — Página do Salão de Cabelo
# ==============================
elif pagina == "Criador de Apps":
    st.title("✂️ App de Agendamento para Salão de Cabelo")
    st.caption("Crie seu app de agendamento em minutos — sem programação.")

    agendamentos = carregar_agendamentos()

    st.subheader("📅 Marque sua consulta")

    data_atual = datetime.now().date()
    datas_disponiveis = [data_atual + timedelta(days=i) for i in range(8)]
    data_selecionada = st.date_input("Data:", value=data_atual, min_value=data_atual)

    profissionais = ["Ana", "Bruna", "Carla", "Diego", "Eduardo"]
    profissional_selecionado = st.selectbox("Cabeleireiro(a):", profissionais)

    horarios_disponiveis = obter_horarios_disponiveis(str(data_selecionada), profissional_selecionado, agendamentos)

    if len(horarios_disponiveis) == 0:
        st.warning("⚠️ Não há horários disponíveis para este profissional nesta data.")
    else:
        horario_selecionado = st.selectbox("Horário:", horarios_disponiveis)

    if st.button("✅ Confirmar Agendamento"):
        novo_agendamento = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
            "data": str(data_selecionada),
            "profissional": profissional_selecionado,
            "horario": horario_selecionado,
            "status": "confirmado"
        }
        agendamentos.append(novo_agendamento)
        salvar_agendamentos(agendamentos)
        st.success("✅ Agendamento confirmado!")
        st.info(
            "ℹ️ Para pagar antecipadamente, entre em contato com o salão via WhatsApp.\n"
            "O app não processa pagamentos — use o botão abaixo para falar com eles."
        )

    st.markdown("---")
    st.markdown('[💬 Falar com o salão no WhatsApp](https://wa.me/351927245410?text=Olá!%20Vim%20do%20app%20de%20agendamento)', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Agendamentos Salvos")

    if agendamentos:
        agendamentos_ordenados = sorted(agendamentos, key=lambda x: (x["data"], x["horario"]), reverse=False)
        for ag in agendamentos_ordenados:
            st.markdown(f"**{ag['profissional']}** • {ag['data']} às {ag['horario']}")
            st.markdown("---")
    else:
        st.info("Nenhum agendamento salvo ainda.")

    st.info(
        "⚠️ Este app é um simulador de agendamento. "
        "Para pagamento antecipado (cartão, transferência, MBWay), o cliente deve entrar em contato via WhatsApp. "
        "No Streamlit Cloud gratuito, não é possível processar pagamentos ou manter banco de dados permanente."
    )

# ==============================
# Chat da MSSP
# ==============================
elif pagina == "Chat da MSSP":
    st.title("💬 Chat da MSSP")
    st.caption("Sua consultora técnica em Shopify, dropshipping e automações.")

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

    st.markdown(
        '[💬 Falar comigo no WhatsApp](https://wa.me/351927245410?text=Olá!%20Vim%20do%20app%20MSSP)',
        unsafe_allow_html=True
    )

    if btn_enviar and mensagem_usuario.strip():
        adicionar_ao_historico("usuario_texto", mensagem_usuario)
        with st.spinner("🧠 A MSSP está analisando..."):
            resposta = responder_mssp(mensagem_usuario=mensagem_usuario, historico_recente=st.session_state.historico)
        adicionar_ao_historico("ia_resposta", resposta, eh_resposta_ia=True)
        st.rerun()

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

    agendamentos = carregar_agendamentos()

    st.subheader("Novo Agendamento")

    plataforma = st.selectbox(
        "Plataforma:",
        ["Instagram", "TikTok", "Facebook", "Shopify Blog"]
    )

    tipo_conteudo = st.text_input(
        "Tipo de conteúdo:",
        placeholder="Ex: produto, oferta, dica, vídeo curto"
    )

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

    st.info(
        "ℹ️ Este agendamento é lógico. A execução automática depende de um servidor ativo 24/7. "
        "No Streamlit Cloud gratuito, o app dorme após inatividade, então não é possível executar postagens reais automaticamente."
    )

# ==============================
# Página: Credenciais
# ==============================
elif pagina == "Credenciais":
    st.title("🔐 Credenciais")
    st.caption("Gerencie suas credenciais com segurança — sem armazenar senhas no código.")

    st.info(
        "ℹ️ **Como funciona a segurança?**\n\n"
        "- As senhas **nunca são salvas** no arquivo `credenciais.json`\n"
        "- As senhas devem ser armazenadas como **variáveis de ambiente** no Streamlit Cloud\n"
        "- Apenas o nome da plataforma e o usuário são salvos\n"
        "- A MSSP **nunca mostra a senha**"
    )

    # Carregar credenciais existentes (sem senhas)
    credenciais = carregar_credenciais()

    # Formulário de cadastro
    st.subheader("➕ Nova Credencial")

    plataforma = st.selectbox(
        "Plataforma:",
        ["Instagram", "TikTok", "Facebook", "Email", "Afiliados"]
    )

    usuario = st.text_input("Usuário/Login:")

    senha = st.text_input("Senha:", type="password")

    if st.button("💾 Salvar com segurança"):
        if not usuario.strip():
            st.warning("⚠️ Por favor, preencha o usuário.")
        elif not senha.strip():
            st.warning("⚠️ Por favor, preencha a senha.")
        else:
            # Adicionar credencial à lista (sem salvar a senha)
            nova_credencial = {
                "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
                "plataforma": plataforma,
                "usuario": usuario.strip(),
                "salva_em": datetime.now().isoformat()
            }
            credenciais.append(nova_credencial)
            salvar_credenciais(credenciais)
            
            # Instruções para o usuário
            st.success("✅ Credencial salva com segurança!")
            st.markdown(
                f"🔑 **Próximo passo obrigatório:**\n\n"
                f"1. Vá para **Settings > Secrets** no seu repositório do Streamlit Cloud\n"
                f"2. Adicione uma nova secret com:\n"
                f"   - **Name**: `SENHA_{plataforma.upper().replace(' ', '_')}`\n"
                f"   - **Value**: sua senha real\n\n"
                f"Exemplo para Instagram: `SENHA_INSTAGRAM` = `minha_senha_secreta`"
            )

    # Mostrar credenciais salvas
    st.markdown("---")
    st.subheader("📋 Credenciais Salvas")

    if credenciais:
        for cred in credenciais:
            data_fmt = datetime.fromisoformat(cred["salva_em"]).strftime("%d/%m/%Y %H:%M")
            st.markdown(f"**{cred['plataforma']}** • {cred['usuario']} • {data_fmt}")
            
            # Botão para testar uso da credencial
            if st.button(f"🔍 Usar credencial ({cred['plataforma']})", key=f"use_{cred['id']}"):
                resultado = usar_credencial(cred["plataforma"])
                st.info(resultado)
            
            st.markdown("---")
    else:
        st.info("Nenhuma credencial salva ainda.")

    # Aviso final
    st.warning(
        "⚠️ **Importante:**\n\n"
        "- Este sistema **não faz login real** nas plataformas\n"
        "- É uma **estrutura preparatória** para automação futura\n"
        "- A aprovação manual será necessária antes de qualquer ação automatizada\n"
        "- Nunca compartilhe suas variáveis de ambiente"
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
elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("Em desenvolvimento.")
