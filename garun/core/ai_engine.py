"""
Garun AI Assistant - Multi-Provider AI Engine
==============================================
Supports multiple AI providers for intelligent conversations:
- Google Gemini (Free tier available)
- OpenAI GPT-4/GPT-3.5
- Groq (Llama 3 - Fast & Free)
"""

import os
from config import (
    SYSTEM_PROMPT, AI_MAX_TOKENS, AI_TEMPERATURE,
    GROQ_API_KEY, AI_MODEL
)

# Try to import optional AI libraries
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("[Garun AI] Groq library not installed. Install with: pip install groq")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIEngine:
    """
    Multi-provider AI Engine for Garun.
    Supports: Groq (Llama 3), Google Gemini, OpenAI GPT-4
    """
    
    # Available providers and their models
    PROVIDERS = {
        "groq": {
            "name": "Groq",
            "models": [
                "openai/gpt-oss-20b",
                "llama-3.1-70b-versatile",
                "mixtral-8x7b-32768"
            ],
            "default_model": "openai/gpt-oss-20b",
            "free": True
        },
        "gemini": {
            "name": "Google Gemini",
            "models": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
            "default_model": "gemini-1.5-flash",
            "free": True
        },
        "openai": {
            "name": "OpenAI GPT",
            "models": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            "default_model": "gpt-4o-mini",
            "free": False
        }
    }
    
    def __init__(self, provider="groq", api_key=None, model=None):
        """
        Initialize AI Engine with specified provider.
        
        Args:
            provider: AI provider ("groq", "gemini", "openai")
            api_key: API key for the provider
            model: Specific model to use (optional)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model
        self.client = None
        self.conversation_history = []
        self.max_history = 20
        
        # Auto-detect API keys from environment
        self._load_api_keys()
        
        # Initialize the selected provider
        self._initialize_provider()
    
    def _load_api_keys(self):
        """Load API keys from environment or config"""
        if not self.api_key:
            if self.provider == "groq":
                self.api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY")
            elif self.provider == "gemini":
                self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            elif self.provider == "openai":
                self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Set default model if not specified
        if not self.model and self.provider in self.PROVIDERS:
            self.model = self.PROVIDERS[self.provider]["default_model"]
    
    def _initialize_provider(self):
        """Initialize the selected AI provider"""
        if not self.api_key:
            print(f"[Garun AI] No API key for {self.provider}. AI features disabled.")
            return
        
        try:
            if self.provider == "groq":
                self._init_groq()
            elif self.provider == "gemini":
                self._init_gemini()
            elif self.provider == "openai":
                self._init_openai()
            else:
                print(f"[Garun AI] Unknown provider: {self.provider}")
        except Exception as e:
            print(f"[Garun AI] Failed to initialize {self.provider}: {e}")
            self.client = None
    
    def _init_groq(self):
        """Initialize Groq client"""
        if not GROQ_AVAILABLE:
            print("[Garun AI] Groq not available. Install: pip install groq")
            return
        
        self.client = Groq(api_key=self.api_key)
        print(f"[Garun AI] Groq initialized with {self.model}")
    
    def _init_gemini(self):
        """Initialize Google Gemini client"""
        if not GEMINI_AVAILABLE:
            print("[Garun AI] Gemini not available. Install: pip install google-generativeai")
            return
        
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=SYSTEM_PROMPT
        )
        print(f"[Garun AI] Gemini initialized with {self.model}")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        if not OPENAI_AVAILABLE:
            print("[Garun AI] OpenAI not available. Install: pip install openai")
            return
        
        self.client = OpenAI(api_key=self.api_key)
        print(f"[Garun AI] OpenAI initialized with {self.model}")
    
    def set_provider(self, provider, api_key=None, model=None):
        """Switch to a different AI provider"""
        self.provider = provider.lower()
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = None
        self.model = model
        self._load_api_keys()
        self._initialize_provider()
    
    def set_api_key(self, api_key):
        """Set or update the API key"""
        self.api_key = api_key
        self._initialize_provider()
    
    def is_available(self):
        """Check if AI is available"""
        return self.client is not None
    
    def get_provider_info(self):
        """Get information about current provider"""
        if self.provider in self.PROVIDERS:
            info = self.PROVIDERS[self.provider].copy()
            info["current_model"] = self.model
            info["is_available"] = self.is_available()
            return info
        return None
    
    def chat(self, message, context=None):
        """
        Send a message and get AI response.
        Routes to the appropriate provider.
        
        Args:
            message: User message
            context: Optional additional context
            
        Returns:
            AI response text
        """
        if not self.is_available():
            return self._get_fallback_response(message)
        
        try:
            if self.provider == "groq":
                return self._chat_groq(message, context)
            elif self.provider == "gemini":
                return self._chat_gemini(message, context)
            elif self.provider == "openai":
                return self._chat_openai(message, context)
            else:
                return self._get_fallback_response(message)
        except Exception as e:
            print(f"[Garun AI] Chat error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _chat_groq(self, message, context=None):
        """Chat using Groq API"""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=AI_MAX_TOKENS,
            temperature=AI_TEMPERATURE
        )
        
        ai_response = response.choices[0].message.content
        self._update_history(message, ai_response)
        return ai_response
    
    def _chat_gemini(self, message, context=None):
        """Chat using Google Gemini API"""
        # Build conversation for Gemini
        full_message = message
        if context:
            full_message = f"[Context: {context}]\n\n{message}"
        
        # Gemini uses chat sessions
        chat = self.client.start_chat(history=[])
        
        # Add conversation history
        for msg in self.conversation_history:
            if msg["role"] == "user":
                chat.history.append({"role": "user", "parts": [msg["content"]]})
            else:
                chat.history.append({"role": "model", "parts": [msg["content"]]})
        
        response = chat.send_message(full_message)
        ai_response = response.text
        
        self._update_history(message, ai_response)
        return ai_response
    
    def _chat_openai(self, message, context=None):
        """Chat using OpenAI API"""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=AI_MAX_TOKENS,
            temperature=AI_TEMPERATURE
        )
        
        ai_response = response.choices[0].message.content
        self._update_history(message, ai_response)
        return ai_response
    
    def _update_history(self, user_message, ai_response):
        """Update conversation history"""
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Trim history if too long
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def _get_fallback_response(self, message):
        """
        Get a fallback response when AI is not available.
        Supports English, Hindi, and Hinglish.
        """
        message_lower = message.lower()
        
        # Try math first
        math_result = self._try_math(message)
        if math_result:
            return math_result
        
        # Hindi/Hinglish greetings
        if any(word in message_lower for word in ['namaste', 'namaskar', 'pranam']):
            return "Namaste! Main Garun hoon, aapka personal AI assistant. Kaise madad kar sakta hoon?"
        
        if any(word in message_lower for word in ['kaise ho', 'kya haal', 'kaisa hai']):
            return "Main bilkul badhiya hoon! Aap batao, kya help chahiye?"
        
        if any(word in message_lower for word in ['shukriya', 'dhanyawad']):
            return "Are koi baat nahi! Kabhi bhi help chahiye ho, bol dena."
        
        # English greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm Garun, your AI assistant. How can I help you?"
        
        if 'how are you' in message_lower:
            return "I'm doing great! How can I assist you?"
        
        if any(word in message_lower for word in ['help', 'what can you do']):
            return ("I can help with:\n"
                   "• Opening apps: 'open chrome'\n"
                   "• Math: 'what is 2+3'\n"
                   "• Weather: 'what's the weather'\n"
                   "• News: 'tell me the news'\n\n"
                   "For smart AI conversations, add your API key!")
        
        if 'thank' in message_lower:
            return "You're welcome! / Koi baat nahi!"
        
        if 'bye' in message_lower or 'alvida' in message_lower:
            return "Goodbye! / Alvida! Jab zarurat ho, bula lena."
        
        # Default response
        return ("Main Garun hoon! / I'm Garun!\n\n"
               "Try: 'open chrome', 'mausam batao', 'what is 2+3'\n\n"
               "🔑 Add API key for smart conversations:\n"
               "• Groq (Free): console.groq.com\n"
               "• Gemini (Free): aistudio.google.com")
    
    def _try_math(self, message):
        """Try to evaluate math expressions"""
        import re
        message_lower = message.lower()
        
        math_keywords = ['what is', 'calculate', 'compute', '+', '-', '*', '/', 'plus', 'minus', 'times']
        if not any(kw in message_lower for kw in math_keywords):
            return None
        
        expr = message_lower
        for word in ['what is', 'calculate', 'compute', 'solve']:
            expr = expr.replace(word, '')
        
        expr = expr.replace('plus', '+').replace('minus', '-')
        expr = expr.replace('times', '*').replace('divided by', '/')
        expr = expr.replace('x', '*').replace('?', '')
        expr = re.sub(r'[^0-9+\-*/().\s]', '', expr).strip()
        
        if not expr:
            return None
        
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            if isinstance(result, float) and result == int(result):
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 4)
            return f"The answer is {result}"
        except:
            return None
    
    def analyze_intent(self, message):
        """Analyze the intent of a message for command routing"""
        message_lower = message.lower()
        
        # System commands
        if any(word in message_lower for word in ['open', 'launch', 'start', 'run', 'kholo', 'chalu']):
            return {"type": "system_control", "action": "open_app"}
        
        if any(word in message_lower for word in ['search', 'find', 'dhundho', 'khojo']):
            if 'file' in message_lower or 'document' in message_lower:
                return {"type": "system_control", "action": "search_files"}
            return {"type": "web_search"}
        
        if any(word in message_lower for word in ['volume', 'mute', 'unmute', 'louder', 'quieter', 'awaz']):
            return {"type": "system_control", "action": "volume"}
        
        # Information
        if any(word in message_lower for word in ['weather', 'mausam', 'temperature', 'tapman']):
            return {"type": "weather"}
        
        if any(word in message_lower for word in ['news', 'headlines', 'samachar', 'khabar']):
            return {"type": "news"}
        
        if any(word in message_lower for word in ['time', 'samay', 'waqt', 'baje']):
            return {"type": "time"}
        
        if any(word in message_lower for word in ['date', 'tarikh', 'din']):
            return {"type": "date"}
        
        # Reminders
        if any(word in message_lower for word in ['remind', 'reminder', 'yaad']):
            return {"type": "reminder"}
        
        # Math
        math_keywords = ['what is', 'calculate', '+', '-', '*', '/', 'plus', 'minus', 'kitna']
        if any(kw in message_lower for kw in math_keywords):
            import re
            if re.search(r'\d', message):
                return {"type": "math"}
        
        # Default to conversation
        return {"type": "conversation"}


# Utility function to list available providers
def get_available_providers():
    """Get list of available AI providers"""
    available = []
    if GROQ_AVAILABLE:
        available.append("groq")
    if GEMINI_AVAILABLE:
        available.append("gemini")
    if OPENAI_AVAILABLE:
        available.append("openai")
    return available
