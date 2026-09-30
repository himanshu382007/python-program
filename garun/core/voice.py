"""
Garun AI Assistant - Voice Engine
==================================
Speech recognition and text-to-speech functionality
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
from config import WAKE_WORDS, VOICE_RATE, VOICE_VOLUME, ASSISTANT_NAME


class VoiceEngine:
    """Handles speech recognition and text-to-speech"""
    
    def __init__(self):
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text-to-speech
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        
        # State
        self.is_listening = False
        self.speak_queue = queue.Queue()
        
        # Start speech thread
        self._start_speech_thread()
        
        # Calibrate microphone
        self._calibrate_microphone()
    
    def _configure_tts(self):
        """Configure text-to-speech settings"""
        self.tts_engine.setProperty('rate', VOICE_RATE)
        self.tts_engine.setProperty('volume', VOICE_VOLUME)
        
        # Try to set a good voice
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            # Prefer Microsoft voices for better quality
            if 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
            elif 'zira' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                print("[Garun] Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("[Garun] Microphone calibrated!")
        except Exception as e:
            print(f"[Garun] Microphone calibration failed: {e}")
    
    def _start_speech_thread(self):
        """Start background thread for TTS"""
        def speech_worker():
            # Create a fresh engine in the worker thread for thread safety
            import pyttsx3
            local_engine = pyttsx3.init()
            local_engine.setProperty('rate', VOICE_RATE)
            local_engine.setProperty('volume', VOICE_VOLUME)
            
            while True:
                text = self.speak_queue.get()
                if text is None:
                    break
                try:
                    print(f"[Garun TTS] Speaking: {text[:50]}...")
                    local_engine.say(text)
                    local_engine.runAndWait()
                    print(f"[Garun TTS] Done speaking")
                except Exception as e:
                    print(f"[Garun TTS] Error: {e}")
        
        self.speech_thread = threading.Thread(target=speech_worker, daemon=True)
        self.speech_thread.start()
    
    def listen(self, timeout=5, phrase_limit=10):
        """
        Listen for voice input and return recognized text.
        Supports English, Hindi, and Hinglish.
        
        Args:
            timeout: Max seconds to wait for speech to start
            phrase_limit: Max seconds of speech to capture
            
        Returns:
            Recognized text or None if failed
        """
        self.is_listening = True
        
        try:
            with self.microphone as source:
                print("[Garun] Listening... (English/Hindi/Hinglish)")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
            
            # Try recognizing with English first (also catches Hinglish)
            text = None
            try:
                text = self.recognizer.recognize_google(audio, language="en-IN")
                print(f"[Garun] Heard (EN-IN): {text}")
            except sr.UnknownValueError:
                # Try Hindi if English fails
                try:
                    text = self.recognizer.recognize_google(audio, language="hi-IN")
                    print(f"[Garun] Heard (HI-IN): {text}")
                except sr.UnknownValueError:
                    # Final fallback - default English
                    try:
                        text = self.recognizer.recognize_google(audio)
                        print(f"[Garun] Heard: {text}")
                    except:
                        pass
            
            if text:
                return text  # Keep original case for Hindi script
            return None
            
        except sr.WaitTimeoutError:
            print("[Garun] Listening timed out")
            return None
        except sr.UnknownValueError:
            print("[Garun] Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"[Garun] Recognition service error: {e}")
            return None
        except Exception as e:
            print(f"[Garun] Listening error: {e}")
            return None
        finally:
            self.is_listening = False
    
    def listen_for_wake_word(self, callback):
        """
        Continuously listen for wake word in background.
        Calls callback with remaining text when wake word detected.
        
        Args:
            callback: Function to call when wake word detected
        """
        def listener():
            while True:
                text = self.listen(timeout=None, phrase_limit=5)
                if text:
                    # Check for wake words
                    for wake_word in WAKE_WORDS:
                        if wake_word in text:
                            # Extract command after wake word
                            command = text.replace(wake_word, "").strip()
                            if command:
                                callback(command)
                            else:
                                # Just wake word, wait for command
                                callback(None)
                            break
        
        thread = threading.Thread(target=listener, daemon=True)
        thread.start()
        return thread
    
    def speak(self, text):
        """
        Speak text using text-to-speech.
        Non-blocking - adds to queue.
        
        Args:
            text: Text to speak
        """
        if text:
            print(f"[Garun] Adding to speech queue: {text[:30]}...")
            self.speak_queue.put(text)
    
    def speak_sync(self, text):
        """
        Speak text synchronously (blocking).
        
        Args:
            text: Text to speak
        """
        if text:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"[Garun] TTS sync error: {e}")
    
    def stop_speaking(self):
        """Stop current speech"""
        try:
            self.tts_engine.stop()
        except:
            pass
    
    def is_wake_word(self, text):
        """
        Check if text contains a wake word.
        
        Args:
            text: Text to check
            
        Returns:
            True if wake word found
        """
        if not text:
            return False
        text_lower = text.lower()
        return any(wake in text_lower for wake in WAKE_WORDS)
    
    def extract_command(self, text):
        """
        Extract command from text after removing wake word.
        
        Args:
            text: Full text potentially containing wake word
            
        Returns:
            Command text without wake word
        """
        if not text:
            return ""
        
        text_lower = text.lower()
        for wake in WAKE_WORDS:
            if wake in text_lower:
                # Find position and extract rest
                idx = text_lower.find(wake)
                return text[idx + len(wake):].strip()
        
        return text.strip()
    
    def cleanup(self):
        """Cleanup resources"""
        self.speak_queue.put(None)
        try:
            self.tts_engine.stop()
        except:
            pass
