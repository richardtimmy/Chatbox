document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('sendButton');
    const userInput = document.getElementById('userInput');
    const messageContainer = document.getElementById('messageContainer');

    sendButton.addEventListener('click', () => {
        sendMessage();
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const messageText = userInput.value.trim().toLowerCase();
        if (messageText === '') return;

        addMessageToChat('user', messageText);
        userInput.value = '';

        // Simulate AI typing indicator
        addMessageToChat('ai', '...', true);
        setTimeout(() => {
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: messageText })
            })
            .then(response => response.json())
            .then(data => {
                updateAIResponse(data.response);
            });
        }, 1000);
    }

    function addMessageToChat(sender, text, isTyping = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        if (isTyping) {
            messageDiv.classList.add('typing-indicator');
            messageDiv.textContent = text;
        } else {
            messageDiv.textContent = text;
        }
        messageContainer.appendChild(messageDiv);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    function updateAIResponse(text) {
        const typingMessage = document.querySelector('.message.ai.typing-indicator');
        if (typingMessage) {
            typingMessage.textContent = text;
            typingMessage.classList.remove('typing-indicator');
        } else {
            addMessageToChat('ai', text);
        }

        if (text.includes("How can I assist you")) {
            showSuggestions();
        }
    }

    function showSuggestions() {
        fetch('/suggestions')
            .then(response => response.json())
            .then(data => {
                const suggestions = data.suggestions;
                suggestions.forEach(suggestion => {
                    addMessageToChat('ai', suggestion);
                });
            });
    }
});
