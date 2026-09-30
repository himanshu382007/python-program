"""
Garun AI Assistant - System Control
=====================================
Controls system functions like opening apps, volume, etc.
"""

import os
import subprocess
import ctypes
from pathlib import Path


class SystemControl:
    """Handles system control operations"""
    
    def __init__(self):
        # Common application paths
        self.app_paths = {
            # Browsers
            'chrome': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            ],
            'firefox': [
                r'C:\Program Files\Mozilla Firefox\firefox.exe',
                r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
            ],
            'edge': [
                r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
            ],
            'brave': [
                r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
                r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'
            ],
            
            # Microsoft Office
            'word': [
                r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
                r'C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE'
            ],
            'excel': [
                r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
                r'C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE'
            ],
            'powerpoint': [
                r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
                r'C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE'
            ],
            
            # Development
            'vscode': [
                r'D:\vscode\Microsoft VS Code\Code.exe',  # Custom location
                os.path.expandvars(r'%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe'),
                r'C:\Program Files\Microsoft VS Code\Code.exe',
                'code'  # Use 'code' command from PATH
            ],
            'visual studio code': [
                r'D:\vscode\Microsoft VS Code\Code.exe',
                os.path.expandvars(r'%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe'),
                r'C:\Program Files\Microsoft VS Code\Code.exe',
                'code'
            ],
            'vs code': [
                r'D:\vscode\Microsoft VS Code\Code.exe',
                os.path.expandvars(r'%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe'),
                r'C:\Program Files\Microsoft VS Code\Code.exe',
                'code'
            ],
            
            # Media
            'spotify': [
                os.path.expandvars(r'%APPDATA%\Spotify\Spotify.exe')
            ],
            'vlc': [
                r'C:\Program Files\VideoLAN\VLC\vlc.exe',
                r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'
            ],
            
            # Communication
            'discord': [
                os.path.expandvars(r'%LOCALAPPDATA%\Discord\Update.exe --processStart Discord.exe')
            ],
            'telegram': [
                os.path.expandvars(r'%APPDATA%\Telegram Desktop\Telegram.exe')
            ],
            'whatsapp': [
                os.path.expandvars(r'%LOCALAPPDATA%\WhatsApp\WhatsApp.exe')
            ],
            
            # System
            'notepad': ['notepad.exe'],
            'calculator': ['calc.exe'],
            'paint': ['mspaint.exe'],
            'explorer': ['explorer.exe'],
            'file explorer': ['explorer.exe'],
            'cmd': ['cmd.exe'],
            'command prompt': ['cmd.exe'],
            'powershell': ['powershell.exe'],
            'terminal': ['wt.exe'],  # Windows Terminal
            'task manager': ['taskmgr.exe'],
            'settings': ['ms-settings:'],
            'control panel': ['control.exe'],
        }
        
        # App name aliases
        self.aliases = {
            'browser': 'chrome',
            'google': 'chrome',
            'google chrome': 'chrome',
            'code': 'vscode',
            'vs code': 'vscode',
            'ppt': 'powerpoint',
            'calc': 'calculator',
            'files': 'explorer',
            'term': 'terminal',
        }
    
    def open_application(self, app_name):
        """
        Open an application by name.
        Searches multiple locations to find and open ANY installed app.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Status message
        """
        app_name = app_name.lower().strip()
        original_name = app_name
        
        print(f"[Garun] Trying to open: {app_name}")  # Debug
        
        # Check aliases
        if app_name in self.aliases:
            app_name = self.aliases[app_name]
        
        # Check known apps first (fastest)
        if app_name in self.app_paths:
            paths = self.app_paths[app_name]
            for path in paths:
                # Handle shell commands (like ms-settings:)
                if path.startswith('ms-'):
                    try:
                        os.startfile(path)
                        return f"Opening {original_name.title()}..."
                    except:
                        continue
                
                # Handle PATH commands (like 'code', 'git', etc.)
                if not os.path.sep in path and not path.endswith('.exe'):
                    try:
                        subprocess.Popen([path], shell=True)
                        return f"Opening {original_name.title()}..."
                    except Exception as e:
                        print(f"[Garun] PATH command failed: {e}")
                        continue
                
                # Handle system executables (like calc.exe, notepad.exe)
                if path.endswith('.exe') and not os.path.isabs(path):
                    try:
                        subprocess.Popen(['start', '', path], shell=True)
                        return f"Opening {original_name.title()}..."
                    except Exception as e:
                        print(f"[Garun] Start failed: {e}")
                        try:
                            os.startfile(path)
                            return f"Opening {original_name.title()}..."
                        except:
                            continue
                
                # Handle regular executables with full path
                if os.path.exists(path):
                    try:
                        # os.startfile is most reliable on Windows
                        os.startfile(path)
                        return f"Opening {original_name.title()}..."
                    except Exception as e:
                        print(f"[Garun] startfile failed for {path}: {e}")
                        continue
        
        # Search Start Menu shortcuts (for most installed apps)
        shortcut_result = self._find_in_start_menu(app_name, original_name)
        if shortcut_result:
            return shortcut_result
        
        # Try Windows Store Apps (UWP apps)
        uwp_result = self._open_uwp_app(app_name, original_name)
        if uwp_result:
            return uwp_result
        
        # Try direct Windows 'start' command with app name
        try:
            result = subprocess.run(
                ['cmd', '/c', 'start', '', app_name],
                shell=False,
                capture_output=True,
                timeout=3
            )
            if result.returncode == 0:
                return f"Opening {original_name.title()}..."
        except:
            pass
        
        # Try opening with .exe extension
        try:
            subprocess.Popen(['start', '', f'{app_name}.exe'], shell=True)
            return f"Opening {original_name.title()}..."
        except:
            pass
        
        # Search Program Files directories
        program_result = self._search_program_files(app_name, original_name)
        if program_result:
            return program_result
        
        # Final fallback: Open Windows search
        try:
            os.startfile(f'search-ms:displayname={app_name}&crumb=System.Generic.String%3A{app_name}')
            return f"I couldn't find {original_name} directly, but I've opened a search for it."
        except:
            pass
        
        return f"I couldn't find or open '{original_name}'. Please make sure it's installed."
    
    def _find_in_start_menu(self, app_name, original_name):
        """Search Start Menu for application shortcuts"""
        import glob
        
        start_menu_paths = [
            os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs'),
            r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs',
        ]
        
        for start_path in start_menu_paths:
            if not os.path.exists(start_path):
                continue
            
            # Search for .lnk files matching the app name
            for root, dirs, files in os.walk(start_path):
                for file in files:
                    if file.lower().endswith('.lnk'):
                        file_lower = file.lower().replace('.lnk', '')
                        # Check if app name matches
                        if app_name in file_lower or file_lower in app_name:
                            shortcut_path = os.path.join(root, file)
                            try:
                                os.startfile(shortcut_path)
                                return f"Opening {original_name.title()}..."
                            except Exception as e:
                                print(f"[Garun] Could not open shortcut: {e}")
                                continue
        
        return None
    
    def _open_uwp_app(self, app_name, original_name):
        """Try to open Windows Store (UWP) apps"""
        # Common UWP app protocols
        uwp_apps = {
            'store': 'ms-windows-store:',
            'microsoft store': 'ms-windows-store:',
            'mail': 'mailto:',
            'calendar': 'outlookcal:',
            'photos': 'ms-photos:',
            'camera': 'microsoft.windows.camera:',
            'maps': 'bingmaps:',
            'xbox': 'xbox:',
            'groove': 'mswindowsmusic:',
            'movies': 'mswindowsvideo:',
            'movies and tv': 'mswindowsvideo:',
            'weather': 'bingweather:',
            'news': 'bingnews:',
            'alarms': 'ms-clock:',
            'clock': 'ms-clock:',
            'alarms and clock': 'ms-clock:',
            'snipping tool': 'ms-screenclip:',
            'snip': 'ms-screenclip:',
            'feedback': 'feedback-hub:',
            'tips': 'ms-get-started:',
            'your phone': 'ms-phone:',
            'phone link': 'ms-phone:',
        }
        
        if app_name in uwp_apps:
            try:
                os.startfile(uwp_apps[app_name])
                return f"Opening {original_name.title()}..."
            except:
                pass
        
        # Try using PowerShell to find and launch UWP apps
        try:
            # Get list of installed apps matching the name
            ps_command = f'''
            $apps = Get-StartApps | Where-Object {{ $_.Name -like "*{app_name}*" }}
            if ($apps) {{
                $app = $apps | Select-Object -First 1
                Start-Process "shell:AppsFolder\\$($app.AppID)"
                Write-Output "SUCCESS"
            }}
            '''
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'SUCCESS' in result.stdout:
                return f"Opening {original_name.title()}..."
        except Exception as e:
            print(f"[Garun] PowerShell app search failed: {e}")
        
        return None
    
    def _search_program_files(self, app_name, original_name):
        """Search Program Files for the application"""
        search_dirs = [
            r'C:\Program Files',
            r'C:\Program Files (x86)',
            os.path.expandvars(r'%LOCALAPPDATA%\Programs'),
            os.path.expandvars(r'%APPDATA%'),
        ]
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
            
            # Look for folders matching app name
            try:
                for item in os.listdir(search_dir):
                    if app_name in item.lower():
                        item_path = os.path.join(search_dir, item)
                        if os.path.isdir(item_path):
                            # Search for .exe file inside
                            exe_path = self._find_exe_in_folder(item_path, app_name)
                            if exe_path:
                                try:
                                    subprocess.Popen([exe_path])
                                    return f"Opening {original_name.title()}..."
                                except:
                                    continue
            except PermissionError:
                continue
        
        return None
    
    def _find_exe_in_folder(self, folder_path, app_name, max_depth=2):
        """Find an executable in a folder that matches the app name"""
        if max_depth <= 0:
            return None
        
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                
                if item.lower().endswith('.exe'):
                    # Prefer exe files that match the app name
                    if app_name in item.lower():
                        return item_path
                    # Also check common exe names
                    if item.lower() in [f'{app_name}.exe', 'app.exe', 'launcher.exe', 'start.exe']:
                        return item_path
                
                # Recursively search subdirectories
                if os.path.isdir(item_path) and max_depth > 1:
                    result = self._find_exe_in_folder(item_path, app_name, max_depth - 1)
                    if result:
                        return result
        except PermissionError:
            pass
        
        return None
    
    def search_files(self, query, location=None):
        """
        Search for files on the system.
        
        Args:
            query: Search query
            location: Optional folder to search in
            
        Returns:
            Status message
        """
        if location:
            search_path = location
        else:
            # Default to user's home directory
            search_path = str(Path.home())
        
        try:
            # Open File Explorer search
            search_url = f'search-ms:query={query}&crumb=location:{search_path}'
            os.startfile(search_url)
            return f"Searching for '{query}'..."
        except Exception as e:
            return f"I couldn't search for files: {str(e)}"
    
    def lock_screen(self):
        """Lock the Windows screen"""
        try:
            ctypes.windll.user32.LockWorkStation()
            return "Locking the screen..."
        except Exception as e:
            return f"I couldn't lock the screen: {str(e)}"
    
    def volume_up(self, amount=10):
        """Increase system volume"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            current = volume.GetMasterVolumeLevelScalar()
            new_vol = min(1.0, current + amount / 100.0)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            
            return f"Volume increased to {int(new_vol * 100)}%"
        except ImportError:
            # Fallback using keyboard simulation
            try:
                import keyboard
                for _ in range(amount // 2):
                    keyboard.press_and_release('volume up')
                return "Volume increased."
            except:
                return "I couldn't adjust the volume. Please install pycaw for volume control."
        except Exception as e:
            return f"I couldn't adjust the volume: {str(e)}"
    
    def volume_down(self, amount=10):
        """Decrease system volume"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            current = volume.GetMasterVolumeLevelScalar()
            new_vol = max(0.0, current - amount / 100.0)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            
            return f"Volume decreased to {int(new_vol * 100)}%"
        except ImportError:
            try:
                import keyboard
                for _ in range(amount // 2):
                    keyboard.press_and_release('volume down')
                return "Volume decreased."
            except:
                return "I couldn't adjust the volume. Please install pycaw for volume control."
        except Exception as e:
            return f"I couldn't adjust the volume: {str(e)}"
    
    def mute(self):
        """Mute system audio"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            
            return "Audio muted."
        except ImportError:
            try:
                import keyboard
                keyboard.press_and_release('volume mute')
                return "Audio muted."
            except:
                return "I couldn't mute the audio."
        except Exception as e:
            return f"I couldn't mute the audio: {str(e)}"
    
    def unmute(self):
        """Unmute system audio"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)
            
            return "Audio unmuted."
        except ImportError:
            try:
                import keyboard
                keyboard.press_and_release('volume mute')
                return "Audio unmuted."
            except:
                return "I couldn't unmute the audio."
        except Exception as e:
            return f"I couldn't unmute the audio: {str(e)}"
    
    def get_system_info(self):
        """Get basic system information"""
        import platform
        
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "computer_name": platform.node()
        }
        
        return (f"You're running {info['os']} version {info['os_version']} "
                f"on a {info['machine']} system. Computer name: {info['computer_name']}")
