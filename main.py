import os
import sys

# Ensure the current directory is in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import
from engine.command import CommandProcessor

class Jarvis:
    def __init__(self):
        self.command_processor = CommandProcessor()
        print("Jarvis AI initialized. Ready for commands!")
    
    def run(self):
        """Run in console mode (original functionality)"""
        print("Welcome to Jarvis AI!")
        print("🎤 I'm always listening! Just speak to me.")
        print("Or type commands if you prefer text.")
        print("Type 'exit' to quit.\n")
        
        # Show voice status
        self.show_voice_status()
        
        # Start with voice mode automatically
        self.continuous_voice_mode()
    
    def run_gui(self):
        """Run with modern GUI interface"""
        try:
            # Try to import and run the GUI
            try:
                from jarvis_gui import JarvisGUI
                gui = JarvisGUI(self)
                print("🚀 Starting JARVIS GUI...")
                gui.run()
            except ImportError as e:
                print(f"❌ GUI import error: {e}")
                print("📟 Falling back to console mode...")
                self.run()
        except Exception as e:
            print(f"❌ GUI Error: {e}")
            print("📟 Falling back to console mode...")
            self.run()
    
    def show_voice_status(self):
        """Show current voice capabilities"""
        print("🔊 VOICE STATUS:")
        if self.command_processor.features.recognizer:
            print("   ✅ Voice Input: ENABLED")
        else:
            print("   ❌ Voice Input: DISABLED")
            
        if (self.command_processor.features.tts_engine or 
            self.command_processor.features.gtts_available):
            print("   ✅ Voice Output: ENABLED")
        else:
            print("   ❌ Voice Output: DISABLED")
        print("=" * 50)
    
    def continuous_voice_mode(self):
        """Always listening voice mode"""
        print("🎤 ALWAYS LISTENING MODE")
        print("Just speak your commands naturally...")
        print("Say 'sleep' to pause listening, 'wake up' to resume")
        print("=" * 50)
        
        # Start with a greeting
        self.command_processor.features.speak("Hello! I am Jarvis. I'm ready to assist you!")
        
        listening = True
        command_count = 0
        
        while True:
            try:
                if listening:
                    print("\n🎤 Listening...", end=" ", flush=True)
                    
                    # Listen for voice command
                    command = self.command_processor.features.listen()
                    
                    if command:
                        command_count += 1
                        print(f"\n👤 You said: {command}")
                        
                        # Check for special commands
                        if any(word in command for word in ['sleep', 'stop listening', 'be quiet']):
                            self.command_processor.features.speak("Going to sleep. Say wake up when you need me.")
                            print("😴 Going to sleep... Say 'wake up' to resume")
                            listening = False
                            continue
                            
                        elif any(word in command for word in ['exit', 'quit', 'goodbye']):
                            self.command_processor.features.speak(f"Goodbye! Processed {command_count} commands.")
                            print(f"\nGoodbye! Processed {command_count} commands.")
                            break
                        
                        elif any(word in command for word in ['text mode', 'type', 'keyboard']):
                            print("📝 Switching to text mode...")
                            self.text_mode()
                            continue
                        
                        elif any(word in command for word in ['gui', 'interface', 'window']):
                            print("🖥️ Switching to GUI mode...")
                            self.run_gui()
                            return
                        
                        # Process the voice command and get response
                        response = self.command_processor.process_command(command)
                        
                        # Print and speak the response
                        print(f"🤖 Jarvis: {response}")
                        self.command_processor.features.speak(response)
                    
                    else:
                        # Show we're still listening
                        if command_count == 0:
                            print("💡 Say something like 'what time is it' or 'hello'")
                
                else:
                    # Sleep mode - wait for wake up command
                    print("\n💤 Sleeping...", end=" ", flush=True)
                    command = self.command_processor.features.listen()
                    
                    if command and any(word in command for word in ['wake up', 'hello jarvis', 'start listening']):
                        self.command_processor.features.speak("I'm back online! How can I help you?")
                        print("✅ Waking up! I'm listening again...")
                        listening = True
                        command_count = 0  # Reset counter
                    
            except KeyboardInterrupt:
                self.command_processor.features.speak("Goodbye!")
                print(f"\n\nGoodbye! Processed {command_count} commands.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("🔄 Continuing...")
    
    def text_mode(self):
        """Fallback text input mode"""
        print("\n" + "=" * 50)
        print("📝 TEXT MODE ACTIVATED")
        print("Type your commands (or 'voice' to switch back to voice mode)")
        print("Type 'gui' to switch to graphical interface")
        print("=" * 50)
        
        command_count = 0
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip().lower()
                
                if not user_input:
                    continue
                    
                command_count += 1
                
                if user_input in ['voice', 'speak', 'listen']:
                    print("🎤 Switching back to voice mode...")
                    self.command_processor.features.speak("Returning to voice mode.")
                    return
                    
                elif user_input in ['gui', 'interface', 'window']:
                    print("🖥️ Switching to GUI mode...")
                    self.run_gui()
                    return
                    
                elif user_input in ['exit', 'quit', 'goodbye']:
                    self.command_processor.features.speak(f"Goodbye! Processed {command_count} commands.")
                    print(f"Goodbye! Processed {command_count} commands.")
                    sys.exit(0)
                
                # Process the text command
                response = self.command_processor.process_command(user_input)
                
                # Print and speak the response
                print(f"🤖 Jarvis: {response}")
                self.command_processor.features.speak(response)
                
            except KeyboardInterrupt:
                self.command_processor.features.speak("Goodbye!")
                print(f"\nGoodbye! Processed {command_count} commands.")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
    
    def start_conversation(self):
        """Alternative method to start a direct conversation"""
        print("🤖 Starting Jarvis Conversation Mode...")
        self.command_processor.features.start_conversation()

if __name__ == "__main__":
    jarvis = Jarvis()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--text':
            jarvis.text_mode()
        elif sys.argv[1] == '--conversation':
            jarvis.start_conversation()
        elif sys.argv[1] == '--gui':
            jarvis.run_gui()
        elif sys.argv[1] == '--console':
            jarvis.run()
        else:
            print("Usage: python main.py [--gui | --console | --text | --conversation]")
            print("Default: --gui")
            jarvis.run_gui()
    else:
        # Default: Run with GUI
        jarvis.run_gui()