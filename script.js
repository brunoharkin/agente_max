document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const sessionId = 'user_' + Math.random().toString(36).substr(2, 9);

    // Adiciona a mensagem inicial do bot
    addMessage('Olá! Aqui é a AndreIA, da Paulo Loja 3 Maxi. Em que posso ajudar?', 'bot');

    // Função para adicionar mensagem ao chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        
        // Rola para a última mensagem
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Função para enviar mensagem
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Desabilita input e botão durante o processamento
        userInput.disabled = true;
        sendButton.disabled = true;

        // Adiciona a mensagem do usuário ao chat
        addMessage(message, 'user');
        
        // Limpa o input
        userInput.value = '';
        
        try {
            // Faz a requisição para o backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.response || 'Erro na comunicação com o servidor');
            }

            // Adiciona a resposta do bot ao chat
            addMessage(data.response, 'bot');

        } catch (error) {
            console.error('Erro:', error);
            addMessage('Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.', 'bot');
        } finally {
            // Reabilita input e botão
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Ajusta a altura do textarea conforme o conteúdo
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 200) + 'px';
    });

    // Mantém o foco no input
    userInput.focus();
}); 