"""
Garun AI Assistant - WhatsApp Controller
=========================================
Make calls and send messages via WhatsApp Web / Desktop
"""

import webbrowser
import urllib.parse
import json
import time
import threading
import os
import re
from pathlib import Path

# Try to import pyautogui for automation
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import pygetwindow as gw
    GW_AVAILABLE = True
except ImportError:
    GW_AVAILABLE = False


class WhatsAppController:
    """
    Control WhatsApp for calling and messaging.
    Uses WhatsApp Desktop shortcuts via PyAutoGUI.
    """
    
    def __init__(self):
        # Paths
        self.base_dir = Path(__file__).parent.parent
        self.contacts_file = self.base_dir / "data" / "contacts.json"
        self.log_file = self.base_dir / "logs" / "whatsapp_debug.log"
        
        # Load contacts
        self.contacts = self._load_contacts()
        self.is_automating = False
        
        # Ensure logs dir exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _log(self, message):
        """Write to debug log file"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except:
            pass
        print(f"[WhatsApp] {message}")

    def _load_contacts(self):
        """Load contacts from file"""
        if self.contacts_file.exists():
            try:
                with open(self.contacts_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_contacts(self):
        """Save contacts to file"""
        self.contacts_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.contacts_file, "w") as f:
            json.dump(self.contacts, f, indent=2)
    
    def add_contact(self, name, phone):
        """Add a contact with robust cleaning"""
        # Remove all except digits and plus
        phone = re.sub(r'[^\d+]', '', phone)
        
        if not phone.startswith("+"):
            phone = "+91" + phone  # Default to India
        
        self.contacts[name.lower()] = phone
        self._save_contacts()
        self._log(f"Added contact: {name} -> {phone}")
        return f"Contact '{name}' saved with number {phone}"
    
    def _log_windows(self):
        """Log all open window titles for debugging"""
        if not GW_AVAILABLE:
            self._log("PyGetWindow not available for window logging")
            return
        try:
            titles = [w.title for w in gw.getAllWindows() if w.title.strip()]
            self._log(f"All active windows: {', '.join(titles)}")
        except Exception as e:
            self._log(f"Error logging windows: {e}")

    def _activate_whatsapp(self):
        """Find and activate the most likely WhatsApp Desktop/Beta window"""
        if not GW_AVAILABLE: 
            self._log("GW_AVAILABLE is False")
            return False
        
        self._log_windows()
        
        # Priority titles
        titles_to_try = ['WhatsApp Beta', 'WhatsApp Desktop', 'WhatsApp']
        all_windows = gw.getAllWindows()
        
        # 1. Try exact matches first (excluding browser tabs starting with '(')
        for target in titles_to_try:
            for w in all_windows:
                title = w.title
                if target.lower() == title.lower():
                    try:
                        self._log(f"Activating exact match: {title}")
                        w.activate()
                        if w.isMinimized: w.restore()
                        return True
                    except: pass
        
        # 2. Try partial matches that don't look like browser tabs
        for target in titles_to_try:
            for w in all_windows:
                title = w.title
                if target.lower() in title.lower() and not title.startswith('('):
                    try:
                        self._log(f"Activating partial match: {title}")
                        w.activate()
                        if w.isMinimized: w.restore()
                        return True
                    except: pass
                    
        return False

    def _send_shortcut(self, keys):
        """Robust shortcut sender with more delay"""
        self._log(f"Sending shortcut: {'+'.join(keys)}")
        for k in keys[:-1]:
            pyautogui.keyDown(k)
        pyautogui.press(keys[-1])
        for k in reversed(keys[:-1]):
            pyautogui.keyUp(k)
        time.sleep(1)

    def call(self, name):
        """Automated audio call"""
        name_lower = name.lower()
        if name_lower not in self.contacts:
            return f"Contact '{name}' not found."
            
        threading.Thread(target=self._perform_call_automation, args=(name, False), daemon=True).start()
        return f"Initiating automated WhatsApp Audio call to {name}..."

    def video_call(self, name):
        """Automated video call"""
        name_lower = name.lower()
        if name_lower not in self.contacts:
            return f"Contact '{name}' not found."
            
        threading.Thread(target=self._perform_call_automation, args=(name, True), daemon=True).start()
        return f"Initiating automated WhatsApp Video call to {name}..."

    def _perform_call_automation(self, name, video=False):
        """Automation thread: protocol trigger + multiple shortcuts/fallbacks"""
        if self.is_automating: 
            self._log("Already automating, skipping call request")
            return
        
        self.is_automating = True
        try:
            import re
            phone_raw = self.contacts[name.lower()]
            phone = re.sub(r'\D', '', phone_raw)
            self._log(f"Starting {'video' if video else 'audio'} call automation for {name} ({phone})")
            
            # 1. Trigger the app
            url = f"whatsapp://send?phone={phone}"
            webbrowser.open(url)
            
            # 2. Wait for the app to load (increased to 12s)
            time.sleep(12) 
            
            # 3. Focus the window
            if not self._activate_whatsapp():
                self._log("Could not activate WhatsApp window")
            
            time.sleep(2)

            # 4. Try shortcuts
            if video:
                # Video Call: Ctrl + Shift + C
                self._send_shortcut(['ctrl', 'shift', 'c'])
                # Backup: Alt + V
                self._send_shortcut(['alt', 'v'])
            else:
                # Audio Call: Ctrl + Shift + O
                self._send_shortcut(['ctrl', 'shift', 'o'])
                # Backup: Alt + C
                self._send_shortcut(['alt', 'c'])
            
            self._log("Call automation sequence completed")
            
        except Exception as e:
            self._log(f"Call Automation CRITICAL ERROR: {e}")
        finally:
            self.is_automating = False

    def message(self, name, text=""):
        """Send a WhatsApp message with automation"""
        name_lower = name.lower()
        self._log(f"Request to message: {name} (Text: {text})")
        
        if name_lower not in self.contacts:
            return f"Contact '{name}' not found."
        
        if not PYAUTOGUI_AVAILABLE or not text:
            phone = re.sub(r'\D', '', self.contacts[name_lower])
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(text)}"
            webbrowser.open(url)
            return f"Opening WhatsApp chat with {name}"

        # Automated send
        threading.Thread(target=self._perform_message_automation, args=(name, text), daemon=True).start()
        return f"Sending automated message to {name}: '{text}'"

    def _perform_message_automation(self, name, text):
        """Automated messaging via Desktop App - Using URL text parameter"""
        if self.is_automating: return
        self.is_automating = True
        try:
            import re
            phone_raw = self.contacts[name.lower()]
            phone = re.sub(r'\D', '', phone_raw)
            self._log(f"Starting message automation for {name} ({phone})")
            
            # Use the URL with text parameter - this pre-fills the message!
            encoded_text = urllib.parse.quote(text)
            url = f"whatsapp://send?phone={phone}&text={encoded_text}"
            self._log(f"Opening URL with text: {url}")
            webbrowser.open(url)
            
            # Wait for app to open with pre-filled message
            time.sleep(10)
            
            # Focus window
            if not self._activate_whatsapp():
                self._log("Could not activate WhatsApp window")
            
            time.sleep(2)
            
            # Just press Enter to send the pre-filled message
            self._log("Pressing Enter to send pre-filled message...")
            pyautogui.press('enter')
            self._log("Message automation completed")
            
        except Exception as e:
            self._log(f"Message Automation Error: {e}")
        finally:
            self.is_automating = False

    def list_contacts(self):
        """List all contacts"""
        if not self.contacts:
            return "No contacts saved. Add with: 'add contact [name] [phone]'"
        
        result = "📇 **Saved Contacts:**\n"
        for name, phone in self.contacts.items():
            result += f"  • {name.title()}: {phone}\n"
        return result

    def process_command(self, message):
        """Integrated command processing for WhatsApp"""
        msg = message.lower()
        words = message.split()
        
        if 'add contact' in msg:
            if len(words) >= 4:
                name = words[2]
                phone = "".join(words[3:])
                return self.add_contact(name, phone)
            return "Usage: add contact [name] [phone]"
            
        if 'list contact' in msg or 'show contact' in msg:
            return self.list_contacts()
            
        if 'video call' in msg:
            for i, w in enumerate(words):
                if w.lower() == 'call' and i + 1 < len(words):
                    name = words[i+1]
                    return self.video_call(name)
            return "Who would you like to video call?"

        if 'call' in msg:
            # Check for name after 'call'
            for i, w in enumerate(words):
                if w.lower() == 'call' and i + 1 < len(words):
                    name = words[i+1]
                    if name.lower() not in ['on', 'via', 'whatsapp']:
                        return self.call(name)
            return "Who would you like to call?"
            
        if any(x in msg for x in ['message', 'text', 'send', 'whatsapp']):
            # Pattern: "message mom hello" or "text mom hi"
            for trig in ['message', 'text', 'send', 'whatsapp']:
                if trig in msg:
                    idx = -1
                    for i, w in enumerate(words):
                        if w.lower() == trig:
                            idx = i
                            break
                    if idx != -1 and idx + 1 < len(words):
                        name = words[idx+1]
                        txt = " ".join(words[idx+2:]) if idx+2 < len(words) else ""
                        if name.lower() not in ['on', 'via', 'to']:
                            return self.message(name, txt)
                        elif idx + 2 < len(words):
                             name = words[idx+2]
                             txt = " ".join(words[idx+3:]) if idx+3 < len(words) else ""
                             return self.message(name, txt)
                             
            return "Usage: message [name] [text]"
            
        return "Command not recognized for WhatsApp module."
