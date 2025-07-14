import os
import requests
import base64
from typing import Dict, Any, Optional
from datetime import datetime
import json

class VoiceSynthesis:
    """
    Fixed voice synthesis service using direct API calls to ElevenLabs
    More reliable than the SDK for production use
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel - clear female voice
        
        print(f"🎤 Fixed Voice Synthesis initialized")
        print(f"API Key present: {'Yes' if self.api_key else 'No'}")
        if self.api_key:
            print(f"API Key (first 10 chars): {self.api_key[:10]}...")
    
    def synthesize_speech(self, text: str, voice_tone: str = 'professional', language: str = 'en') -> Dict[str, Any]:
        """
        Convert text to speech using direct ElevenLabs API calls
        """
        if not self.api_key:
            return self._mock_response(text)
        
        try:
            # Select voice based on tone and language
            voice_id = self._get_voice_id(voice_tone, language)
            
            # Prepare request
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            headers = {
                'Content-Type': 'application/json',
                'xi-api-key': self.api_key
            }
            
            # Optimize text for speech
            optimized_text = self._optimize_text(text, language)
            
            # Use multilingual model for better language support
            model_id = "eleven_multilingual_v2" if language != 'en' else "eleven_monolingual_v1"
            
            data = {
                "text": optimized_text,
                "model_id": model_id,
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.85,
                    "style": 0.20,
                    "use_speaker_boost": True
                }
            }
            
            print(f"🗣️ Synthesizing speech: '{text[:50]}...' with voice {voice_id}")
            
            # Make request with timeout
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                audio_data = response.content
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                print(f"✅ Speech synthesis successful! Audio size: {len(audio_data)} bytes")
                
                return {
                    'success': True,
                    'text': text,
                    'optimized_text': optimized_text,
                    'voice_id': voice_id,
                    'voice_tone': voice_tone,
                    'language': language,
                    'audio_format': 'mp3',
                    'audio_size': len(audio_data),
                    'audio_base64': audio_base64,
                    'duration_estimate': self._estimate_duration(text),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                error_msg = f"ElevenLabs API error: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return self._error_response(error_msg)
                
        except Exception as e:
            error_msg = f"Voice synthesis exception: {str(e)}"
            print(f"❌ {error_msg}")
            return self._error_response(error_msg)
    
    def test_connection(self) -> Dict[str, Any]:
        """Test ElevenLabs API connection"""
        if not self.api_key:
            return {
                'success': False,
                'message': 'No API key configured',
                'mock_mode': True,
                'test_audio_size': 0
            }
        
        try:
            print("🔍 Testing ElevenLabs connection...")
            
            # Test with simple phrase
            result = self.synthesize_speech("Hello! I'm Mia, your tech support assistant. My voice is working perfectly!")
            
            return {
                'success': result['success'],
                'message': 'Connection successful' if result['success'] else 'Connection failed',
                'mock_mode': False,
                'test_audio_size': result.get('audio_size', 0)
            }
            
        except Exception as e:
            error_msg = f"Connection test failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'message': error_msg,
                'mock_mode': False,
                'test_audio_size': 0
            }
    
    def _get_voice_id(self, voice_tone: str, language: str = 'en') -> str:
        """Get voice ID based on tone and language"""
        
        # English voices
        if language == 'en':
            voice_map = {
                'professional': "21m00Tcm4TlvDq8ikWAM",  # Rachel - professional female
                'warm': "EXAVITQu4vr4xnSDxMaL",         # Bella - warm female
                'confident': "pNInz6obpgDQGcFmaJgB",     # Adam - confident male
                'supportive': "XrExE9yKIg1WjnnlVkGX"     # Matilda - supportive female
            }
        # Spanish voices
        elif language == 'es':
            voice_map = {
                'professional': "MF3mGyEYCl7XYWbV9V6O",  # Elli - professional Spanish
                'warm': "XB0fDUnXU5powFXDhCwa",         # Charlotte - warm Spanish
                'confident': "VR6AewLTigWG4xSOukaG",     # Arnold - confident Spanish
                'supportive': "ErXwobaYiN019PkySvjV"     # Antoni - supportive Spanish
            }
        else:
            # Default to English
            voice_map = {
                'professional': "21m00Tcm4TlvDq8ikWAM",
                'warm': "EXAVITQu4vr4xnSDxMaL",
                'confident': "pNInz6obpgDQGcFmaJgB",
                'supportive': "XrExE9yKIg1WjnnlVkGX"
            }
        
        return voice_map.get(voice_tone, self.default_voice_id)
    
    def _optimize_text(self, text: str, language: str = 'en') -> str:
        """Optimize text for better speech synthesis"""
        # Remove excessive punctuation
        optimized = text.replace('...', '.')
        optimized = optimized.replace('!!', '!')
        optimized = optimized.replace('??', '?')
        
        # Handle technical terms based on language
        if language == 'en':
            tech_replacements = {
                'WiFi': 'Wi-Fi',
                'API': 'A-P-I',
                'URL': 'U-R-L',
                'XETA': 'ZETA',
                'HTML': 'H-T-M-L',
                'CSS': 'C-S-S',
                'USB': 'U-S-B'
            }
        elif language == 'es':
            tech_replacements = {
                'WiFi': 'Wi-Fi',
                'API': 'A-P-I',
                'URL': 'U-R-L',
                'XETA': 'ZETA',
                'email': 'correo electrónico',
                'router': 'enrutador'
            }
        else:
            tech_replacements = {
                'XETA': 'ZETA'
            }
        
        for term, replacement in tech_replacements.items():
            optimized = optimized.replace(term, replacement)
        
        return optimized
    
    def _estimate_duration(self, text: str) -> float:
        """Estimate audio duration"""
        words = len(text.split())
        return round((words / 150) * 60, 2)  # ~150 words per minute
    
    def _mock_response(self, text: str) -> Dict[str, Any]:
        """Mock response when API key not available"""
        return {
            'success': True,
            'text': text,
            'voice_tone': 'mock',
            'audio_size': 1024,
            'audio_base64': 'mock_audio_data',
            'mock': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def _error_response(self, error: str) -> Dict[str, Any]:
        """Error response format"""
        return {
            'success': False,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }

    # Legacy compatibility methods
    def get_available_voices(self) -> Dict[str, Any]:
        """Get available voices for compatibility"""
        return {
            'success': True,
            'voices': [
                {'id': 'professional', 'name': 'Professional Mia', 'language': 'en'},
                {'id': 'warm', 'name': 'Warm Mia', 'language': 'en'},
                {'id': 'confident', 'name': 'Confident Mia', 'language': 'en'},
                {'id': 'supportive', 'name': 'Supportive Mia', 'language': 'en'}
            ]
        }
    
    def set_voice_profile(self, voice_tone: str) -> bool:
        """Set voice profile for compatibility"""
        return True

