import os
import io
import base64
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import tempfile

try:
    from elevenlabs import ElevenLabs, Voice, VoiceSettings
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("Warning: ElevenLabs SDK not available. Voice synthesis will be disabled.")

from src.models.multilingual_support import MultilingualSupport

@dataclass
class VoiceProfile:
    """Represents a voice profile for Mia with language support"""
    voice_id: str
    name: str
    description: str
    language: str
    language_name: str
    stability: float
    similarity_boost: float
    style: float
    use_speaker_boost: bool

class VoiceSynthesis:
    """
    Voice synthesis service for Mia Avatar using ElevenLabs
    Converts text responses to natural speech with personality
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.client = None
        self.multilingual = MultilingualSupport()
        self.voice_profiles = self._load_multilingual_voice_profiles()
        self.current_voice = 'professional_female_en'
        
        if ELEVENLABS_AVAILABLE and self.api_key:
            try:
                self.client = ElevenLabs(api_key=self.api_key)
                print("✅ ElevenLabs client initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize ElevenLabs client: {e}")
                self.client = None
        else:
            print("⚠️ ElevenLabs not available - using mock voice synthesis")
    
    def _load_multilingual_voice_profiles(self) -> Dict[str, VoiceProfile]:
        """Load predefined voice profiles for different scenarios and languages"""
        return {
            # English Voices
            'professional_female_en': VoiceProfile(
                voice_id='EXAVITQu4vr4xnSDxMaL',  # Bella - Professional female voice
                name='Professional Mia (English)',
                description='Professional, clear, and friendly voice for general tech support in English',
                language='en',
                language_name='English',
                stability=0.75,
                similarity_boost=0.85,
                style=0.20,
                use_speaker_boost=True
            ),
            'warm_friendly_en': VoiceProfile(
                voice_id='ThT5KcBeYPX3keUQqHPh',  # Dorothy - Warm and friendly
                name='Warm Mia (English)',
                description='Warm, empathetic voice for understanding and support in English',
                language='en',
                language_name='English',
                stability=0.70,
                similarity_boost=0.80,
                style=0.35,
                use_speaker_boost=True
            ),
            'confident_expert_en': VoiceProfile(
                voice_id='pNInz6obpgDQGcFmaJgB',  # Adam - Confident and clear
                name='Expert Mia (English)',
                description='Confident, knowledgeable voice for complex explanations in English',
                language='en',
                language_name='English',
                stability=0.80,
                similarity_boost=0.90,
                style=0.15,
                use_speaker_boost=True
            ),
            'encouraging_supportive_en': VoiceProfile(
                voice_id='XrExE9yKIg1WjnnlVkGX',  # Matilda - Encouraging
                name='Supportive Mia (English)',
                description='Encouraging, patient voice for difficult problems in English',
                language='en',
                language_name='English',
                stability=0.65,
                similarity_boost=0.75,
                style=0.40,
                use_speaker_boost=True
            ),
            
            # Spanish Voices
            'professional_female_es': VoiceProfile(
                voice_id='MF3mGyEYCl7XYWbV9V6O',  # Elli - Professional Spanish
                name='Mía Profesional (Español)',
                description='Voz profesional, clara y amigable para soporte técnico en español',
                language='es',
                language_name='Español',
                stability=0.75,
                similarity_boost=0.85,
                style=0.20,
                use_speaker_boost=True
            ),
            'warm_friendly_es': VoiceProfile(
                voice_id='XB0fDUnXU5powFXDhCwa',  # Charlotte - Warm Spanish
                name='Mía Cálida (Español)',
                description='Voz cálida y empática para comprensión y apoyo en español',
                language='es',
                language_name='Español',
                stability=0.70,
                similarity_boost=0.80,
                style=0.35,
                use_speaker_boost=True
            ),
            'confident_expert_es': VoiceProfile(
                voice_id='VR6AewLTigWG4xSOukaG',  # Arnold - Confident Spanish
                name='Mía Experta (Español)',
                description='Voz confiada y conocedora para explicaciones complejas en español',
                language='es',
                language_name='Español',
                stability=0.80,
                similarity_boost=0.90,
                style=0.15,
                use_speaker_boost=True
            ),
            'encouraging_supportive_es': VoiceProfile(
                voice_id='ErXwobaYiN019PkySvjV',  # Antoni - Encouraging Spanish
                name='Mía Alentadora (Español)',
                description='Voz alentadora y paciente para problemas difíciles en español',
                language='es',
                language_name='Español',
                stability=0.65,
                similarity_boost=0.75,
                style=0.40,
                use_speaker_boost=True
            )
        }
    
    def synthesize_speech(
        self, 
        text: str, 
        voice_tone: str = 'professional',
        language: str = 'en',
        output_format: str = 'mp3_44100_128',
        optimize_latency: int = 2,
        return_base64: bool = True
    ) -> Dict[str, Any]:
        """
        Convert text to speech using ElevenLabs API
        
        Args:
            text: Text to convert to speech
            voice_tone: Voice tone/profile to use
            output_format: Audio format (mp3_44100_128, wav, etc.)
            optimize_latency: Latency optimization level (0-4)
            return_base64: Whether to return audio as base64 string
            
        Returns:
            Dictionary with audio data and metadata
        """
        if not self.client:
            return self._mock_synthesis(text, voice_tone)
        
        try:
            # Map voice tone to voice profile with language
            voice_profile = self._get_voice_profile(voice_tone, language)
            
            # Prepare voice settings
            voice_settings = VoiceSettings(
                stability=voice_profile.stability,
                similarity_boost=voice_profile.similarity_boost,
                style=voice_profile.style,
                use_speaker_boost=voice_profile.use_speaker_boost
            )
            
            # Optimize text for speech synthesis
            optimized_text = self._optimize_text_for_speech(text)
            
            # Generate speech
            audio_generator = self.client.generate(
                text=optimized_text,
                voice=Voice(
                    voice_id=voice_profile.voice_id,
                    settings=voice_settings
                ),
                model="eleven_multilingual_v2",
                output_format=output_format,
                optimize_streaming_latency=optimize_latency
            )
            
            # Collect audio data
            audio_data = b''.join(audio_generator)
            
            # Prepare response
            response = {
                'success': True,
                'text': text,
                'optimized_text': optimized_text,
                'voice_profile': voice_profile.name,
                'voice_tone': voice_tone,
                'audio_format': output_format,
                'audio_size': len(audio_data),
                'duration_estimate': self._estimate_duration(optimized_text),
                'timestamp': datetime.now().isoformat()
            }
            
            if return_base64:
                response['audio_base64'] = base64.b64encode(audio_data).decode('utf-8')
            else:
                # Save to temporary file
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix=f'.{output_format.split("_")[0]}'
                )
                temp_file.write(audio_data)
                temp_file.close()
                response['audio_file_path'] = temp_file.name
            
            return response
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': text,
                'voice_tone': voice_tone,
                'timestamp': datetime.now().isoformat()
            }
    
    def synthesize_with_timing(
        self, 
        text: str, 
        voice_tone: str = 'professional'
    ) -> Dict[str, Any]:
        """
        Synthesize speech with timing information for lip-sync
        """
        result = self.synthesize_speech(text, voice_tone)
        
        if result['success']:
            # Calculate timing for lip-sync
            timing_data = self._calculate_lip_sync_timing(
                result['optimized_text'], 
                result['duration_estimate']
            )
            result['lip_sync_timing'] = timing_data
        
        return result
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voice profiles"""
        voices = []
        for key, profile in self.voice_profiles.items():
            voices.append({
                'key': key,
                'name': profile.name,
                'description': profile.description,
                'voice_id': profile.voice_id
            })
        return voices
    
    def set_voice_profile(self, voice_key: str) -> bool:
        """Set the current voice profile"""
        if voice_key in self.voice_profiles:
            self.current_voice = voice_key
            return True
        return False
    
    def _get_voice_profile(self, voice_tone: str, language: str = 'en') -> VoiceProfile:
        """Map voice tone to appropriate voice profile for the specified language"""
        tone_mapping = {
            'professional': f'professional_female_{language}',
            'warm': f'warm_friendly_{language}',
            'focused': f'confident_expert_{language}',
            'clear': f'professional_female_{language}',
            'confirming': f'professional_female_{language}',
            'excited': f'encouraging_supportive_{language}',
            'empathetic': f'warm_friendly_{language}',
            'uncertain': f'warm_friendly_{language}',
            'confident': f'confident_expert_{language}'
        }
        
        profile_key = tone_mapping.get(voice_tone, f'professional_female_{language}')
        
        # Fallback to English if language-specific profile doesn't exist
        if profile_key not in self.voice_profiles:
            fallback_key = tone_mapping.get(voice_tone, 'professional_female_en')
            if fallback_key in self.voice_profiles:
                profile_key = fallback_key
            else:
                profile_key = 'professional_female_en'
        
        return self.voice_profiles[profile_key]
    
    def _optimize_text_for_speech(self, text: str, language: str = 'en') -> str:
        """Optimize text for better speech synthesis in multiple languages"""
        # Remove excessive punctuation
        optimized = text.replace('...', '.')
        optimized = optimized.replace('!!', '!')
        optimized = optimized.replace('??', '?')
        
        # Add pauses for better pacing
        optimized = optimized.replace('. ', '. <break time="0.3s"/> ')
        optimized = optimized.replace('! ', '! <break time="0.3s"/> ')
        optimized = optimized.replace('? ', '? <break time="0.3s"/> ')
        
        # Handle technical terms based on language
        if language == 'en':
            tech_replacements = {
                'WiFi': 'Wi-Fi',
                'API': 'A-P-I',
                'URL': 'U-R-L',
                'HTML': 'H-T-M-L',
                'CSS': 'C-S-S',
                'JavaScript': 'Java Script',
                'USB': 'U-S-B'
            }
        elif language == 'es':
            tech_replacements = {
                'WiFi': 'Wi-Fi',
                'API': 'A-P-I',
                'URL': 'U-R-L',
                'HTML': 'H-T-M-L',
                'CSS': 'C-S-S',
                'JavaScript': 'Java Script',
                'USB': 'U-S-B',
                'email': 'correo electrónico',
                'router': 'enrutador'
            }
        else:
            tech_replacements = {}
        
        for term, replacement in tech_replacements.items():
            optimized = optimized.replace(term, replacement)
        
        return optimized
    
    def _estimate_duration(self, text: str) -> float:
        """Estimate audio duration based on text length"""
        # Average speaking rate: ~150 words per minute
        words = len(text.split())
        duration = (words / 150) * 60  # Convert to seconds
        return round(duration, 2)
    
    def _calculate_lip_sync_timing(self, text: str, duration: float) -> Dict[str, Any]:
        """Calculate timing data for lip-sync animation"""
        words = text.split()
        word_count = len(words)
        
        if word_count == 0:
            return {'words': [], 'total_duration': 0}
        
        # Estimate timing for each word
        word_timings = []
        current_time = 0.0
        
        for i, word in enumerate(words):
            # Estimate word duration based on length and position
            base_duration = duration / word_count
            word_duration = base_duration * (0.8 + (len(word) / 10))
            
            word_timings.append({
                'word': word,
                'start_time': round(current_time, 2),
                'end_time': round(current_time + word_duration, 2),
                'duration': round(word_duration, 2)
            })
            
            current_time += word_duration
        
        return {
            'words': word_timings,
            'total_duration': duration,
            'word_count': word_count,
            'average_word_duration': round(duration / word_count, 2)
        }
    
    def _mock_synthesis(self, text: str, voice_tone: str) -> Dict[str, Any]:
        """Mock synthesis for testing when ElevenLabs is not available"""
        return {
            'success': True,
            'text': text,
            'optimized_text': text,
            'voice_profile': 'Mock Voice',
            'voice_tone': voice_tone,
            'audio_format': 'mp3_44100_128',
            'audio_size': 1024,
            'duration_estimate': self._estimate_duration(text),
            'audio_base64': 'mock_audio_data_base64',
            'mock': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test ElevenLabs API connection"""
        if not self.client:
            return {
                'success': False,
                'message': 'ElevenLabs client not initialized',
                'mock_mode': True
            }
        
        try:
            # Test with a simple phrase
            test_result = self.synthesize_speech(
                "Hello! I'm Mia, your tech support assistant.",
                voice_tone='professional'
            )
            
            return {
                'success': test_result['success'],
                'message': 'ElevenLabs connection successful' if test_result['success'] else 'Connection failed',
                'mock_mode': False,
                'test_audio_size': test_result.get('audio_size', 0)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection test failed: {str(e)}',
                'mock_mode': False
            }

