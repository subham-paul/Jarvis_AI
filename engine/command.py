# Use relative imports
from .features import Features
from .db import Database

class CommandProcessor:
    def __init__(self):
        self.features = Features()
        self.db = Database()
    
    def process_command(self, command):
        """Process and execute commands"""
        if not command:
            return "I didn't receive any command."
        
        command = command.lower().strip()
        print(f"Processing: {command}")
        
        # ===== MUSIC COMMANDS (ADDED AT TOP FOR PRIORITY) =====
        if any(word in command for word in ['play', 'song', 'music', 'gaana']):
            if 'stop' in command or 'pause' in command or 'band' in command:
                return self.features.stop_music()
            elif 'status' in command:
                return self.features.get_music_status()
            elif 'list' in command:
                return self.features.list_available_songs()
            else:
                # Extract song name from play command
                song_name = command
                play_words = ['play', 'song', 'music', 'gaana', 'chalao', 'sunao']
                for word in play_words:
                    song_name = song_name.replace(word, '')
                
                # Remove extra words
                extra_words = ['please', 'jarvis', 'can you', 'could you', 'would you', 'the']
                for word in extra_words:
                    song_name = song_name.replace(word, '')
                
                song_name = song_name.strip()
                
                if song_name:
                    return self.features.play_youtube_song(song_name)
                else:
                    return "Please specify which song you want to play."
        
        # Stop music commands
        elif any(word in command for word in ['stop music', 'stop song', 'band karo', 'music stop']):
            return self.features.stop_music()
        
        # Music status
        elif any(word in command for word in ['music status', 'song status', 'what is playing']):
            return self.features.get_music_status()
        
        # List songs
        elif any(word in command for word in ['list songs', 'available songs', 'what songs can you play']):
            return self.features.list_available_songs()
        
        # ===== TIME COMMANDS =====
        elif any(word in command for word in ['time', 'what time']):
            return self.features.get_time()
        
        # ===== DATE COMMANDS =====
        elif any(word in command for word in ['date', 'what date', 'today']):
            return self.features.get_date()
        
        # ===== WEATHER COMMANDS =====
        elif 'weather' in command:
            import re
            
            # Remove common phrases to isolate location
            clean_command = command
            
            # Remove common question patterns but keep the location
            patterns_to_remove = [
                r'what is the weather',
                r'what\'s the weather', 
                r'tell me the weather',
                r'please tell me weather',
                r'how is the weather',
                r'weather forecast',
                r'weather like',
                r'what is',
                r'what\'s',
                r'tell me',
                r'please'
            ]
            
            for pattern in patterns_to_remove:
                clean_command = re.sub(pattern, '', clean_command, flags=re.IGNORECASE)
            
            clean_command = clean_command.strip()
            
            # Extract location using multiple patterns - ANY location name
            location = None
            
            patterns = [
                r'weather in (.+?)(?:\?|$)',      # "weather in kalimpong"
                r'weather at (.+?)(?:\?|$)',      # "weather at darjeeling"  
                r'(.+?) weather',                 # "kalimpong weather"
                r'in (.+?)(?:\?|$)',              # "in darjeeling"
                r'at (.+?)(?:\?|$)',              # "at kalimpong"
                r'for (.+?)(?:\?|$)',             # "weather for siliguri"
                r'^(.+?)$'                        # just the location name
            ]
            
            for pattern in patterns:
                match = re.search(pattern, clean_command, re.IGNORECASE)
                if match:
                    potential_location = match.group(1).strip()
                    # Basic validation - location should not be empty or common words
                    if (potential_location and 
                        len(potential_location) > 2 and 
                        potential_location.lower() not in ['the', 'a', 'an', 'my', 'our', 'is', 'how']):
                        location = potential_location
                        break
            
            # If no location found with patterns, try simple extraction
            if not location:
                # Remove "weather" and whatever remains is the location
                simple_location = clean_command.replace('weather', '').strip()
                if simple_location and len(simple_location) > 2:
                    location = simple_location
            
            print(f"DEBUG: Command: '{command}'")
            print(f"DEBUG: Cleaned: '{clean_command}'") 
            print(f"DEBUG: Extracted location: '{location}'")
            
            return self.features.get_weather(location)
        
        # ===== INTRODUCTION COMMANDS =====
        
        # Name commands
        elif any(word in command for word in ['what is your name', 'your name', 'who are you']):
            return self.features.get_name()
        
        # Introduction commands
        elif any(word in command for word in ['introduce yourself', 'introduction', 'about you']):
            return self.features.introduce()
        
        # Creator commands
        elif any(word in command for word in ['who created you', 'your creator', 'made you']):
            return self.features.get_creator()
        
        # Capabilities commands
        elif any(word in command for word in ['what can you do', 'capabilities', 'help', 'features']):
            return self.features.get_capabilities()
        
        # ===== CALCULATION COMMANDS =====
        elif any(word in command for word in ['calculate', 'compute']):
            if 'calculate' in command:
                expr = command.replace('calculate', '').strip()
            elif 'compute' in command:
                expr = command.replace('compute', '').strip()
            else:
                expr = command
            
            expr = expr.replace('?', '').strip()
            if expr:
                return self.features.calculate(expr)
            else:
                return "Please provide a calculation expression."
        
        # "What is" commands for calculations (SPECIFIC PATTERN)
        elif command.startswith('what is ') and any(op in command for op in ['+', '-', '*', '/', 'x']):
            expr = command.replace('what is', '').replace('?', '').strip()
            if expr:
                return self.features.calculate(expr)
            else:
                return "Please provide a calculation expression."
        
        # ===== SEARCH COMMANDS =====
        elif any(word in command for word in ['search', 'look up', 'find']):
            query = command
            for word in ['search', 'look up', 'find']:
                query = query.replace(word, '')
            query = query.strip()
            if query:
                return self.features.search_web(query)
            else:
                return "Please provide a search query."
        
        # ===== NEWS COMMANDS =====
        elif any(word in command for word in ['news', 'headlines']):
            return self.features.get_news()
        
        # ===== JOKE COMMANDS =====
        elif any(word in command for word in ['joke', 'tell me a joke']):
            return self.features.tell_joke()
        
        # ===== SYSTEM INFO COMMANDS =====
        elif any(word in command for word in ['system info', 'system information']):
            return self.features.get_system_info()
        
        # ===== REMINDER COMMANDS =====
        elif 'remind' in command or 'reminder' in command:
            import re
            match = re.search(r'remind me to (.+) in (\d+) minutes?', command)
            if match:
                reminder_text = match.group(1).strip()
                minutes = match.group(2)
                return self.features.set_reminder(reminder_text, int(minutes))
            
            match = re.search(r'set reminder (.+) in (\d+) minutes?', command)
            if match:
                reminder_text = match.group(1).strip()
                minutes = match.group(2)
                return self.features.set_reminder(reminder_text, int(minutes))
            
            return "Please use format: 'remind me to [task] in [number] minutes'"
        
        # ===== GREETING COMMANDS =====
        elif any(word in command for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I assist you today?"
        
        elif any(word in command for word in ['thank you', 'thanks']):
            return "You're welcome!"
        
        elif any(word in command for word in ['goodbye', 'bye', 'exit']):
            return "Goodbye! Have a great day!"
        
        # ===== DEFAULT RESPONSE =====
        else:
            response = "I'm not sure how to help with that. Try: 'play music', 'time', 'weather', 'news', 'calculations', or ask 'what can you do?'"
            self.db.log_command(command, response)
            return response