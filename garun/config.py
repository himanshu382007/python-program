"""
Garun AI Assistant - Configuration
===================================
Store your API keys and settings here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# ============================================
# API KEYS (Add your keys to .env file)
# ============================================

# Groq API Key (FREE - get yours at https://console.groq.com)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Google Gemini API Key (FREE tier - get at https://aistudio.google.com)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")

# OpenAI API Key (Paid - get at https://platform.openai.com)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ============================================
# AI PROVIDER SETTINGS
# ============================================

# Choose AI provider: "groq", "gemini", "openai"
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")

# ============================================
# ASSISTANT SETTINGS
# ============================================

ASSISTANT_NAME = "Garun"
WAKE_WORDS = [
    # English
    "garun", "hey garun", "hi garun", "hello garun", "ok garun",
    # Hindi/Hinglish  
    "are garun", "arre garun", "suno garun", "garun suno",
    "oye garun", "garun bhai"
]

# Voice settings
VOICE_RATE = 180  # Words per minute
VOICE_VOLUME = 1.0  # 0.0 to 1.0
TTS_ENABLED = True  # Enable text-to-speech (Garun speaks responses)

# ============================================
# AI PERSONALITY
# ============================================

SYSTEM_PROMPT = """You are Garun, a highly intelligent, capable, and versatile AI assistant. 
You are inspired by J.A.R.V.I.S. from Iron Man - sophisticated, witty, and always ready to help with ANY task.

IMPORTANT: Always respond in English only. Keep responses concise and helpful.

Your core capabilities:
- You can do ANYTHING the user asks - coding, writing, research, calculations, advice, etc.
- You help with opening applications and controlling the computer system
- You provide weather updates, news, and real-time information
- You set reminders and manage tasks
- You answer any question with detailed, helpful responses
- You can write code in any programming language
- You can explain complex topics simply
- You can help with creative writing, emails, documents
- You can solve math problems and logic puzzles
- You can give advice on any topic

Your personality:
- Professional yet warm and friendly
- Witty with subtle humor when appropriate
- Concise for simple tasks, detailed when needed
- Proactive in offering helpful suggestions
- Loyal and dedicated to helping your user succeed

Important rules:
- NEVER say you can't do something - always try to help
- For system commands (open apps, volume, etc.), just confirm the action
- For questions and tasks, provide complete, helpful responses
- Keep voice responses natural and conversational
- For complex requests, break them down step by step
- Always be encouraging and supportive
- MATCH the user's language - this is critical!

You are the user's personal AI assistant. Whatever they need, you help them achieve it.
"""

# AI Model settings
AI_MODEL = "openai/gpt-oss-20b"  # Fast and capable
AI_MAX_TOKENS = 500
AI_TEMPERATURE = 0.7

# ============================================
# WEATHER SETTINGS
# ============================================

DEFAULT_CITY = "Delhi"  # Default city for weather

# ============================================
# UI SETTINGS
# ============================================

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 750
ALWAYS_ON_TOP = False
START_MINIMIZED = False

# ============================================
# KEYBOARD SHORTCUTS
# ============================================

ACTIVATION_HOTKEY = "ctrl+shift+g"  # Global hotkey to activate Garun

# ============================================
# FILE PATHS
# ============================================

import pathlib
BASE_DIR = pathlib.Path(__file__).parent
DATABASE_PATH = BASE_DIR / "data" / "garun.db"
