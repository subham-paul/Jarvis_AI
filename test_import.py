import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Current directory:", os.getcwd())
print("Files in engine folder:", os.listdir('engine'))

try:
    from engine.features import Features
    print("SUCCESS: Features imported!")
except ImportError as e:
    print("ERROR:", e)

try:
    from engine.command import CommandProcessor
    print("SUCCESS: CommandProcessor imported!")
except ImportError as e:
    print("ERROR:", e)