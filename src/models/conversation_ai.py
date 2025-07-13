import re
import json
import random
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from src.models.multilingual_support import MultilingualSupport

@dataclass
class ConversationMessage:
    """Represents a single message in the conversation"""
    id: str
    timestamp: datetime
    user_message: str
    ai_response: str
    intent: str
    confidence: float
    entities: Dict[str, Any]
    context: Dict[str, Any]

class ConversationAI:
    """
    Core conversational AI system for Mia Avatar
    Handles natural language understanding, intent recognition, and response generation
    """
    
    def __init__(self):
        self.sessions = {}  # Store conversation sessions
        self.personality_traits = self._load_personality()
        self.intent_patterns = self._load_intent_patterns()
        self.entity_patterns = self._load_entity_patterns()
        self.response_templates = self._load_response_templates()
        self.multilingual = MultilingualSupport()  # Initialize multilingual support
        
    def process_message(self, user_message: str, session_id: str = 'default', context: Dict = None) -> Dict[str, Any]:
        """
        Process a user message and generate an appropriate response with multilingual support
        """
        if context is None:
            context = {}
        
        # Detect language from user message
        detected_language = self.multilingual.detect_language(user_message)
        
        # Initialize session if it doesn't exist
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'messages': [],
                'context': {},
                'user_profile': {},
                'conversation_state': 'greeting',
                'language': detected_language
            }
        
        session = self.sessions[session_id]
        
        # Update session language if different from detected
        if session.get('language', 'en') != detected_language:
            session['language'] = detected_language
            self.multilingual.set_language(detected_language)
        
        # Update session context
        session['context'].update(context)
        session['context']['language'] = detected_language
        
        # Check for XETA-specific queries first
        xeta_response = self.handle_xeta_query(user_message, detected_language)
        if xeta_response:
            # Create message record for XETA response
            message_record = {
                'timestamp': datetime.now().isoformat(),
                'user_message': user_message,
                'bot_response': xeta_response['response'],
                'intent': xeta_response['intent'],
                'emotion': xeta_response['emotion'],
                'animation': xeta_response['animation'],
                'voice_tone': xeta_response['voice_tone'],
                'language': detected_language
            }
            session['messages'].append(message_record)
            return xeta_response
        
        # Analyze the user message with language context
        intent_analysis = self.analyze_intent(user_message, detected_language)
        entities = self.extract_entities(user_message, detected_language)
        
        # Generate multilingual response based on intent and context
        response_text = self.generate_multilingual_response(
            intent_analysis['intent'],
            user_message,
            session['context'],
            entities,
            detected_language
        )
        
        # Create message record
        message = ConversationMessage(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            user_message=user_message,
            ai_response=response_text,
            intent=intent_analysis['intent'],
            confidence=intent_analysis['confidence'],
            entities=entities,
            context=session['context'].copy()
        )
        
        # Store message in session
        session['messages'].append(message)
        
        # Update conversation state
        self._update_conversation_state(session, intent_analysis['intent'])
        
        return {
            'text': response_text,
            'intent': intent_analysis['intent'],
            'confidence': intent_analysis['confidence'],
            'entities': entities,
            'message_id': message.id
        }
    
    def analyze_intent(self, user_message: str) -> Dict[str, Any]:
        """
        Analyze user intent from the message
        """
        message_lower = user_message.lower().strip()
        
        # Check for specific intent patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    confidence = self._calculate_confidence(pattern, message_lower)
                    return {
                        'intent': intent,
                        'confidence': confidence,
                        'category': self._get_intent_category(intent),
                        'urgency': self._assess_urgency(message_lower)
                    }
        
        # Default to general inquiry
        return {
            'intent': 'general_inquiry',
            'confidence': 0.5,
            'category': 'general',
            'urgency': 'low'
        }
    
    def extract_entities(self, user_message: str) -> Dict[str, Any]:
        """
        Extract entities from user message (devices, software, issues, etc.)
        """
        entities = {
            'devices': [],
            'software': [],
            'issues': [],
            'urgency_indicators': [],
            'emotions': []
        }
        
        message_lower = user_message.lower()
        
        # Extract device mentions
        device_patterns = [
            r'\b(computer|laptop|desktop|pc|mac|iphone|android|phone|tablet|ipad)\b',
            r'\b(printer|scanner|monitor|keyboard|mouse|webcam|microphone)\b',
            r'\b(router|modem|wifi|internet|network)\b'
        ]
        
        for pattern in device_patterns:
            matches = re.findall(pattern, message_lower)
            entities['devices'].extend(matches)
        
        # Extract software mentions
        software_patterns = [
            r'\b(windows|macos|linux|chrome|firefox|safari|edge)\b',
            r'\b(office|word|excel|powerpoint|outlook|teams|zoom)\b',
            r'\b(photoshop|illustrator|autocad|slack|discord)\b'
        ]
        
        for pattern in software_patterns:
            matches = re.findall(pattern, message_lower)
            entities['software'].extend(matches)
        
        # Extract issue types
        issue_patterns = [
            r'\b(crash|freeze|slow|error|bug|problem|issue|broken|not working)\b',
            r'\b(virus|malware|security|hack|breach|spam)\b',
            r'\b(update|install|download|backup|restore|sync)\b'
        ]
        
        for pattern in issue_patterns:
            matches = re.findall(pattern, message_lower)
            entities['issues'].extend(matches)
        
        # Extract urgency indicators
        urgency_patterns = [
            r'\b(urgent|emergency|asap|immediately|critical|important)\b',
            r'\b(deadline|due|meeting|presentation|work)\b'
        ]
        
        for pattern in urgency_patterns:
            matches = re.findall(pattern, message_lower)
            entities['urgency_indicators'].extend(matches)
        
        # Extract emotional indicators
        emotion_patterns = [
            r'\b(frustrated|angry|confused|worried|stressed|panic)\b',
            r'\b(happy|pleased|satisfied|grateful|thankful)\b'
        ]
        
        for pattern in emotion_patterns:
            matches = re.findall(pattern, message_lower)
            entities['emotions'].extend(matches)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def generate_response(self, intent: str, user_message: str, context: Dict, entities: Dict) -> str:
        """
        Generate an appropriate response based on intent and context
        """
        # Get base response template
        templates = self.response_templates.get(intent, self.response_templates['general_inquiry'])
        base_response = random.choice(templates)
        
        # Personalize response based on context and entities
        personalized_response = self._personalize_response(
            base_response, user_message, context, entities
        )
        
        # Add Mia's personality touch
        final_response = self._add_personality(personalized_response, intent, entities)
        
        return final_response
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent recognition patterns"""
        return {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\b(how are you|what\'s up|greetings)\b'
            ],
            'problem_solving': [
                r'\b(help|problem|issue|trouble|error|broken|not working)\b',
                r'\b(fix|solve|repair|troubleshoot)\b',
                r'\b(can\'t|cannot|won\'t|doesn\'t work)\b'
            ],
            'how_to': [
                r'\b(how to|how do i|how can i|show me how)\b',
                r'\b(tutorial|guide|instructions|steps)\b'
            ],
            'software_support': [
                r'\b(install|download|update|upgrade|configure)\b',
                r'\b(software|program|application|app)\b'
            ],
            'hardware_support': [
                r'\b(computer|laptop|printer|monitor|keyboard|mouse)\b',
                r'\b(hardware|device|equipment)\b'
            ],
            'network_support': [
                r'\b(internet|wifi|network|connection|router|modem)\b',
                r'\b(slow internet|no connection|can\'t connect)\b'
            ],
            'security_support': [
                r'\b(virus|malware|security|antivirus|firewall)\b',
                r'\b(hack|breach|suspicious|spam|phishing)\b'
            ],
            'account_support': [
                r'\b(password|login|account|username|forgot)\b',
                r'\b(reset|recover|change password)\b'
            ],
            'confirmation': [
                r'\b(yes|yeah|yep|correct|right|exactly)\b',
                r'\b(that\'s right|that works|perfect)\b'
            ],
            'denial': [
                r'\b(no|nope|not really|incorrect|wrong)\b',
                r'\b(that\'s not it|doesn\'t work|still broken)\b'
            ],
            'gratitude': [
                r'\b(thank you|thanks|appreciate|grateful)\b',
                r'\b(that helped|you\'re great|awesome)\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|talk later|have a good day)\b',
                r'\b(that\'s all|i\'m done|finished)\b'
            ]
        }
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load response templates for different intents"""
        return {
            'greeting': [
                "Hi there! I'm Mia, your tech support specialist. I'm here to help you with any technical issues you might have. What can I assist you with today?",
                "Hello! Welcome to tech support. I'm Mia, and I'm excited to help you solve any technical challenges you're facing. How can I make your day better?",
                "Hey! I'm Mia, your friendly tech support avatar. I'm here to turn your tech troubles into tech triumphs! What's on your mind?"
            ],
            'problem_solving': [
                "I understand you're experiencing a technical issue. Let me help you get this sorted out! Can you tell me more details about what's happening?",
                "No worries, I'm here to help solve this problem with you. Technical issues can be frustrating, but we'll figure this out together. What exactly is going wrong?",
                "I can definitely help you with that! Let's troubleshoot this step by step. Can you describe what you were doing when the problem started?"
            ],
            'how_to': [
                "I'd be happy to walk you through that process! Let me break it down into simple, easy-to-follow steps for you.",
                "Great question! I love helping people learn new things. Let me guide you through this step by step.",
                "Absolutely! I'll show you exactly how to do that. Here's a clear, simple approach that should work perfectly for you."
            ],
            'software_support': [
                "Software issues can be tricky, but I'm here to help! Let's get your software working smoothly again. What specific software are we dealing with?",
                "I'm experienced with all kinds of software problems. Let's diagnose what's happening and get you back up and running quickly!",
                "Software troubles? No problem! I'll help you get everything configured properly. Tell me more about what you're trying to accomplish."
            ],
            'hardware_support': [
                "Hardware issues can be concerning, but many are easier to fix than you might think! Let's check a few things together.",
                "I'm here to help with your hardware problem. Let's start with some basic diagnostics to identify what's going on.",
                "Hardware troubles can be frustrating, but we'll get this sorted out! Can you tell me what device is giving you trouble?"
            ],
            'network_support': [
                "Network connectivity issues are among the most common problems I help with. Let's get your connection back to full strength!",
                "Internet troubles? I've got you covered! Let's run through some quick checks to restore your connection.",
                "Network problems can really disrupt your day. Let me help you get back online quickly and reliably!"
            ],
            'security_support': [
                "Security is incredibly important, and I'm glad you're being proactive about it! Let's make sure your system is safe and secure.",
                "I take security concerns very seriously. Let's address this issue right away to protect your data and privacy.",
                "Security issues need immediate attention. I'm here to help you secure your system and prevent future problems."
            ],
            'account_support': [
                "Account access issues can be really frustrating! Let me help you regain access to your account safely and securely.",
                "I'll help you sort out your account problem. Account security is important, so we'll make sure to do this properly.",
                "Account troubles? No worries! I'll guide you through the recovery process step by step."
            ],
            'confirmation': [
                "Perfect! I'm glad that's working for you now. Is there anything else I can help you with today?",
                "Excellent! It sounds like we've got that sorted out. Do you have any other technical questions I can assist with?",
                "Great to hear! I'm happy we could resolve that together. Feel free to ask if you need help with anything else!"
            ],
            'denial': [
                "I understand that didn't work as expected. Let's try a different approach to solve this problem.",
                "No problem! Sometimes it takes a few different methods to find the right solution. Let me suggest another approach.",
                "That's okay! Technical issues can be complex. Let's explore some other options to get this working for you."
            ],
            'gratitude': [
                "You're very welcome! I'm so happy I could help you today. That's exactly what I'm here for!",
                "It was my pleasure to help! I love solving technical problems and making people's lives easier.",
                "Thank you for the kind words! I'm thrilled we could get everything working perfectly for you."
            ],
            'goodbye': [
                "Have a wonderful day! Remember, I'm always here if you need any more tech support. Take care!",
                "It was great helping you today! Don't hesitate to reach out if you have any more technical questions. Goodbye!",
                "Thanks for letting me help you! I hope everything continues to work smoothly. See you next time!"
            ],
            'general_inquiry': [
                "I'm here to help with any technical questions or issues you might have. What would you like assistance with today?",
                "I'd be happy to help you with that! Can you tell me a bit more about what you're looking for?",
                "That's an interesting question! Let me see how I can best assist you with that. Can you provide some more details?"
            ]
        }
    
    def _load_tech_keywords(self) -> Dict[str, List[str]]:
        """Load technology-related keywords for better understanding"""
        return {
            'operating_systems': ['windows', 'macos', 'linux', 'ios', 'android'],
            'browsers': ['chrome', 'firefox', 'safari', 'edge', 'opera'],
            'office_software': ['word', 'excel', 'powerpoint', 'outlook', 'teams'],
            'devices': ['computer', 'laptop', 'phone', 'tablet', 'printer', 'router'],
            'issues': ['slow', 'crash', 'freeze', 'error', 'virus', 'malware']
        }
    
    def _load_personality_traits(self) -> Dict[str, Any]:
        """Load Mia's personality traits for response generation"""
        return {
            'professional': True,
            'friendly': True,
            'witty': True,
            'understanding': True,
            'helpful': True,
            'encouraging': True,
            'patient': True,
            'knowledgeable': True
        }
    
    def _calculate_confidence(self, pattern: str, message: str) -> float:
        """Calculate confidence score for intent matching"""
        matches = len(re.findall(pattern, message))
        message_length = len(message.split())
        
        # Base confidence on pattern matches and message context
        base_confidence = min(0.9, 0.3 + (matches * 0.2))
        
        # Adjust based on message length and clarity
        if message_length > 5:
            base_confidence += 0.1
        
        return round(base_confidence, 2)
    
    def _get_intent_category(self, intent: str) -> str:
        """Categorize intents for better organization"""
        categories = {
            'greeting': 'social',
            'goodbye': 'social',
            'gratitude': 'social',
            'problem_solving': 'technical',
            'software_support': 'technical',
            'hardware_support': 'technical',
            'network_support': 'technical',
            'security_support': 'technical',
            'account_support': 'technical',
            'how_to': 'educational',
            'confirmation': 'feedback',
            'denial': 'feedback'
        }
        return categories.get(intent, 'general')
    
    def _assess_urgency(self, message: str) -> str:
        """Assess the urgency level of the user's request"""
        urgent_keywords = ['urgent', 'emergency', 'critical', 'asap', 'immediately', 'deadline']
        high_keywords = ['important', 'soon', 'quickly', 'meeting', 'presentation']
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in urgent_keywords):
            return 'urgent'
        elif any(keyword in message_lower for keyword in high_keywords):
            return 'high'
        else:
            return 'normal'
    
    def _personalize_response(self, base_response: str, user_message: str, context: Dict, entities: Dict) -> str:
        """Personalize the response based on user context and entities"""
        response = base_response
        
        # Add specific device/software mentions if relevant
        if entities.get('devices'):
            device = entities['devices'][0]
            response = response.replace('your system', f'your {device}')
        
        if entities.get('software'):
            software = entities['software'][0]
            response += f" I see you're working with {software}."
        
        # Adjust tone based on emotional indicators
        if entities.get('emotions'):
            emotion = entities['emotions'][0]
            if emotion in ['frustrated', 'angry', 'stressed']:
                response = "I completely understand how frustrating this can be. " + response
            elif emotion in ['happy', 'pleased', 'grateful']:
                response = "I'm so glad to hear that! " + response
        
        return response
    
    def _add_personality(self, response: str, intent: str, entities: Dict) -> str:
        """Add Mia's personality touches to the response"""
        # Add encouraging phrases for problem-solving
        if intent == 'problem_solving' and random.random() < 0.3:
            encouragements = [
                " Don't worry, we'll get this figured out!",
                " I'm confident we can solve this together!",
                " Technical issues happen to everyone - let's fix this!"
            ]
            response += random.choice(encouragements)
        
        # Add witty touches occasionally
        if random.random() < 0.2 and intent not in ['security_support', 'urgent']:
            witty_additions = [
                " Technology can be quirky sometimes, but that's what makes it interesting!",
                " Every tech problem is just a puzzle waiting to be solved!",
                " I love a good technical challenge!"
            ]
            response += random.choice(witty_additions)
        
        return response
    
    def _update_conversation_state(self, session: Dict, intent: str):
        """Update the conversation state based on the current intent"""
        state_transitions = {
            'greeting': 'active',
            'problem_solving': 'troubleshooting',
            'how_to': 'teaching',
            'confirmation': 'resolved',
            'goodbye': 'ending'
        }
        
        if intent in state_transitions:
            session['conversation_state'] = state_transitions[intent]
    
    def update_context(self, session_id: str, context_updates: Dict):
        """Update session context with new information"""
        if session_id in self.sessions:
            self.sessions[session_id]['context'].update(context_updates)
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]['messages']
        return [
            {
                'id': msg.id,
                'timestamp': msg.timestamp.isoformat(),
                'user_message': msg.user_message,
                'ai_response': msg.ai_response,
                'intent': msg.intent,
                'confidence': msg.confidence
            }
            for msg in messages
        ]
    
    def clear_session(self, session_id: str):
        """Clear conversation history for a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def record_feedback(self, session_id: str, message_id: str, rating: int, feedback_text: str = ''):
        """Record user feedback for continuous improvement"""
        # In a production system, this would save to a database
        # For now, we'll just log it
        feedback_record = {
            'session_id': session_id,
            'message_id': message_id,
            'rating': rating,
            'feedback_text': feedback_text,
            'timestamp': datetime.now().isoformat()
        }
        
        # TODO: Implement feedback storage and analysis
        print(f"Feedback recorded: {feedback_record}")


    
    def generate_multilingual_response(
        self, 
        intent: str, 
        user_message: str, 
        context: Dict, 
        entities: Dict, 
        language: str
    ) -> str:
        """
        Generate response in the specified language
        """
        # Check if this is a language switch request
        if self._is_language_switch_request(user_message, language):
            return self._handle_language_switch(user_message, language)
        
        # Use multilingual knowledge base for technical solutions
        if intent in ['problem_solving', 'how_to', 'explanation']:
            solution = self._get_multilingual_solution(user_message, language)
            if solution:
                return self.multilingual.format_multilingual_response(
                    'explanation', 
                    solution, 
                    language
                )['text']
        
        # Generate standard response with personality
        base_response = self.generate_response(intent, user_message, context, entities)
        
        # Format with multilingual template
        formatted_response = self.multilingual.format_multilingual_response(
            intent, 
            base_response, 
            language
        )
        
        return formatted_response['text']
    
    def analyze_intent(self, message: str, language: str = 'en') -> Dict[str, Any]:
        """
        Enhanced intent analysis with multilingual support
        """
        # Get base intent analysis
        base_analysis = self._analyze_base_intent(message)
        
        # Add language-specific intent patterns
        if language == 'es':
            spanish_patterns = {
                'greeting': [r'\b(hola|buenos días|buenas tardes|buenas noches)\b'],
                'gratitude': [r'\b(gracias|muchas gracias|te agradezco)\b'],
                'problem_solving': [r'\b(problema|error|no funciona|ayuda|necesito)\b'],
                'how_to': [r'\b(cómo|como hacer|instrucciones|pasos)\b']
            }
            
            for intent_type, patterns in spanish_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, message.lower()):
                        base_analysis['intent'] = intent_type
                        base_analysis['confidence'] = min(base_analysis['confidence'] + 0.2, 1.0)
                        break
        
        return base_analysis
    
    def extract_entities(self, message: str, language: str = 'en') -> Dict[str, List[str]]:
        """
        Enhanced entity extraction with multilingual support
        """
        # Get base entities
        entities = self._extract_base_entities(message)
        
        # Add language-specific entity patterns
        if language == 'es':
            spanish_entities = {
                'devices': [r'\b(computadora|ordenador|laptop|móvil|celular|teléfono)\b'],
                'software': [r'\b(programa|aplicación|app|navegador|correo)\b'],
                'issues': [r'\b(problema|error|falla|no funciona|lento|virus)\b'],
                'emotions': [r'\b(frustrado|molesto|preocupado|confundido|feliz)\b']
            }
            
            for entity_type, patterns in spanish_entities.items():
                if entity_type not in entities:
                    entities[entity_type] = []
                
                for pattern in patterns:
                    matches = re.findall(pattern, message.lower())
                    entities[entity_type].extend(matches)
        
        return entities
    
    def _is_language_switch_request(self, message: str, current_language: str) -> bool:
        """
        Detect if user is requesting to switch languages
        """
        switch_patterns = {
            'en': [r'\b(english|speak english|in english)\b'],
            'es': [r'\b(español|spanish|en español|habla español)\b']
        }
        
        message_lower = message.lower()
        for lang, patterns in switch_patterns.items():
            if lang != current_language:
                for pattern in patterns:
                    if re.search(pattern, message_lower):
                        return True
        return False
    
    def _handle_language_switch(self, message: str, current_language: str) -> str:
        """
        Handle language switch requests
        """
        # Detect requested language
        if re.search(r'\b(english|speak english|in english)\b', message.lower()):
            requested_language = 'en'
        elif re.search(r'\b(español|spanish|en español|habla español)\b', message.lower()):
            requested_language = 'es'
        else:
            requested_language = 'en'  # Default to English
        
        # Switch language
        switch_result = self.multilingual.handle_language_switch_request(requested_language)
        
        if switch_result['success']:
            return switch_result['message']
        else:
            return switch_result['error']
    
    def _get_multilingual_solution(self, query: str, language: str) -> Optional[str]:
        """
        Get technical solution in the specified language
        """
        solutions = self.multilingual.search_multilingual_solutions(query, language)
        
        if solutions:
            best_solution = solutions[0]['solution']
            
            # Format solution as step-by-step guide
            steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(best_solution['steps'])])
            
            return f"{best_solution['description']}\n\n{steps_text}"
        
        return None
    
    def _analyze_base_intent(self, message: str) -> Dict[str, Any]:
        """
        Base intent analysis (language-agnostic)
        """
        message_lower = message.lower()
        intent_scores = {}
        
        # Calculate scores for each intent
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, message_lower))
                score += matches
            intent_scores[intent] = score
        
        # Find best intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3.0, 1.0)  # Normalize confidence
            
            if confidence > 0.1:
                return {
                    'intent': best_intent,
                    'confidence': confidence,
                    'all_scores': intent_scores
                }
        
        # Default intent
        return {
            'intent': 'general',
            'confidence': 0.5,
            'all_scores': intent_scores
        }
    
    def _extract_base_entities(self, message: str) -> Dict[str, List[str]]:
        """
        Base entity extraction (language-agnostic)
        """
        entities = {}
        message_lower = message.lower()
        
        for entity_type, patterns in self.entity_patterns.items():
            entities[entity_type] = []
            for pattern in patterns:
                matches = re.findall(pattern, message_lower)
                entities[entity_type].extend(matches)
        
        return entities
    
    def get_language_capabilities(self) -> Dict[str, Any]:
        """
        Get information about supported languages and capabilities
        """
        return {
            'supported_languages': self.multilingual.get_supported_languages(),
            'current_language': self.multilingual.current_language,
            'language_detection': True,
            'automatic_translation': True,
            'multilingual_knowledge_base': True,
            'voice_synthesis_languages': ['en', 'es']
        }
    
    def switch_language(self, language_code: str, session_id: str = 'default') -> Dict[str, Any]:
        """
        Manually switch language for a session
        """
        if session_id in self.sessions:
            self.sessions[session_id]['language'] = language_code
        
        switch_result = self.multilingual.handle_language_switch_request(language_code)
        
        return {
            'success': switch_result['success'],
            'message': switch_result.get('message', switch_result.get('error')),
            'language': language_code,
            'session_id': session_id
        }


    def _load_personality(self):
        """Load Mia's personality traits"""
        return {
            'name': 'Mia',
            'role': 'Beautiful Multilingual Tech Support Assistant',
            'traits': [
                'professional', 'friendly', 'helpful', 'patient', 'knowledgeable',
                'beautiful', 'confident', 'empathetic', 'multilingual'
            ],
            'communication_style': {
                'tone': 'warm and professional',
                'approach': 'solution-oriented',
                'empathy_level': 'high',
                'technical_level': 'adaptive'
            },
            'languages': ['english', 'spanish'],
            'specialties': [
                'WiFi troubleshooting', 'password reset', 'email configuration',
                'software installation', 'hardware diagnostics', 'network security'
            ]
        }
    
    def _load_intent_patterns(self):
        """Load intent recognition patterns"""
        return {
            'greeting': [
                r'\b(hello|hi|hey|good morning|good afternoon|hola|buenos días)\b',
                r'\b(greetings|salutations|saludos)\b'
            ],
            'wifi_problem': [
                r'\b(wifi|wi-fi|internet|connection|network|router)\b.*\b(problem|issue|not working|slow|down)\b',
                r'\b(can\'t connect|cannot connect|no internet|no connection)\b'
            ],
            'password_reset': [
                r'\b(forgot|forgotten|reset|change)\b.*\b(password|pass)\b',
                r'\b(locked out|can\'t login|cannot login)\b'
            ],
            'email_setup': [
                r'\b(email|mail)\b.*\b(setup|configure|not working|problem)\b',
                r'\b(outlook|gmail|yahoo)\b.*\b(setup|configure|help)\b'
            ],
            'slow_computer': [
                r'\b(computer|pc|laptop)\b.*\b(slow|sluggish|lagging|freezing)\b',
                r'\b(performance|speed)\b.*\b(issue|problem)\b'
            ],
            'software_installation': [
                r'\b(install|installation|setup)\b.*\b(software|program|application)\b',
                r'\b(can\'t install|won\'t install|installation failed)\b'
            ],
            'printer_issues': [
                r'\b(printer|print)\b.*\b(not working|problem|issue|error)\b',
                r'\b(can\'t print|won\'t print|printing problem)\b'
            ],
            'gratitude': [
                r'\b(thank you|thanks|appreciate|grateful|gracias)\b',
                r'\b(that worked|perfect|great|excellent|wonderful)\b'
            ],
            'goodbye': [
                r'\b(goodbye|bye|see you|farewell|adiós|hasta luego)\b',
                r'\b(that\'s all|i\'m done|no more questions)\b'
            ]
        }
    
    def _load_entity_patterns(self):
        """Load entity recognition patterns"""
        return {
            'devices': [
                r'\b(computer|laptop|desktop|pc|mac|phone|smartphone|tablet|ipad|iphone|android)\b'
            ],
            'software': [
                r'\b(windows|mac|macos|ios|android|chrome|firefox|safari|edge|office|word|excel|outlook)\b'
            ],
            'network_terms': [
                r'\b(wifi|wi-fi|internet|router|modem|network|connection|bandwidth)\b'
            ],
            'email_providers': [
                r'\b(gmail|outlook|yahoo|hotmail|icloud|aol)\b'
            ],
            'emotions': [
                r'\b(frustrated|angry|confused|worried|stressed|urgent|help|please)\b'
            ]
        }
    
    def _load_response_templates(self):
        """Load response templates for different scenarios"""
        return {
            'greeting': {
                'english': [
                    "Hello! I'm Mia, your beautiful tech support assistant. How can I help you today?",
                    "Hi there! I'm here to help you with any tech issues. What's troubling you?",
                    "Welcome! I'm Mia, and I'm excited to help solve your technical challenges."
                ],
                'spanish': [
                    "¡Hola! Soy Mía, tu hermosa asistente de soporte técnico. ¿Cómo puedo ayudarte hoy?",
                    "¡Hola! Estoy aquí para ayudarte con cualquier problema técnico. ¿Qué te está molestando?",
                    "¡Bienvenido! Soy Mía, y estoy emocionada de ayudar a resolver tus desafíos técnicos."
                ]
            },
            'clarification': {
                'english': [
                    "Could you provide more details about the issue you're experiencing?",
                    "To better assist you, can you tell me what device or software you're having trouble with?",
                    "I'd love to help! Can you describe exactly what happens when you try to {action}?"
                ],
                'spanish': [
                    "¿Podrías proporcionar más detalles sobre el problema que estás experimentando?",
                    "Para asistirte mejor, ¿puedes decirme con qué dispositivo o software tienes problemas?",
                    "¡Me encantaría ayudar! ¿Puedes describir exactamente qué pasa cuando intentas {action}?"
                ]
            },
            'success': {
                'english': [
                    "Wonderful! I'm so glad we could resolve that together.",
                    "Perfect! Is there anything else I can help you with today?",
                    "Excellent! You did a great job following those steps."
                ],
                'spanish': [
                    "¡Maravilloso! Me alegra mucho que hayamos podido resolver eso juntos.",
                    "¡Perfecto! ¿Hay algo más en lo que pueda ayudarte hoy?",
                    "¡Excelente! Hiciste un gran trabajo siguiendo esos pasos."
                ]
            }
        }


    
    def handle_xeta_query(self, message: str, language: str = "english") -> Dict[str, Any]:
        """Handle XETA-specific queries"""
        message_lower = message.lower()
        
        # XETA-specific intent detection
        if any(word in message_lower for word in ["xeta", "router", "kit", "earn", "tokens"]):
            if any(word in message_lower for word in ["install", "setup", "connect"]):
                return self._generate_xeta_installation_response(language)
            elif any(word in message_lower for word in ["earn", "money", "tokens", "income"]):
                return self._generate_xeta_earning_response(language)
            elif any(word in message_lower for word in ["price", "cost", "buy", "purchase"]):
                return self._generate_xeta_pricing_response(language)
            elif any(word in message_lower for word in ["account", "login", "access"]):
                return self._generate_xeta_account_response(language)
            else:
                return self._generate_xeta_general_response(language)
        
        return None
    
    def _generate_xeta_installation_response(self, language: str) -> Dict[str, Any]:
        """Generate XETA installation help response"""
        if language == "spanish":
            return {
                "response": "¡Perfecto! Te ayudo con la instalación de tu Kit XETA. Primero, necesito saber qué tipo de configuración de internet tienes actualmente. ¿Tienes un módem/router todo-en-uno de tu ISP, o un sistema WiFi separado como Eero o Netgear Orbi?",
                "intent": "xeta_installation",
                "emotion": "helpful",
                "animation": "explaining",
                "voice_tone": "professional",
                "follow_up": "Una vez que me digas tu configuración, te guiaré paso a paso por todo el proceso de instalación."
            }
        else:
            return {
                "response": "Perfect! I'll help you install your XETA Kit. First, I need to know what type of internet setup you currently have. Do you have an all-in-one modem/router from your ISP, or a separate WiFi system like Eero or Netgear Orbi?",
                "intent": "xeta_installation", 
                "emotion": "helpful",
                "animation": "explaining",
                "voice_tone": "professional",
                "follow_up": "Once you tell me your setup, I'll guide you step-by-step through the entire installation process."
            }
    
    def _generate_xeta_earning_response(self, language: str) -> Dict[str, Any]:
        """Generate XETA earning explanation response"""
        if language == "spanish":
            return {
                "response": "¡Excelente pregunta! Con XETA ganas tokens de cuatro maneras principales: 1) Mantener tu dispositivo conectado y en línea, 2) Alojar datos encriptados para la red, 3) Ejecutar tareas de cómputo de IA, y 4) Compartir tu ancho de banda. Mientras más tiempo estés en línea, más ganas. Los tokens se pueden gastar en servicios, apostar para más ganancias, o vender por dinero en efectivo.",
                "intent": "xeta_earning",
                "emotion": "encouraging", 
                "animation": "explaining",
                "voice_tone": "enthusiastic",
                "follow_up": "¿Te gustaría saber más sobre algún aspecto específico de las ganancias con XETA?"
            }
        else:
            return {
                "response": "Excellent question! With XETA, you earn tokens in four main ways: 1) Keeping your device plugged in and online, 2) Hosting encrypted data for the network, 3) Running AI compute tasks, and 4) Sharing your bandwidth. The longer you're online, the more you earn. Tokens can be spent on services, staked for more earnings, or sold for cash.",
                "intent": "xeta_earning",
                "emotion": "encouraging",
                "animation": "explaining", 
                "voice_tone": "enthusiastic",
                "follow_up": "Would you like to know more about any specific aspect of earning with XETA?"
            }
    
    def _generate_xeta_pricing_response(self, language: str) -> Dict[str, Any]:
        """Generate XETA pricing information response"""
        if language == "spanish":
            return {
                "response": "El Kit Inicial XETA cuesta $1,350 e incluye todo lo que necesitas: 2 routers WiFi7 para cobertura mesh completa del hogar, cables de alimentación, cable ethernet, guía de configuración con código QR, y acceso completo a la red de ganancias XETA. A diferencia de un router normal de $200 que solo te cuesta dinero, el Kit XETA puede pagarse a sí mismo con el tiempo a través de las ganancias de tokens.",
                "intent": "xeta_pricing",
                "emotion": "confident",
                "animation": "explaining",
                "voice_tone": "professional",
                "follow_up": "Stock limitado disponible. ¿Te gustaría saber más sobre las opciones de compra?"
            }
        else:
            return {
                "response": "The XETA Starter Kit costs $1,350 and includes everything you need: 2 WiFi7 routers for complete whole-home mesh coverage, power cables, ethernet cable, QR code setup guide, and full access to the XETA earning network. Unlike a regular $200 router that only costs you money, the XETA Kit can pay for itself over time through token earnings.",
                "intent": "xeta_pricing",
                "emotion": "confident", 
                "animation": "explaining",
                "voice_tone": "professional",
                "follow_up": "Limited stock available. Would you like to know more about purchasing options?"
            }
    
    def _generate_xeta_account_response(self, language: str) -> Dict[str, Any]:
        """Generate XETA account access response"""
        if language == "spanish":
            return {
                "response": "Para acceder a tu cuenta XETA, ve a xeta.net, haz clic en 'Account' > 'Log In', ingresa tu dirección de email y haz clic en 'Continue'. Recibirás un email de verificación - simplemente haz clic en el enlace para acceder. Tu cuenta muestra todas tus órdenes, información de rastreo, registro de productos y acceso a tu cuenta de embajador.",
                "intent": "xeta_account",
                "emotion": "helpful",
                "animation": "explaining",
                "voice_tone": "supportive",
                "follow_up": "¿Necesitas ayuda con algún aspecto específico de tu cuenta XETA?"
            }
        else:
            return {
                "response": "To access your XETA account, go to xeta.net, click 'Account' > 'Log In', enter your email address and click 'Continue'. You'll receive a verification email - simply click the link to access your account. Your account shows all your orders, tracking info, product registration, and ambassador account access.",
                "intent": "xeta_account",
                "emotion": "helpful",
                "animation": "explaining", 
                "voice_tone": "supportive",
                "follow_up": "Do you need help with any specific aspect of your XETA account?"
            }
    
    def _generate_xeta_general_response(self, language: str) -> Dict[str, Any]:
        """Generate general XETA information response"""
        if language == "spanish":
            return {
                "response": "XETA está revolucionando el internet creando una red descentralizada donde TÚ eres dueño de la infraestructura y ganas dinero por participar. Es una oportunidad de $6.7 billones en telecomunicaciones, computación en la nube e IA. Con XETA, no solo obtienes internet WiFi7 súper rápido, sino que también ganas tokens que tienen valor real. ¡Es el futuro del internet!",
                "intent": "xeta_general",
                "emotion": "enthusiastic",
                "animation": "welcoming",
                "voice_tone": "excited",
                "follow_up": "¿Qué aspecto específico de XETA te interesa más: instalación, ganancias, o información del producto?"
            }
        else:
            return {
                "response": "XETA is revolutionizing the internet by creating a decentralized network where YOU own the infrastructure and earn money for participating. It's a $6.7 trillion opportunity across telecommunications, cloud computing, and AI. With XETA, you don't just get blazing-fast WiFi7 internet - you earn tokens that have real value. It's the future of the internet!",
                "intent": "xeta_general",
                "emotion": "enthusiastic", 
                "animation": "welcoming",
                "voice_tone": "excited",
                "follow_up": "What specific aspect of XETA interests you most: installation, earning, or product information?"
            }

