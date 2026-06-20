# jarvis_gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import math
from datetime import datetime

# -------------------------
# Mock Jarvis for demo (replace with your real Jarvis instance)
# -------------------------
class MockFeatures:
    def __init__(self):
        self.song_database = {
            "ghar se nikalte hi": "track1",
            "tum hi ho": "track2",
            "kesariya": "track3",
        }

    def listen(self):
        # Demo: no real listening
        return None

    def speak(self, text):
        # Demo: no TTS
        print("JARVIS would speak:", text)

class MockCommandProcessor:
    def __init__(self):
        self.features = MockFeatures()

    def process_command(self, cmd):
        cmd = cmd.lower()
        if "play" in cmd:
            return f"Playing {cmd.replace('play', '').strip().title()}"
        if "stop" in cmd:
            return "Music stopped."
        return f"Executed command: {cmd}"

class MockJarvis:
    def __init__(self):
        self.command_processor = MockCommandProcessor()

# -------------------------
# Jarvis GUI
# -------------------------
class JarvisGUI:
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
        self.root = tk.Tk()
        self.setup_gui()

    def setup_gui(self):
        # Window setup
        self.root.title("JARVIS AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')

        # Make window semi-transparent
        self.root.attributes('-alpha', 0.97)

        # Header
        header_frame = tk.Frame(self.root, bg='#0a0a0a')
        header_frame.pack(fill='x', padx=30, pady=15)

        # Title
        title_label = tk.Label(
            header_frame,
            text="JARVIS AI ASSISTANT",
            font=('Arial', 20, 'bold'),
            fg='#00ffcc',
            bg='#0a0a0a'
        )
        title_label.pack(side='left')

        # Status indicator
        self.status_label = tk.Label(
            header_frame,
            text="● OPERATIONAL",
            font=('Arial', 12),
            fg='#00ffcc',
            bg='#0a0a0a'
        )
        self.status_label.pack(side='right')

        # Main content area
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill='both', expand=True, padx=30, pady=15)

        # Left frame for robot & HUD
        left_frame = tk.Frame(main_frame, bg='#0a0a0a', width=420)
        left_frame.pack(side='left', fill='y', padx=(0, 25))

        # Right frame for chat and controls
        right_frame = tk.Frame(main_frame, bg='#0a0a0a')
        right_frame.pack(side='right', fill='both', expand=True)

        # ===== HUD + ROBOT CANVAS =====
        robot_container = tk.Frame(left_frame, bg='#0a0a0a', width=380, height=580)
        robot_container.pack(pady=10)
        robot_container.pack_propagate(False)

        # Robot canvas (larger for HUD rings)
        self.robot_canvas = tk.Canvas(
            robot_container,
            width=380,
            height=580,
            bg='#07121a',
            highlightthickness=0
        )
        self.robot_canvas.pack()

        # draw and animate HUD-style robot
        self.animation_phase = 0
        self.hud_center = (190, 260)  # center of HUD
        self.draw_premium_hud_robot()

        # System status block (kept compact)
        status_frame = tk.Frame(left_frame, bg='#1a1a1a', relief='ridge', bd=1)
        status_frame.pack(fill='x', pady=15)

        status_title = tk.Label(
            status_frame,
            text="SYSTEM STATUS",
            font=('Arial', 12, 'bold'),
            fg='#00ffcc',
            bg='#1a1a1a'
        )
        status_title.pack(pady=(8, 5))

        # Status items
        status_items = [
            ("AI Core", "ONLINE", "#00ff00"),
            ("Voice Module", "ACTIVE", "#00ff00"),
            ("Audio Output", "READY", "#00ff00"),
            ("Network", "CONNECTED", "#00ff00")
        ]

        for item, status, color in status_items:
            item_frame = tk.Frame(status_frame, bg='#1a1a1a')
            item_frame.pack(fill='x', padx=10, pady=2)

            tk.Label(item_frame, text=item, font=('Arial', 10),
                     fg='#cccccc', bg='#1a1a1a').pack(side='left')
            tk.Label(item_frame, text=status, font=('Arial', 10, 'bold'),
                     fg=color, bg='#1a1a1a').pack(side='right')

        # Capabilities
        capabilities_frame = tk.Frame(left_frame, bg='#1a1a1a', relief='ridge', bd=1)
        capabilities_frame.pack(fill='x', pady=10)

        capabilities_title = tk.Label(
            capabilities_frame,
            text="CORE CAPABILITIES",
            font=('Arial', 12, 'bold'),
            fg='#00ffcc',
            bg='#1a1a1a'
        )
        capabilities_title.pack(pady=(8, 5))

        capabilities = [
            "✓ Weather Updates", "✓ Time & Date", "✓ Calculations",
            "✓ Web Search", "✓ News Headlines", "✓ Jokes & Fun",
            "✓ System Info", "✓ Music Playback", "✓ Voice Control"
        ]

        for capability in capabilities:
            tk.Label(capabilities_frame, text=capability, font=('Arial', 9),
                    fg='#00ff99', bg='#1a1a1a', anchor='w').pack(fill='x', padx=10, pady=1)

        # ===== CHAT AND CONTROLS =====

        # Chat display area
        chat_frame = tk.Frame(right_frame, bg='#1a1a1a', relief='ridge', bd=1)
        chat_frame.pack(fill='both', expand=True, pady=(0, 15))

        chat_header = tk.Frame(chat_frame, bg='#2a2a2a')
        chat_header.pack(fill='x')

        tk.Label(chat_header, text="CONVERSATION LOG", font=('Arial', 11, 'bold'),
                 fg='#00ffcc', bg='#2a2a2a').pack(pady=5)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=70,
            height=18,
            font=('Consolas', 10),
            bg='#0f0f0f',
            fg='#00ffcc',
            insertbackground='#00ffcc',
            relief='flat',
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill='both', expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # Input area
        input_container = tk.Frame(right_frame, bg='#1a1a1a', relief='ridge', bd=1)
        input_container.pack(fill='x', pady=10)

        input_header = tk.Frame(input_container, bg='#2a2a2a')
        input_header.pack(fill='x')

        tk.Label(input_header, text="COMMAND INTERFACE", font=('Arial', 11, 'bold'),
                 fg='#00ffcc', bg='#2a2a2a').pack(pady=5)

        input_frame = tk.Frame(input_container, bg='#1a1a1a')
        input_frame.pack(fill='x', padx=15, pady=10)

        # Input label
        input_label = tk.Label(
            input_frame,
            text="Ask me anything",
            font=('Arial', 11, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        input_label.pack(anchor='w', pady=(0, 5))

        # Input field
        self.input_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='#0f0f0f',
            fg='#00ffcc',
            insertbackground='#00ffcc',
            relief='sunken',
            borderwidth=2,
            width=50
        )
        self.input_entry.pack(fill='x', pady=(0, 10))
        self.input_entry.bind('<Return>', self.send_text_command)
        self.input_entry.focus_set()

        # Controls panel
        controls_frame = tk.Frame(right_frame, bg='#1a1a1a', relief='ridge', bd=1)
        controls_frame.pack(fill='x', pady=10)

        controls_header = tk.Frame(controls_frame, bg='#2a2a2a')
        controls_header.pack(fill='x')

        tk.Label(controls_header, text="CONTROL PANEL", font=('Arial', 11, 'bold'),
                 fg='#00ffcc', bg='#2a2a2a').pack(pady=5)

        # Main controls
        main_controls = tk.Frame(controls_frame, bg='#1a1a1a')
        main_controls.pack(fill='x', padx=15, pady=10)

        # Voice control
        self.voice_button = tk.Button(
            main_controls,
            text="🎤 START LISTENING",
            font=('Arial', 11, 'bold'),
            bg='#006666',
            fg='white',
            relief='raised',
            borderwidth=2,
            width=15,
            command=self.toggle_voice_listening
        )
        self.voice_button.pack(side='left', padx=(0, 10))

        # Music controls
        music_frame = tk.Frame(main_controls, bg='#1a1a1a')
        music_frame.pack(side='left', padx=20)

        self.play_button = tk.Button(
            music_frame,
            text="▶️ PLAY MUSIC",
            font=('Arial', 10, 'bold'),
            bg='#004466',
            fg='white',
            relief='raised',
            borderwidth=2,
            command=self.play_music_dialog
        )
        self.play_button.pack(side='left', padx=(0, 5))

        self.stop_button = tk.Button(
            music_frame,
            text="⏹️ STOP",
            font=('Arial', 10, 'bold'),
            bg='#660033',
            fg='white',
            relief='raised',
            borderwidth=2,
            command=self.stop_music
        )
        self.stop_button.pack(side='left')

        # Console button
        console_button = tk.Button(
            main_controls,
            text="📟 CONSOLE MODE",
            font=('Arial', 10, 'bold'),
            bg='#333333',
            fg='white',
            relief='raised',
            borderwidth=2,
            command=self.switch_to_console
        )
        console_button.pack(side='right')

        # Tune indicator
        tune_frame = tk.Frame(right_frame, bg='#1a1a1a')
        tune_frame.pack(fill='x', pady=5)

        self.tune_label = tk.Label(
            tune_frame,
            text="🎵 TUNE HERE ...",
            font=('Arial', 10, 'italic'),
            fg='#666666',
            bg='#1a1a1a'
        )
        self.tune_label.pack(anchor='w')

        # Initialize states
        self.is_listening = False
        self.current_tune = "No music playing"

        # Start voice monitoring in background
        self.start_voice_monitor()

        # Start robot/HUD animations
        self.start_robot_animations()

        # Add welcome message
        self.add_message("JARVIS", "Advanced AI System Online. Ready for commands.\nAll modules operational. How may I assist you today?")

    # -------------------------
    # HUD + Robot drawing
    # -------------------------
    def draw_premium_hud_robot(self):
        """Draw a HUD-style circular UI with a central robot-like emblem and 'J.A.R.V.I.S.' text"""
        c = self.robot_canvas
        c.delete("all")

        cx, cy = self.hud_center

        # Background faint blueprint style
        for i in range(8):
            offset = i * 20
            c.create_rectangle(10+offset, 10+offset, 370-offset, 560-offset,
                               outline='#04202a' if i % 2 == 0 else '', width=1)

        # Draw multiple concentric HUD rings
        ring_colors = ['#003033', '#004b51', '#006b66', '#00a499']
        radii = [160, 130, 100, 70]
        for idx, r in enumerate(radii):
            col = ring_colors[idx % len(ring_colors)]
            c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=col, width=2)

            # segmented ring effect
            segments = 60 - idx*10
            for s in range(segments):
                angle = (2 * math.pi / segments) * s + (self.animation_phase * 0.02)
                x1 = cx + (r - 6) * math.cos(angle)
                y1 = cy + (r - 6) * math.sin(angle)
                x2 = cx + (r + 6) * math.cos(angle)
                y2 = cy + (r + 6) * math.sin(angle)
                if s % (3 + idx) == 0:
                    c.create_line(x1, y1, x2, y2, fill=ring_colors[(idx+1) % len(ring_colors)], width=2)

        # Rotating markers / ticks on outer ring
        for i in range(36):
            angle = math.radians(i * 10 + (self.animation_phase * 0.6))
            r_out = 170
            r_in = 155
            x1 = cx + r_in * math.cos(angle)
            y1 = cy + r_in * math.sin(angle)
            x2 = cx + r_out * math.cos(angle)
            y2 = cy + r_out * math.sin(angle)
            if i % 3 == 0:
                c.create_line(x1, y1, x2, y2, fill='#00ffcc', width=1)

        # Inner tech grid
        inner_r = 58
        for a in range(0, 360, 20):
            angle = math.radians(a + (self.animation_phase * 0.8))
            x = cx + inner_r * math.cos(angle)
            y = cy + inner_r * math.sin(angle)
            c.create_line(cx, cy, x, y, fill='#003a3a', width=1)

        # Central emblem / small robot silhouette (simplified)
        # torso
        c.create_oval(cx - 28, cy - 18, cx + 28, cy + 18, fill='#002527', outline='#00bfa6', width=2)
        # head
        c.create_polygon(cx-12, cy-36, cx+12, cy-36, cx+18, cy-18, cx-18, cy-18,
                         fill='#001a1a', outline='#00d4b4', width=2)
        # visor (animated)
        self.visor_display = c.create_rectangle(cx-18, cy-30, cx+18, cy-22, fill='#003333', outline='')

        # small chest text
        c.create_text(cx, cy+4, text="AI", fill='#00ffcc', font=('Arial', 9, 'bold'))

        # CENTRAL LABEL: J.A.R.V.I.S.
        c.create_text(cx, cy + 120, text="J.A.R.V.I.S.", fill='#00ffcc', font=('Arial', 18, 'bold'))

        # Thrusters (animated ovals)
        self.left_thruster = c.create_oval(cx - 60, cy + 36, cx - 36, cy + 56, fill='#003333', outline='')
        self.right_thruster = c.create_oval(cx + 36, cy + 36, cx + 60, cy + 56, fill='#003333', outline='')

        # HUD labels / mini-windows
        c.create_rectangle(cx+80, cy-40, cx+160, cy-10, fill='#001a1a', outline='#00bfa6', width=1)
        c.create_text(cx+120, cy-25, text="Core: ONLINE", fill='#00ff99', font=('Arial', 8))
        c.create_rectangle(cx-160, cy+40, cx-80, cy+70, fill='#001a1a', outline='#00bfa6', width=1)
        c.create_text(cx-120, cy+55, text="NET: OK", fill='#00ff99', font=('Arial', 8))

    def animate_robot(self):
        """Premium HUD & robot animations"""
        c = self.robot_canvas
        self.animation_phase = (self.animation_phase + 1) % 100000

        # Visor pulsing color (safe clamp to 0-255)
        alpha = abs(math.sin(self.animation_phase * 0.12))  # 0..1
        g = int(120 + alpha * 135)   # between 120 and 255
        b = int(120 + alpha * 135)
        visor_color = '#{:02x}{:02x}{:02x}'.format(0, g, b)
        try:
            c.itemconfig(self.visor_display, fill=visor_color)
        except Exception:
            pass

        # Thruster glow effect (animated)
        thr_alpha = abs(math.sin(self.animation_phase * 0.18))
        blue = int(80 + thr_alpha * 175)
        thr_color = '#{:02x}{:02x}{:02x}'.format(0, 255, blue if blue <= 255 else 255)
        try:
            c.itemconfig(self.left_thruster, fill=thr_color)
            c.itemconfig(self.right_thruster, fill=thr_color)
        except Exception:
            pass

        # Redraw rings & rotating markers by re-drawing HUD entirely for smooth rotation
        self.draw_premium_hud_robot()

        # Continue animation (fast enough for smoothness)
        self.root.after(60, self.animate_robot)

    def start_robot_animations(self):
        """Start all robot/HUD animations"""
        self.animate_robot()

    # -------------------------
    # Voice monitoring (background)
    # -------------------------
    def start_voice_monitor(self):
        """Start background thread for voice monitoring"""
        def monitor_voice():
            while True:
                if self.is_listening:
                    try:
                        command = self.jarvis.command_processor.features.listen()
                        if command:
                            self.process_voice_command(command)
                    except Exception:
                        pass
                time.sleep(1)

        thread = threading.Thread(target=monitor_voice, daemon=True)
        thread.start()

    def toggle_voice_listening(self):
        """Toggle voice listening on/off"""
        if not self.is_listening:
            self.is_listening = True
            self.voice_button.config(
                text="🔴 STOP LISTENING",
                bg='#990000'
            )
            self.status_label.config(text="● LISTENING", fg='#ff0000')
            self.add_message("System", "Voice listening activated...")
        else:
            self.is_listening = False
            self.voice_button.config(
                text="🎤 START LISTENING",
                bg='#006666'
            )
            self.status_label.config(text="● OPERATIONAL", fg='#00ffcc')
            self.add_message("System", "Voice listening stopped")

    def process_voice_command(self, command):
        """Process voice command and display response"""
        self.add_message("You", command)

        # Process command through Jarvis
        response = self.jarvis.command_processor.process_command(command)

        # Display response
        self.add_message("JARVIS", response)

        # Speak the response
        try:
            self.jarvis.command_processor.features.speak(response)
        except Exception:
            pass

        # Update tune if it's a music command
        if any(word in command.lower() for word in ['play', 'music', 'song']):
            self.update_tune_display(command)

    def send_text_command(self, event=None):
        """Send text command from input field"""
        command = self.input_entry.get().strip()
        if command:
            self.add_message("You", command)
            self.input_entry.delete(0, tk.END)

            # Process command
            try:
                response = self.jarvis.command_processor.process_command(command)
            except Exception as e:
                response = f"Error processing command: {e}"
            self.add_message("JARVIS", response)

            # Speak response if it's not too long
            try:
                if len(response) < 100:
                    self.jarvis.command_processor.features.speak(response)
            except Exception:
                pass

            # Update tune if it's a music command
            if any(word in command.lower() for word in ['play', 'music', 'song']):
                self.update_tune_display(command)

    def add_message(self, sender, message):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)

        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Add sender tag with timestamp
        if sender == "JARVIS":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"JARVIS: ", 'jarvis_tag')
            self.chat_display.insert(tk.END, f"{message}\n", 'jarvis_text')
        elif sender == "You":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"You: ", 'user_tag')
            self.chat_display.insert(tk.END, f"{message}\n", 'user_text')
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n", 'system_text')

        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

        # Configure tags for premium styling
        self.chat_display.tag_config('timestamp', foreground='#666666')
        self.chat_display.tag_config('jarvis_tag', foreground='#00ffcc', font=('Arial', 10, 'bold'))
        self.chat_display.tag_config('jarvis_text', foreground='#00ff99')
        self.chat_display.tag_config('user_tag', foreground='#0088ff', font=('Arial', 10, 'bold'))
        self.chat_display.tag_config('user_text', foreground='#66aaff')
        self.chat_display.tag_config('system_text', foreground='#ff6600')

    def update_tune_display(self, command):
        """Update the tune display with current song"""
        # Extract song name from command
        song_name = command.lower()
        play_words = ['play', 'song', 'music', 'gaana']
        for word in play_words:
            song_name = song_name.replace(word, '')
        song_name = song_name.strip()

        if song_name:
            self.tune_label.config(text=f"🎵 NOW PLAYING: {song_name.title()}", fg='#00ffcc')
            self.current_tune = song_name.title()

    # -------------------------
    # Music dialog and controls
    # -------------------------
    def play_music_dialog(self):
        """Open premium music dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Music Player - JARVIS AI")
        dialog.geometry("500x400")
        dialog.configure(bg='#1a1a1a')
        dialog.transient(self.root)
        dialog.grab_set()

        # Header
        header = tk.Frame(dialog, bg='#2a2a2a')
        header.pack(fill='x')
        tk.Label(header, text="MUSIC PLAYER", font=('Arial', 14, 'bold'),
                 fg='#00ffcc', bg='#2a2a2a').pack(pady=10)

        content = tk.Frame(dialog, bg='#1a1a1a')
        content.pack(fill='both', expand=True, padx=20, pady=10)

        # Song selection
        tk.Label(content, text="Select Song:", fg='white', bg='#1a1a1a',
                 font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 5))

        # Available songs
        available_songs = list(self.jarvis.command_processor.features.song_database.keys())

        song_var = tk.StringVar()
        song_combo = ttk.Combobox(content, textvariable=song_var, values=available_songs,
                                  width=40, font=('Arial', 10))
        song_combo.pack(fill='x', pady=(0, 15))

        # Quick play section
        quick_frame = tk.Frame(content, bg='#1a1a1a')
        quick_frame.pack(fill='x', pady=10)

        tk.Label(quick_frame, text="Quick Play:", fg='#cccccc', bg='#1a1a1a',
                 font=('Arial', 10, 'bold')).pack(anchor='w')

        # Popular songs grid
        popular_songs = ["ghar se nikalte hi", "tum hi ho", "tera zikr", "kesariya",
                         "apna bana le", "besharam rang", "see you again", "shape of you"]

        grid_frame = tk.Frame(quick_frame, bg='#1a1a1a')
        grid_frame.pack(fill='x', pady=5)

        for i, song in enumerate(popular_songs):
            row = i // 2
            col = i % 2
            btn = tk.Button(
                grid_frame,
                text=f"🎵 {song.title()}",
                font=('Arial', 9),
                bg='#003366',
                fg='white',
                relief='raised',
                borderwidth=1,
                command=lambda s=song: self.quick_play(s, dialog)
            )
            btn.grid(row=row, column=col, padx=5, pady=2, sticky='ew')

        # Equal column weight
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Control buttons
        button_frame = tk.Frame(content, bg='#1a1a1a')
        button_frame.pack(fill='x', pady=20)

        def play_selected_song():
            song_name = song_var.get()
            if song_name:
                self.add_message("You", f"play {song_name}")
                response = self.jarvis.command_processor.process_command(f"play {song_name}")
                self.add_message("JARVIS", response)
                self.update_tune_display(song_name)
                dialog.destroy()

        play_btn = tk.Button(button_frame, text="▶️ PLAY SELECTED",
                             command=play_selected_song, bg='#006600', fg='white',
                             font=('Arial', 11, 'bold'), relief='raised', borderwidth=2)
        play_btn.pack(side='left', padx=(0, 10))

        tk.Button(button_frame, text="❌ CLOSE", command=dialog.destroy,
                  bg='#660000', fg='white', font=('Arial', 10),
                  relief='raised', borderwidth=2).pack(side='right')

    def quick_play(self, song_name, dialog):
        """Quick play a song"""
        self.add_message("You", f"play {song_name}")
        response = self.jarvis.command_processor.process_command(f"play {song_name}")
        self.add_message("JARVIS", response)
        self.update_tune_display(song_name)
        dialog.destroy()

    def stop_music(self):
        """Stop currently playing music"""
        self.add_message("You", "stop music")
        response = self.jarvis.command_processor.process_command("stop music")
        self.add_message("JARVIS", response)
        self.tune_label.config(text="🎵 TUNE HERE ...", fg='#666666')
        self.current_tune = "No music playing"

    def switch_to_console(self):
        """Switch back to console mode"""
        self.add_message("System", "Switching to console mode...")
        self.root.after(1000, self.root.destroy)

    def run(self):
        """Start the GUI"""
        self.root.mainloop()

# -------------------------
# Run demo if file executed directly
# -------------------------
if __name__ == "__main__":
    jarvis = MockJarvis()  # replace with your Jarvis instance if available
    gui = JarvisGUI(jarvis)
    gui.run()
