"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    ═══  GARUN  ═══                            ║
║                                                               ║
║              Your Personal AI Assistant                       ║
║                                                               ║
║  Voice-activated • AI-powered • System control                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Usage:
    python main.py           - Launch Garun with GUI
    python main.py --help    - Show help

Keyboard Shortcuts:
    Ctrl+Shift+G  - Activate voice input
    Escape        - Stop listening

Voice Commands:
    "Hey Garun"   - Wake word to start listening
    "Garun, open Chrome" - Example command
"""

import sys
import os
import argparse
import threading

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """Check if required packages are installed"""
    required = [
        ('customtkinter', 'customtkinter'),
        ('speech_recognition', 'SpeechRecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('requests', 'requests'),
    ]
    
    missing = []
    for import_name, package_name in required:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print("+============================================================+")
        print("|  Missing required packages! Please install them first:     |")
        print("+============================================================+")
        print(f"|  pip install {' '.join(missing):<44} |")
        print("|                                                            |")
        print("|  Or install all dependencies:                              |")
        print("|  pip install -r requirements.txt                           |")
        print("+============================================================+")
        return False
    
    return True


def print_banner():
    """Print the Garun banner"""
    banner = """
    +===============================================================+
    |                                                               |
    |      GGGG    AA    RRRR   U   U  N   N                        |
    |     G       A  A   R   R  U   U  NN  N                        |
    |     G  GG  AAAAAA  RRRR   U   U  N N N                        |
    |     G   G  A    A  R  R   U   U  N  NN                        |
    |      GGGG  A    A  R   R   UUU   N   N                        |
    |                                                               |
    |              Your Personal AI Assistant                       |
    |                                                               |
    +===============================================================+
    """
    print(banner)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Garun - Your Personal AI Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py              Launch Garun with GUI
    python main.py --no-voice   Launch without voice features
    python main.py --cli        Launch in command-line mode
        """
    )
    
    parser.add_argument(
        '--no-voice',
        action='store_true',
        help='Disable voice recognition features'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true', 
        help='Run in command-line mode without GUI'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check dependencies and exit'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    if args.check:
        print("[OK] All dependencies are installed!")
        sys.exit(0)
    
    # CLI mode
    if args.cli:
        run_cli_mode()
        return
    
    # GUI mode
    run_gui_mode(enable_voice=not args.no_voice)


def run_gui_mode(enable_voice=True):
    """Run Garun with graphical interface"""
    print("[Garun] Starting GUI mode...")
    
    try:
        from core.assistant import GarunAssistant
        from ui.main_window import MainWindow
        
        # Initialize assistant
        print("[Garun] Initializing assistant...")
        assistant = GarunAssistant()
        
        # Create and run window
        print("[Garun] Creating window...")
        app = MainWindow(assistant=assistant)
        
        # Register global hotkey if keyboard is available
        try:
            import keyboard
            from config import ACTIVATION_HOTKEY
            
            def on_hotkey():
                app.after(0, app._toggle_voice)
            
            keyboard.add_hotkey(ACTIVATION_HOTKEY, on_hotkey)
            print(f"[Garun] Global hotkey registered: {ACTIVATION_HOTKEY}")
        except ImportError:
            print("[Garun] Note: Install 'keyboard' package for global hotkeys")
        except Exception as e:
            print(f"[Garun] Could not register global hotkey: {e}")
        
        print("[Garun] Ready! Say 'Hey Garun' or press the voice button.")
        print("[Garun] Press Ctrl+Shift+G to activate from anywhere.")
        
        # Run the application
        app.mainloop()
        
        # Cleanup
        assistant.cleanup()
        
    except Exception as e:
        print(f"[Garun] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_cli_mode():
    """Run Garun in command-line mode"""
    print("[Garun] Starting CLI mode...")
    print("[Garun] Type 'quit' or 'exit' to stop.\n")
    
    try:
        from core.assistant import GarunAssistant
        
        assistant = GarunAssistant()
        
        # Greeting
        greeting = assistant.get_greeting()
        print(f"Garun: {greeting}\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("Garun: Goodbye! Have a great day!")
                    break
                
                # Process message
                response = assistant.process_message(user_input)
                print(f"Garun: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nGarun: Goodbye!")
                break
        
        assistant.cleanup()
        
    except Exception as e:
        print(f"[Garun] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
