from flask import Flask, render_template, request, jsonify
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from engine.command import CommandProcessor
    jarvis_available = True
    command_processor = CommandProcessor()
except ImportError as e:
    print(f"Jarvis engine not available: {e}")
    jarvis_available = False
    command_processor = None

app = Flask(__name__)

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

# API endpoint for commands
@app.route('/api/command', methods=['POST'])
def api_command():
    if not jarvis_available:
        return jsonify({
            'success': False,
            'error': 'Jarvis engine not available'
        })
    
    data = request.json
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        response = command_processor.process_command(command)
        return jsonify({
            'success': True,
            'command': command,
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)