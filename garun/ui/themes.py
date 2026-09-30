"""
Garun AI Assistant - Premium Cyberpunk Theme
=============================================
Ultra-modern futuristic color palette with neon accents and glassmorphism
"""

# ============================================
# COLOR PALETTE - ENHANCED NEON CYBERPUNK
# ============================================

class Colors:
    """Premium cyberpunk color scheme for Garun"""
    
    # Backgrounds - Deep space blacks with blue undertones
    BG_DARK = "#050510"          # Deepest void
    BG_PRIMARY = "#0a0a1a"       # Main background
    BG_SECONDARY = "#0f0f25"     # Card backgrounds
    BG_TERTIARY = "#151535"      # Elevated surfaces
    BG_HOVER = "#1a1a45"         # Hover states
    BG_GRADIENT_START = "#0a0a1a"
    BG_GRADIENT_END = "#1a0a2a"
    
    # Primary - Electric Cyan/Teal
    PRIMARY = "#00ffff"          # Bright neon cyan
    PRIMARY_DARK = "#00d4d4"     # Darker cyan
    PRIMARY_LIGHT = "#66ffff"    # Lighter cyan
    PRIMARY_GLOW = "#004455"     # Cyan glow
    PRIMARY_SUBTLE = "#0a2530"   # Very subtle cyan
    
    # Accent - Hot Magenta/Pink
    ACCENT = "#ff00ff"           # Neon magenta
    ACCENT_DARK = "#cc00cc"      # Darker magenta
    ACCENT_LIGHT = "#ff66ff"     # Lighter magenta
    ACCENT_GLOW = "#550055"      # Magenta glow
    
    # Secondary - Vibrant Purple
    PURPLE = "#9d4edd"           # Vivid purple
    PURPLE_DARK = "#7b2cbf"      # Deep purple
    PURPLE_LIGHT = "#c77dff"     # Light purple
    
    # Electric Blue
    BLUE = "#00a8ff"             # Electric blue
    BLUE_DARK = "#0088cc"        # Darker blue
    BLUE_GLOW = "#003355"        # Blue glow
    
    # Neon Green
    GREEN = "#00ff88"            # Matrix green
    GREEN_DARK = "#00cc6a"       # Darker green
    GREEN_GLOW = "#003322"       # Green glow
    
    # Warning/Alert Colors
    ORANGE = "#ff8c00"           # Neon orange
    RED = "#ff3355"              # Hot red
    YELLOW = "#ffff00"           # Bright yellow
    
    # Text Colors - High contrast
    TEXT_PRIMARY = "#f0f0ff"     # Almost white with hint of blue
    TEXT_SECONDARY = "#b0b0cc"   # Light gray-blue
    TEXT_MUTED = "#6060a0"       # Muted blue-gray
    TEXT_BRIGHT = "#ffffff"      # Pure white
    TEXT_GLOW = "#00ffff"        # Glowing text
    
    # Gradients (for canvas/custom drawing)
    GRADIENT_CYAN_MAGENTA = ("#00ffff", "#ff00ff")
    GRADIENT_BLUE_PURPLE = ("#00a8ff", "#9d4edd")
    GRADIENT_PURPLE_PINK = ("#9d4edd", "#ff00ff")
    
    # Status Colors
    SUCCESS = "#00ff88"
    WARNING = "#ff8c00"
    ERROR = "#ff3355"
    INFO = "#00ffff"
    
    # Glassmorphism Effects - NO ALPHA, use solid colors
    GLASS_BG = "#151535"          # Solid background
    GLASS_BORDER = "#3a3a5a"      # Light border
    GLASS_HIGHLIGHT = "#2a2a4a"   # Highlight
    BORDER_GLOW = "#0088aa"       # Glowing border (solid cyan-ish)
    
    # Special Effects
    SHADOW = "#000000"
    NEON_GLOW = "#00ffff"
    

# ============================================
# FONTS - MODERN TYPOGRAPHY
# ============================================

class Fonts:
    """Modern font configurations"""
    
    # Font families
    FAMILY_PRIMARY = ("Segoe UI", "Arial", "sans-serif")
    FAMILY_MONO = ("JetBrains Mono", "Consolas", "Courier New", "monospace")
    FAMILY_DISPLAY = ("Segoe UI Light", "Segoe UI", "Arial")
    FAMILY_HEADING = ("Segoe UI Semibold", "Segoe UI", "Arial")
    
    # Font sizes
    SIZE_XS = 10
    SIZE_SM = 11
    SIZE_MD = 13
    SIZE_LG = 15
    SIZE_XL = 18
    SIZE_XXL = 24
    SIZE_TITLE = 32
    SIZE_HERO = 42
    
    # Pre-configured fonts
    HERO = ("Segoe UI Light", 36, "normal")
    TITLE = ("Segoe UI Light", 26, "normal")
    HEADING = ("Segoe UI Semibold", 18, "normal")
    SUBHEADING = ("Segoe UI", 15, "bold")
    BODY = ("Segoe UI", 13, "normal")
    BODY_BOLD = ("Segoe UI", 13, "bold")
    SMALL = ("Segoe UI", 11, "normal")
    TINY = ("Segoe UI", 10, "normal")
    MONO = ("Consolas", 12, "normal")
    BUTTON = ("Segoe UI Semibold", 12, "normal")


# ============================================
# DIMENSIONS - REFINED SPACING
# ============================================

class Dimensions:
    """UI dimension constants"""
    
    # Window - Larger for better presence
    WINDOW_WIDTH = 480
    WINDOW_HEIGHT = 720
    WINDOW_MIN_WIDTH = 400
    WINDOW_MIN_HEIGHT = 550
    
    # Padding - Generous spacing
    PAD_XS = 4
    PAD_SM = 8
    PAD_MD = 14
    PAD_LG = 20
    PAD_XL = 28
    PAD_XXL = 40
    
    # Border radius - Smoother curves
    RADIUS_XS = 4
    RADIUS_SM = 8
    RADIUS_MD = 12
    RADIUS_LG = 18
    RADIUS_XL = 28
    RADIUS_ROUND = 9999
    
    # Component sizes
    BUTTON_HEIGHT = 42
    BUTTON_WIDTH = 100
    INPUT_HEIGHT = 48
    VISUALIZER_SIZE = 150
    AVATAR_SIZE = 44
    ICON_SIZE = 26
    
    # Borders
    BORDER_THIN = 1
    BORDER_NORMAL = 2
    BORDER_THICK = 3


# ============================================
# ANIMATIONS
# ============================================

class Animation:
    """Animation timing constants"""
    
    INSTANT = 50       # ms - instant feedback
    FAST = 150         # ms - quick transitions
    NORMAL = 250       # ms - standard transitions
    SLOW = 400         # ms - slow, smooth animations
    SMOOTH = 500       # ms - extra smooth
    PULSE = 1000       # ms - pulsing animations
    GLOW = 2000        # ms - slow glow cycles
    BREATHE = 3000     # ms - breathing effect


# ============================================
# ICON SET - UNICODE SYMBOLS
# ============================================

class Icons:
    """Unicode icons for UI elements"""
    
    # Navigation
    MENU = "☰"
    CLOSE = "✕"
    BACK = "←"
    FORWARD = "→"
    UP = "↑"
    DOWN = "↓"
    
    # Actions
    SEND = "➤"
    MIC = "🎤"
    MIC_OFF = "🎤"
    SPEAKER = "🔊"
    SPEAKER_OFF = "🔇"
    SETTINGS = "⚙"
    PIN = "📌"
    
    # Status
    ONLINE = "●"
    OFFLINE = "○"
    LISTENING = "◉"
    SPEAKING = "◈"
    PROCESSING = "⟳"
    SUCCESS = "✓"
    ERROR = "✗"
    WARNING = "⚠"
    
    # Features
    WEATHER = "☀"
    NEWS = "📰"
    REMINDER = "⏰"
    SMART_HOME = "🏠"
    MUSIC = "🎵"
    SEARCH = "🔍"
    
    # Decorative
    STAR = "★"
    DIAMOND = "◆"
    CIRCLE = "●"
    SQUARE = "■"
    TRIANGLE = "▲"


# ============================================
# CUSTOMTKINTER THEME CONFIG
# ============================================

def get_ctk_theme():
    """Get CustomTkinter theme configuration"""
    return {
        "CTk": {
            "fg_color": [Colors.BG_PRIMARY, Colors.BG_PRIMARY]
        },
        "CTkFrame": {
            "fg_color": [Colors.BG_SECONDARY, Colors.BG_SECONDARY],
            "border_color": [Colors.BORDER_GLOW, Colors.BORDER_GLOW],
            "border_width": 1,
            "corner_radius": Dimensions.RADIUS_MD
        },
        "CTkButton": {
            "fg_color": [Colors.PRIMARY_DARK, Colors.PRIMARY_DARK],
            "hover_color": [Colors.PRIMARY, Colors.PRIMARY],
            "text_color": [Colors.BG_DARK, Colors.BG_DARK],
            "corner_radius": Dimensions.RADIUS_SM,
            "border_width": 0
        },
        "CTkEntry": {
            "fg_color": [Colors.BG_TERTIARY, Colors.BG_TERTIARY],
            "border_color": [Colors.BLUE_DARK, Colors.PRIMARY],
            "text_color": [Colors.TEXT_PRIMARY, Colors.TEXT_PRIMARY],
            "placeholder_text_color": [Colors.TEXT_MUTED, Colors.TEXT_MUTED],
            "corner_radius": Dimensions.RADIUS_SM,
            "border_width": 2
        },
        "CTkLabel": {
            "fg_color": "transparent",
            "text_color": [Colors.TEXT_PRIMARY, Colors.TEXT_PRIMARY]
        },
        "CTkTextbox": {
            "fg_color": [Colors.BG_TERTIARY, Colors.BG_TERTIARY],
            "border_color": [Colors.BLUE_DARK, Colors.BLUE_DARK],
            "text_color": [Colors.TEXT_PRIMARY, Colors.TEXT_PRIMARY],
            "corner_radius": Dimensions.RADIUS_SM,
            "border_width": 1
        },
        "CTkScrollableFrame": {
            "fg_color": [Colors.BG_SECONDARY, Colors.BG_SECONDARY],
            "corner_radius": Dimensions.RADIUS_MD
        }
    }


# ============================================
# STYLE PRESETS
# ============================================

class StylePresets:
    """Predefined style combinations"""
    
    @staticmethod
    def neon_button():
        return {
            "fg_color": Colors.PRIMARY_DARK,
            "hover_color": Colors.PRIMARY,
            "text_color": Colors.BG_DARK,
            "corner_radius": Dimensions.RADIUS_SM,
            "border_width": 0
        }
    
    @staticmethod
    def ghost_button():
        return {
            "fg_color": "transparent",
            "hover_color": Colors.BG_HOVER,
            "text_color": Colors.PRIMARY,
            "corner_radius": Dimensions.RADIUS_SM,
            "border_width": 2,
            "border_color": Colors.PRIMARY
        }
    
    @staticmethod
    def accent_button():
        return {
            "fg_color": Colors.ACCENT_DARK,
            "hover_color": Colors.ACCENT,
            "text_color": Colors.TEXT_BRIGHT,
            "corner_radius": Dimensions.RADIUS_SM
        }
    
    @staticmethod
    def glass_card():
        return {
            "fg_color": Colors.BG_SECONDARY,
            "corner_radius": Dimensions.RADIUS_LG,
            "border_width": 1,
            "border_color": Colors.BORDER_GLOW
        }
