"""
Garun AI Assistant - Premium Chat Widget
=========================================
Modern chat interface with elegant message bubbles and smooth interactions
"""

import customtkinter as ctk
from datetime import datetime
from ui.themes import Colors, Fonts, Dimensions, Icons


class MessageBubble(ctk.CTkFrame):
    """Premium chat message bubble with modern styling"""
    
    def __init__(self, parent, message, is_user=True, timestamp=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.is_user = is_user
        
        # Different styles for user vs assistant
        if is_user:
            bg_color = Colors.BG_TERTIARY
            border_color = Colors.BLUE_DARK
            text_color = Colors.TEXT_PRIMARY
        else:
            bg_color = Colors.PRIMARY_SUBTLE
            border_color = Colors.PRIMARY_DARK
            text_color = Colors.TEXT_PRIMARY
        
        # Configure frame
        self.configure(
            fg_color=bg_color,
            corner_radius=Dimensions.RADIUS_LG,
            border_width=1,
            border_color=border_color
        )
        
        # Message content
        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            font=Fonts.BODY,
            text_color=text_color,
            wraplength=300,
            justify="left",
            anchor="w"
        )
        self.message_label.pack(
            padx=Dimensions.PAD_MD,
            pady=(Dimensions.PAD_SM, Dimensions.PAD_XS),
            anchor="w"
        )
        
        # Timestamp with subtle styling
        time_str = timestamp or datetime.now().strftime("%H:%M")
        self.time_label = ctk.CTkLabel(
            self,
            text=time_str,
            font=Fonts.TINY,
            text_color=Colors.TEXT_MUTED
        )
        self.time_label.pack(
            padx=Dimensions.PAD_MD,
            pady=(0, Dimensions.PAD_SM),
            anchor="e" if is_user else "w"
        )


class ChatWidget(ctk.CTkFrame):
    """Premium chat interface with modern design"""
    
    def __init__(self, parent, on_send_message=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_send_message = on_send_message
        self.messages = []
        
        # Configure frame
        self.configure(fg_color="transparent")
        
        # Create layout
        self._create_widgets()
    
    def _create_widgets(self):
        """Create chat interface widgets"""
        
        # ============================================
        # CHAT HISTORY SECTION
        # ============================================
        
        # Chat container with subtle glow border
        self.chat_container = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=Dimensions.RADIUS_LG,
            border_width=1,
            border_color=Colors.BORDER_GLOW
        )
        self.chat_container.pack(
            fill="both",
            expand=True,
            padx=Dimensions.PAD_SM,
            pady=Dimensions.PAD_SM
        )
        
        # Header bar
        self.header_frame = ctk.CTkFrame(
            self.chat_container,
            fg_color=Colors.BG_TERTIARY,
            corner_radius=0,
            height=35
        )
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        
        self.chat_title = ctk.CTkLabel(
            self.header_frame,
            text="💬 CONVERSATION",
            font=("Segoe UI Semibold", 11),
            text_color=Colors.PRIMARY
        )
        self.chat_title.pack(side="left", padx=Dimensions.PAD_MD, pady=Dimensions.PAD_XS)
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            self.header_frame,
            text="Clear",
            width=50,
            height=25,
            font=Fonts.TINY,
            fg_color="transparent",
            hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MUTED,
            corner_radius=Dimensions.RADIUS_SM,
            command=self.clear_chat
        )
        self.clear_btn.pack(side="right", padx=Dimensions.PAD_SM, pady=Dimensions.PAD_XS)
        
        # Scrollable chat area
        self.chat_frame = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color="transparent",
            scrollbar_button_color=Colors.PRIMARY_DARK,
            scrollbar_button_hover_color=Colors.PRIMARY
        )
        self.chat_frame.pack(
            fill="both",
            expand=True,
            padx=Dimensions.PAD_XS,
            pady=Dimensions.PAD_XS
        )
        
        # ============================================
        # INPUT SECTION
        # ============================================
        
        self.input_container = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=Dimensions.RADIUS_LG,
            border_width=1,
            border_color=Colors.BORDER_GLOW,
            height=65
        )
        self.input_container.pack(
            fill="x",
            padx=Dimensions.PAD_SM,
            pady=(0, Dimensions.PAD_SM)
        )
        self.input_container.pack_propagate(False)
        
        # Text input with modern styling
        self.input_entry = ctk.CTkEntry(
            self.input_container,
            placeholder_text="Type a message or say 'Hey Garun'...",
            font=Fonts.BODY,
            height=45,
            fg_color=Colors.BG_TERTIARY,
            border_color=Colors.BLUE_DARK,
            border_width=2,
            text_color=Colors.TEXT_PRIMARY,
            placeholder_text_color=Colors.TEXT_MUTED,
            corner_radius=Dimensions.RADIUS_MD
        )
        self.input_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(Dimensions.PAD_MD, Dimensions.PAD_SM),
            pady=Dimensions.PAD_SM
        )
        self.input_entry.bind("<Return>", self._on_enter_pressed)
        self.input_entry.bind("<FocusIn>", self._on_focus_in)
        self.input_entry.bind("<FocusOut>", self._on_focus_out)
        
        # Send button with glow effect
        self.send_button = ctk.CTkButton(
            self.input_container,
            text=Icons.SEND,
            width=50,
            height=45,
            font=("Segoe UI", 20),
            fg_color=Colors.PRIMARY_DARK,
            hover_color=Colors.PRIMARY,
            text_color=Colors.BG_DARK,
            corner_radius=Dimensions.RADIUS_MD,
            command=self._send_message
        )
        self.send_button.pack(
            side="right",
            padx=(0, Dimensions.PAD_MD),
            pady=Dimensions.PAD_SM
        )
        
        # Welcome message
        self._add_welcome_message()
    
    def _on_focus_in(self, event):
        """Handle input focus in"""
        self.input_entry.configure(border_color=Colors.PRIMARY)
    
    def _on_focus_out(self, event):
        """Handle input focus out"""
        self.input_entry.configure(border_color=Colors.BLUE_DARK)
    
    def _add_welcome_message(self):
        """Add stylized welcome message"""
        welcome_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=Colors.BG_TERTIARY,
            corner_radius=Dimensions.RADIUS_LG
        )
        welcome_frame.pack(fill="x", pady=Dimensions.PAD_MD, padx=Dimensions.PAD_SM)
        
        # Welcome icon/title
        title_label = ctk.CTkLabel(
            welcome_frame,
            text="✦ Welcome to Garun ✦",
            font=("Segoe UI Semibold", 14),
            text_color=Colors.PRIMARY
        )
        title_label.pack(pady=(Dimensions.PAD_MD, Dimensions.PAD_XS))
        
        # Welcome message
        msg_label = ctk.CTkLabel(
            welcome_frame,
            text="I'm your personal AI assistant. How can I help you today?",
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=280
        )
        msg_label.pack(pady=(0, Dimensions.PAD_SM))
        
        # Quick action hints
        hints_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        hints_frame.pack(pady=(0, Dimensions.PAD_MD))
        
        hints = ["💬 Chat", "🎤 Voice", "📱 Apps", "☀ Weather"]
        for hint in hints:
            hint_label = ctk.CTkLabel(
                hints_frame,
                text=hint,
                font=Fonts.SMALL,
                text_color=Colors.TEXT_MUTED,
                fg_color=Colors.BG_HOVER,
                corner_radius=Dimensions.RADIUS_SM,
                padx=8,
                pady=2
            )
            hint_label.pack(side="left", padx=2)
    
    def _on_enter_pressed(self, event):
        """Handle Enter key press"""
        self._send_message()
    
    def _send_message(self):
        """Send the current input message"""
        message = self.input_entry.get().strip()
        if message:
            # Add user message to chat
            self.add_message(message, is_user=True)
            
            # Clear input
            self.input_entry.delete(0, "end")
            
            # Callback to process message
            if self.on_send_message:
                self.on_send_message(message)
    
    def add_message(self, message, is_user=True, timestamp=None):
        """Add a new message bubble to the chat"""
        
        # Container for alignment
        container = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        container.pack(
            fill="x",
            pady=(Dimensions.PAD_XS, Dimensions.PAD_SM)
        )
        
        # Sender indicator
        sender = "You" if is_user else "Garun"
        sender_icon = "👤" if is_user else "🤖"
        sender_color = Colors.TEXT_SECONDARY if is_user else Colors.PRIMARY
        
        sender_label = ctk.CTkLabel(
            container,
            text=f"{sender_icon} {sender}",
            font=("Segoe UI Semibold", 10),
            text_color=sender_color
        )
        sender_label.pack(
            anchor="e" if is_user else "w",
            padx=Dimensions.PAD_SM
        )
        
        # Message bubble
        bubble = MessageBubble(
            container,
            message=message,
            is_user=is_user,
            timestamp=timestamp
        )
        bubble.pack(
            anchor="e" if is_user else "w",
            padx=Dimensions.PAD_SM
        )
        
        self.messages.append({
            "message": message,
            "is_user": is_user,
            "timestamp": timestamp or datetime.now().strftime("%H:%M")
        })
        
        # Smooth scroll to bottom
        self.after(50, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))
    
    def clear_chat(self):
        """Clear all messages from the chat"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.messages = []
        self._add_welcome_message()
    
    def get_input_text(self):
        """Get current text in input field"""
        return self.input_entry.get()
    
    def set_input_text(self, text):
        """Set text in input field"""
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, text)
    
    def focus_input(self):
        """Focus the input field"""
        self.input_entry.focus_set()
