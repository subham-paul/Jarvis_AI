from flask import Flask, render_template, request, jsonify
import threading
import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Global variables for Jarvis
jarvis_instance = None
command_processor = None

def initialize_jarvis():
    global jarvis_instance, command_processor
    try:
        from main import Jarvis
        jarvis_instance = Jarvis()
        command_processor = jarvis_instance.command_processor
        print("✅ Jarvis AI engine loaded successfully!")
        return True
    except ImportError as e:
        print(f"❌ Jarvis engine import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Jarvis initialization error: {e}")
        return False

# Initialize Jarvis when the app starts
jarvis_available = initialize_jarvis()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/jarvis')
def jarvis():
    return render_template('jarvis.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/status')
def api_status():
    return jsonify({
        'jarvis_available': jarvis_available,
        'status': 'online' if jarvis_available else 'offline'
    })

@app.route('/api/command', methods=['POST'])
def api_command():
    if not jarvis_available:
        return jsonify({
            'success': False,
            'error': 'Jarvis engine not available. Please run the desktop app for full functionality: python main.py --gui'
        })
    
    data = request.json
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        print(f"Processing command: {command}")
        response = command_processor.process_command(command)
        print(f"Response: {response}")
        return jsonify({
            'success': True,
            'command': command,
            'response': response
        })
    except Exception as e:
        print(f"Command processing error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/start', methods=['POST'])
def start_voice_listening():
    if not jarvis_available:
        return jsonify({
            'success': False,
            'error': 'Voice system not available in web mode'
        })
    
    def listen_in_thread():
        try:
            print("Starting voice listening...")
            command = command_processor.features.listen()
            if command:
                print(f"Voice command received: {command}")
                # Process the command
                response = command_processor.process_command(command)
                print(f"Voice response: {response}")
                # Here you could implement WebSocket to send back to client
        except Exception as e:
            print(f"Voice listening error: {e}")
    
    thread = threading.Thread(target=listen_in_thread)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True, 
        'message': 'Voice listening started (check console for output)'
    })

if __name__ == '__main__':
    print("🚀 Starting Jarvis AI Web Interface...")
    print("📍 Web Server: http://localhost:5000")
    print("💡 For full voice functionality, run: python main.py --gui")
    print("🔊 Voice in web mode may have limitations")
    app.run(debug=True, port=5000, use_reloader=False)