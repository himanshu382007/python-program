"""
Garun AI Assistant - Smart Home Controller
============================================
Framework for smart home device control
"""


class SmartHomeController:
    """
    Smart home control framework.
    
    This is a modular framework that can be extended to support
    various smart home platforms like:
    - Philips Hue
    - Home Assistant
    - Google Home
    - Amazon Alexa
    - IFTTT
    """
    
    def __init__(self):
        # Device registry
        self.devices = {}
        
        # Supported device types
        self.device_types = ['light', 'fan', 'ac', 'tv', 'speaker']
        
        # Simulated devices for demo
        self._init_demo_devices()
    
    def _init_demo_devices(self):
        """Initialize demo devices for testing"""
        self.devices = {
            'living room light': {'type': 'light', 'state': 'off', 'brightness': 100},
            'bedroom light': {'type': 'light', 'state': 'off', 'brightness': 100},
            'kitchen light': {'type': 'light', 'state': 'off', 'brightness': 100},
            'ceiling fan': {'type': 'fan', 'state': 'off', 'speed': 3},
            'bedroom fan': {'type': 'fan', 'state': 'off', 'speed': 3},
            'ac': {'type': 'ac', 'state': 'off', 'temperature': 24},
            'air conditioner': {'type': 'ac', 'state': 'off', 'temperature': 24},
            'tv': {'type': 'tv', 'state': 'off', 'volume': 50},
        }
    
    def process_command(self, command):
        """
        Process a smart home command.
        
        Args:
            command: Natural language command
            
        Returns:
            Result message
        """
        command_lower = command.lower()
        
        # Determine action
        if any(word in command_lower for word in ['turn on', 'switch on', 'enable']):
            action = 'on'
        elif any(word in command_lower for word in ['turn off', 'switch off', 'disable']):
            action = 'off'
        elif 'increase' in command_lower or 'up' in command_lower or 'brighter' in command_lower:
            action = 'increase'
        elif 'decrease' in command_lower or 'down' in command_lower or 'dimmer' in command_lower:
            action = 'decrease'
        elif 'set' in command_lower:
            action = 'set'
        else:
            action = 'toggle'
        
        # Find device
        device_name = self._find_device(command_lower)
        
        if device_name:
            return self._control_device(device_name, action, command_lower)
        else:
            # Check for general commands
            if 'light' in command_lower:
                return self._control_all_type('light', action)
            elif 'fan' in command_lower:
                return self._control_all_type('fan', action)
            
            return ("I couldn't identify which device you want to control. "
                   "Try saying something like 'turn on the living room light'.")
    
    def _find_device(self, command):
        """Find device mentioned in command"""
        for device_name in self.devices:
            if device_name in command:
                return device_name
        return None
    
    def _control_device(self, device_name, action, command):
        """Control a specific device"""
        device = self.devices.get(device_name)
        
        if not device:
            return f"I couldn't find a device called '{device_name}'."
        
        device_type = device['type']
        
        # Handle different device types
        if device_type == 'light':
            return self._control_light(device_name, device, action, command)
        elif device_type == 'fan':
            return self._control_fan(device_name, device, action, command)
        elif device_type == 'ac':
            return self._control_ac(device_name, device, action, command)
        elif device_type == 'tv':
            return self._control_tv(device_name, device, action, command)
        else:
            if action == 'on':
                device['state'] = 'on'
                return f"Turning on the {device_name}."
            elif action == 'off':
                device['state'] = 'off'
                return f"Turning off the {device_name}."
            else:
                return f"Toggling the {device_name}."
    
    def _control_light(self, name, device, action, command):
        """Control a light device"""
        if action == 'on':
            device['state'] = 'on'
            return f"💡 Turning on the {name}."
        elif action == 'off':
            device['state'] = 'off'
            return f"💡 Turning off the {name}."
        elif action == 'increase':
            device['brightness'] = min(100, device['brightness'] + 20)
            return f"💡 Increasing {name} brightness to {device['brightness']}%."
        elif action == 'decrease':
            device['brightness'] = max(10, device['brightness'] - 20)
            return f"💡 Decreasing {name} brightness to {device['brightness']}%."
        else:
            device['state'] = 'off' if device['state'] == 'on' else 'on'
            return f"💡 Toggling the {name}."
    
    def _control_fan(self, name, device, action, command):
        """Control a fan device"""
        if action == 'on':
            device['state'] = 'on'
            return f"🌀 Turning on the {name}."
        elif action == 'off':
            device['state'] = 'off'
            return f"🌀 Turning off the {name}."
        elif action == 'increase':
            device['speed'] = min(5, device['speed'] + 1)
            return f"🌀 Increasing {name} speed to {device['speed']}."
        elif action == 'decrease':
            device['speed'] = max(1, device['speed'] - 1)
            return f"🌀 Decreasing {name} speed to {device['speed']}."
        else:
            device['state'] = 'off' if device['state'] == 'on' else 'on'
            return f"🌀 Toggling the {name}."
    
    def _control_ac(self, name, device, action, command):
        """Control an AC device"""
        import re
        
        if action == 'on':
            device['state'] = 'on'
            return f"❄️ Turning on the {name} at {device['temperature']}°C."
        elif action == 'off':
            device['state'] = 'off'
            return f"❄️ Turning off the {name}."
        elif action == 'increase':
            device['temperature'] = min(30, device['temperature'] + 1)
            return f"❄️ Setting {name} to {device['temperature']}°C."
        elif action == 'decrease':
            device['temperature'] = max(16, device['temperature'] - 1)
            return f"❄️ Setting {name} to {device['temperature']}°C."
        elif action == 'set':
            # Extract temperature
            temp_match = re.search(r'(\d+)\s*(?:degree|°|c)?', command)
            if temp_match:
                temp = int(temp_match.group(1))
                device['temperature'] = max(16, min(30, temp))
            return f"❄️ Setting {name} to {device['temperature']}°C."
        else:
            device['state'] = 'off' if device['state'] == 'on' else 'on'
            return f"❄️ Toggling the {name}."
    
    def _control_tv(self, name, device, action, command):
        """Control a TV device"""
        if action == 'on':
            device['state'] = 'on'
            return f"📺 Turning on the {name}."
        elif action == 'off':
            device['state'] = 'off'
            return f"📺 Turning off the {name}."
        elif action == 'increase':
            device['volume'] = min(100, device['volume'] + 10)
            return f"📺 Increasing {name} volume to {device['volume']}."
        elif action == 'decrease':
            device['volume'] = max(0, device['volume'] - 10)
            return f"📺 Decreasing {name} volume to {device['volume']}."
        else:
            device['state'] = 'off' if device['state'] == 'on' else 'on'
            return f"📺 Toggling the {name}."
    
    def _control_all_type(self, device_type, action):
        """Control all devices of a type"""
        count = 0
        for name, device in self.devices.items():
            if device['type'] == device_type:
                if action == 'on':
                    device['state'] = 'on'
                elif action == 'off':
                    device['state'] = 'off'
                count += 1
        
        if count == 0:
            return f"No {device_type}s found to control."
        
        action_word = "on" if action == 'on' else "off"
        return f"Turning {action_word} all {count} {device_type}(s)."
    
    def list_devices(self):
        """List all registered devices"""
        if not self.devices:
            return "No smart home devices registered."
        
        response = "🏠 Smart Home Devices:\n\n"
        for name, device in self.devices.items():
            state = device['state']
            state_emoji = "🟢" if state == 'on' else "⚫"
            response += f"{state_emoji} {name.title()} ({device['type']}): {state}\n"
        
        return response.strip()
    
    def get_device_status(self, device_name):
        """Get status of a specific device"""
        device = self.devices.get(device_name.lower())
        if device:
            return f"{device_name.title()} is currently {device['state']}."
        return f"Device '{device_name}' not found."
