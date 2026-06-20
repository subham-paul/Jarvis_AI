import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    
    print("Testing microphone...")
    print("Available microphones:")
    
    try:
        # List all microphones
        mics = sr.Microphone.list_microphone_names()
        for i, mic in enumerate(mics):
            print(f"{i}: {mic}")
        
        # Test default microphone
        with sr.Microphone() as source:
            print(f"\nUsing default microphone: {mics[0] if mics else 'Unknown'}")
            print("Calibrating for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("Speak now... (say 'hello test')")
            audio = recognizer.listen(source, timeout=10)
            
            print("Processing...")
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                print("✅ Microphone is working!")
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError as e:
                print(f"❌ Error with speech recognition: {e}")
                
    except Exception as e:
        print(f"❌ Microphone error: {e}")

if __name__ == "__main__":
    test_microphone()