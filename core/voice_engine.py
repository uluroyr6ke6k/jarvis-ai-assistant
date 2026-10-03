"""
J.A.R.V.I.S. Voice Engine
Handles Speech-to-Text and Text-to-Speech
"""

import threading
import pyttsx3
import speech_recognition as sr
from config import (
    VOICE_ENGINE, STT_ENGINE, VOICE_RATE, VOICE_VOLUME,
    LISTEN_TIMEOUT, PHRASE_TIME_LIMIT, MICROPHONE_INDEX,
    MICROPHONE_ENERGY_THRESHOLD
)
from core.logger import log_info, log_error, log_debug

class VoiceEngine:
    """Handles voice input/output"""
    
    def __init__(self):
        """Initialize voice engine"""
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=MICROPHONE_INDEX)
        
        # Configure TTS
        self._configure_tts()
        
        # Configure STT
        self._configure_stt()
        
        self.is_listening = False
        self.callback = None
        
        log_info("Voice Engine initialized")
    
    def _configure_tts(self):
        """Configure Text-to-Speech settings"""
        try:
            self.tts_engine.setProperty('rate', VOICE_RATE)
            self.tts_engine.setProperty('volume', VOICE_VOLUME)
            log_debug("TTS configured")
        except Exception as e:
            log_error(f"Error configuring TTS: {e}", e)
    
    def _configure_stt(self):
        """Configure Speech-to-Text settings"""
        try:
            self.recognizer.energy_threshold = MICROPHONE_ENERGY_THRESHOLD
            self.recognizer.dynamic_energy_threshold = True
            log_debug("STT configured")
        except Exception as e:
            log_error(f"Error configuring STT: {e}", e)
    
    def speak(self, text, blocking=True):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            blocking: Wait for speech to complete
        """
        try:
            log_debug(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait() if blocking else None
        except Exception as e:
            log_error(f"Error speaking: {e}", e)
    
    def listen(self, timeout=LISTEN_TIMEOUT):
        """
        Listen for voice input
        
        Args:
            timeout: Maximum listening duration in seconds
        
        Returns:
            str: Recognized text or None if failed
        """
        try:
            log_info("Listening...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=PHRASE_TIME_LIMIT
                )
            
            # Use Google Speech Recognition (free, no API key)
            text = self.recognizer.recognize_google(audio)
            log_info(f"Recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            log_debug("Could not understand audio")
            self.speak("Sorry, I didn't understand that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            log_error(f"Speech recognition error: {e}", e)
            self.speak("I'm having trouble with speech recognition right now.")
            return None
        except Exception as e:
            log_error(f"Unexpected error in listen: {e}", e)
            return None
    
    def start_listening_thread(self, callback):
        """
        Start listening in background thread
        
        Args:
            callback: Function to call with recognized text
        """
        self.callback = callback
        self.is_listening = True
        thread = threading.Thread(target=self._listening_loop, daemon=True)
        thread.start()
        log_info("Listening thread started")
    
    def stop_listening(self):
        """Stop background listening"""
        self.is_listening = False
        log_info("Listening thread stopped")
    
    def _listening_loop(self):
        """Background listening loop"""
        while self.is_listening:
            text = self.listen()
            if text and self.callback:
                self.callback(text)
    
    def set_voice_rate(self, rate):
        """Set speech rate (50-300)"""
        try:
            self.tts_engine.setProperty('rate', rate)
            log_debug(f"Voice rate set to {rate}")
        except Exception as e:
            log_error(f"Error setting voice rate: {e}", e)
    
    def set_voice_volume(self, volume):
        """Set voice volume (0.0-1.0)"""
        try:
            self.tts_engine.setProperty('volume', volume)
            log_debug(f"Voice volume set to {volume}")
        except Exception as e:
            log_error(f"Error setting voice volume: {e}", e)

# Global voice engine instance
voice_engine = None

def get_voice_engine():
    """Get or create voice engine instance"""
    global voice_engine
    if voice_engine is None:
        voice_engine = VoiceEngine()
    return voice_engine
