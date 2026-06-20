import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.features import Features

def test_voice():
    print("Testing Jarvis voice...")
    features = Features()
    
    # Test if voice speaks
    print("Jarvis should speak now...")
    features.speak("Hello! I am Jarvis. Can you hear me?")
    print("If you didn't hear anything, check your speakers and volume.")

if __name__ == "__main__":
    test_voice()