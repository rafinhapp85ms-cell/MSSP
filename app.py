import streamlit as st
import json
import os
from datetime import datetime, timedelta
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
# Diretórios e arquivos de histórico
# ==============================
AGENDAMENTOS_ARQUIVO = "agendamentos_salao.json"

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
# Função para obter horários disponíveis
# ==============================
def obter_horarios_disponiveis(data_selecionada, profissional_selecionado, agendamentos):
    # Horários padrão (09:00, 10:00, 11:00, 12:00, 14:00, 15:00, 16:00, 17:00, 18:00, 19:00)
    horarios_padrao = [
        "09:00", "10:00", "11:00", "12:00",
        "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"
    ]
    
    # Filtrar agendamentos na data e profissional
    agendamentos_filtrados = [
        ag for ag in agendamentos
        if ag["data"] == data_selecionada and ag["profissional"] == profissional_selecionado
    ]
    
    # Remover horários ocupados
    horarios_ocupados = {ag["horario"] for ag in agendamentos_filtrados}
    horarios_disponiveis = [h for h in horarios_padrao if h not in horarios_ocupados]
    
    return horarios_disponiveis

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP — Menu")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Criador de Apps", "Chat da MSSP", "Agendador de Postagens", "Histórico de Conversas", "Histórico de Imagens", "Configurações"),
    index=1
)

# ==============================
# Criador de Apps — Página do Salão de Cabelo
# ==============================
if pagina == "Criador de Apps":
    st.title("✂️ App de Agendamento para Salão de Cabelo")
    st.caption("Crie seu app de agendamento em minutos — sem programação.")

    # Carregar agendamentos
    agendamentos = carregar_agendamentos()

    # Formulário de agendamento
    st.subheader("📅 Marque sua consulta")

    # Seleção de data (hoje + 7 dias)
    data_atual = datetime.now().date()
    datas_disponiveis = [data_atual + timedelta(days=i) for i in range(8)]
    data_selecionada = st.date_input("Data:", value=data_atual, min_value=data_atual)

    # Seleção de profissional
    profissionais = ["Ana", "Bruna", "Carla", "Diego", "Eduardo"]
    profissional_selecionado = st.selectbox("Cabeleireiro(a):", profissionais)

    # Obter horários disponíveis
    horarios_disponiveis = obter_horarios_disponiveis(str(data_selecionada), profissional_selecionado, agendamentos)

    if len(horarios_disponiveis) == 0:
        st.warning("⚠️ Não há horários disponíveis para este profissional nesta data.")
    else:
        horario_selecionado = st.selectbox("Horário:", horarios_disponiveis)

    # Botão de agendamento
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

    # Botão de WhatsApp
    st.markdown("---")
    st.markdown('[💬 Falar com o salão no WhatsApp](https://wa.me/351927245410?text=Olá!%20Vim%20do%20app%20de%20agendamento)', unsafe_allow_html=True)

    # Mostrar agendamentos salvos
    st.markdown("---")
    st.subheader("📋 Agendamentos Salvos")

    if agendamentos:
        agendamentos_ordenados = sorted(agendamentos, key=lambda x: (x["data"], x["horario"]), reverse=False)
        for ag in agendamentos_ordenados:
            st.markdown(f"**{ag['profissional']}** • {ag['data']} às {ag['horario']}")
            st.markdown("---")
    else:
        st.info("Nenhum agendamento salvo ainda.")

    # Aviso importante
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
elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("Em desenvolvimento.")
