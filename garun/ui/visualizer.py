"""
Garun AI Assistant - Premium Voice Visualizer
==============================================
Stunning animated circular visualizer with particle effects
"""

import customtkinter as ctk
import math
import random
from ui.themes import Colors, Dimensions


class VoiceVisualizer(ctk.CTkCanvas):
    """
    Premium animated circular visualizer for voice input.
    Features particle effects, smooth gradients, and dynamic animations.
    """
    
    def __init__(self, parent, size=150, **kwargs):
        # Use the parent's background color
        bg_color = Colors.BG_SECONDARY
        
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=bg_color,
            highlightthickness=0,
            **kwargs
        )
        
        self.size = size
        self.center = size // 2
        self.base_radius = size // 3
        
        # Animation state
        self.state = "idle"  # idle, listening, speaking, processing
        self.animation_phase = 0
        self.particles = []
        self.wave_points = []
        
        # Initialize particles for effects
        self._init_particles()
        
        # Colors for different states
        self.state_colors = {
            "idle": (Colors.PRIMARY_DARK, Colors.BLUE),
            "listening": (Colors.PRIMARY, Colors.PRIMARY_LIGHT),
            "speaking": (Colors.ACCENT, Colors.ACCENT_LIGHT),
            "processing": (Colors.PURPLE, Colors.PURPLE_LIGHT)
        }
        
        # Start animation loop
        self._animate()
    
    def _init_particles(self):
        """Initialize floating particles"""
        self.particles = []
        for _ in range(15):
            self.particles.append({
                "x": random.uniform(0, self.size),
                "y": random.uniform(0, self.size),
                "size": random.uniform(1, 3),
                "speed": random.uniform(0.2, 0.8),
                "angle": random.uniform(0, 2 * math.pi),
                "opacity": random.uniform(0.3, 0.8)
            })
    
    def set_state(self, state):
        """Set visualizer state: idle, listening, speaking, processing"""
        if state in self.state_colors:
            self.state = state
    
    def _animate(self):
        """Main animation loop"""
        self.delete("all")
        
        # Draw particles in background
        self._draw_particles()
        
        # Draw based on current state
        if self.state == "idle":
            self._draw_idle()
        elif self.state == "listening":
            self._draw_listening()
        elif self.state == "speaking":
            self._draw_speaking()
        elif self.state == "processing":
            self._draw_processing()
        
        # Update phase
        self.animation_phase += 0.04
        if self.animation_phase > 2 * math.pi:
            self.animation_phase = 0
        
        # Update particles
        self._update_particles()
        
        # Continue animation
        self.after(33, self._animate)  # ~30 FPS
    
    def _draw_particles(self):
        """Draw floating ambient particles"""
        primary_color, secondary_color = self.state_colors[self.state]
        
        for p in self.particles:
            # Calculate distance from center for color intensity
            dist = math.sqrt((p["x"] - self.center)**2 + (p["y"] - self.center)**2)
            if dist < self.base_radius * 1.5:
                color = primary_color
            else:
                color = Colors.TEXT_MUTED
            
            self.create_oval(
                p["x"] - p["size"], p["y"] - p["size"],
                p["x"] + p["size"], p["y"] + p["size"],
                fill=color,
                outline=""
            )
    
    def _update_particles(self):
        """Update particle positions"""
        for p in self.particles:
            # Move particle
            p["x"] += math.cos(p["angle"]) * p["speed"]
            p["y"] += math.sin(p["angle"]) * p["speed"]
            
            # Slight drift toward center when active
            if self.state != "idle":
                dx = self.center - p["x"]
                dy = self.center - p["y"]
                p["x"] += dx * 0.01
                p["y"] += dy * 0.01
            
            # Wrap around edges
            if p["x"] < 0: p["x"] = self.size
            if p["x"] > self.size: p["x"] = 0
            if p["y"] < 0: p["y"] = self.size
            if p["y"] > self.size: p["y"] = 0
            
            # Random direction changes
            if random.random() < 0.02:
                p["angle"] += random.uniform(-0.5, 0.5)
    
    def _draw_idle(self):
        """Draw idle state - elegant pulsing orb"""
        primary_color, secondary_color = self.state_colors["idle"]
        
        # Breathing animation
        pulse = math.sin(self.animation_phase) * 0.12 + 1
        
        # Multiple glow layers (outer to inner)
        for i in range(5):
            r = self.base_radius * pulse * (1.4 - i * 0.1)
            width = 1 + (4 - i) * 0.5
            color = primary_color if i < 2 else secondary_color
            
            self.create_oval(
                self.center - r, self.center - r,
                self.center + r, self.center + r,
                outline=color,
                width=width
            )
        
        # Core orb with gradient effect
        core_radius = self.base_radius * 0.4 * pulse
        
        # Inner glow
        for i in range(3):
            r = core_radius + i * 3
            self.create_oval(
                self.center - r, self.center - r,
                self.center + r, self.center + r,
                fill=Colors.PRIMARY_GLOW if i > 0 else primary_color,
                outline=""
            )
        
        # Center bright spot
        self.create_oval(
            self.center - 4, self.center - 4,
            self.center + 4, self.center + 4,
            fill=Colors.TEXT_BRIGHT,
            outline=""
        )
        
        # Orbiting accent dots
        for i in range(3):
            angle = self.animation_phase * 0.5 + (2 * math.pi * i / 3)
            orbit_radius = self.base_radius * 1.1
            x = self.center + orbit_radius * math.cos(angle)
            y = self.center + orbit_radius * math.sin(angle)
            
            self.create_oval(
                x - 2, y - 2, x + 2, y + 2,
                fill=primary_color,
                outline=""
            )
    
    def _draw_listening(self):
        """Draw listening state - dynamic audio wave circle"""
        primary_color, secondary_color = self.state_colors["listening"]
        
        # Outer ring
        self.create_oval(
            self.center - self.base_radius * 1.3,
            self.center - self.base_radius * 1.3,
            self.center + self.base_radius * 1.3,
            self.center + self.base_radius * 1.3,
            outline=primary_color,
            width=2
        )
        
        # Dynamic audio bars in circle
        num_bars = 24
        for i in range(num_bars):
            angle = (2 * math.pi * i / num_bars) - math.pi / 2
            
            # Animated height
            wave = math.sin(self.animation_phase * 3 + i * 0.3)
            noise = random.uniform(-0.2, 0.2)
            height = 15 + (wave + noise) * 18
            
            inner_r = self.base_radius * 0.45
            outer_r = inner_r + height
            
            x1 = self.center + inner_r * math.cos(angle)
            y1 = self.center + inner_r * math.sin(angle)
            x2 = self.center + outer_r * math.cos(angle)
            y2 = self.center + outer_r * math.sin(angle)
            
            # Color gradient based on height
            color = primary_color if height > 20 else secondary_color
            
            self.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=4,
                capstyle="round"
            )
        
        # Pulsing center
        pulse = math.sin(self.animation_phase * 2) * 0.15 + 1
        center_r = 10 * pulse
        self.create_oval(
            self.center - center_r, self.center - center_r,
            self.center + center_r, self.center + center_r,
            fill=primary_color,
            outline=""
        )
        
        # Status indicator
        self._draw_status("● LISTENING", primary_color)
    
    def _draw_speaking(self):
        """Draw speaking state - rippling wave rings"""
        primary_color, secondary_color = self.state_colors["speaking"]
        
        # Expanding ripple rings
        num_rings = 4
        for i in range(num_rings):
            phase_offset = (self.animation_phase * 1.5 + i * 0.8) % (2 * math.pi)
            scale = phase_offset / (2 * math.pi)
            
            radius = self.base_radius * 0.3 + scale * self.base_radius
            alpha = 1 - scale
            width = max(1, int(4 * alpha))
            
            self.create_oval(
                self.center - radius, self.center - radius,
                self.center + radius, self.center + radius,
                outline=primary_color,
                width=width
            )
        
        # Sound wave effect around outer ring
        wave_radius = self.base_radius * 1.2
        points = []
        for i in range(60):
            angle = (2 * math.pi * i / 60)
            wave = math.sin(self.animation_phase * 4 + i * 0.2) * 5
            r = wave_radius + wave
            x = self.center + r * math.cos(angle)
            y = self.center + r * math.sin(angle)
            points.extend([x, y])
        
        if len(points) >= 6:
            self.create_polygon(points, outline=secondary_color, fill="", width=1, smooth=True)
        
        # Core speaker icon effect
        pulse = math.sin(self.animation_phase * 3) * 0.2 + 1
        core_radius = self.base_radius * 0.35 * pulse
        
        # Glowing core
        for i in range(3):
            r = core_radius + i * 5
            color = primary_color if i == 0 else Colors.ACCENT_GLOW
            self.create_oval(
                self.center - r, self.center - r,
                self.center + r, self.center + r,
                fill=color if i == 0 else "",
                outline=color if i > 0 else ""
            )
        
        # Status indicator
        self._draw_status("◉ SPEAKING", primary_color)
    
    def _draw_processing(self):
        """Draw processing state - orbital spinner"""
        primary_color, secondary_color = self.state_colors["processing"]
        
        # Outer rotating ring
        self.create_oval(
            self.center - self.base_radius * 1.1,
            self.center - self.base_radius * 1.1,
            self.center + self.base_radius * 1.1,
            self.center + self.base_radius * 1.1,
            outline=Colors.BG_TERTIARY,
            width=3
        )
        
        # Spinning arc
        arc_extent = 90
        start_angle = math.degrees(self.animation_phase * 3)
        self.create_arc(
            self.center - self.base_radius * 1.1,
            self.center - self.base_radius * 1.1,
            self.center + self.base_radius * 1.1,
            self.center + self.base_radius * 1.1,
            start=start_angle,
            extent=arc_extent,
            outline=primary_color,
            style="arc",
            width=3
        )
        
        # Orbiting dots with trail effect
        num_dots = 6
        for i in range(num_dots):
            angle = (2 * math.pi * i / num_dots) + self.animation_phase * 2
            
            # Each dot has slight trail
            for j in range(3):
                trail_angle = angle - j * 0.1
                dist = self.base_radius * 0.65
                x = self.center + dist * math.cos(trail_angle)
                y = self.center + dist * math.sin(trail_angle)
                
                size = 6 - j * 1.5
                color = primary_color if j == 0 else secondary_color
                
                self.create_oval(
                    x - size, y - size,
                    x + size, y + size,
                    fill=color,
                    outline=""
                )
        
        # Center pulsing core
        pulse = math.sin(self.animation_phase * 4) * 0.2 + 1
        self.create_oval(
            self.center - 8 * pulse, self.center - 8 * pulse,
            self.center + 8 * pulse, self.center + 8 * pulse,
            fill=primary_color,
            outline=""
        )
        
        # Status indicator
        self._draw_status("⟳ PROCESSING", primary_color)
    
    def _draw_status(self, text, color):
        """Draw status text below visualizer"""
        self.create_text(
            self.center, self.size - 8,
            text=text,
            fill=color,
            font=("Segoe UI Semibold", 9)
        )
