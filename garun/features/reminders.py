"""
Garun AI Assistant - Reminder Service
=======================================
Manages reminders with SQLite storage
"""

import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path
import threading


class ReminderService:
    """Manages reminders with persistent storage"""
    
    def __init__(self, db_path=None):
        # Set up database path
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "data"
            db_dir.mkdir(exist_ok=True)
            db_path = db_dir / "reminders.db"
        
        self.db_path = str(db_path)
        self.connection = None
        self.notification_callback = None
        self.check_thread = None
        self.running = False
        
        # Initialize database
        self._init_database()
        
        # Start reminder checker
        self._start_checker()
    
    def _init_database(self):
        """Initialize the SQLite database"""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                remind_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed INTEGER DEFAULT 0,
                notified INTEGER DEFAULT 0
            )
        ''')
        
        self.connection.commit()
    
    def _start_checker(self):
        """Start background thread to check reminders"""
        self.running = True
        
        def checker():
            while self.running:
                self._check_due_reminders()
                # Check every 30 seconds
                threading.Event().wait(30)
        
        self.check_thread = threading.Thread(target=checker, daemon=True)
        self.check_thread.start()
    
    def _check_due_reminders(self):
        """Check for due reminders and trigger notifications"""
        try:
            cursor = self.connection.cursor()
            now = datetime.now().isoformat()
            
            cursor.execute('''
                SELECT id, message, remind_at FROM reminders
                WHERE remind_at <= ? AND completed = 0 AND notified = 0
            ''', (now,))
            
            due_reminders = cursor.fetchall()
            
            for reminder_id, message, remind_at in due_reminders:
                # Mark as notified
                cursor.execute(
                    'UPDATE reminders SET notified = 1 WHERE id = ?',
                    (reminder_id,)
                )
                
                # Trigger notification
                if self.notification_callback:
                    self.notification_callback(message)
                else:
                    print(f"[Garun Reminder] {message}")
            
            self.connection.commit()
            
        except Exception as e:
            print(f"[Garun] Reminder check error: {e}")
    
    def set_notification_callback(self, callback):
        """Set callback for reminder notifications"""
        self.notification_callback = callback
    
    def add_reminder(self, message, remind_at):
        """
        Add a new reminder.
        
        Args:
            message: Reminder message
            remind_at: datetime when to remind
            
        Returns:
            Confirmation message
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO reminders (message, remind_at)
                VALUES (?, ?)
            ''', (message, remind_at.isoformat()))
            
            self.connection.commit()
            
            # Format confirmation
            time_str = remind_at.strftime("%I:%M %p on %B %d")
            return f"I'll remind you to '{message}' at {time_str}."
            
        except Exception as e:
            return f"I couldn't set the reminder: {str(e)}"
    
    def parse_and_set(self, text):
        """
        Parse natural language and set reminder.
        
        Args:
            text: Natural language reminder request
            
        Returns:
            Confirmation or error message
        """
        text_lower = text.lower()
        
        # Extract the reminder message
        message = self._extract_message(text_lower)
        if not message:
            return "What would you like me to remind you about?"
        
        # Extract the time
        remind_time = self._parse_time(text_lower)
        if not remind_time:
            return f"When would you like me to remind you to '{message}'?"
        
        return self.add_reminder(message, remind_time)
    
    def _extract_message(self, text):
        """Extract reminder message from text"""
        # Patterns to extract the message
        patterns = [
            r'remind me to (.+?) (?:at|in|on|tomorrow|today)',
            r'remind me to (.+)',
            r'reminder to (.+?) (?:at|in|on)',
            r'reminder to (.+)',
            r'remember to (.+?) (?:at|in|on)',
            r'remember to (.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                message = match.group(1).strip()
                # Clean up trailing time words
                message = re.sub(r'\s+(at|in|on|tomorrow|today|tonight).*$', '', message)
                return message
        
        return None
    
    def _parse_time(self, text):
        """Parse time from natural language"""
        now = datetime.now()
        
        # Check for specific time patterns
        
        # "at X:XX" or "at X"
        time_match = re.search(r'at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            period = time_match.group(3)
            
            if period == 'pm' and hour < 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            elif period is None and hour < 12 and hour < now.hour:
                # Assume PM if hour has passed
                hour += 12
            
            remind_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, set for tomorrow
            if remind_time <= now:
                remind_time += timedelta(days=1)
            
            return remind_time
        
        # "in X minutes/hours"
        in_match = re.search(r'in (\d+) (minute|minutes|min|mins|hour|hours|hr|hrs)', text)
        if in_match:
            amount = int(in_match.group(1))
            unit = in_match.group(2)
            
            if 'hour' in unit or 'hr' in unit:
                return now + timedelta(hours=amount)
            else:
                return now + timedelta(minutes=amount)
        
        # "tomorrow"
        if 'tomorrow' in text:
            # Default to 9 AM tomorrow
            tomorrow = now + timedelta(days=1)
            remind_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            
            # Check if there's a specific time
            time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2) or 0)
                period = time_match.group(3)
                
                if period == 'pm' and hour < 12:
                    hour += 12
                elif period == 'am' and hour == 12:
                    hour = 0
                
                remind_time = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            return remind_time
        
        # "tonight"
        if 'tonight' in text:
            return now.replace(hour=20, minute=0, second=0, microsecond=0)
        
        # Default: 1 hour from now
        return now + timedelta(hours=1)
    
    def list_reminders(self, include_completed=False):
        """
        List all active reminders.
        
        Args:
            include_completed: Include completed reminders
            
        Returns:
            Formatted list of reminders
        """
        try:
            cursor = self.connection.cursor()
            
            if include_completed:
                cursor.execute('SELECT id, message, remind_at, completed FROM reminders ORDER BY remind_at')
            else:
                cursor.execute('SELECT id, message, remind_at, completed FROM reminders WHERE completed = 0 ORDER BY remind_at')
            
            reminders = cursor.fetchall()
            
            if not reminders:
                return "You have no active reminders."
            
            response = "📝 Your reminders:\n\n"
            for reminder_id, message, remind_at, completed in reminders:
                remind_dt = datetime.fromisoformat(remind_at)
                time_str = remind_dt.strftime("%I:%M %p, %b %d")
                status = "✓" if completed else "○"
                response += f"{status} {message}\n   ⏰ {time_str}\n\n"
            
            return response.strip()
            
        except Exception as e:
            return f"I couldn't list your reminders: {str(e)}"
    
    def complete_reminder(self, reminder_id):
        """Mark a reminder as completed"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('UPDATE reminders SET completed = 1 WHERE id = ?', (reminder_id,))
            self.connection.commit()
            return "Reminder marked as complete."
        except Exception as e:
            return f"Couldn't complete reminder: {str(e)}"
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
            self.connection.commit()
            return "Reminder deleted."
        except Exception as e:
            return f"Couldn't delete reminder: {str(e)}"
    
    def clear_all(self):
        """Clear all reminders"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM reminders')
            self.connection.commit()
            return "All reminders cleared."
        except Exception as e:
            return f"Couldn't clear reminders: {str(e)}"
    
    def close(self):
        """Close database connection"""
        self.running = False
        if self.connection:
            self.connection.close()
