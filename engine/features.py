import requests
import json
import random
import platform
import psutil
from datetime import datetime, timedelta
import webbrowser
import sqlite3
import subprocess
import threading
import time

# Use relative imports
from .config import Config
from .db import Database

# Try to import voice-related libraries
try:
    import speech_recognition as sr
    VOICE_RECOGNITION_AVAILABLE = True
except ImportError:
    VOICE_RECOGNITION_AVAILABLE = False
    print("SpeechRecognition not available")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("pyttsx3 not available")

# Try to import gTTS for alternative voice
try:
    from gtts import gTTS
    import pygame
    import io
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("gTTS not available - install: pip install gtts pygame")

# Try to import YouTube related libraries
try:
    from yt_dlp import YoutubeDL
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    print("yt-dlp not available - install: pip install yt-dlp")

# Try to import Selenium for guaranteed autoplay
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Selenium not available - install: pip install selenium")

class Features:
    def __init__(self):
        self.db = Database()
        self.setup_voice()
        self.setup_speech_recognition()
        
        # Music playback variables
        self.current_song_process = None
        self.is_playing = False
        self.current_song_name = ""
        self.current_driver = None  # For Selenium browser control
        
        # Common songs database - ADD YOUR SONGS HERE
        self.song_database = {
            "ghar se nikalte hi": "https://youtu.be/f1qz8vn3XbY?si=3jqgeg4E0rI3iG3I",
            "tum hi ho": "https://youtu.be/Umqb9KENgmk?si=V73crrHbyZ-S0TzL",
            "see you again": "https://youtu.be/NDEWXnMRq3c?si=5jDEo0ADx1GbFBWs",
            "shape of you": "https://youtu.be/liTfD88dbCo?si=qgEjLpJW0t1Fhb4U",
            "despacito": "https://youtu.be/TfkP5ubz1z4?si=Y7Y6_VtjMKFuUohX",
            "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
            "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
            "let me love you": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "senorita": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "dilbar": "https://www.youtube.com/watch?v=G-s6D0fYD6E",
            "lut gaye": "https://www.youtube.com/watch?v=sC0dR4xR-2Y",
            "makhna": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "billi": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "tera ban jaunga": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "haal still": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            
            # ADD MORE SONGS HERE - COPY AND PASTE BELOW:
            "tera zikr": "https://www.youtube.com/watch?v=dLhJp6Hq5oM",
            "apna bana le": "https://www.youtube.com/watch?v=ZIC_BeCq_nM",
            "kesariya": "https://www.youtube.com/watch?v=k1hJoR4bAmI",
            "besharam rang": "https://www.youtube.com/watch?v=H5NqIsVtw8A",
            "chaleya": "https://www.youtube.com/watch?v=WgK8_IeRF_c",
            "arsh": "https://www.youtube.com/watch?v=WgK8_IeRF_c",
            "perfect": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
            "sohigh": "https://www.youtube.com/watch?v=1N_WuR1gx7A",
            "brown munde": "https://www.youtube.com/watch?v=VsgS9u_T1Iw",
            
            # ADD THESE POPULAR SONGS:
            "rang de basanti": "https://www.youtube.com/watch?v=0Z59-5sMbhU",
            "tum se hi": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "tujh mein rab dikhta hai": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "heeriye": "https://www.youtube.com/watch?v=VSX3SA2V1BQ",
            "satranga": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "zinda banda": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "naina da kya kasoor": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "lehanga": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "gulabi sadi": "https://www.youtube.com/watch?v=2B0RxuYQ7dE",
            "sakhiyan": "https://www.youtube.com/watch?v=2B0RxuYQ7dE"
            # ADD EVEN MORE SONGS HERE...
        }
    
    def setup_voice(self):
        """Initialize text-to-speech engine with multiple fallbacks"""
        self.tts_engine = None
        self.gtts_available = GTTS_AVAILABLE
        self.pygame_available = GTTS_AVAILABLE
        
        if Config.VOICE_ENABLED:
            # Try pyttsx3 first (if available)
            if TTS_AVAILABLE:
                try:
                    self.tts_engine = pyttsx3.init()
                    # Get available voices and set the best one
                    voices = self.tts_engine.getProperty('voices')
                    if voices:
                        self.tts_engine.setProperty('voice', voices[0].id)  # Use first available voice
                    self.tts_engine.setProperty('rate', Config.VOICE_RATE)
                    self.tts_engine.setProperty('volume', Config.VOICE_VOLUME)
                    print("🎯 Voice output enabled (pyttsx3)")
                    return
                except Exception as e:
                    print(f"pyttsx3 failed: {e}")
            
            # Try gTTS as fallback
            if self.gtts_available:
                try:
                    pygame.mixer.init()
                    print("🎯 Voice output enabled (gTTS)")
                except Exception as e:
                    print(f"gTTS setup warning: {e}")
            else:
                print("❌ Voice output disabled - no TTS engine available")
        else:
            print("🔇 Voice output disabled in config")
    
    def setup_speech_recognition(self):
        """Initialize speech recognition with better error handling"""
        self.recognizer = None
        self.microphone = None
        
        if Config.VOICE_ENABLED and VOICE_RECOGNITION_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Calibrate for ambient noise
                print("🔊 Calibrating microphone for ambient noise...")
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("🎤 Voice input enabled - You can speak to Jarvis!")
                
            except Exception as e:
                print(f"❌ Speech recognition setup failed: {e}")
                print("💡 You can still use text commands.")
                self.recognizer = None
                self.microphone = None
        else:
            if Config.VOICE_ENABLED:
                print("❌ Voice input disabled - install: pip install SpeechRecognition")
            else:
                print("🔇 Voice input disabled in config")
    
    def speak(self, text):
        """Convert text to speech with multiple fallbacks"""
        print(f"🤖 Jarvis: {text}")
        
        if not Config.VOICE_ENABLED:
            return
        
        # Try pyttsx3 first
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return
            except Exception as e:
                print(f"❌ pyttsx3 speech error: {e}")
                # Fall through to gTTS
        
        # Try gTTS as fallback
        if self.gtts_available:
            try:
                # Create speech using gTTS
                tts = gTTS(text=text, lang='en', slow=False)
                
                # Save to in-memory file
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                audio_file.seek(0)
                
                # Play using pygame
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                    
            except Exception as e:
                print(f"❌ gTTS speech error: {e}")
        else:
            print("🔇 No voice engine available - text only mode")
    
    def listen(self):
        """Listen for voice commands with better error handling"""
        if not self.recognizer or not Config.VOICE_ENABLED:
            print("🔇 Voice recognition not available. Using text input.")
            return None
        
        try:
            print("🎤 Listening... (Speak now)")
            with self.microphone as source:
                # Listen with longer timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=Config.SPEECH_TIMEOUT, 
                    phrase_time_limit=Config.SPEECH_PHRASE_LIMIT
                )
            
            print("🔄 Processing your speech...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected. Switching to text mode.")
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except Exception as e:
            print(f"❌ Listening error: {e}")
            print("📝 Switching to text input.")
            return None

    # ===== MUSIC PLAYBACK FUNCTIONALITY =====
    
    def play_youtube_song(self, song_name):
        """Play YouTube song - WORKING VERSION"""
        try:
            # Stop any currently playing song
            self.stop_music()
            
            # Find the song in database
            song_url = self.find_song_url(song_name)
            
            if not song_url:
                # If song not found, search on YouTube
                search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
                webbrowser.open(search_url)
                return f"🔍 Song '{song_name}' not in database. Opening YouTube search..."
            
            self.speak(f"Playing {song_name}")
            
            # SIMPLE & RELIABLE: Just open YouTube with the song
            print(f"🎵 Opening YouTube: {song_name}")
            print(f"🎵 URL: {song_url}")
            webbrowser.open(song_url)
            
            self.is_playing = True
            self.current_song_name = song_name
            
            return f"🎵 Now playing: {song_name} in YouTube"
            
        except Exception as e:
            print(f"❌ Error playing song: {e}")
            # Fallback: search and open in browser
            search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"🔍 Opening YouTube search for: {song_name}"

    def play_music_enhanced(self, song_name):
        """Enhanced music playback with browser detection"""
        try:
            self.stop_music()
            
            song_url = self.find_song_url(song_name)
            if not song_url:
                return f"Song '{song_name}' not found in database."
            
            self.speak(f"Playing {song_name}")
            
            # Extract video ID for better URL formats
            video_id = self.extract_video_id(song_url)
            
            if video_id:
                # Try multiple URL formats in sequence
                urls_to_try = [
                    f"https://www.youtube.com/watch?v={video_id}&autoplay=1",  # Standard autoplay
                    f"https://www.youtube.com/embed/{video_id}?autoplay=1",    # Embed with autoplay
                    f"https://www.youtube.com/v/{video_id}?autoplay=1",        # Alternative format
                    song_url,  # Original URL as fallback
                ]
                
                for url in urls_to_try:
                    try:
                        print(f"🎵 Trying URL: {url}")
                        success = webbrowser.open(url, new=1)
                        if success:
                            print(f"✅ Successfully opened: {url}")
                            break
                        time.sleep(1)
                    except Exception as e:
                        print(f"❌ Failed with URL: {url}, error: {e}")
                        continue
            else:
                # Fallback to simple method
                autoplay_url = song_url + "&autoplay=1"
                print(f"🎵 Using fallback URL: {autoplay_url}")
                webbrowser.open(autoplay_url)
            
            self.is_playing = True
            self.current_song_name = song_name
            
            return f"🎵 Now playing: {song_name} in your browser"
            
        except Exception as e:
            print(f"❌ Enhanced playback error: {e}")
            # Ultimate fallback
            song_url = self.find_song_url(song_name)
            if song_url:
                webbrowser.open(song_url)
            return f"🎵 Opening: {song_name}"

    def play_music_system(self, song_name):
        """Play music using system audio players - SIMPLE & EFFECTIVE"""
        try:
            self.stop_music()
            
            song_url = self.find_song_url(song_name)
            if not song_url:
                return f"Song '{song_name}' not found in database."
            
            self.speak(f"Playing {song_name}")
            
            # SIMPLE SOLUTION: Use system default browser with autoplay
            # This works reliably on all systems
            autoplay_url = song_url + "&autoplay=1"
            
            # Enhanced method: Try to start playing immediately
            system = platform.system().lower()
            
            if system == "windows":
                # Windows - use start command with default browser
                try:
                    subprocess.Popen(f'start "" "{autoplay_url}"', shell=True)
                except:
                    webbrowser.open(autoplay_url)
            
            elif system == "darwin":  # macOS
                # macOS - use open command
                try:
                    subprocess.Popen(['open', autoplay_url])
                except:
                    webbrowser.open(autoplay_url)
            
            elif system == "linux":
                # Linux - use xdg-open
                try:
                    subprocess.Popen(['xdg-open', autoplay_url])
                except:
                    webbrowser.open(autoplay_url)
            
            else:
                # Fallback for unknown systems
                webbrowser.open(autoplay_url)
            
            self.is_playing = True
            self.current_song_name = song_name
            
            return f"🎵 Now playing: {song_name}"
            
        except Exception as e:
            print(f"System music error: {e}")
            # Ultimate fallback
            song_url = self.find_song_url(song_name)
            if song_url:
                webbrowser.open(song_url)
            return f"🎵 Opening: {song_name}"

    def play_music_simple_python(self, song_name):
        """Simple Python-based music player using pygame"""
        try:
            self.stop_music()
            
            song_url = self.find_song_url(song_name)
            if not song_url:
                return f"Song '{song_name}' not found in database."
            
            self.speak(f"Playing {song_name}")
            
            def pygame_play():
                try:
                    # Download and convert YouTube audio
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'temp_audio.%(ext)s',
                        'quiet': True,
                    }
                    
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(song_url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        # Play with pygame
                        pygame.mixer.init()
                        pygame.mixer.music.load(filename)
                        pygame.mixer.music.play()
                        
                        self.is_playing = True
                        self.current_song_name = song_name
                        
                        # Wait for playback to finish
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                        
                        self.is_playing = False
                        
                        # Clean up temp file
                        try:
                            import os
                            os.remove(filename)
                        except:
                            pass
                            
                except Exception as e:
                    print(f"Python audio error: {e}")
                    # Fallback to browser
                    webbrowser.open(song_url + "&autoplay=1")
                    self.is_playing = True
                    self.current_song_name = song_name
            
            music_thread = threading.Thread(target=pygame_play)
            music_thread.daemon = True
            music_thread.start()
            
            return f"🎵 Now playing: {song_name}"
            
        except Exception as e:
            print(f"Python music error: {e}")
            return self.play_music_system(song_name)
    
    def play_youtube_selenium(self, song_name):
        """Play YouTube song using Selenium - GUARANTEED AUTOPLAY"""
        try:
            # Find the song in database
            song_url = self.find_song_url(song_name)
            
            if not song_url:
                return f"Song '{song_name}' not found in database."
            
            self.speak(f"Playing {song_name} using automated browser")
            
            # Set up Chrome options for autoplay
            chrome_options = Options()
            chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
            chrome_options.add_argument("--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            print("🚀 Starting Chrome browser for autoplay...")
            
            # Initialize driver
            self.current_driver = webdriver.Chrome(options=chrome_options)
            self.current_driver.get(song_url)
            
            # Wait for page to load and handle various scenarios
            try:
                # Wait for the page to load
                WebDriverWait(self.current_driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                print("✅ Video element found")
                
                # Try to click the play button if it exists
                try:
                    play_button = WebDriverWait(self.current_driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "ytp-play-button"))
                    )
                    play_button.click()
                    print("✅ Automatically clicked play button")
                except:
                    print("ℹ️ Play button not found or not clickable, video might auto-play")
                
                # Wait a bit for video to start
                time.sleep(3)
                
                # Check if video is playing
                video_element = self.current_driver.find_element(By.TAG_NAME, "video")
                is_playing = self.current_driver.execute_script("return arguments[0].currentTime > 0 && !arguments[0].paused", video_element)
                
                if is_playing:
                    print("✅ Video is successfully playing!")
                else:
                    print("⚠️ Video might not be playing automatically")
                    
            except Exception as e:
                print(f"⚠️ Could not auto-click play button: {e}")
                print("🎵 Video page loaded successfully")
            
            self.is_playing = True
            self.current_song_name = song_name
            
            return f"🎵 Now playing: {song_name} with guaranteed autoplay"
            
        except Exception as e:
            print(f"❌ Selenium error: {e}")
            # Fallback to enhanced browser method
            return self.play_youtube_enhanced(song_name)
    
    def play_youtube_enhanced(self, song_name):
        """Enhanced browser method with multiple autoplay attempts"""
        try:
            song_url = self.find_song_url(song_name)
            
            if not song_url:
                return f"Song '{song_name}' not found in database."
            
            video_id = self.extract_video_id(song_url)
            
            if video_id:
                # Try multiple URL formats for better autoplay
                urls_to_try = [
                    f"https://www.youtube.com/watch?v={video_id}&autoplay=1",  # Standard with autoplay
                    f"https://www.youtube.com/embed/{video_id}?autoplay=1",    # Embed with autoplay
                    f"https://www.youtube.com/v/{video_id}?autoplay=1",        # Alternative format
                    f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=0",  # Unmuted
                ]
                
                for url in urls_to_try:
                    try:
                        print(f"🎵 Trying URL: {url}")
                        webbrowser.open(url)
                        time.sleep(2)
                        break
                    except Exception as e:
                        print(f"❌ Failed with URL: {url}, error: {e}")
                        continue
            else:
                # Fallback to simple method
                autoplay_url = song_url + "&autoplay=1"
                print(f"🎵 Using fallback URL: {autoplay_url}")
                webbrowser.open(autoplay_url)
            
            self.is_playing = True
            self.current_song_name = song_name
            
            return f"🎵 Now playing: {song_name} in your browser"
            
        except Exception as e:
            print(f"❌ Enhanced playback error: {e}")
            # Ultimate fallback
            song_url = self.find_song_url(song_name)
            if song_url:
                webbrowser.open(song_url)
            return f"🎵 Opening: {song_name}"
    
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        try:
            if 'youtube.com/watch?v=' in url:
                return url.split('youtube.com/watch?v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                return url.split('youtu.be/')[1].split('?')[0]
            return None
        except:
            return None
    
    def play_youtube_song_advanced(self, song_name):
        """Advanced music playback with yt-dlp (optional)"""
        if not YT_DLP_AVAILABLE:
            return self.play_youtube_song(song_name)  # Fallback to simple method
            
        try:
            # Stop any currently playing song
            self.stop_music()
            
            # Find the song in database
            song_url = self.find_song_url(song_name)
            
            if not song_url:
                return f"Sorry, I couldn't find the song '{song_name}' in my database."
            
            self.speak(f"Playing {song_name} from YouTube")
            
            # Play in background thread to avoid blocking
            def play_song():
                try:
                    # Using yt-dlp to get best audio stream
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(song_url, download=False)
                        audio_url = info['url']
                        
                        # Try to play using available players
                        players = ['mpv', 'mplayer', 'vlc']
                        for player in players:
                            try:
                                self.current_song_process = subprocess.Popen([
                                    player, '--no-video', '--no-terminal', audio_url
                                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                
                                self.is_playing = True
                                self.current_song_name = song_name
                                
                                # Wait for process to complete
                                self.current_song_process.wait()
                                self.is_playing = False
                                break
                            except FileNotFoundError:
                                continue
                        else:
                            # If no player found, fallback to browser with autoplay
                            autoplay_url = song_url + "&autoplay=1"
                            webbrowser.open(autoplay_url)
                            self.is_playing = True
                            self.current_song_name = song_name
                        
                except Exception as e:
                    print(f"❌ Advanced music playback error: {e}")
                    # Fallback: open in browser with autoplay
                    autoplay_url = song_url + "&autoplay=1"
                    webbrowser.open(autoplay_url)
                    self.is_playing = True
                    self.current_song_name = song_name
            
            # Start playback in separate thread
            music_thread = threading.Thread(target=play_song)
            music_thread.daemon = True
            music_thread.start()
            
            return f"🎵 Now playing: {song_name}"
            
        except Exception as e:
            print(f"❌ Error in advanced playback: {e}")
            return self.play_youtube_song(song_name)  # Fallback to simple method
    
    def find_song_url(self, song_name):
        """Find YouTube URL for requested song"""
        song_name_lower = song_name.lower()
        
        # Exact match
        if song_name_lower in self.song_database:
            return self.song_database[song_name_lower]
        
        # Partial match
        for known_song, url in self.song_database.items():
            if known_song in song_name_lower or song_name_lower in known_song:
                return url
        
        # If not found in database, return None
        return None
    
    def stop_music(self):
        """Stop currently playing music"""
        # Stop pygame if active
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        
        # Stop Selenium browser if active
        if hasattr(self, 'current_driver') and self.current_driver:
            try:
                self.current_driver.quit()
                self.current_driver = None
                print("✅ Closed Selenium browser")
            except Exception as e:
                print(f"❌ Error closing Selenium browser: {e}")
    
        # Stop subprocess if active
        if self.is_playing and self.current_song_process:
            try:
                self.current_song_process.terminate()
                self.is_playing = False
                self.speak(f"Stopped {self.current_song_name}")
                self.current_song_name = ""
                return "⏹️ Music stopped"
            except Exception as e:
                print(f"❌ Error stopping music: {e}")
                return "❌ Error stopping music"
        elif self.is_playing:
            # If playing in browser, we can't stop it programmatically
            self.is_playing = False
            self.speak("Music stopped in browser")
            self.current_song_name = ""
            return "🎵 Music was playing in browser. I've stopped tracking it."
        else:
            return "❌ No music is currently playing"
    
    def pause_music(self):
        """Pause music (if supported)"""
        if self.is_playing:
            self.speak("Pause functionality is limited with YouTube playback. Say 'stop' to stop the music.")
            return "⏸️ For precise pause control, please use the YouTube player directly."
        return "❌ No music is currently playing"
    
    def get_music_status(self):
        """Get current music playback status"""
        if self.is_playing:
            return f"🎵 Currently playing: {self.current_song_name}"
        else:
            return "🔇 No music is currently playing"
    
    def add_song_to_database(self, song_name, youtube_url):
        """Add a new song to the database"""
        self.song_database[song_name.lower()] = youtube_url
        return f"✅ Added '{song_name}' to music database"
    
    def list_available_songs(self):
        """List all available songs in database"""
        if self.song_database:
            song_list = "\n".join([f"• {song.title()}" for song in self.song_database.keys()])
            return f"🎵 Available songs:\n{song_list}"
        else:
            return "❌ No songs in database"

    def start_conversation(self):
        """Start a voice conversation with Jarvis"""
        self.speak("Hello! I am Jarvis. How can I assist you today?")
        
        while True:
            try:
                # Listen for command
                command = self.listen()
                
                if command is None:
                    # Fall back to text input
                    command = input("Type your command (or 'quit' to exit): ").lower()
                
                if command in ['quit', 'exit', 'bye', 'goodbye']:
                    self.speak("Goodbye! Have a great day!")
                    break
                
                # Process the command
                response = self.process_command(command)
                self.speak(response)
                
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ Conversation error: {e}")
                self.speak("I encountered an error. Please try again.")
    
    def process_command(self, command):
        """Process voice or text commands and return responses"""
        command = command.lower()
        
        # Music commands
        if any(word in command for word in ['play', 'song', 'music', 'gaana']):
            if 'stop' in command or 'pause' in command or 'band' in command:
                return self.stop_music()
            elif 'status' in command:
                return self.get_music_status()
            elif 'list' in command:
                return self.list_available_songs()
            elif 'add' in command:
                # Extract song name and URL from command
                return "To add a song, use: add song [song name] with URL [youtube url]"
            else:
                # Extract song name
                song_name = self.extract_song_name(command)
                if song_name:
                    return self.play_music_enhanced(song_name)  # Use the enhanced version
                else:
                    return "Please specify which song you want to play."
        
        # Stop commands
        elif any(word in command for word in ['stop music', 'stop song', 'band karo', 'music stop']):
            return self.stop_music()
        
        # Time commands
        elif any(word in command for word in ['time', 'current time']):
            return self.get_time()
        
        # Date commands
        elif any(word in command for word in ['date', 'today', 'current date']):
            return self.get_date()
        
        # Weather commands
        elif 'weather' in command:
            location = self.extract_location(command)
            return self.get_weather(location)
        
        # Calculation commands
        elif any(word in command for word in ['calculate', 'math', 'what is']):
            expression = self.extract_calculation(command)
            return self.calculate(expression)
        
        # Search commands
        elif any(word in command for word in ['search', 'google']):
            query = self.extract_search_query(command)
            return self.search_web(query)
        
        # News commands
        elif any(word in command for word in ['news', 'headlines']):
            return self.get_news()
        
        # Joke commands
        elif any(word in command for word in ['joke', 'funny']):
            return self.tell_joke()
        
        # System info commands
        elif any(word in command for word in ['system', 'specs', 'hardware']):
            return self.get_system_info()
        
        # Introduction commands
        elif any(word in command for word in ['who are you', 'introduce', 'your name']):
            return self.introduce()
        
        elif any(word in command for word in ['what can you do', 'capabilities', 'help']):
            return self.get_capabilities()
        
        elif any(word in command for word in ['creator', 'who made you']):
            return self.get_creator()
        
        # Reminder commands
        elif 'reminder' in command:
            return self.handle_reminder(command)
        
        # Greetings
        elif any(word in command for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you today?"
        
        else:
            return "I'm not sure how to help with that. Try asking about time, weather, music, or say 'help' to see what I can do."
    
    def extract_song_name(self, command):
        """Extract song name from play command"""
        # Remove play-related words
        play_words = ['play', 'song', 'music', 'gaana', 'chalao', 'sunao']
        for word in play_words:
            command = command.replace(word, '')
        
        # Remove extra words
        extra_words = ['please', 'jarvis', 'can you', 'could you', 'would you', 'the']
        for word in extra_words:
            command = command.replace(word, '')
        
        return command.strip()
    
    def extract_location(self, command):
        """Extract location from weather command"""
        words = command.split()
        if 'in' in words:
            index = words.index('in')
            return ' '.join(words[index+1:])
        elif 'for' in words:
            index = words.index('for')
            return ' '.join(words[index+1:])
        return None
    
    def extract_calculation(self, command):
        """Extract calculation expression from command"""
        # Remove common phrases and get the math part
        phrases_to_remove = ['calculate', 'what is', 'math', 'compute']
        for phrase in phrases_to_remove:
            command = command.replace(phrase, '')
        return command.strip()
    
    def extract_search_query(self, command):
        """Extract search query from command"""
        phrases_to_remove = ['search for', 'search', 'google', 'look up']
        for phrase in phrases_to_remove:
            command = command.replace(phrase, '')
        return command.strip()
    
    def handle_reminder(self, command):
        """Handle reminder commands"""
        if 'set' in command:
            try:
                # Extract reminder text and time
                words = command.split()
                time_index = -1
                for i, word in enumerate(words):
                    if word in ['in', 'after'] and i+2 < len(words):
                        time_index = i
                        break
                
                if time_index != -1:
                    minutes = int(words[time_index+1])
                    reminder_text = ' '.join(words[2:time_index])
                    return self.set_reminder(reminder_text, minutes)
                else:
                    return "Please specify the reminder time. For example: 'set reminder to call mom in 30 minutes'"
            except:
                return "I couldn't understand the reminder format. Try: 'set reminder to call mom in 30 minutes'"
        return "Reminder feature activated. Say 'set reminder' followed by your reminder."
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}"
        return response
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        response = f"Today is {current_date}"
        return response
    
    def get_weather(self, location=None):
        """Get weather information for ANY location"""
        # Check if API key is configured
        if (not hasattr(Config, 'OPENWEATHER_API_KEY') or 
            not Config.OPENWEATHER_API_KEY or 
            Config.OPENWEATHER_API_KEY.startswith('your_')):
            return "❌ Weather API key not configured. Please add your API key to engine/config.py"
        
        # If no location provided, use default
        if not location:
            location = "London"  # Default fallback
            print(f"DEBUG: Using default location: {location}")
        else:
            print(f"DEBUG: Using requested location: {location}")
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={Config.OPENWEATHER_API_KEY}&units=metric"
            
            print(f"DEBUG: API URL: {url}")  # Debug the actual API call
            
            response = requests.get(url, timeout=10)
            
            print(f"DEBUG: API Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                location_name = data['name']
                country = data['sys']['country'] if 'sys' in data and 'country' in data['sys'] else ''
                
                if country:
                    return f"✅ The weather in {location_name}, {country} is {desc} with a temperature of {temp}°C"
                else:
                    return f"✅ The weather in {location_name} is {desc} with a temperature of {temp}°C"
            
            elif response.status_code == 401:
                return "❌ Invalid API key. Please check your OpenWeather API key in config.py"
            
            elif response.status_code == 404:
                return f"❌ Location '{location}' not found. Try another location name."
            
            else:
                return f"❌ Could not fetch weather for {location}. Error: {response.status_code}"
                
        except Exception as e:
            return f"❌ Error fetching weather: {str(e)}"
    
    def calculate(self, expression):
        """Perform calculations"""
        try:
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Invalid characters in calculation"
            
            result = eval(expression)
            return f"The answer is {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def search_web(self, query):
        """Search the web"""
        try:
            webbrowser.open(f"https://www.youtube.com/watch?v=2B0RxuYQ7dE")
            return f"Searching the web for {query}"
        except Exception as e:
            return f"Error opening browser: {str(e)}"
    
    def get_news(self):
        """Get latest news using RSS feeds (no API key required)"""
        try:
            import feedparser
            
            # Try multiple news sources
            news_sources = [
                "http://feeds.bbci.co.uk/news/rss.xml",  # BBC News
                "https://rss.cnn.com/rss/edition.rss",   # CNN
                "https://feeds.reuters.com/reuters/topNews"  # Reuters
            ]
            
            all_news = []
            
            for source in news_sources:
                try:
                    feed = feedparser.parse(source)
                    if feed.entries:
                        for entry in feed.entries[:2]:  # Get 2 headlines from each source
                            all_news.append(entry.title)
                        break  # Use the first successful source
                except:
                    continue  # Try next source if this fails
            
            if all_news:
                news = "Here are the latest news headlines: "
                for i, headline in enumerate(all_news[:3], 1):
                    news += f"{i}. {headline}. "
                return news
            else:
                return "Sorry, I couldn't fetch the latest news from any source."
                
        except ImportError:
            return "Please install feedparser: pip install feedparser"
        except Exception as e:
            return f"Error fetching news: {str(e)}"
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        return random.choice(jokes)
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            info_lines = []
            
            # ===== OPERATING SYSTEM =====
            info_lines.append("--- OPERATING SYSTEM ---")
            try:
                system = platform.system()
                version = platform.version()
                release = platform.release()
                architecture = platform.architecture()[0]
                platform_info = platform.platform()
                
                info_lines.append("• Platform: " + str(platform_info))
                info_lines.append("• System: " + str(system) + " " + str(release))
                info_lines.append("• Version: " + str(version))
                info_lines.append("• Architecture: " + str(architecture))
            except Exception as e:
                info_lines.append("• OS Details: Not available")
            
            # ===== PROCESSOR =====
            info_lines.append("--- PROCESSOR ---")
            try:
                processor = platform.processor()
                if processor and processor != "":
                    # Clean processor name
                    if "Intel" in processor:
                        clean_processor = "Intel " + processor.split("Intel")[-1].strip()
                    elif "AMD" in processor:
                        clean_processor = "AMD " + processor.split("AMD")[-1].strip()
                    else:
                        clean_processor = processor
                    info_lines.append("• Model: " + str(clean_processor))
                else:
                    info_lines.append("• Model: Not detected")
                
                # CPU cores and usage
                physical_cores = psutil.cpu_count(logical=False)
                logical_cores = psutil.cpu_count(logical=True)
                cpu_usage = psutil.cpu_percent()
                info_lines.append("• Cores: " + str(physical_cores) + " physical, " + str(logical_cores) + " logical")
                info_lines.append("• Usage: " + str(cpu_usage) + "%")
            except Exception as e:
                info_lines.append("• Processor: Not available")
            
            # ===== MEMORY (RAM) =====
            info_lines.append("--- MEMORY ---")
            try:
                memory = psutil.virtual_memory()
                total_ram_gb = round(memory.total / (1024**3), 1)
                used_ram_gb = round(memory.used / (1024**3), 1)
                available_ram_gb = round(memory.available / (1024**3), 1)
                ram_percent = memory.percent
                
                info_lines.append("• Total: " + str(total_ram_gb) + " GB")
                info_lines.append("• Used: " + str(used_ram_gb) + " GB (" + str(ram_percent) + "%)")
                info_lines.append("• Available: " + str(available_ram_gb) + " GB")
            except Exception as e:
                info_lines.append("• RAM: Not available")
            
            # ===== STORAGE =====
            info_lines.append("--- STORAGE ---")
            try:
                disk = psutil.disk_usage('/')
                total_disk_gb = round(disk.total / (1024**3), 1)
                used_disk_gb = round(disk.used / (1024**3), 1)
                free_disk_gb = round(disk.free / (1024**3), 1)
                disk_percent = disk.percent
                
                info_lines.append("• Total: " + str(total_disk_gb) + " GB")
                info_lines.append("• Used: " + str(used_disk_gb) + " GB (" + str(disk_percent) + "%)")
                info_lines.append("• Free: " + str(free_disk_gb) + " GB")
            except Exception as e:
                info_lines.append("• Storage: Not available")
            
            # ===== SYSTEM UPTIME =====
            info_lines.append("--- SYSTEM ---")
            try:
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time
                days = uptime.days
                hours = int(uptime.seconds // 3600)
                minutes = int((uptime.seconds % 3600) // 60)
                
                info_lines.append("• Boot Time: " + str(boot_time.strftime('%Y-%m-%d %H:%M:%S')))
                info_lines.append("• Uptime: " + str(days) + "d " + str(hours) + "h " + str(minutes) + "m")
            except Exception as e:
                info_lines.append("• Uptime: Not available")
            
            # ===== PYTHON INFO =====
            info_lines.append("--- PYTHON ---")
            try:
                python_version = platform.python_version()
                implementation = platform.python_implementation()
                info_lines.append("• Version: " + str(python_version))
                info_lines.append("• Implementation: " + str(implementation))
            except Exception as e:
                info_lines.append("• Python: Not available")
            
            # Join all lines
            return "💻 COMPREHENSIVE SYSTEM INFORMATION:\n" + "\n".join(info_lines)
            
        except Exception as e:
            return "System information is available"

    def get_name(self):
        """Tell the user Jarvis's name"""
        return "My name is Jarvis. I am your personal AI assistant!"
    
    def introduce(self):
        """Introduce Jarvis AI"""
        introduction = """
🤖 I am Jarvis AI - Your Personal Assistant!

I was created in 2024 to help you with various tasks. Here's what I can do:

• Tell you the current time and date
• Provide weather information for any location
• Perform calculations
• Search the web
• Share latest news headlines
• Tell jokes
• Show system information
• Set reminders
• Play music from YouTube
• And much more!

Just ask me anything you need help with!
"""
        return introduction
    
    def get_creator(self):
        """Tell about the creator"""
        return "I was created by a developer to assist users with daily tasks and information."
    
    def get_capabilities(self):
        """List Jarvis capabilities"""
        capabilities = """
📋 Here's what I can help you with:

🕒 **Time & Date**
  - Current time
  - Today's date

🌤️ **Weather**
  - Weather for any city worldwide

🔢 **Calculations**
  - Basic math calculations
  - Complex expressions

🌐 **Web & Information**
  - Web searches
  - Latest news headlines
  - System information

🎵 **Music & Entertainment**
  - Play songs from YouTube
  - Stop music playback
  - Tell jokes
  - Have conversations

⏰ **Productivity**
  - Set reminders
  - Manage tasks

Just say 'help' to see these options anytime!
"""
        return capabilities
    
    def set_reminder(self, reminder_text, minutes_from_now):
        """Set a reminder"""
        try:
            reminder_time = datetime.now() + timedelta(minutes=minutes_from_now)
            
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reminders (reminder_text, reminder_time) VALUES (?, ?)",
                (reminder_text, reminder_time)
            )
            conn.commit()
            conn.close()
            return f"Reminder set for {minutes_from_now} minutes from now: {reminder_text}"
        except Exception as e:
            return f"Error setting reminder: {str(e)}"