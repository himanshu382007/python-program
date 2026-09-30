# Garun AI Assistant

<div align="center">

```
    ██████╗  █████╗ ██████╗ ██╗   ██╗███╗   ██╗
   ██╔════╝ ██╔══██╗██╔══██╗██║   ██║████╗  ██║
   ██║  ███╗███████║█  ███╔╝██║   ██║██╔██╗ ██║
   ██║   ██║██╔══██║██╔══██╗██║   ██║██║╚██╗██║
   ╚██████╔╝██║  ██║██║  ██║╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

**Your Personal AI Assistant**

*Voice-activated • AI-powered • System control*

</div>

---

## ✨ Features

- 🎤 **Voice Activation** - Say "Hey Garun" to wake
- 💬 **AI Conversations** - Powered by Groq (free!)
- 🖥️ **System Control** - Open apps, search files, control volume
- 🌤️ **Weather Updates** - Real-time weather information
- 📰 **News Headlines** - Stay updated with latest news
- ⏰ **Reminders** - Set reminders with natural language
- 🏠 **Smart Home** - Control your smart devices

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up AI (Optional but Recommended)

Get your **FREE** Groq API key:
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up (no credit card needed)
3. Create an API key
4. Add it to `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### 3. Run Garun

```bash
# Using Python
python main.py

# Or double-click
run_garun.bat
```

---

## 🎮 How to Use

### Voice Commands
| Say This | Garun Does |
|----------|------------|
| "Hey Garun, open Chrome" | Opens Google Chrome |
| "What's the weather in Delhi?" | Shows weather info |
| "Open calculator" | Opens Calculator |
| "Remind me to call mom at 5 PM" | Sets a reminder |
| "Tell me the news" | Reads headlines |
| "Lock the screen" | Locks Windows |
| "Volume up" | Increases volume |

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+G` | Activate voice input (global) |
| `Escape` | Stop listening |

### Text Input
Just type in the chat box and press Enter!

---

## 📁 Project Structure

```
garun/
├── main.py              # Entry point
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── core/
│   ├── assistant.py     # Main assistant logic
│   ├── voice.py         # Speech recognition & TTS
│   ├── ai_engine.py     # Groq AI integration
│   └── commands.py      # Command processor
├── features/
│   ├── system_control.py
│   ├── weather.py
│   ├── news.py
│   ├── reminders.py
│   └── smart_home.py
└── ui/
    ├── main_window.py   # Main GUI
    ├── chat_widget.py   # Chat interface
    ├── visualizer.py    # Voice visualizer
    └── themes.py        # Cyberpunk theme
```

---

## ⚙️ Configuration

Edit `config.py` to customize:
- Assistant name and wake words
- Voice speed and volume
- Default city for weather
- AI personality and model

---

## 🤝 Extending Garun

### Adding New Commands
Edit `core/commands.py` to add new command patterns.

### Adding Smart Home Devices
Extend `features/smart_home.py` with your device integrations.

---

## 📝 License

This project is created for personal use. Feel free to modify and extend!

---

<div align="center">

**Made with ❤️ by You**

*Inspired by J.A.R.V.I.S.*

</div>
