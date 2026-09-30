"""
Garun AI Assistant - Computer Vision Module
============================================
The "Eyes" of JARVIS - Face detection, recognition, and screen awareness
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
import base64
import json

# Try to import OpenCV
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[Vision] OpenCV not installed. Run: pip install opencv-python")

# Try to import face_recognition
try:
    import face_recognition
    import numpy as np
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("[Vision] face_recognition not installed. Run: pip install face_recognition")


class Vision:
    """
    Computer Vision capabilities for Garun.
    - Face detection and recognition
    - Screen capture
    - Send screenshots to AI for analysis
    """
    
    def __init__(self):
        self.known_faces = {}  # name -> encoding
        self.camera = None
        self.data_path = Path(__file__).parent.parent / "data" / "faces"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Load known faces
        if FACE_RECOGNITION_AVAILABLE:
            self._load_known_faces()
    
    def _load_known_faces(self):
        """Load known face encodings from disk"""
        encodings_file = self.data_path / "encodings.json"
        if encodings_file.exists():
            try:
                with open(encodings_file, "r") as f:
                    data = json.load(f)
                    for name, encoding in data.items():
                        self.known_faces[name] = np.array(encoding)
                print(f"[Vision] Loaded {len(self.known_faces)} known faces")
            except Exception as e:
                print(f"[Vision] Error loading faces: {e}")
    
    def _save_known_faces(self):
        """Save known face encodings to disk"""
        encodings_file = self.data_path / "encodings.json"
        data = {name: encoding.tolist() for name, encoding in self.known_faces.items()}
        with open(encodings_file, "w") as f:
            json.dump(data, f)
    
    # ==========================================
    # CAMERA CONTROL
    # ==========================================
    
    def open_camera(self, camera_id=0):
        """Open webcam"""
        if not CV2_AVAILABLE:
            return False, "OpenCV not installed"
        
        self.camera = cv2.VideoCapture(camera_id)
        if self.camera.isOpened():
            return True, "Camera opened"
        return False, "Failed to open camera"
    
    def close_camera(self):
        """Close webcam"""
        if self.camera:
            self.camera.release()
            self.camera = None
        return "Camera closed"
    
    def capture_frame(self):
        """Capture a single frame from webcam"""
        if not CV2_AVAILABLE:
            return None, "OpenCV not installed"
        
        if not self.camera or not self.camera.isOpened():
            success, msg = self.open_camera()
            if not success:
                return None, msg
        
        ret, frame = self.camera.read()
        if ret:
            return frame, "Frame captured"
        return None, "Failed to capture frame"
    
    # ==========================================
    # FACE DETECTION & RECOGNITION
    # ==========================================
    
    def detect_faces(self, frame=None):
        """
        Detect faces in frame or capture new frame.
        Returns list of face locations.
        """
        if not CV2_AVAILABLE:
            return [], "OpenCV not installed"
        
        if frame is None:
            frame, msg = self.capture_frame()
            if frame is None:
                return [], msg
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Use Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        
        return list(faces), f"Detected {len(faces)} face(s)"
    
    def recognize_faces(self, frame=None):
        """
        Recognize faces in frame.
        Returns list of recognized names.
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return [], "face_recognition not installed. Run: pip install face_recognition"
        
        if frame is None:
            frame, msg = self.capture_frame()
            if frame is None:
                return [], msg
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all face locations and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        recognized = []
        for face_encoding in face_encodings:
            # Compare with known faces
            name = "Unknown"
            
            if self.known_faces:
                known_encodings = list(self.known_faces.values())
                known_names = list(self.known_faces.keys())
                
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                
                if True in matches:
                    match_index = matches.index(True)
                    name = known_names[match_index]
            
            recognized.append(name)
        
        return recognized, f"Recognized {len(recognized)} face(s)"
    
    def who_is_there(self):
        """
        Check who's in front of the camera.
        Returns greeting based on recognized faces.
        """
        frame, msg = self.capture_frame()
        if frame is None:
            return msg
        
        faces, detect_msg = self.recognize_faces(frame)
        
        self.close_camera()
        
        if not faces:
            return "I don't see anyone in front of the camera."
        
        known = [f for f in faces if f != "Unknown"]
        unknown = [f for f in faces if f == "Unknown"]
        
        response = ""
        if known:
            names = ", ".join(known)
            hour = datetime.now().hour
            if hour < 12:
                greeting = "Good morning"
            elif hour < 17:
                greeting = "Good afternoon"
            else:
                greeting = "Good evening"
            response = f"{greeting}, {names}! Welcome back. The system is secure."
        
        if unknown:
            if len(unknown) == 1:
                response += "\n⚠️ I also see an unrecognized person."
            else:
                response += f"\n⚠️ I see {len(unknown)} unrecognized people."
        
        return response if response else "I see people but couldn't identify them."
    
    def register_face(self, name):
        """
        Register a new face.
        Takes a photo and saves the face encoding.
        """
        if not FACE_RECOGNITION_AVAILABLE:
            return "face_recognition not installed"
        
        frame, msg = self.capture_frame()
        if frame is None:
            return msg
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get face encoding
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if not face_locations:
            self.close_camera()
            return "No face detected. Please position yourself in front of the camera."
        
        if len(face_locations) > 1:
            self.close_camera()
            return "Multiple faces detected. Please ensure only one person is visible."
        
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        
        # Save face image
        face_img_path = self.data_path / f"{name}.jpg"
        cv2.imwrite(str(face_img_path), frame)
        
        # Save encoding
        self.known_faces[name] = face_encoding
        self._save_known_faces()
        
        self.close_camera()
        return f"Face registered successfully! I'll remember you as {name}."
    
    # ==========================================
    # SCREEN CAPTURE
    # ==========================================
    
    def capture_screen(self, save_path=None):
        """
        Capture current screen.
        Returns path to saved screenshot.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if save_path is None:
            save_path = self.data_path.parent / "screenshots"
            save_path.mkdir(parents=True, exist_ok=True)
            save_path = save_path / f"screen_{timestamp}.png"
        
        try:
            # Use PowerShell to capture screen on Windows
            ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save("{save_path}")
'''
            subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True, timeout=10
            )
            
            if Path(save_path).exists():
                return str(save_path), "Screenshot captured"
            return None, "Failed to capture screenshot"
        except Exception as e:
            return None, f"Error: {e}"
    
    def screenshot_to_base64(self, image_path=None):
        """
        Convert screenshot to base64 for sending to AI.
        Captures new screenshot if path not provided.
        """
        if image_path is None:
            image_path, msg = self.capture_screen()
            if image_path is None:
                return None, msg
        
        try:
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
            return img_data, "Image encoded"
        except Exception as e:
            return None, f"Error encoding image: {e}"
    
    def analyze_screen(self, ai_engine=None, question="What do you see on my screen?"):
        """
        Capture screen and send to AI for analysis.
        Requires Gemini or GPT-4o for vision capability.
        """
        if ai_engine is None:
            return "No AI engine provided. Cannot analyze screen."
        
        # Check if AI supports vision
        provider = ai_engine.provider
        if provider not in ["gemini", "openai"]:
            return "Screen analysis requires Gemini or GPT-4 Vision. Current provider doesn't support vision."
        
        # Capture screen
        screenshot_path, msg = self.capture_screen()
        if screenshot_path is None:
            return msg
        
        # For now, return a message about the feature
        return (f"📸 Screenshot saved to: {screenshot_path}\n\n"
                f"To analyze this with AI, you'll need to:\n"
                f"1. Use Gemini 1.5 Pro or GPT-4o\n"
                f"2. The AI will 'see' your screen and help debug code!\n\n"
                f"This feature is ready for when you configure a vision-capable AI.")
    
    # ==========================================
    # UTILITIES
    # ==========================================
    
    def get_status(self):
        """Get vision module status"""
        return {
            "opencv_available": CV2_AVAILABLE,
            "face_recognition_available": FACE_RECOGNITION_AVAILABLE,
            "known_faces": list(self.known_faces.keys()),
            "camera_active": self.camera is not None and self.camera.isOpened()
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.close_camera()
        cv2.destroyAllWindows() if CV2_AVAILABLE else None
