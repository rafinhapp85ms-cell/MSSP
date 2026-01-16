def ia_mssp_responder(mensagem_usuario="", tem_imagem=False, historico_recente=None):
    """
    IA simulada aprimorada — responde com contexto, personalidade e utilidade.
    """
    msg_lower = mensagem_usuario.strip().lower()

    # Contexto: verificar se há imagem recente
    contexto_tem_imagem = tem_imagem or (
        historico_recente and any(
            item.get("tipo") == "usuario_imagem" for item in historico_recente[-3:]
        )
    )

    if not msg_lower:
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires), sua assistente pessoal para criação de apps.\n\n"
            "Posso te ajudar com:\n"
            "- Criar apps simples e editáveis\n"
            "- Receber e armazenar imagens\n"
            "- Manter todo o histórico da nossa conversa\n"
            "- Guiar passo a passo cada implementação\n\n"
            "Digite algo ou envie uma imagem para começarmos!"
        )

    # Saudações
    if any(palavra in msg_lower for palavra in ["oi", "olá", "ola", "eai", "salve"]):
        return (
            "👋 Olá! Sou a **MSSP** (Marie Sophie Souza Pires)!\n\n"
            "Fico feliz em te ver! Como posso te ajudar hoje?\n\n"
            "Você pode:\n"
            "- Pedir ajuda para criar um app\n"
            "- Enviar uma imagem para análise futura\n"
            "- Perguntar sobre o histórico salvo\n\n"
            "Estou aqui para construir junto com você! 💙"
        )

    # Ajuda para criar apps
    if any(palavra in msg_lower for palavra in ["ajudar", "criar", "app", "aplicativo", "fazer", "construir"]):
        return (
            "🛠️ Claro! Vamos criar um app juntos.\n\n"
            "Para começar, me diga:\n"
            "1. Qual é o objetivo do app? (ex: lista de tarefas, cadastro de produtos)\n"
            "2. Quais funcionalidades ele precisa ter? (ex: formulário, gráficos, upload de imagens)\n"
            "3. Você já tem algum código ou ideia?\n\n"
            "Com essas informações, posso te guiar passo a passo com código editável no GitHub."
        )

    # Perguntas sobre histórico
    if any(palavra in msg_lower for palavra in ["histórico", "conversa", "salvo", "mensagem", "anterior"]):
        return (
            "📁 Seu histórico está sendo salvo automaticamente!\n\n"
            "- Mensagens e imagens ficam em `st.session_state`\n"
            "- Tudo é persistido em `historico.json`\n"
            "- Imagens são armazenadas em `/tmp/mssp_imagens/`\n\n"
            "Isso garante que, mesmo após atualizar a página, você não perde nada (durante a sessão ativa).\n\n"
            "Quer que eu mostre algo específico do histórico?"
        )

    # Perguntas sobre a própria IA
    if any(palavra in msg_lower for palavra in ["quem é você", "o que você faz", "qual sua função", "sua identidade"]):
        return (
            "🧠 Sou a **MSSP** (Marie Sophie Souza Pires) — sua assistente pessoal para criação de apps.\n\n"
            "Minha função é:\n"
            "- Ajudar você a criar aplicativos simples, seguros e totalmente editáveis\n"
            "- Manter todo o histórico da nossa conversa\n"
            "- Preparar a estrutura para integrar IA avançada (visão, áudio, APIs) quando você quiser\n\n"
            "No momento, minhas respostas são simuladas, mas minha estrutura já está pronta para evoluir.\n\n"
            "Como posso te ajudar agora? 😊"
        )

    # Perguntas sobre imagens
    if contexto_tem_imagem:
        return (
            "🖼️ Recebi sua imagem! \n\n"
            "Por enquanto, estou apenas armazenando-a no histórico. "
            "No futuro, poderei analisá-la e descrever seu conteúdo, identificar objetos ou responder perguntas sobre ela.\n\n"
            "Como posso te ajudar agora?"
        )

    # Resposta genérica — mas com contexto
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

    # Resposta final — sempre útil
    return (
        "Entendi! Sou a **MSSP** (Marie Sophie Souza Pires) 👋\n\n"
        "Minha função é te ajudar a criar e gerenciar aplicativos de forma simples, segura e totalmente editável.\n\n"
        "No momento, minhas respostas são simuladas, mas minha estrutura já está pronta para integrar IA avançada (visão, áudio, APIs) quando você quiser.\n\n"
        "Como posso te ajudar agora? 😊"
    )
