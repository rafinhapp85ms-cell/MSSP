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
