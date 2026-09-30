"""
Garun AI Assistant - Main Window
=================================
The primary application window with cyberpunk aesthetics
"""

import customtkinter as ctk
import threading
from ui.themes import Colors, Fonts, Dimensions
from ui.visualizer import VoiceVisualizer
from ui.chat_widget import ChatWidget
from ui.settings_dialog import SettingsDialog
from config import TTS_ENABLED


class MainWindow(ctk.CTk):
    """Main application window for Garun"""
    
    def __init__(self, assistant=None):
        super().__init__()
        
        self.assistant = assistant
        self.is_listening = False
        self.tts_enabled = TTS_ENABLED  # Text-to-speech enabled by default
        self.wake_word_active = True  # Background wake word listening
        
        # Window configuration
        self._configure_window()
        
        # Create UI components
        self._create_widgets()
        
        # Bind events
        self._bind_events()
        
        # Start background wake word listening
        self._start_wake_word_listening()
    
    def _configure_window(self):
        """Configure main window properties"""
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Window settings
        self.title("GARUN")
        self.geometry(f"{Dimensions.WINDOW_WIDTH}x{Dimensions.WINDOW_HEIGHT}")
        self.minsize(Dimensions.WINDOW_MIN_WIDTH, Dimensions.WINDOW_MIN_HEIGHT)
        
        # Dark background
        self.configure(fg_color=Colors.BG_PRIMARY)
        
        # Center window on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - Dimensions.WINDOW_WIDTH) // 2
        y = (self.winfo_screenheight() - Dimensions.WINDOW_HEIGHT) // 2
        self.geometry(f"+{x}+{y}")
        
        # Window icon (will be set if icon exists)
        try:
            self.iconbitmap("assets/icon.ico")
        except:
            pass
    
    def _create_widgets(self):
        """Create all UI widgets with premium styling"""
        
        # ============================================
        # PREMIUM HEADER
        # ============================================
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=0,
            height=70,
            border_width=0
        )
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        
        # Glowing accent line at top
        self.accent_line = ctk.CTkFrame(
            self.header_frame,
            fg_color=Colors.PRIMARY,
            height=2,
            corner_radius=0
        )
        self.accent_line.pack(fill="x", side="top")
        
        # Title container
        self.title_container = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )
        self.title_container.pack(side="left", padx=Dimensions.PAD_LG, pady=Dimensions.PAD_SM)
        
        # Premium Title with glow effect
        self.title_label = ctk.CTkLabel(
            self.title_container,
            text="✦ GARUN ✦",
            font=("Segoe UI Light", 28),
            text_color=Colors.PRIMARY
        )
        self.title_label.pack()
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.title_container,
            text="AI ASSISTANT",
            font=("Segoe UI", 9),
            text_color=Colors.TEXT_MUTED
        )
        self.subtitle_label.pack()
        
        # Status indicator with modern styling
        self.status_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color=Colors.BG_TERTIARY,
            corner_radius=Dimensions.RADIUS_ROUND
        )
        self.status_frame.pack(side="right", padx=Dimensions.PAD_LG, pady=Dimensions.PAD_MD)
        
        self.status_dot = ctk.CTkLabel(
            self.status_frame,
            text="●",
            font=("Segoe UI", 10),
            text_color=Colors.GREEN
        )
        self.status_dot.pack(side="left", padx=(Dimensions.PAD_SM, 4))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Online",
            font=("Segoe UI Semibold", 10),
            text_color=Colors.TEXT_SECONDARY
        )
        self.status_label.pack(side="left", padx=(0, Dimensions.PAD_SM))
        
        # ============================================
        # PREMIUM VISUALIZER SECTION
        # ============================================
        self.visualizer_frame = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=Dimensions.RADIUS_XL,
            height=200,
            border_width=1,
            border_color=Colors.BORDER_GLOW
        )
        self.visualizer_frame.pack(
            fill="x",
            padx=Dimensions.PAD_LG,
            pady=(Dimensions.PAD_SM, Dimensions.PAD_LG)
        )
        self.visualizer_frame.pack_propagate(False)
        
        # Voice visualizer - larger and more prominent
        self.visualizer = VoiceVisualizer(
            self.visualizer_frame,
            size=160
        )
        self.visualizer.pack(pady=Dimensions.PAD_MD)
        
        # ============================================
        # CHAT SECTION
        # ============================================
        self.chat_widget = ChatWidget(
            self,
            on_send_message=self._on_message_sent
        )
        self.chat_widget.pack(
            fill="both",
            expand=True,
            padx=Dimensions.PAD_SM,
            pady=(0, Dimensions.PAD_SM)
        )
        
        # ============================================
        # PREMIUM BOTTOM TOOLBAR
        # ============================================
        self.toolbar_frame = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=0,
            height=60
        )
        self.toolbar_frame.pack(fill="x", side="bottom")
        self.toolbar_frame.pack_propagate(False)
        
        # Top accent line
        self.toolbar_accent = ctk.CTkFrame(
            self.toolbar_frame,
            fg_color=Colors.BLUE_DARK,
            height=1,
            corner_radius=0
        )
        self.toolbar_accent.pack(fill="x", side="top")
        
        # Button container for centering
        self.button_container = ctk.CTkFrame(
            self.toolbar_frame,
            fg_color="transparent"
        )
        self.button_container.pack(expand=True, fill="both")
        
        # Voice button - Primary action
        self.voice_button = ctk.CTkButton(
            self.button_container,
            text="🎤 Voice",
            width=100,
            height=40,
            font=("Segoe UI Semibold", 12),
            fg_color=Colors.PRIMARY_DARK,
            hover_color=Colors.PRIMARY,
            text_color=Colors.BG_DARK,
            corner_radius=Dimensions.RADIUS_MD,
            command=self._toggle_voice
        )
        self.voice_button.pack(side="left", padx=Dimensions.PAD_MD, pady=Dimensions.PAD_SM)
        
        # Speaker toggle button (TTS on/off)
        self.speaker_button = ctk.CTkButton(
            self.button_container,
            text="🔊 Speaker",
            width=100,
            height=40,
            font=("Segoe UI Semibold", 12),
            fg_color=Colors.ACCENT_DARK if self.tts_enabled else Colors.BG_TERTIARY,
            hover_color=Colors.ACCENT if self.tts_enabled else Colors.BG_HOVER,
            text_color=Colors.TEXT_BRIGHT if self.tts_enabled else Colors.TEXT_PRIMARY,
            corner_radius=Dimensions.RADIUS_MD,
            command=self._toggle_speaker
        )
        self.speaker_button.pack(side="left", padx=(0, Dimensions.PAD_SM), pady=Dimensions.PAD_SM)
        
        # Settings button
        self.settings_button = ctk.CTkButton(
            self.button_container,
            text="⚙",
            width=40,
            height=40,
            font=("Segoe UI", 16),
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_SECONDARY,
            corner_radius=Dimensions.RADIUS_MD,
            command=self._open_settings
        )
        self.settings_button.pack(side="left", padx=(0, Dimensions.PAD_SM), pady=Dimensions.PAD_SM)
        
        # Keyboard shortcut hint
        self.shortcut_frame = ctk.CTkFrame(
            self.button_container,
            fg_color=Colors.BG_TERTIARY,
            corner_radius=Dimensions.RADIUS_SM
        )
        self.shortcut_frame.pack(side="right", padx=Dimensions.PAD_MD, pady=Dimensions.PAD_SM)
        
        self.shortcut_label = ctk.CTkLabel(
            self.shortcut_frame,
            text="⌨ Ctrl+Shift+G",
            font=("Segoe UI", 9),
            text_color=Colors.TEXT_MUTED
        )
        self.shortcut_label.pack(padx=Dimensions.PAD_SM, pady=4)
        
        # Pin button (always on top)
        self.is_pinned = False
        self.pin_button = ctk.CTkButton(
            self.button_container,
            text="📌",
            width=40,
            height=40,
            font=("Segoe UI", 14),
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_SECONDARY,
            corner_radius=Dimensions.RADIUS_MD,
            command=self._toggle_pin
        )
        self.pin_button.pack(side="right", padx=(0, Dimensions.PAD_SM), pady=Dimensions.PAD_SM)
    
    def _bind_events(self):
        """Bind keyboard and window events"""
        # Close handling
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Keyboard shortcuts
        self.bind("<Control-Shift-G>", lambda e: self._toggle_voice())
        self.bind("<Escape>", lambda e: self._stop_listening())
    
    def _start_wake_word_listening(self):
        """Start background wake word detection"""
        if not self.assistant or not hasattr(self.assistant, 'voice'):
            print("[Garun] Wake word listening not available - no voice engine")
            return
        
        def on_wake_word(command):
            """Called when wake word is detected"""
            # Bring window to front
            self.after(0, self._on_wake_word_detected, command)
        
        # Start listening in background thread
        def wake_word_listener():
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            # Import wake words from config
            from config import WAKE_WORDS
            
            print("[Garun] Wake word listening started! Say 'Hey Garun' to activate.")
            
            while self.wake_word_active:
                try:
                    with microphone as source:
                        # Shorter timeout for faster wake word detection
                        recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    
                    # Recognize speech
                    text = recognizer.recognize_google(audio).lower()
                    print(f"[Garun] Heard: {text}")
                    
                    # Check for wake words
                    for wake_word in WAKE_WORDS:
                        if wake_word in text:
                            # Extract command after wake word
                            command = text.split(wake_word, 1)[-1].strip()
                            on_wake_word(command if command else None)
                            break
                            
                except sr.WaitTimeoutError:
                    continue  # No speech detected, keep listening
                except sr.UnknownValueError:
                    continue  # Could not understand, keep listening
                except sr.RequestError as e:
                    print(f"[Garun] Speech service error: {e}")
                    continue
                except Exception as e:
                    print(f"[Garun] Wake word error: {e}")
                    continue
        
        threading.Thread(target=wake_word_listener, daemon=True).start()
    
    def _on_wake_word_detected(self, command=None):
        """Handle wake word detection"""
        # Bring window to front and focus
        self.deiconify()  # Restore if minimized
        self.lift()  # Bring to front
        self.focus_force()  # Focus the window
        
        # Visual feedback
        self.visualizer.set_state("listening")
        self.set_status("I'm here! How can I help?", Colors.PRIMARY)
        
        # Speak acknowledgment
        if self.tts_enabled and self.assistant:
            self.assistant.speak("Yes, I'm here!")
        
        # If command was included with wake word, process it
        if command:
            self.chat_widget.add_message(command, is_user=True)
            self._on_message_sent(command)
        else:
            # Just show ready state, wait for user input
            self.after(3000, lambda: self.set_status("Online", Colors.GREEN))
            self.after(3000, lambda: self.visualizer.set_state("idle"))

    def _on_message_sent(self, message):
        """Handle message sent from chat widget"""
        # Set processing state
        self.visualizer.set_state("processing")
        self.set_status("Processing...", Colors.PURPLE)
        
        # Process in thread to not block UI
        def process():
            response = None
            if self.assistant:
                response = self.assistant.process_message(message)
            else:
                response = "I'm not fully connected yet. Please check the configuration."
            
            # Update UI in main thread
            self.after(0, lambda: self._show_response(response))
        
        threading.Thread(target=process, daemon=True).start()
    
    def _show_response(self, response):
        """Show assistant response in chat"""
        self.chat_widget.add_message(response, is_user=False)
        self.visualizer.set_state("idle")
        self.set_status("Online", Colors.GREEN)
        
        # Speak response if TTS is enabled and assistant has voice
        if self.tts_enabled and self.assistant and hasattr(self.assistant, 'speak'):
            self.visualizer.set_state("speaking")
            threading.Thread(
                target=lambda: self._speak_and_reset(response),
                daemon=True
            ).start()
    
    def _clean_text_for_speech(self, text):
        """Remove markdown symbols and clean text for TTS"""
        import re
        # Remove markdown formatting
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'\*(.+?)\*', r'\1', text)      # *italic*
        text = re.sub(r'__(.+?)__', r'\1', text)      # __bold__
        text = re.sub(r'_(.+?)_', r'\1', text)        # _italic_
        text = re.sub(r'`(.+?)`', r'\1', text)        # `code`
        text = re.sub(r'#+\s*', '', text)             # # headers
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # [links](url)
        text = re.sub(r'[•●○◦►▶→]', '', text)         # bullet points
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # list items
        text = re.sub(r'\s+', ' ', text)              # multiple spaces
        return text.strip()

    def _speak_and_reset(self, text):
        """Speak text and reset visualizer"""
        if self.assistant:
            clean_text = self._clean_text_for_speech(text)
            print(f"[Garun UI] Speaking: {clean_text[:50]}...")
            self.assistant.speak_sync(clean_text)
            print(f"[Garun UI] Done speaking")
        self.after(0, lambda: self.visualizer.set_state("idle"))
    
    def _toggle_voice(self):
        """Toggle voice listening mode"""
        if self.is_listening:
            self._stop_listening()
        else:
            self._start_listening()
    
    def _start_listening(self):
        """Start voice listening"""
        self.is_listening = True
        self.visualizer.set_state("listening")
        self.voice_button.configure(
            text="🎤 Stop",
            fg_color=Colors.PRIMARY_DARK
        )
        self.set_status("Listening...", Colors.PRIMARY)
        
        # Start listening in thread
        if self.assistant and hasattr(self.assistant, 'listen'):
            def listen():
                text = self.assistant.listen()
                if text:
                    self.after(0, lambda: self._on_voice_input(text))
                self.after(0, self._stop_listening)
            
            threading.Thread(target=listen, daemon=True).start()
    
    def _stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.visualizer.set_state("idle")
        self.voice_button.configure(
            text="🎤 Voice",
            fg_color=Colors.BG_TERTIARY
        )
        self.set_status("Online", Colors.GREEN)
    
    def _on_voice_input(self, text):
        """Handle voice input"""
        # Show what was heard
        self.chat_widget.add_message(text, is_user=True)
        # Process the message
        self._on_message_sent(text)
    
    def _toggle_pin(self):
        """Toggle always-on-top"""
        self.is_pinned = not self.is_pinned
        self.attributes("-topmost", self.is_pinned)
        self.pin_button.configure(
            fg_color=Colors.PRIMARY_DARK if self.is_pinned else Colors.BG_TERTIARY
        )
    
    def _toggle_speaker(self):
        """Toggle text-to-speech on/off"""
        self.tts_enabled = not self.tts_enabled
        self.speaker_button.configure(
            text="🔊 Speaker" if self.tts_enabled else "🔇 Muted",
            fg_color=Colors.PRIMARY_DARK if self.tts_enabled else Colors.BG_TERTIARY
        )
        # Stop any current speech if disabling
        if not self.tts_enabled and self.assistant and hasattr(self.assistant, 'voice'):
            self.assistant.voice.stop_speaking()
    
    def _open_settings(self):
        """Open premium settings dialog"""
        dialog = SettingsDialog(self, assistant=self.assistant)
        self.wait_window(dialog)
        
        # Apply settings if saved
        if dialog.result:
            self.tts_enabled = dialog.result.get("tts_enabled", True)
            self._update_speaker_button()
            
            # Apply always on top
            if dialog.result.get("always_on_top"):
                self.attributes("-topmost", True)
            else:
                self.attributes("-topmost", False)
    
    def _update_speaker_button(self):
        """Update speaker button appearance"""
        self.speaker_button.configure(
            text="🔊 Speaker" if self.tts_enabled else "🔇 Muted",
            fg_color=Colors.PRIMARY_DARK if self.tts_enabled else Colors.BG_TERTIARY
        )
    
    def set_status(self, text, color=Colors.GREEN):
        """Update status indicator"""
        self.status_label.configure(text=text)
        self.status_dot.configure(text_color=color)
    
    def _on_close(self):
        """Handle window close"""
        self.wake_word_active = False  # Stop wake word listening
        self.destroy()



