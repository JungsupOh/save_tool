let isComposing = false;

function openChatbot() {
    document.getElementById('chatbotModal').style.display = 'block';
}

function closeChatbot() {
    document.getElementById('chatbotModal').style.display = 'none';
    document.getElementById('chat-body').innerHTML = ''; // Clear chat history
}

function closeModal(event) {
    if (event.target === document.getElementById('chatbotModal')) {
        closeChatbot();
    }
}

function sendMessage() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();
    if (message && !isComposing) {
        var chatBody = document.getElementById('chat-body');
        var userMessageDiv = document.createElement('div');
        userMessageDiv.textContent = message;
        userMessageDiv.className = 'user-message';
        chatBody.appendChild(userMessageDiv);

        // Clear input field
        input.value = '';
        chatBody.scrollTop = chatBody.scrollHeight; // Scroll to the bottom

        // Send the message to the backend API
        fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                var botMessageDiv = document.createElement('div');
                botMessageDiv.textContent = data.response;
                botMessageDiv.className = 'bot-message';
                chatBody.appendChild(botMessageDiv);
                chatBody.scrollTop = chatBody.scrollHeight; // Scroll to the bottom
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add event listener for Enter key
document.getElementById('chat-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !isComposing) {
        event.preventDefault();  // Prevent the default action (form submission)
        sendMessage();
    }
});

// Handle composition events
document.getElementById('chat-input').addEventListener('compositionstart', function() {
    isComposing = true;
});

document.getElementById('chat-input').addEventListener('compositionend', function() {
    isComposing = false;
});
