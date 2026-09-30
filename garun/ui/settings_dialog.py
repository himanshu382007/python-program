"""
Garun AI Assistant - Settings Dialog
=====================================
Modern settings UI for configuring AI providers, API keys, and preferences
"""

import customtkinter as ctk
from ui.themes import Colors, Fonts, Dimensions
import os
from pathlib import Path


class SettingsDialog(ctk.CTkToplevel):
    """Premium settings dialog with AI provider configuration"""
    
    def __init__(self, parent, assistant=None):
        super().__init__(parent)
        
        self.assistant = assistant
        self.result = None
        
        # Window setup
        self.title("⚙️ Garun Settings")
        self.geometry("500x650")
        self.configure(fg_color=Colors.BG_DARK)
        self.resizable(False, False)
        
        # Center on parent
        self.transient(parent)
        self.grab_set()
        
        # Create UI
        self._create_widgets()
        self._load_current_settings()
        
        # Focus
        self.after(100, self.focus_force)
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        self._create_header(main_frame)
        
        # Scrollable content
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            scrollbar_button_color=Colors.PRIMARY,
            scrollbar_button_hover_color=Colors.PRIMARY_GLOW
        )
        scroll_frame.pack(fill="both", expand=True, pady=(15, 0))
        
        # Sections
        self._create_ai_section(scroll_frame)
        self._create_voice_section(scroll_frame)
        self._create_appearance_section(scroll_frame)
        
        # Footer buttons
        self._create_footer(main_frame)
    
    def _create_header(self, parent):
        """Create header with title"""
        header = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="⚙️ Settings",
            font=ctk.CTkFont(family=Fonts.HEADING, size=24, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(side="left")
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            header,
            text="Configure your AI assistant",
            font=ctk.CTkFont(family=Fonts.BODY, size=12),
            text_color=Colors.TEXT_MUTED
        )
        subtitle.pack(side="left", padx=(15, 0), pady=(5, 0))
    
    def _create_section_header(self, parent, icon, title):
        """Create a section header"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(20, 10), padx=15)
        
        label = ctk.CTkLabel(
            header,
            text=f"{icon} {title}",
            font=ctk.CTkFont(family=Fonts.HEADING, size=16, weight="bold"),
            text_color=Colors.PRIMARY
        )
        label.pack(side="left")
        
        # Divider line
        divider = ctk.CTkFrame(parent, fg_color=Colors.BORDER, height=1)
        divider.pack(fill="x", padx=15)
    
    def _create_ai_section(self, parent):
        """Create AI provider settings section"""
        self._create_section_header(parent, "🧠", "AI Provider")
        
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        
        # Provider selection
        provider_frame = ctk.CTkFrame(content, fg_color="transparent")
        provider_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            provider_frame,
            text="Active Provider",
            font=ctk.CTkFont(family=Fonts.BODY, size=13),
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w")
        
        self.provider_var = ctk.StringVar(value="groq")
        self.provider_menu = ctk.CTkOptionMenu(
            provider_frame,
            variable=self.provider_var,
            values=["groq", "gemini", "openai"],
            font=ctk.CTkFont(family=Fonts.BODY, size=13),
            fg_color=Colors.BG_TERTIARY,
            button_color=Colors.PRIMARY,
            button_hover_color=Colors.PRIMARY_GLOW,
            dropdown_fg_color=Colors.BG_TERTIARY,
            dropdown_hover_color=Colors.PRIMARY,
            width=200,
            command=self._on_provider_change
        )
        self.provider_menu.pack(anchor="w", pady=(5, 0))
        
        # Provider info
        self.provider_info = ctk.CTkLabel(
            provider_frame,
            text="",
            font=ctk.CTkFont(family=Fonts.BODY, size=11),
            text_color=Colors.TEXT_MUTED,
            wraplength=400
        )
        self.provider_info.pack(anchor="w", pady=(5, 0))
        
        # API Key inputs
        self._create_api_key_inputs(content)
        
        # Test connection button
        self.test_btn = ctk.CTkButton(
            content,
            text="🔄 Test Connection",
            font=ctk.CTkFont(family=Fonts.BODY, size=13),
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.PRIMARY,
            text_color=Colors.TEXT_PRIMARY,
            height=35,
            width=150,
            command=self._test_connection
        )
        self.test_btn.pack(anchor="w", pady=(15, 0))
        
        self.test_result = ctk.CTkLabel(
            content,
            text="",
            font=ctk.CTkFont(family=Fonts.BODY, size=12),
            text_color=Colors.GREEN
        )
        self.test_result.pack(anchor="w", pady=(5, 0))
    
    def _create_api_key_inputs(self, parent):
        """Create API key input fields"""
        keys_frame = ctk.CTkFrame(parent, fg_color="transparent")
        keys_frame.pack(fill="x", pady=(15, 0))
        
        # Groq API Key
        groq_frame = ctk.CTkFrame(keys_frame, fg_color="transparent")
        groq_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            groq_frame,
            text="Groq API Key",
            font=ctk.CTkFont(family=Fonts.BODY, size=12),
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w")
        
        self.groq_key = ctk.CTkEntry(
            groq_frame,
            placeholder_text="gsk_... (get free at console.groq.com)",
            font=ctk.CTkFont(family=Fonts.MONO, size=12),
            fg_color=Colors.BG_TERTIARY,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_PRIMARY,
            height=38,
            show="•"
        )
        self.groq_key.pack(fill="x", pady=(3, 0))
        
        # Gemini API Key
        gemini_frame = ctk.CTkFrame(keys_frame, fg_color="transparent")
        gemini_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            gemini_frame,
            text="Gemini API Key",
            font=ctk.CTkFont(family=Fonts.BODY, size=12),
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w")
        
        self.gemini_key = ctk.CTkEntry(
            gemini_frame,
            placeholder_text="AIza... (get free at aistudio.google.com)",
            font=ctk.CTkFont(family=Fonts.MONO, size=12),
            fg_color=Colors.BG_TERTIARY,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_PRIMARY,
            height=38,
            show="•"
        )
        self.gemini_key.pack(fill="x", pady=(3, 0))
        
        # OpenAI API Key
        openai_frame = ctk.CTkFrame(keys_frame, fg_color="transparent")
        openai_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            openai_frame,
            text="OpenAI API Key",
            font=ctk.CTkFont(family=Fonts.BODY, size=12),
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w")
        
        self.openai_key = ctk.CTkEntry(
            openai_frame,
            placeholder_text="sk-... (paid, platform.openai.com)",
            font=ctk.CTkFont(family=Fonts.MONO, size=12),
            fg_color=Colors.BG_TERTIARY,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_PRIMARY,
            height=38,
            show="•"
        )
        self.openai_key.pack(fill="x", pady=(3, 0))
    
    def _create_voice_section(self, parent):
        """Create voice settings section"""
        self._create_section_header(parent, "🎤", "Voice & Speech")
        
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        
        # TTS Enabled
        tts_frame = ctk.CTkFrame(content, fg_color="transparent")
        tts_frame.pack(fill="x", pady=5)
        
        self.tts_var = ctk.BooleanVar(value=True)
        tts_switch = ctk.CTkSwitch(
            tts_frame,
            text="Text-to-Speech Enabled",
            variable=self.tts_var,
            font=ctk.CTkFont(family=Fonts.BODY, size=13),
            text_color=Colors.TEXT_PRIMARY,
            progress_color=Colors.PRIMARY,
            button_color=Colors.TEXT_PRIMARY,
            button_hover_color=Colors.PRIMARY_GLOW
        )
        tts_switch.pack(anchor="w")
        
        # Voice Speed
        speed_frame = ctk.CTkFrame(content, fg_color="transparent")
        speed_frame.pack(fill="x", pady=(15, 5))
        
        ctk.CTkLabel(
            speed_frame,
            text="Voice Speed",
            font=ctk.CTkFont(family=Fonts.BODY, size=12),
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w")
        
        self.speed_slider = ctk.CTkSlider(
            speed_frame,
            from_=100,
            to=250,
            number_of_steps=15,
            progress_color=Colors.PRIMARY,
            button_color=Colors.TEXT_PRIMARY,
            button_hover_color=Colors.PRIMARY_GLOW,
            fg_color=Colors.BG_TERTIARY
        )
        self.speed_slider.set(180)
        self.speed_slider.pack(fill="x", pady=(5, 0))
        
        speed_labels = ctk.CTkFrame(speed_frame, fg_color="transparent")
        speed_labels.pack(fill="x")
        ctk.CTkLabel(speed_labels, text="Slow", font=ctk.CTkFont(size=10), text_color=Colors.TEXT_MUTED).pack(side="left")
        ctk.CTkLabel(speed_labels, text="Fast", font=ctk.CTkFont(size=10), text_color=Colors.TEXT_MUTED).pack(side="right")
    
    def _create_appearance_section(self, parent):
        """Create appearance settings section"""
        self._create_section_header(parent, "🎨", "Appearance")
        
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        
        # Always on top
        self.ontop_var = ctk.BooleanVar(value=False)
        ontop_switch = ctk.CTkSwitch(
            content,
            text="Always on Top",
            variable=self.ontop_var,
            font=ctk.CTkFont(family=Fonts.BODY, size=13),
            text_color=Colors.TEXT_PRIMARY,
            progress_color=Colors.PRIMARY,
            button_color=Colors.TEXT_PRIMARY,
            button_hover_color=Colors.PRIMARY_GLOW
        )
        ontop_switch.pack(anchor="w", pady=5)
        
        # Start minimized
        self.minimized_var = ctk.BooleanVar(value=False)
        minimized_switch = ctk.CTkSwitch(
            content,
            text="Start Minimized",
            variable=self.minimized_var,
            font=ctk.CTkFont(family=Fonts.BODY, size=13),
            text_color=Colors.TEXT_PRIMARY,
            progress_color=Colors.PRIMARY,
            button_color=Colors.TEXT_PRIMARY,
            button_hover_color=Colors.PRIMARY_GLOW
        )
        minimized_switch.pack(anchor="w", pady=5)
    
    def _create_footer(self, parent):
        """Create footer with action buttons"""
        footer = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        footer.pack(fill="x", pady=(15, 0))
        footer.pack_propagate(False)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            footer,
            text="Cancel",
            font=ctk.CTkFont(family=Fonts.BODY, size=14),
            fg_color="transparent",
            hover_color=Colors.BG_TERTIARY,
            text_color=Colors.TEXT_SECONDARY,
            border_width=1,
            border_color=Colors.BORDER,
            height=42,
            width=100,
            command=self._on_cancel
        )
        cancel_btn.pack(side="left")
        
        # Save button
        save_btn = ctk.CTkButton(
            footer,
            text="💾 Save Settings",
            font=ctk.CTkFont(family=Fonts.BODY, size=14, weight="bold"),
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_GLOW,
            text_color=Colors.BG_DARK,
            height=42,
            width=150,
            command=self._on_save
        )
        save_btn.pack(side="right")
    
    def _load_current_settings(self):
        """Load current settings into UI"""
        from config import (
            AI_PROVIDER, GROQ_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY,
            TTS_ENABLED, VOICE_RATE, ALWAYS_ON_TOP, START_MINIMIZED
        )
        
        # AI Provider
        self.provider_var.set(AI_PROVIDER)
        self._update_provider_info()
        
        # API Keys (show masked if present)
        if GROQ_API_KEY:
            self.groq_key.insert(0, GROQ_API_KEY)
        if GEMINI_API_KEY:
            self.gemini_key.insert(0, GEMINI_API_KEY)
        if OPENAI_API_KEY:
            self.openai_key.insert(0, OPENAI_API_KEY)
        
        # Voice settings
        self.tts_var.set(TTS_ENABLED)
        self.speed_slider.set(VOICE_RATE)
        
        # Appearance
        self.ontop_var.set(ALWAYS_ON_TOP)
        self.minimized_var.set(START_MINIMIZED)
    
    def _on_provider_change(self, value):
        """Handle provider change"""
        self._update_provider_info()
    
    def _update_provider_info(self):
        """Update provider info text"""
        provider = self.provider_var.get()
        info_map = {
            "groq": "⚡ Groq: Fast Llama 3 models. FREE with generous limits!",
            "gemini": "✨ Gemini: Google's AI. FREE tier available.",
            "openai": "🔥 OpenAI: GPT-4 models. Paid, highest quality."
        }
        self.provider_info.configure(text=info_map.get(provider, ""))
    
    def _test_connection(self):
        """Test AI connection"""
        provider = self.provider_var.get()
        api_key = {
            "groq": self.groq_key.get(),
            "gemini": self.gemini_key.get(),
            "openai": self.openai_key.get()
        }.get(provider, "")
        
        if not api_key or api_key.startswith("•"):
            self.test_result.configure(text="⚠️ Enter API key first", text_color=Colors.YELLOW)
            return
        
        self.test_result.configure(text="🔄 Testing...", text_color=Colors.TEXT_MUTED)
        self.update()
        
        try:
            from core.ai_engine import AIEngine
            test_ai = AIEngine(provider=provider, api_key=api_key)
            
            if test_ai.is_available():
                response = test_ai.chat("Say 'Hello!' in one word")
                if response and len(response) > 0:
                    self.test_result.configure(text="✅ Connected successfully!", text_color=Colors.GREEN)
                else:
                    self.test_result.configure(text="⚠️ Connected but no response", text_color=Colors.YELLOW)
            else:
                self.test_result.configure(text="❌ Failed to connect", text_color=Colors.RED)
        except Exception as e:
            self.test_result.configure(text=f"❌ Error: {str(e)[:50]}", text_color=Colors.RED)
    
    def _on_save(self):
        """Save settings"""
        try:
            self._save_to_env_file()
            self.result = {
                "provider": self.provider_var.get(),
                "tts_enabled": self.tts_var.get(),
                "voice_rate": int(self.speed_slider.get()),
                "always_on_top": self.ontop_var.get(),
                "start_minimized": self.minimized_var.get()
            }
            self.destroy()
        except Exception as e:
            print(f"[Settings] Error saving: {e}")
    
    def _save_to_env_file(self):
        """Save API keys to .env file"""
        from config import BASE_DIR
        env_path = BASE_DIR / ".env"
        
        # Build env content
        lines = [
            "# Garun AI Assistant Configuration",
            f"AI_PROVIDER={self.provider_var.get()}",
            ""
        ]
        
        groq_key = self.groq_key.get()
        if groq_key and not groq_key.startswith("•"):
            lines.append(f"GROQ_API_KEY={groq_key}")
        
        gemini_key = self.gemini_key.get()
        if gemini_key and not gemini_key.startswith("•"):
            lines.append(f"GEMINI_API_KEY={gemini_key}")
        
        openai_key = self.openai_key.get()
        if openai_key and not openai_key.startswith("•"):
            lines.append(f"OPENAI_API_KEY={openai_key}")
        
        # Write to file
        with open(env_path, "w") as f:
            f.write("\n".join(lines))
        
        print(f"[Settings] Saved to {env_path}")
    
    def _on_cancel(self):
        """Cancel and close"""
        self.result = None
        self.destroy()
