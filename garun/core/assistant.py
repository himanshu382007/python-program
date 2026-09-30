"""
Garun AI Assistant - Main Assistant Class
==========================================
Coordinates all components of the assistant
"""

from core.voice import VoiceEngine
from core.ai_engine import AIEngine, get_available_providers
from core.commands import CommandProcessor
from features.system_control import SystemControl
from features.weather import WeatherService
from features.news import NewsService
from features.reminders import ReminderService
from features.smart_home import SmartHomeController
from config import AI_PROVIDER, GROQ_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY


class GarunAssistant:
    """Main assistant class that coordinates all components"""
    
    def __init__(self):
        print("[Garun] Initializing Garun AI Assistant...")
        
        # Initialize features
        self.features = {
            "system": SystemControl(),
            "weather": WeatherService(),
            "news": NewsService(),
            "reminders": ReminderService(),
            "smart_home": SmartHomeController()
        }
        
        # Initialize core components
        self.voice = VoiceEngine()
        
        # Initialize AI with multi-provider support
        self._init_ai_engine()
        
        self.commands = CommandProcessor(self.features)
        
        print("[Garun] Assistant initialized successfully!")
    
    def _init_ai_engine(self):
        """Initialize AI engine with the best available provider"""
        # Get API key for configured provider
        api_key = self._get_api_key(AI_PROVIDER)
        
        if api_key:
            self.ai = AIEngine(provider=AI_PROVIDER, api_key=api_key)
        else:
            # Try other providers if primary isn't configured
            self.ai = self._fallback_ai_provider()
    
    def _get_api_key(self, provider):
        """Get API key for specified provider"""
        keys = {
            "groq": GROQ_API_KEY,
            "gemini": GEMINI_API_KEY,
            "openai": OPENAI_API_KEY
        }
        return keys.get(provider.lower(), "")
    
    def _fallback_ai_provider(self):
        """Try to find any available AI provider"""
        providers_to_try = ["groq", "gemini", "openai"]
        
        for provider in providers_to_try:
            api_key = self._get_api_key(provider)
            if api_key:
                print(f"[Garun] Using fallback provider: {provider}")
                return AIEngine(provider=provider, api_key=api_key)
        
        # No API keys configured, use fallback-only engine
        print("[Garun] No AI API keys configured. Using fallback mode.")
        return AIEngine(provider="groq")
    
    def process_message(self, message):
        """
        Process a text message and return response.
        
        Args:
            message: User message
            
        Returns:
            Response string
        """
        if not message:
            return "I didn't catch that. Could you please repeat?"
        
        return self.commands.process(message)
    
    def listen(self):
        """
        Listen for voice input.
        
        Returns:
            Recognized text or None
        """
        return self.voice.listen()
    
    def speak(self, text):
        """
        Speak text out loud.
        
        Args:
            text: Text to speak
        """
        self.voice.speak(text)
    
    def speak_sync(self, text):
        """
        Speak text synchronously (blocking).
        
        Args:
            text: Text to speak
        """
        self.voice.speak_sync(text)
    
    def set_api_key(self, api_key, provider=None):
        """
        Set API key for AI provider.
        
        Args:
            api_key: API key
            provider: Provider name (optional, uses current if not specified)
        """
        if provider:
            self.ai.set_provider(provider, api_key)
        else:
            self.ai.set_api_key(api_key)
        self.commands.ai_engine.set_api_key(api_key)
    
    def set_provider(self, provider, api_key=None):
        """
        Switch AI provider.
        
        Args:
            provider: Provider name ("groq", "gemini", "openai")
            api_key: Optional API key
        """
        if not api_key:
            api_key = self._get_api_key(provider)
        self.ai.set_provider(provider, api_key)
    
    def get_current_provider(self):
        """Get current AI provider info"""
        return self.ai.get_provider_info()
    
    def get_available_providers(self):
        """Get list of available AI providers"""
        return get_available_providers()
    
    def is_ai_available(self):
        """Check if AI is available"""
        return self.ai.is_available()
    
    def get_greeting(self):
        """Get a greeting message"""
        from datetime import datetime
        hour = datetime.now().hour
        
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        provider_info = self.ai.get_provider_info()
        if provider_info and provider_info.get("is_available"):
            provider_name = provider_info.get("name", "AI")
            return f"{greeting}! I'm Garun powered by {provider_name}. How can I help you?"
        
        return f"{greeting}! I'm Garun, your personal AI assistant. How can I help you today?"
    
    def cleanup(self):
        """Cleanup resources"""
        self.voice.cleanup()
        self.features["reminders"].close()
        print("[Garun] Cleanup complete. Goodbye!")

