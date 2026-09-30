"""
Garun AI Assistant - Security Module
=====================================
Security Operations Center (SOC) features for JARVIS
- Network monitoring
- USB device detection
- File integrity checking
- System security status
"""

import os
import subprocess
import hashlib
import json
import socket
import platform
from pathlib import Path
from datetime import datetime
import threading
import time


class SecurityHub:
    """
    Security Operations Center for Garun.
    Perfect for Cyber Security students!
    """
    
    def __init__(self, callback=None):
        """
        Initialize Security Hub.
        
        Args:
            callback: Function to call when security event detected
        """
        self.callback = callback
        self.known_devices = set()
        self.monitoring = False
        self.watch_folders = []
        self.file_hashes = {}
        
        # Load known devices from file
        self._load_known_devices()
    
    def _load_known_devices(self):
        """Load known MAC addresses from config"""
        config_path = Path(__file__).parent.parent / "data" / "known_devices.json"
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    data = json.load(f)
                    self.known_devices = set(data.get("mac_addresses", []))
            except:
                pass
    
    def _save_known_devices(self):
        """Save known devices to config"""
        config_path = Path(__file__).parent.parent / "data" / "known_devices.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump({"mac_addresses": list(self.known_devices)}, f, indent=2)
    
    # ==========================================
    # NETWORK SECURITY
    # ==========================================
    
    def get_network_info(self):
        """Get current network information"""
        try:
            result = subprocess.run(
                ["ipconfig", "/all"] if platform.system() == "Windows" else ["ifconfig"],
                capture_output=True, text=True, timeout=10
            )
            
            info = {
                "hostname": socket.gethostname(),
                "raw_output": result.stdout,
                "ip_addresses": [],
                "mac_addresses": []
            }
            
            # Parse IP addresses
            for line in result.stdout.split("\n"):
                line = line.strip()
                if "IPv4" in line or "inet " in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        ip = parts[1].strip().split()[0]
                        info["ip_addresses"].append(ip)
                elif "Physical Address" in line or "ether" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        mac = ":".join(parts[1:]).strip().replace("-", ":")
                        info["mac_addresses"].append(mac)
            
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def scan_network(self):
        """
        Scan local network for devices using ARP.
        Returns list of IP and MAC addresses.
        """
        try:
            result = subprocess.run(
                ["arp", "-a"],
                capture_output=True, text=True, timeout=10
            )
            
            devices = []
            for line in result.stdout.split("\n"):
                line = line.strip()
                parts = line.split()
                
                if len(parts) >= 2:
                    # Windows: IP address is first, MAC is second
                    # Try to extract IP and MAC
                    ip = None
                    mac = None
                    
                    for part in parts:
                        # Check if it looks like an IP
                        if part.count(".") == 3 and not ip:
                            ip = part
                        # Check if it looks like a MAC
                        elif (part.count("-") == 5 or part.count(":") == 5) and not mac:
                            mac = part.upper().replace("-", ":")
                    
                    if ip and mac and mac != "FF:FF:FF:FF:FF:FF":
                        is_known = mac in self.known_devices
                        devices.append({
                            "ip": ip,
                            "mac": mac,
                            "known": is_known
                        })
            
            return devices
        except Exception as e:
            return [{"error": str(e)}]
    
    def check_network_security(self):
        """
        Check for unknown devices on network.
        Returns security status and any alerts.
        """
        devices = self.scan_network()
        unknown = [d for d in devices if not d.get("known", True) and "error" not in d]
        
        status = {
            "total_devices": len([d for d in devices if "error" not in d]),
            "known_devices": len([d for d in devices if d.get("known")]),
            "unknown_devices": len(unknown),
            "unknown_list": unknown,
            "secure": len(unknown) == 0,
            "timestamp": datetime.now().isoformat()
        }
        
        if unknown and self.callback:
            self.callback(f"⚠️ ALERT: {len(unknown)} unknown device(s) detected on network!")
        
        return status
    
    def trust_device(self, mac_address):
        """Add a device to trusted list"""
        mac = mac_address.upper().replace("-", ":")
        self.known_devices.add(mac)
        self._save_known_devices()
        return f"Device {mac} added to trusted list."
    
    def block_device(self, mac_address):
        """
        Block a device (shows command to run).
        Actual blocking requires admin privileges.
        """
        # Note: Actually blocking requires router access or admin netsh commands
        return (f"To block device {mac_address}, you can:\n"
                f"1. Access your router settings and block the MAC\n"
                f"2. Run as admin: netsh advfirewall firewall add rule...")
    
    # ==========================================
    # USB MONITORING
    # ==========================================
    
    def get_usb_devices(self):
        """Get list of connected USB devices"""
        try:
            # Use WMIC to get USB devices on Windows
            result = subprocess.run(
                ["wmic", "path", "Win32_USBHub", "get", "DeviceID,Description"],
                capture_output=True, text=True, timeout=10
            )
            
            devices = []
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            
            for line in lines:
                line = line.strip()
                if line:
                    devices.append(line)
            
            return devices
        except Exception as e:
            return [f"Error: {e}"]
    
    def monitor_usb(self, callback=None):
        """
        Start monitoring for USB insertions.
        Calls callback when new device detected.
        """
        if callback:
            self.callback = callback
        
        initial_devices = set(self.get_usb_devices())
        
        def monitor():
            nonlocal initial_devices
            while self.monitoring:
                current = set(self.get_usb_devices())
                new_devices = current - initial_devices
                
                if new_devices:
                    for device in new_devices:
                        if self.callback:
                            self.callback(
                                f"🔌 NEW USB DEVICE DETECTED!\n"
                                f"Device: {device}\n"
                                f"Should I trust it or investigate?"
                            )
                    initial_devices = current
                
                time.sleep(2)
        
        self.monitoring = True
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        return "USB monitoring started. I'll alert you of any new devices."
    
    def stop_usb_monitor(self):
        """Stop USB monitoring"""
        self.monitoring = False
        return "USB monitoring stopped."
    
    # ==========================================
    # FILE INTEGRITY
    # ==========================================
    
    def hash_file(self, file_path):
        """Calculate SHA256 hash of a file"""
        try:
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return f"Error: {e}"
    
    def check_file_integrity(self, folder_path):
        """
        Check file integrity in a folder.
        Calculates hashes and compares with stored values.
        """
        folder = Path(folder_path)
        if not folder.exists():
            return {"error": "Folder not found"}
        
        results = {
            "folder": str(folder),
            "files_checked": 0,
            "new_files": [],
            "modified_files": [],
            "unchanged_files": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        for file_path in folder.rglob("*"):
            if file_path.is_file():
                results["files_checked"] += 1
                current_hash = self.hash_file(file_path)
                str_path = str(file_path)
                
                if str_path in self.file_hashes:
                    if self.file_hashes[str_path] != current_hash:
                        results["modified_files"].append(str_path)
                    else:
                        results["unchanged_files"] += 1
                else:
                    results["new_files"].append(str_path)
                
                self.file_hashes[str_path] = current_hash
        
        return results
    
    def watch_folder(self, folder_path):
        """Add a folder to integrity monitoring"""
        folder = Path(folder_path)
        if folder.exists():
            self.watch_folders.append(str(folder))
            # Initial hash calculation
            self.check_file_integrity(folder_path)
            return f"Now monitoring: {folder}"
        return f"Folder not found: {folder_path}"
    
    # ==========================================
    # SYSTEM SECURITY STATUS
    # ==========================================
    
    def get_security_status(self):
        """Get overall system security status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "firewall": self._check_firewall(),
            "antivirus": self._check_antivirus(),
            "updates": self._check_updates(),
            "network": self.check_network_security(),
            "overall": "SECURE"
        }
        
        # Determine overall status
        if status["network"]["unknown_devices"] > 0:
            status["overall"] = "CAUTION"
        
        return status
    
    def _check_firewall(self):
        """Check Windows Firewall status"""
        try:
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles", "state"],
                capture_output=True, text=True, timeout=10
            )
            return "ON" if "ON" in result.stdout.upper() else "OFF"
        except:
            return "UNKNOWN"
    
    def _check_antivirus(self):
        """Check if Windows Defender is running"""
        try:
            result = subprocess.run(
                ["powershell", "-Command", 
                 "Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled"],
                capture_output=True, text=True, timeout=10
            )
            return "ActiveWindows Defender ON" if "True" in result.stdout else "Check Manually"
        except:
            return "UNKNOWN"
    
    def _check_updates(self):
        """Check for pending Windows updates"""
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "(New-Object -ComObject Microsoft.Update.AutoUpdate).DetectNow()"],
                capture_output=True, text=True, timeout=30
            )
            return "Checked"
        except:
            return "UNKNOWN"
    
    # ==========================================
    # SECURITY ALERTS
    # ==========================================
    
    def format_security_report(self):
        """Generate a formatted security report"""
        status = self.get_security_status()
        
        report = f"""
🛡️ SECURITY STATUS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━
🖥️ Host: {status['hostname']}
⏰ Time: {status['timestamp']}

🔥 Firewall: {status['firewall']}
🛡️ Antivirus: {status['antivirus']}

🌐 NETWORK STATUS:
   Total Devices: {status['network']['total_devices']}
   Known: {status['network']['known_devices']}
   Unknown: {status['network']['unknown_devices']}

📊 OVERALL: {status['overall']}
━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if status['network']['unknown_devices'] > 0:
            report += "\n⚠️ UNKNOWN DEVICES:\n"
            for device in status['network']['unknown_list']:
                report += f"   • {device['ip']} ({device['mac']})\n"
        
        return report.strip()
