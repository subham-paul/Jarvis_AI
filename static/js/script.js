// Jarvis AI Website JavaScript with Real API Integration

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(10, 10, 10, 0.98)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
        }
    });

    // Jarvis Demo Console Functionality
    const commandInput = document.getElementById('commandInput');
    const sendCommand = document.getElementById('sendCommand');
    const commandHistory = document.getElementById('commandHistory');
    const quickButtons = document.querySelectorAll('.quick-buttons button');
    const voiceButton = document.getElementById('voiceButton');
    
    let isListening = false;

    if (commandInput && sendCommand) {
        // Send command on button click
        sendCommand.addEventListener('click', processCommand);

        // Send command on Enter key
        commandInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                processCommand();
            }
        });

        // Quick command buttons
        quickButtons.forEach(button => {
            button.addEventListener('click', function() {
                const command = this.getAttribute('data-command');
                addMessage('You', command);
                sendCommandToJarvis(command);
                commandInput.value = '';
            });
        });
    }

    // Voice button functionality
    if (voiceButton) {
        voiceButton.addEventListener('click', toggleVoiceListening);
    }

    function processCommand() {
        const command = commandInput.value.trim();
        if (command) {
            addMessage('You', command);
            sendCommandToJarvis(command);
            commandInput.value = '';
        }
    }

    function addMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender.toLowerCase()}-message`;
        
        const timestamp = new Date().toLocaleTimeString();
        messageDiv.innerHTML = `<span class="timestamp">[${timestamp}]</span> <strong>${sender}:</strong> ${message}`;
        
        commandHistory.appendChild(messageDiv);
        commandHistory.scrollTop = commandHistory.scrollHeight;
    }

    // Real API integration with Jarvis AI
    async function sendCommandToJarvis(command) {
        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message jarvis-message typing';
        typingIndicator.innerHTML = '<strong>Jarvis:</strong> <span class="typing-dots">...</span>';
        commandHistory.appendChild(typingIndicator);
        commandHistory.scrollTop = commandHistory.scrollHeight;

        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });

            // Remove typing indicator
            typingIndicator.remove();

            const data = await response.json();
            
            if (data.success) {
                addMessage('Jarvis', data.response);
                
                // Update music display if it's a music command
                if (command.toLowerCase().includes('play')) {
                    updateMusicDisplay(command);
                }
                
                // Speak the response if it's not too long
                if (data.response.length < 100) {
                    speakResponse(data.response);
                }
            } else {
                addMessage('Jarvis', `Error: ${data.error}`);
            }
        } catch (error) {
            // Remove typing indicator
            typingIndicator.remove();
            
            console.error('API Error:', error);
            addMessage('Jarvis', 'Sorry, I encountered a connection error. Please make sure the Jarvis server is running.');
            
            // Fallback to simulated response
            simulateJarvisResponse(command);
        }
    }

    // Fallback simulated responses (if API is not available)
    function simulateJarvisResponse(command) {
        let response = '';
        const lowerCommand = command.toLowerCase();

        // Simulate Jarvis responses based on command
        if (lowerCommand.includes('play') && (lowerCommand.includes('music') || lowerCommand.includes('song'))) {
            const song = command.replace('play', '').replace('music', '').replace('song', '').trim();
            response = `I would play "${song}" from YouTube, but the voice system is not connected. Run "python main.py --gui" for full functionality. 🎵`;
        } else if (lowerCommand.includes('time')) {
            const time = new Date().toLocaleTimeString();
            response = `The current time is ${time}`;
        } else if (lowerCommand.includes('weather')) {
            response = `I would get weather information, but the API is not connected. Run the full Jarvis system for real weather data. ☀️`;
        } else if (lowerCommand.includes('joke')) {
            const jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!",
                "Why did the math book look so sad? Because it had too many problems!"
            ];
            response = jokes[Math.floor(Math.random() * jokes.length)];
        } else if (lowerCommand.includes('calculate')) {
            const expression = command.replace('calculate', '').trim();
            try {
                const result = eval(expression);
                response = `The answer is ${result}`;
            } catch (e) {
                response = "I couldn't calculate that. Please check your expression.";
            }
        } else if (lowerCommand.includes('news')) {
            response = "I would fetch latest news, but the news API is not connected in web mode.";
        } else if (lowerCommand.includes('system') || lowerCommand.includes('info')) {
            response = "System Information: This is web demo mode. Run the desktop app for detailed system info.";
        } else if (lowerCommand.includes('hello') || lowerCommand.includes('hi')) {
            response = "Hello! I'm Jarvis. For full voice functionality, please run the desktop application with: python main.py --gui";
        } else {
            response = "I understand you said: '" + command + "'. For full functionality with voice control, please run the desktop application.";
        }

        // Simulate typing delay
        setTimeout(() => {
            addMessage('Jarvis', response);
        }, 1000);
    }

    // Voice control functions
    function toggleVoiceListening() {
        if (!isListening) {
            startVoiceListening();
        } else {
            stopVoiceListening();
        }
    }

    async function startVoiceListening() {
        if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
            addMessage('Jarvis', 'Your browser does not support speech recognition. Please use Chrome or Edge.');
            return;
        }

        try {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = function() {
                isListening = true;
                voiceButton.innerHTML = '🔴 Stop Listening';
                voiceButton.classList.add('listening');
                addMessage('System', 'Voice listening activated... Speak now');
            };

            recognition.onresult = function(event) {
                const command = event.results[0][0].transcript;
                addMessage('You', command);
                sendCommandToJarvis(command);
            };

            recognition.onerror = function(event) {
                addMessage('System', 'Voice recognition error: ' + event.error);
                stopVoiceListening();
            };

            recognition.onend = function() {
                stopVoiceListening();
            };

            recognition.start();
        } catch (error) {
            addMessage('Jarvis', 'Voice recognition failed: ' + error.message);
        }
    }

    function stopVoiceListening() {
        isListening = false;
        voiceButton.innerHTML = '🎤 Start Voice';
        voiceButton.classList.remove('listening');
        addMessage('System', 'Voice listening stopped');
    }

    // Text-to-speech function
    function speakResponse(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            utterance.volume = 0.7;
            window.speechSynthesis.speak(utterance);
        }
    }

    // Update music display
    function updateMusicDisplay(command) {
        const songName = command.replace('play', '').replace('music', '').replace('song', '').trim();
        const tuneLabel = document.querySelector('.tune-label');
        if (tuneLabel) {
            tuneLabel.textContent = `🎵 Now Playing: ${songName}`;
            tuneLabel.style.color = '#00ffcc';
        }
    }

    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            
            // Simulate form submission
            alert(`Thank you, ${name}! Your message has been sent successfully. We'll get back to you at ${email} soon.`);
            this.reset();
        });
    }

    // Animation on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .team-card, .stat-item');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
            }
        });
    };

    // Set initial styles for animated elements
    document.querySelectorAll('.feature-card, .team-card, .stat-item').forEach(element => {
        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";
        element.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    });

    // Run animation on load and scroll
    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);

    // Add welcome message
    setTimeout(() => {
        addMessage('Jarvis', 'Welcome! I am Jarvis AI. You can type commands or use voice. For full functionality with music playback and voice control, run the desktop application with: python main.py --gui');
    }, 1000);
});

// Add CSS for typing animation
const style = document.createElement('style');
style.textContent = `
    .typing-dots::after {
        content: '';
        animation: typing 1.5s infinite;
    }
    
    @keyframes typing {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60%, 100% { content: '...'; }
    }
    
    .timestamp {
        color: #666;
        font-size: 0.8em;
        margin-right: 5px;
    }
    
    .listening {
        background-color: #ff4444 !important;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .you-message {
        color: #66aaff;
        margin: 10px 0;
        text-align: right;
    }
    
    .jarvis-message {
        color: #00ff99;
        margin: 10px 0;
        text-align: left;
    }
    
    .system-message {
        color: #ff6600;
        margin: 10px 0;
        text-align: center;
        font-style: italic;
    }
`;
document.head.appendChild(style);