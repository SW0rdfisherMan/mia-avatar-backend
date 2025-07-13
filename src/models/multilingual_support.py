import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LanguageProfile:
    """Language profile configuration"""
    code: str
    name: str
    native_name: str
    voice_id: str
    greeting: str
    fallback_message: str
    tech_terms: Dict[str, str]

class MultilingualSupport:
    """
    Multilingual support system for Mia Avatar
    Handles language detection, translation, and localized responses
    """
    
    def __init__(self):
        self.supported_languages = self._load_language_profiles()
        self.default_language = 'en'
        self.current_language = 'en'
        
        # Language detection patterns
        self.language_patterns = {
            'es': [
                r'\b(hola|buenos días|buenas tardes|buenas noches|ayuda|problema|necesito)\b',
                r'\b(gracias|por favor|disculpe|perdón|no funciona|error)\b',
                r'\b(computadora|ordenador|internet|wifi|contraseña|correo)\b'
            ],
            'en': [
                r'\b(hello|hi|good morning|good afternoon|help|problem|need)\b',
                r'\b(thanks|please|excuse me|sorry|not working|error)\b',
                r'\b(computer|internet|wifi|password|email|issue)\b'
            ]
        }
        
        # Load multilingual responses and knowledge
        self.responses = self._load_multilingual_responses()
        self.knowledge_base = self._load_multilingual_knowledge()
    
    def _load_language_profiles(self) -> Dict[str, LanguageProfile]:
        """Load supported language profiles"""
        return {
            'en': LanguageProfile(
                code='en',
                name='English',
                native_name='English',
                voice_id='EXAVITQu4vr4xnSDxMaL',  # Bella - Professional English
                greeting='Hello! I\'m Mia, your tech support assistant. How can I help you today?',
                fallback_message='I\'m sorry, I didn\'t understand that. Could you please rephrase your question?',
                tech_terms={
                    'wifi': 'Wi-Fi',
                    'internet': 'internet',
                    'computer': 'computer',
                    'password': 'password',
                    'email': 'email',
                    'browser': 'browser',
                    'software': 'software',
                    'hardware': 'hardware'
                }
            ),
            'es': LanguageProfile(
                code='es',
                name='Spanish',
                native_name='Español',
                voice_id='MF3mGyEYCl7XYWbV9V6O',  # Elli - Professional Spanish
                greeting='¡Hola! Soy Mía, tu asistente de soporte técnico. ¿Cómo puedo ayudarte hoy?',
                fallback_message='Lo siento, no entendí eso. ¿Podrías reformular tu pregunta por favor?',
                tech_terms={
                    'wifi': 'Wi-Fi',
                    'internet': 'internet',
                    'computadora': 'computadora',
                    'ordenador': 'ordenador',
                    'contraseña': 'contraseña',
                    'correo': 'correo electrónico',
                    'navegador': 'navegador',
                    'software': 'software',
                    'hardware': 'hardware'
                }
            )
        }
    
    def _load_multilingual_responses(self) -> Dict[str, Dict[str, str]]:
        """Load multilingual response templates"""
        return {
            'greeting': {
                'en': 'Hello! I\'m Mia, your beautiful tech support assistant. How can I help you today?',
                'es': '¡Hola! Soy Mía, tu hermosa asistente de soporte técnico. ¿Cómo puedo ayudarte hoy?'
            },
            'understanding': {
                'en': 'I understand your concern. Let me help you with that.',
                'es': 'Entiendo tu preocupación. Déjame ayudarte con eso.'
            },
            'problem_solving': {
                'en': 'Let me analyze this problem and find the best solution for you.',
                'es': 'Déjame analizar este problema y encontrar la mejor solución para ti.'
            },
            'explanation': {
                'en': 'Here\'s how to solve this step by step:',
                'es': 'Aquí te explico cómo resolver esto paso a paso:'
            },
            'confirmation': {
                'en': 'Perfect! Is there anything else I can help you with?',
                'es': '¡Perfecto! ¿Hay algo más en lo que pueda ayudarte?'
            },
            'gratitude': {
                'en': 'You\'re very welcome! I\'m always here to help.',
                'es': '¡De nada! Siempre estoy aquí para ayudar.'
            },
            'thinking': {
                'en': 'Let me think about this for a moment...',
                'es': 'Déjame pensar en esto por un momento...'
            },
            'celebration': {
                'en': 'Excellent! We\'ve solved the problem successfully!',
                'es': '¡Excelente! ¡Hemos resuelto el problema exitosamente!'
            },
            'language_switch': {
                'en': 'I\'ve switched to English. How can I assist you?',
                'es': 'He cambiado al español. ¿Cómo puedo asistirte?'
            },
            'language_detection': {
                'en': 'I detected you might prefer English. Would you like to continue in English?',
                'es': 'Detecté que podrías preferir español. ¿Te gustaría continuar en español?'
            }
        }
    
    def _load_multilingual_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Load multilingual technical knowledge base"""
        return {
            'wifi_connection': {
                'en': {
                    'title': 'WiFi Connection Issues',
                    'description': 'Steps to troubleshoot WiFi connectivity problems',
                    'steps': [
                        'Check if WiFi is enabled on your device',
                        'Restart your router by unplugging it for 30 seconds',
                        'Forget and reconnect to your WiFi network',
                        'Update your network drivers',
                        'Contact your internet service provider if issues persist'
                    ],
                    'keywords': ['wifi', 'internet', 'connection', 'network', 'router']
                },
                'es': {
                    'title': 'Problemas de Conexión WiFi',
                    'description': 'Pasos para solucionar problemas de conectividad WiFi',
                    'steps': [
                        'Verifica que el WiFi esté habilitado en tu dispositivo',
                        'Reinicia tu router desconectándolo por 30 segundos',
                        'Olvida y reconecta a tu red WiFi',
                        'Actualiza los controladores de red',
                        'Contacta a tu proveedor de internet si los problemas persisten'
                    ],
                    'keywords': ['wifi', 'internet', 'conexión', 'red', 'router', 'enrutador']
                }
            },
            'password_reset': {
                'en': {
                    'title': 'Password Reset Guide',
                    'description': 'How to safely reset your passwords',
                    'steps': [
                        'Go to the login page and click "Forgot Password"',
                        'Enter your email address',
                        'Check your email for reset instructions',
                        'Create a strong new password',
                        'Update your password manager'
                    ],
                    'keywords': ['password', 'reset', 'forgot', 'login', 'account']
                },
                'es': {
                    'title': 'Guía para Restablecer Contraseña',
                    'description': 'Cómo restablecer tus contraseñas de forma segura',
                    'steps': [
                        'Ve a la página de inicio de sesión y haz clic en "Olvidé mi contraseña"',
                        'Ingresa tu dirección de correo electrónico',
                        'Revisa tu correo para las instrucciones de restablecimiento',
                        'Crea una nueva contraseña segura',
                        'Actualiza tu administrador de contraseñas'
                    ],
                    'keywords': ['contraseña', 'restablecer', 'olvidé', 'login', 'cuenta', 'acceso']
                }
            },
            'email_setup': {
                'en': {
                    'title': 'Email Setup Instructions',
                    'description': 'Configure your email client properly',
                    'steps': [
                        'Open your email application',
                        'Select "Add Account" or "New Account"',
                        'Enter your email address and password',
                        'Configure server settings if needed',
                        'Test sending and receiving emails'
                    ],
                    'keywords': ['email', 'setup', 'configure', 'account', 'mail']
                },
                'es': {
                    'title': 'Instrucciones de Configuración de Correo',
                    'description': 'Configura tu cliente de correo correctamente',
                    'steps': [
                        'Abre tu aplicación de correo electrónico',
                        'Selecciona "Agregar cuenta" o "Nueva cuenta"',
                        'Ingresa tu dirección de correo y contraseña',
                        'Configura los ajustes del servidor si es necesario',
                        'Prueba enviando y recibiendo correos'
                    ],
                    'keywords': ['correo', 'email', 'configurar', 'cuenta', 'configuración']
                }
            }
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of user input
        """
        text_lower = text.lower()
        language_scores = {}
        
        for lang_code, patterns in self.language_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                score += matches
            language_scores[lang_code] = score
        
        # Return language with highest score, default to English
        if language_scores:
            detected_lang = max(language_scores, key=language_scores.get)
            if language_scores[detected_lang] > 0:
                return detected_lang
        
        return self.default_language
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        return False
    
    def get_response_template(self, response_type: str, language: Optional[str] = None) -> str:
        """Get localized response template"""
        lang = language or self.current_language
        
        if response_type in self.responses and lang in self.responses[response_type]:
            return self.responses[response_type][lang]
        
        # Fallback to English if translation not available
        if response_type in self.responses and 'en' in self.responses[response_type]:
            return self.responses[response_type]['en']
        
        return self.supported_languages[lang].fallback_message
    
    def get_knowledge_solution(self, solution_key: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Get localized knowledge base solution"""
        lang = language or self.current_language
        
        if solution_key in self.knowledge_base and lang in self.knowledge_base[solution_key]:
            return self.knowledge_base[solution_key][lang]
        
        # Fallback to English
        if solution_key in self.knowledge_base and 'en' in self.knowledge_base[solution_key]:
            return self.knowledge_base[solution_key]['en']
        
        return None
    
    def search_multilingual_solutions(self, query: str, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for solutions in the specified language"""
        lang = language or self.current_language
        query_lower = query.lower()
        
        matching_solutions = []
        
        for solution_key, solution_data in self.knowledge_base.items():
            if lang in solution_data:
                solution = solution_data[lang]
                
                # Check if query matches keywords or content
                keywords = solution.get('keywords', [])
                title = solution.get('title', '').lower()
                description = solution.get('description', '').lower()
                
                score = 0
                
                # Check keywords
                for keyword in keywords:
                    if keyword.lower() in query_lower:
                        score += 3
                
                # Check title and description
                query_words = query_lower.split()
                for word in query_words:
                    if word in title:
                        score += 2
                    if word in description:
                        score += 1
                
                if score > 0:
                    matching_solutions.append({
                        'key': solution_key,
                        'solution': solution,
                        'score': score,
                        'language': lang
                    })
        
        # Sort by score (highest first)
        matching_solutions.sort(key=lambda x: x['score'], reverse=True)
        return matching_solutions[:5]  # Return top 5 matches
    
    def get_voice_profile_for_language(self, language: Optional[str] = None) -> str:
        """Get appropriate voice ID for the language"""
        lang = language or self.current_language
        return self.supported_languages[lang].voice_id
    
    def get_language_info(self, language_code: str) -> Dict[str, Any]:
        """Get information about a specific language"""
        if language_code in self.supported_languages:
            profile = self.supported_languages[language_code]
            return {
                'code': profile.code,
                'name': profile.name,
                'native_name': profile.native_name,
                'voice_id': profile.voice_id,
                'greeting': profile.greeting
            }
        return None
    
    def get_supported_languages(self) -> List[Dict[str, Any]]:
        """Get list of all supported languages"""
        languages = []
        for code, profile in self.supported_languages.items():
            languages.append({
                'code': profile.code,
                'name': profile.name,
                'native_name': profile.native_name,
                'greeting': profile.greeting
            })
        return languages
    
    def translate_tech_terms(self, text: str, target_language: Optional[str] = None) -> str:
        """Translate technical terms in text"""
        lang = target_language or self.current_language
        
        if lang not in self.supported_languages:
            return text
        
        tech_terms = self.supported_languages[lang].tech_terms
        translated_text = text
        
        for term, translation in tech_terms.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            translated_text = pattern.sub(translation, translated_text)
        
        return translated_text
    
    def format_multilingual_response(
        self, 
        response_type: str, 
        content: str, 
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format a complete multilingual response"""
        lang = language or self.current_language
        
        template = self.get_response_template(response_type, lang)
        
        # Combine template with content if both exist
        if template and content:
            if response_type == 'explanation':
                formatted_text = f"{template}\n\n{content}"
            else:
                formatted_text = f"{template} {content}"
        else:
            formatted_text = content or template
        
        # Translate technical terms
        formatted_text = self.translate_tech_terms(formatted_text, lang)
        
        return {
            'text': formatted_text,
            'language': lang,
            'language_name': self.supported_languages[lang].name,
            'response_type': response_type,
            'voice_id': self.supported_languages[lang].voice_id,
            'timestamp': datetime.now().isoformat()
        }
    
    def handle_language_switch_request(self, requested_language: str) -> Dict[str, Any]:
        """Handle user request to switch languages"""
        if requested_language in self.supported_languages:
            old_language = self.current_language
            self.set_language(requested_language)
            
            switch_message = self.get_response_template('language_switch', requested_language)
            
            return {
                'success': True,
                'old_language': old_language,
                'new_language': requested_language,
                'message': switch_message,
                'voice_id': self.supported_languages[requested_language].voice_id
            }
        else:
            available_languages = [lang.name for lang in self.supported_languages.values()]
            return {
                'success': False,
                'error': f'Language not supported. Available languages: {", ".join(available_languages)}',
                'available_languages': self.get_supported_languages()
            }


    
    def translate_text(self, text: str, source_language: str, target_language: str) -> str:
        """
        Translate text from source language to target language
        This is a simplified implementation - in production, you would use a translation service
        """
        if source_language == target_language:
            return text
        
        # Simple translation mappings for common tech support terms
        translation_mappings = {
            'english_to_spanish': {
                'WiFi connection problem': 'Problema de conexión WiFi',
                'password reset': 'restablecimiento de contraseña',
                'email setup': 'configuración de correo',
                'slow computer': 'computadora lenta',
                'printer issue': 'problema de impresora',
                'software installation': 'instalación de software',
                'internet connection': 'conexión a internet',
                'network problem': 'problema de red',
                'Hello': 'Hola',
                'Thank you': 'Gracias',
                'Help': 'Ayuda',
                'Problem': 'Problema',
                'Solution': 'Solución'
            },
            'spanish_to_english': {
                'Problema de conexión WiFi': 'WiFi connection problem',
                'restablecimiento de contraseña': 'password reset',
                'configuración de correo': 'email setup',
                'computadora lenta': 'slow computer',
                'problema de impresora': 'printer issue',
                'instalación de software': 'software installation',
                'conexión a internet': 'internet connection',
                'problema de red': 'network problem',
                'Hola': 'Hello',
                'Gracias': 'Thank you',
                'Ayuda': 'Help',
                'Problema': 'Problem',
                'Solución': 'Solution'
            }
        }
        
        # Determine translation direction
        if source_language == 'english' and target_language == 'spanish':
            mapping = translation_mappings['english_to_spanish']
        elif source_language == 'spanish' and target_language == 'english':
            mapping = translation_mappings['spanish_to_english']
        else:
            # Unsupported language pair, return original text
            return text
        
        # Try exact match first
        if text in mapping:
            return mapping[text]
        
        # Try partial matches for longer texts
        translated_text = text
        for source_phrase, target_phrase in mapping.items():
            if source_phrase.lower() in text.lower():
                translated_text = translated_text.replace(source_phrase, target_phrase)
        
        return translated_text

