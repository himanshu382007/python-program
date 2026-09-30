"""
Garun AI Assistant - Browser Automation
========================================
Web browsing and search capabilities
"""

import webbrowser
import subprocess
import urllib.parse


class BrowserController:
    """
    Browser automation for Garun.
    - Open websites
    - Search Google, YouTube, etc.
    - Quick links to common sites
    """
    
    def __init__(self):
        # Quick links for common sites
        self.quick_sites = {
            # Search engines
            "google": "https://www.google.com",
            "bing": "https://www.bing.com",
            "duckduckgo": "https://duckduckgo.com",
            
            # Social media
            "youtube": "https://www.youtube.com",
            "twitter": "https://twitter.com",
            "x": "https://twitter.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com",
            
            # Development
            "github": "https://github.com",
            "stackoverflow": "https://stackoverflow.com",
            "chatgpt": "https://chat.openai.com",
            "claude": "https://claude.ai",
            "gemini": "https://gemini.google.com",
            
            # Entertainment
            "netflix": "https://www.netflix.com",
            "hotstar": "https://www.hotstar.com",
            "prime video": "https://www.primevideo.com",
            "spotify": "https://open.spotify.com",
            
            # Utilities
            "gmail": "https://mail.google.com",
            "google drive": "https://drive.google.com",
            "google docs": "https://docs.google.com",
            "google sheets": "https://sheets.google.com",
            "whatsapp": "https://web.whatsapp.com",
            "telegram": "https://web.telegram.org",
            
            # Education
            "wikipedia": "https://www.wikipedia.org",
            "coursera": "https://www.coursera.org",
            "udemy": "https://www.udemy.com",
            
            # News
            "news": "https://news.google.com",
            "bbc": "https://www.bbc.com",
            "cnn": "https://www.cnn.com",
        }
        
        # Search URL templates
        self.search_templates = {
            "google": "https://www.google.com/search?q={}",
            "youtube": "https://www.youtube.com/results?search_query={}",
            "bing": "https://www.bing.com/search?q={}",
            "duckduckgo": "https://duckduckgo.com/?q={}",
            "wikipedia": "https://en.wikipedia.org/wiki/Special:Search?search={}",
            "github": "https://github.com/search?q={}",
            "stackoverflow": "https://stackoverflow.com/search?q={}",
            "amazon": "https://www.amazon.in/s?k={}",
            "flipkart": "https://www.flipkart.com/search?q={}",
        }
    
    def open_url(self, url):
        """
        Open a URL in the default browser.
        """
        try:
            # Add https if not present
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            
            webbrowser.open(url)
            return f"Opening {url}"
        except Exception as e:
            return f"Failed to open URL: {e}"
    
    def open_site(self, site_name):
        """
        Open a quick site by name.
        """
        site_lower = site_name.lower()
        
        if site_lower in self.quick_sites:
            url = self.quick_sites[site_lower]
            webbrowser.open(url)
            return f"Opening {site_name}"
        else:
            # Try opening as direct URL
            return self.open_url(site_name)
    
    def search(self, query, engine="google"):
        """
        Search the web using specified engine.
        
        Args:
            query: Search query
            engine: Search engine (google, youtube, bing, etc.)
        """
        engine = engine.lower()
        
        if engine not in self.search_templates:
            engine = "google"
        
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        url = self.search_templates[engine].format(encoded_query)
        
        webbrowser.open(url)
        return f"Searching {engine.title()} for: {query}"
    
    def search_google(self, query):
        """Search Google"""
        return self.search(query, "google")
    
    def search_youtube(self, query):
        """Search YouTube"""
        return self.search(query, "youtube")
    
    def search_github(self, query):
        """Search GitHub"""
        return self.search(query, "github")
    
    def search_shopping(self, query, site="amazon"):
        """Search shopping sites"""
        return self.search(query, site)
    
    # ==========================================
    # BROWSER CONTROL
    # ==========================================
    
    def open_incognito(self, url=""):
        """Open browser in incognito/private mode"""
        try:
            # Try Chrome first
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if not url:
                url = "about:blank"
            
            subprocess.Popen([chrome_path, "--incognito", url])
            return "Opening Chrome in incognito mode"
        except:
            try:
                # Try Edge
                subprocess.Popen(["msedge", "--inprivate", url])
                return "Opening Edge in private mode"
            except:
                webbrowser.open(url)
                return "Opened in default browser (couldn't find Chrome/Edge for incognito)"
    
    def close_browser(self):
        """Close browser windows (careful with this!)"""
        try:
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], 
                         capture_output=True, timeout=5)
            return "Chrome closed"
        except:
            return "Couldn't close browser"
    
    # ==========================================
    # QUICK ACTIONS
    # ==========================================
    
    def check_email(self):
        """Open Gmail"""
        return self.open_site("gmail")
    
    def watch_youtube(self, query=None):
        """Open YouTube or search"""
        if query:
            return self.search_youtube(query)
        return self.open_site("youtube")
    
    def open_github(self, repo=None):
        """Open GitHub or specific repo"""
        if repo:
            return self.open_url(f"https://github.com/{repo}")
        return self.open_site("github")
    
    def code_help(self, query):
        """Search for coding help on StackOverflow"""
        return self.search(query, "stackoverflow")
    
    # ==========================================
    # BRAVE BROWSER
    # ==========================================
    
    def open_in_brave(self, url=""):
        """Open URL in Brave browser"""
        try:
            brave_paths = [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            ]
            
            for brave_path in brave_paths:
                if __import__('os').path.exists(brave_path):
                    if not url:
                        url = "about:blank"
                    elif not url.startswith(("http://", "https://")):
                        url = "https://" + url
                    
                    subprocess.Popen([brave_path, url])
                    return f"🦁 Opening Brave: {url}"
            
            return "Brave browser not found. Please install Brave."
        except Exception as e:
            return f"Error opening Brave: {e}"
    
    def search_in_brave(self, query, engine="google"):
        """Search using Brave browser"""
        try:
            brave_paths = [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            ]
            
            # Get search URL
            engine = engine.lower()
            if engine == "youtube":
                url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"
            else:
                url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
            
            for brave_path in brave_paths:
                if __import__('os').path.exists(brave_path):
                    subprocess.Popen([brave_path, url])
                    return f"🦁 Searching {engine.title()} in Brave: {query}"
            
            # Fallback to default browser
            webbrowser.open(url)
            return f"Searching {engine.title()} for: {query} (Brave not found, using default browser)"
        except Exception as e:
            return f"Error: {e}"
    
    def brave_youtube(self, query):
        """Search YouTube in Brave browser"""
        return self.search_in_brave(query, "youtube")
    
    def brave_incognito(self, url=""):
        """Open Brave in private mode"""
        try:
            brave_paths = [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            ]
            
            for brave_path in brave_paths:
                if __import__('os').path.exists(brave_path):
                    if not url:
                        url = "about:blank"
                    subprocess.Popen([brave_path, "--incognito", url])
                    return "🦁 Opening Brave in Private mode..."
            
            return "Brave browser not found."
        except Exception as e:
            return f"Error: {e}"

