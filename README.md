# 🤖 Jarvis AI

A powerful **AI Virtual Assistant** built with **Python** and **Flask** that interacts with users through **voice commands** and **text-to-speech technology**. Inspired by the iconic J.A.R.V.I.S. assistant, this project automates daily tasks, answers user queries, opens applications and websites, retrieves real-time information, and provides an intelligent voice-controlled experience.

> **Your personal AI assistant—ready to listen, understand, and respond.**

---

# ✨ Features

- 🎙️ Voice command recognition
- 🗣️ Natural text-to-speech responses
- 🤖 AI-powered virtual assistant
- 🌐 Open websites using voice commands
- 📱 Launch desktop applications
- 🔍 Search the web instantly
- 🌦️ Weather information retrieval
- 📰 Latest news updates
- ⏰ Date and time announcements
- 💻 System information monitoring
- 🎵 Play music
- 📊 CPU & Memory usage monitoring
- 🌐 Flask-based web interface
- ⚡ Fast and responsive interaction

---

# 🛠️ Tech Stack

## Backend

- Python 3.x
- Flask

## Artificial Intelligence

- Speech Recognition
- Text-to-Speech (TTS)
- Voice Processing

## Libraries Used

| Library | Purpose |
|----------|---------|
| **pyttsx3** | Offline Text-to-Speech Engine |
| **SpeechRecognition** | Voice Command Recognition |
| **requests** | API & HTTP Requests |
| **psutil** | System Information Monitoring |
| **Flask** | Web Framework |
| **pygame** | Audio Playback |
| **gTTS** | Google Text-to-Speech |

---

# 📂 Project Structure

```text
Jarvis_AI/
│
├── app.py
├── jarvis.py
├── requirements.txt
├── config.py
│
├── static/
│   ├── css/
│   ├── js/
│   ├── audio/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── assistant.html
│   └── ...
│
├── utils/
│   ├── speech.py
│   ├── commands.py
│   ├── system.py
│   └── ...
│
├── README.md
│
└── ...
```

---

# 🚀 Features Overview

- 🎤 Voice Recognition
- 🗣️ AI Voice Responses
- 🌐 Web Search
- 📱 Application Launcher
- ⏰ Time & Date
- 🌦️ Weather Updates
- 📰 News Headlines
- 🎵 Music Playback
- 📊 System Monitoring
- 💻 Browser-Based Interface

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/subham-paul/Jarvis_AI.git
```

```bash
cd Jarvis_AI
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables *(Optional)*

Create a `.env` file if your project requires API keys.

```env
WEATHER_API_KEY=your_api_key
NEWS_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

---

## 5. Run the Application

```bash
python app.py
```

or

```bash
flask run
```

---

# 🌐 Open in Browser

```
http://127.0.0.1:5000
```

---

# 🎙️ Voice Commands (Examples)

| Command | Action |
|----------|--------|
| "Open Google" | Opens Google in your browser |
| "Open YouTube" | Opens YouTube |
| "What's the weather?" | Fetches current weather |
| "Tell me the time" | Announces current time |
| "Play music" | Plays available music |
| "Search Python" | Performs a web search |
| "CPU usage" | Displays CPU usage |
| "System status" | Shows system information |
| "Open Calculator" | Launches Calculator |
| "Exit Jarvis" | Closes the assistant |

---

# ⚙️ How It Works

1. User gives a voice command.
2. **SpeechRecognition** converts speech into text.
3. The command is analyzed and matched with predefined actions.
4. Required APIs or local system functions are executed.
5. **pyttsx3** or **gTTS** converts the response into speech.
6. Flask displays responses through the web interface while the assistant speaks them aloud.

---

# 📊 Applications

- Personal Voice Assistant
- Smart Home Automation
- Productivity Assistant
- Educational AI Projects
- Desktop Automation
- Voice-Controlled Systems
- AI Demonstrations
- Accessibility Solutions

---

# 🚀 Future Enhancements

- 🤖 ChatGPT / LLM Integration
- 🧠 Context-Aware Conversations
- 🌍 Multi-language Support
- 👤 Voice Authentication
- 📧 Email Automation
- 📅 Calendar Integration
- 📱 WhatsApp & Telegram Integration
- 🎥 Face Recognition
- ☁️ Cloud Synchronization
- 📱 Mobile Application Support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork this repository.

2. Create a feature branch.

```bash
git checkout -b feature/NewFeature
```

3. Commit your changes.

```bash
git commit -m "Add New Feature"
```

4. Push your changes.

```bash
git push origin feature/NewFeature
```

5. Open a Pull Request.

---

# 🐞 Reporting Issues

Found a bug or have a feature request?

Please create an issue with a detailed explanation.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## **Subham Paul**

Passionate about **Artificial Intelligence, Python, Voice Assistants, Automation, Machine Learning, and Web Development.**

- GitHub: https://github.com/subham-paul
- LinkedIn: https://www.linkedin.com/in/subham-paul-india/

---

# ⭐ Show Your Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork the project
- 🤝 Contribute
- 💬 Share your feedback


---

## 🙏 Acknowledgements

Special thanks to the open-source communities behind:

- Python
- Flask
- SpeechRecognition
- pyttsx3
- gTTS
- pygame
- psutil
- requests

for providing the technologies that made this AI assistant possible.

---

> **"Your intelligent voice assistant—designed to simplify everyday tasks with the power of Artificial Intelligence."** 🤖🎙️
