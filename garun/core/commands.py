"""
Garun AI Assistant - Command Processor
=======================================
Routes commands to appropriate handlers
Includes: Security, Vision, Browser, and all JARVIS features
"""

from datetime import datetime
from core.ai_engine import AIEngine


class CommandProcessor:
    """Processes and routes user commands"""
    
    def __init__(self, features):
        """
        Initialize command processor.
        
        Args:
            features: Dict of feature modules
        """
        self.features = features
        self.ai_engine = AIEngine()
        
        # Initialize advanced modules
        self._init_advanced_modules()
    
    def _init_advanced_modules(self):
        """Initialize security, vision, and browser modules"""
        try:
            from features.security_hub import SecurityHub
            self.security = SecurityHub(callback=self._security_callback)
            print("[Garun] Security Hub initialized")
        except Exception as e:
            self.security = None
            print(f"[Garun] Security Hub unavailable: {e}")
        
        try:
            from core.vision import Vision
            self.vision = Vision()
            print("[Garun] Vision module initialized")
        except Exception as e:
            self.vision = None
            print(f"[Garun] Vision module unavailable: {e}")
        
        try:
            from features.browser import BrowserController
            self.browser = BrowserController()
            print("[Garun] Browser controller initialized")
        except Exception as e:
            self.browser = None
            print(f"[Garun] Browser controller unavailable: {e}")
        
        try:
            from features.whatsapp import WhatsAppController
            self.whatsapp = WhatsAppController()
            print("[Garun] WhatsApp controller initialized")
        except Exception as e:
            self.whatsapp = None
            print(f"[Garun] WhatsApp unavailable: {e}")    
    def _security_callback(self, message):
        """Callback for security alerts"""
        print(f"[SECURITY ALERT] {message}")
    
    def process(self, message):
        """
        Process a user message and return response.
        
        Args:
            message: User message string
            
        Returns:
            Response string
        """
        # Analyze intent
        intent = self.ai_engine.analyze_intent(message)
        intent_type = intent.get("type", "conversation")
        message_lower = message.lower()
        
        print(f"[Garun] Intent: {intent_type}")  # Debug logging
        
        # Check for new command types first
        # WhatsApp commands (call, message, contacts)
        if self._is_whatsapp_command(message_lower):
            return self._handle_whatsapp(message)
        
        # Security commands
        if self._is_security_command(message_lower):
            return self._handle_security(message)
        
        # Vision commands
        if self._is_vision_command(message_lower):
            return self._handle_vision(message)
        
        # Web search/browser commands
        if self._is_browser_command(message_lower):
            return self._handle_browser(message)
        
        # Route to appropriate handler
        try:
            if intent_type == "math":
                return self._handle_math(message)
            
            elif intent_type == "system_control":
                return self._handle_system_control(message, intent)
            
            elif intent_type == "weather":
                return self._handle_weather(message)
            
            elif intent_type == "news":
                return self._handle_news(message)
            
            elif intent_type == "time":
                return self._handle_time()
            
            elif intent_type == "date":
                return self._handle_date()
            
            elif intent_type == "reminder":
                return self._handle_reminder(message)
            
            elif intent_type == "smart_home":
                return self._handle_smart_home(message)
            
            elif intent_type == "web_search":
                return self._handle_browser(message)
            
            else:
                # Use AI for general conversation
                return self._handle_conversation(message)
                
        except Exception as e:
            print(f"[Garun] Command error: {e}")
            return f"I encountered an error processing that request: {str(e)}"
    
    # ==========================================
    # COMMAND TYPE DETECTION
    # ==========================================
    
    def _is_security_command(self, message):
        """Check if message is a security command"""
        security_keywords = [
            'security', 'secure', 'network', 'scan network', 'devices on network',
            'usb', 'monitor', 'hash', 'integrity', 'firewall', 'antivirus',
            'who is on', 'unknown device', 'suspicious', 'threat'
        ]
        return any(kw in message for kw in security_keywords)
    
    def _is_vision_command(self, message):
        """Check if message is a vision command"""
        vision_keywords = [
            'who is there', 'who\'s there', 'see me', 'recognize', 'face',
            'look at', 'camera', 'webcam', 'screenshot', 'screen', 'capture screen',
            'register my face', 'remember me', 'what do you see'
        ]
        return any(kw in message for kw in vision_keywords)
    
    def _is_browser_command(self, message):
        """Check if message is a browser/search command"""
        browser_keywords = [
            'search', 'google', 'youtube', 'browse', 'open website',
            'go to', 'search for', 'look up', 'find on', 'github',
            'stackoverflow', 'check email', 'gmail', 'incognito'
        ]
        return any(kw in message for kw in browser_keywords)
    
    def _is_whatsapp_command(self, message):
        """Check if message is a WhatsApp command"""
        whatsapp_keywords = [
            'call ', 'whatsapp', 'message ', 'text ',
            'add contact', 'list contact', 'show contact'
        ]
        return any(kw in message for kw in whatsapp_keywords)
    
    # ==========================================
    # WHATSAPP HANDLERS
    # ==========================================
    
    def _handle_whatsapp(self, message):
        """Handle WhatsApp commands"""
        if not self.whatsapp:
            return "WhatsApp controller not available."
        
        return self.whatsapp.process_command(message)
    
    # ==========================================
    # SECURITY HANDLERS
    # ==========================================
    
    def _handle_security(self, message):
        """Handle security-related commands"""
        if not self.security:
            return "Security module is not available."
        
        message_lower = message.lower()
        
        # Network scanning
        if 'scan network' in message_lower or 'network scan' in message_lower:
            return self._format_network_scan()
        
        if 'devices on network' in message_lower or 'who is on' in message_lower:
            return self._format_network_scan()
        
        # Security status report
        if 'security status' in message_lower or 'security report' in message_lower:
            return self.security.format_security_report()
        
        # USB monitoring
        if 'monitor usb' in message_lower or 'watch usb' in message_lower:
            return self.security.monitor_usb()
        
        if 'stop monitor' in message_lower:
            return self.security.stop_usb_monitor()
        
        # File integrity
        if 'hash' in message_lower or 'integrity' in message_lower:
            # Extract folder path if provided
            return "To check file integrity, specify a folder path. Example: 'check integrity of C:\\Documents'"
        
        # Network info
        if 'network info' in message_lower or 'ip address' in message_lower:
            info = self.security.get_network_info()
            return f"🌐 Network Info:\nHostname: {info.get('hostname')}\nIP Addresses: {', '.join(info.get('ip_addresses', []))}"
        
        # General security
        return self.security.format_security_report()
    
    def _format_network_scan(self):
        """Format network scan results"""
        devices = self.security.scan_network()
        if not devices or (len(devices) == 1 and 'error' in devices[0]):
            return "Couldn't scan network. Error: " + str(devices[0].get('error', 'Unknown'))
        
        response = "🌐 **Network Scan Results:**\n\n"
        known = [d for d in devices if d.get('known')]
        unknown = [d for d in devices if not d.get('known') and 'error' not in d]
        
        response += f"📊 Found {len(devices)} devices\n"
        response += f"✅ Known: {len(known)}\n"
        response += f"⚠️ Unknown: {len(unknown)}\n\n"
        
        if unknown:
            response += "**Unknown Devices:**\n"
            for d in unknown:
                response += f"  • {d['ip']} ({d['mac']})\n"
            response += "\nSay 'trust device [MAC]' to add to trusted list."
        else:
            response += "All devices are known. Network is secure!"
        
        return response
    
    # ==========================================
    # VISION HANDLERS
    # ==========================================
    
    def _handle_vision(self, message):
        """Handle vision-related commands"""
        if not self.vision:
            return "Vision module requires OpenCV. Install with: pip install opencv-python face-recognition"
        
        message_lower = message.lower()
        
        # Who's there?
        if 'who is there' in message_lower or 'who\'s there' in message_lower:
            return self.vision.who_is_there()
        
        # Register face
        if 'register' in message_lower or 'remember me' in message_lower:
            # Extract name
            name = self._extract_name_for_face(message)
            if name:
                return self.vision.register_face(name)
            return "What name should I remember you as? Say 'register my face as [Name]'"
        
        # Screenshot
        if 'screenshot' in message_lower or 'capture screen' in message_lower:
            path, msg = self.vision.capture_screen()
            if path:
                return f"📸 Screenshot saved: {path}"
            return msg
        
        # Analyze screen
        if 'analyze' in message_lower and 'screen' in message_lower:
            return self.vision.analyze_screen(self.ai_engine)
        
        # Status
        status = self.vision.get_status()
        faces = status.get('known_faces', [])
        return f"👁️ Vision Status:\nOpenCV: {'✅' if status['opencv_available'] else '❌'}\nFace Recognition: {'✅' if status['face_recognition_available'] else '❌'}\nKnown Faces: {', '.join(faces) if faces else 'None registered'}"
    
    def _extract_name_for_face(self, message):
        """Extract name from face registration request"""
        patterns = ['register my face as ', 'remember me as ', 'my name is ', 'call me ']
        message_lower = message.lower()
        
        for pattern in patterns:
            if pattern in message_lower:
                idx = message_lower.find(pattern) + len(pattern)
                name = message[idx:].strip().rstrip('?.,!')
                return name.title()
        return None
    
    # ==========================================
    # BROWSER HANDLERS
    # ==========================================
    
    def _handle_browser(self, message):
        """Handle browser and search commands"""
        if not self.browser:
            return "Browser controller is not available."
        
        message_lower = message.lower()
        
        # Google search
        if 'google' in message_lower or 'search for' in message_lower:
            query = self._extract_search_query(message_lower)
            if query:
                return self.browser.search_google(query)
        
        # YouTube search
        if 'youtube' in message_lower:
            if 'search' in message_lower:
                query = self._extract_search_query(message_lower)
                if query:
                    return self.browser.search_youtube(query)
            return self.browser.open_site("youtube")
        
        # GitHub
        if 'github' in message_lower:
            query = self._extract_search_query(message_lower)
            if query:
                return self.browser.search_github(query)
            return self.browser.open_site("github")
        
        # StackOverflow
        if 'stackoverflow' in message_lower or 'stack overflow' in message_lower:
            query = self._extract_search_query(message_lower)
            if query:
                return self.browser.code_help(query)
        
        # Gmail
        if 'email' in message_lower or 'gmail' in message_lower:
            return self.browser.check_email()
        
        # Incognito
        if 'incognito' in message_lower or 'private' in message_lower:
            return self.browser.open_incognito()
        
        # Open website by name
        if 'open' in message_lower or 'go to' in message_lower:
            site = self._extract_site_name(message_lower)
            if site:
                return self.browser.open_site(site)
        
        # General search
        query = self._extract_search_query(message_lower)
        if query:
            return self.browser.search_google(query)
        
        return "What would you like me to search for?"
    
    def _extract_site_name(self, message):
        """Extract website name from message"""
        patterns = ['open ', 'go to ', 'browse to ', 'visit ']
        for pattern in patterns:
            if pattern in message:
                idx = message.find(pattern) + len(pattern)
                site = message[idx:].strip().rstrip('?.,!')
                # Remove trailing words
                site = site.split()[0] if site.split() else None
                return site
        return None
    
    # ==========================================
    # EXISTING HANDLERS
    # ==========================================
    
    def _handle_math(self, message):
        """Handle math calculations"""
        result = self.ai_engine._try_math(message)
        if result:
            return result
        return "I couldn't calculate that. Try something like 'what is 2+3' or 'calculate 10*5'"
    
    def _handle_system_control(self, message, intent):
        """Handle system control commands"""
        action = intent.get("action", "")
        system = self.features.get("system")
        
        if not system:
            return "System controls are not available."
        
        message_lower = message.lower()
        
        if action == "open_app":
            # Extract app name
            app_name = self._extract_app_name(message_lower)
            if app_name:
                result = system.open_application(app_name)
                return result
            return "Which application would you like me to open?"
        
        elif action == "search_files":
            # Extract search query
            query = self._extract_search_query(message_lower)
            if query:
                result = system.search_files(query)
                return result
            return "What would you like me to search for?"
        
        elif action == "volume":
            if 'mute' in message_lower:
                return system.mute()
            elif 'unmute' in message_lower:
                return system.unmute()
            elif 'up' in message_lower or 'louder' in message_lower or 'increase' in message_lower:
                return system.volume_up()
            elif 'down' in message_lower or 'quieter' in message_lower or 'decrease' in message_lower:
                return system.volume_down()
            return "Would you like me to increase, decrease, or mute the volume?"
        
        elif action == "lock":
            return system.lock_screen()
        
        elif action == "power":
            if 'shutdown' in message_lower or 'shut down' in message_lower:
                return "For safety reasons, I won't automatically shut down. Please use the Start menu to shut down."
            elif 'restart' in message_lower or 'reboot' in message_lower:
                return "For safety reasons, I won't automatically restart. Please use the Start menu to restart."
        
        return "I'm not sure what system action you want me to perform."
    
    def _handle_weather(self, message):
        """Handle weather requests"""
        weather = self.features.get("weather")
        if not weather:
            return "Weather service is not available."
        
        # Extract city if mentioned
        city = self._extract_city(message)
        return weather.get_weather(city)
    
    def _handle_news(self, message):
        """Handle news requests"""
        news = self.features.get("news")
        if not news:
            return "News service is not available."
        
        # Check for category
        message_lower = message.lower()
        if 'tech' in message_lower or 'technology' in message_lower:
            return news.get_news("technology")
        elif 'sport' in message_lower:
            return news.get_news("sports")
        elif 'business' in message_lower:
            return news.get_news("business")
        
        return news.get_news()
    
    def _handle_time(self):
        """Handle time requests"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}."
    
    def _handle_date(self):
        """Handle date requests"""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}."
    
    def _handle_reminder(self, message):
        """Handle reminder requests"""
        reminders = self.features.get("reminders")
        if not reminders:
            return "Reminder service is not available."
        
        message_lower = message.lower()
        
        # List reminders
        if 'list' in message_lower or 'show' in message_lower or 'what' in message_lower:
            return reminders.list_reminders()
        
        # Set reminder
        return reminders.parse_and_set(message)
    
    def _handle_smart_home(self, message):
        """Handle smart home requests"""
        smart_home = self.features.get("smart_home")
        if not smart_home:
            return "Smart home features are not yet configured."
        
        return smart_home.process_command(message)
    
    def _handle_conversation(self, message):
        """Handle general conversation with AI"""
        return self.ai_engine.chat(message)
    
    # Helper methods
    def _extract_app_name(self, message):
        """Extract application name from message"""
        # Remove common words
        words_to_remove = ['open', 'launch', 'start', 'run', 'please', 'can', 'you', 
                          'could', 'would', 'the', 'app', 'application', 'program',
                          'kholo', 'chalu', 'karo']
        
        words = message.split()
        app_words = [w for w in words if w not in words_to_remove]
        
        if app_words:
            return ' '.join(app_words)
        return None
    
    def _extract_search_query(self, message):
        """Extract search query from message"""
        words_to_remove = ['search', 'find', 'look', 'for', 'file', 'files', 
                          'document', 'documents', 'named', 'called', 'please',
                          'google', 'youtube', 'on', 'github', 'stackoverflow']
        
        words = message.split()
        query_words = [w for w in words if w not in words_to_remove]
        
        if query_words:
            return ' '.join(query_words)
        return None
    
    def _extract_city(self, message):
        """Extract city name from weather request"""
        message_lower = message.lower()
        
        # Common patterns
        patterns = ['weather in ', 'weather for ', 'weather at ', 'mausam ']
        for pattern in patterns:
            if pattern in message_lower:
                idx = message_lower.find(pattern) + len(pattern)
                city = message[idx:].strip()
                # Remove trailing punctuation
                city = city.rstrip('?.,!')
                if city:
                    return city
        
        return None  # Use default city
