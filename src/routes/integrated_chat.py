from flask import Blueprint, request, jsonify
from src.models.conversation_ai import ConversationAI
from src.models.voice_synthesis import VoiceSynthesis
from datetime import datetime

integrated_chat_bp = Blueprint('integrated_chat', __name__)

# Initialize services
conversation_ai = ConversationAI()
voice_service = VoiceSynthesis()

@integrated_chat_bp.route('/complete-response', methods=['POST'])
def get_complete_response():
    """
    Get complete AI response with voice synthesis and avatar coordination
    This is the main endpoint for full Mia interactions
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        context = data.get('context', {})
        include_voice = data.get('include_voice', True)
        voice_format = data.get('voice_format', 'mp3_44100_128')
        
        if not user_message:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        # Get AI response
        ai_response = conversation_ai.process_message(
            user_message=user_message,
            session_id=session_id,
            context=context
        )
        
        # Get avatar instructions
        avatar_instructions = get_avatar_instructions(ai_response)
        
        # Prepare base response
        complete_response = {
            'user_message': user_message,
            'ai_response': {
                'text': ai_response['text'],
                'intent': ai_response['intent'],
                'confidence': ai_response['confidence'],
                'entities': ai_response['entities'],
                'message_id': ai_response['message_id']
            },
            'avatar_instructions': avatar_instructions,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        # Add voice synthesis if requested
        if include_voice:
            voice_result = voice_service.synthesize_with_timing(
                text=ai_response['text'],
                voice_tone=avatar_instructions['voice_tone']
            )
            
            if voice_result['success']:
                complete_response['voice_synthesis'] = {
                    'audio_base64': voice_result['audio_base64'],
                    'duration_estimate': voice_result['duration_estimate'],
                    'lip_sync_timing': voice_result['lip_sync_timing'],
                    'voice_profile': voice_result['voice_profile'],
                    'optimized_text': voice_result['optimized_text'],
                    'mock_mode': voice_result.get('mock', False)
                }
                
                # Enhanced avatar coordination with voice timing
                complete_response['avatar_coordination'] = {
                    'expression': avatar_instructions['expression'],
                    'gesture': avatar_instructions['gesture'],
                    'voice_tone': avatar_instructions['voice_tone'],
                    'animation_duration': avatar_instructions['animation_duration'],
                    'voice_duration': voice_result['duration_estimate'],
                    'total_interaction_time': max(
                        avatar_instructions['animation_duration'],
                        voice_result['duration_estimate']
                    ),
                    'lip_sync_data': voice_result['lip_sync_timing'],
                    'synchronized': True
                }
            else:
                complete_response['voice_synthesis'] = {
                    'error': voice_result.get('error', 'Voice synthesis failed'),
                    'mock_mode': True
                }
                complete_response['avatar_coordination'] = avatar_instructions
        else:
            complete_response['avatar_coordination'] = avatar_instructions
        
        return jsonify(complete_response)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@integrated_chat_bp.route('/quick-response', methods=['POST'])
def get_quick_response():
    """
    Get quick AI response without voice synthesis for faster interactions
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        context = data.get('context', {})
        
        if not user_message:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        # Get AI response
        ai_response = conversation_ai.process_message(
            user_message=user_message,
            session_id=session_id,
            context=context
        )
        
        # Get avatar instructions
        avatar_instructions = get_avatar_instructions(ai_response)
        
        return jsonify({
            'user_message': user_message,
            'ai_response': {
                'text': ai_response['text'],
                'intent': ai_response['intent'],
                'confidence': ai_response['confidence'],
                'entities': ai_response['entities'],
                'message_id': ai_response['message_id']
            },
            'avatar_instructions': avatar_instructions,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'response_type': 'quick',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@integrated_chat_bp.route('/voice-only', methods=['POST'])
def synthesize_voice_only():
    """
    Generate voice synthesis for existing AI response
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice_tone = data.get('voice_tone', 'professional')
        session_id = data.get('session_id', 'default')
        
        if not text:
            return jsonify({
                'error': 'Text is required',
                'status': 'error'
            }), 400
        
        # Synthesize voice with timing
        voice_result = voice_service.synthesize_with_timing(
            text=text,
            voice_tone=voice_tone
        )
        
        if not voice_result['success']:
            return jsonify({
                'error': voice_result.get('error', 'Voice synthesis failed'),
                'status': 'error'
            }), 500
        
        return jsonify({
            'text': text,
            'voice_synthesis': {
                'audio_base64': voice_result['audio_base64'],
                'duration_estimate': voice_result['duration_estimate'],
                'lip_sync_timing': voice_result['lip_sync_timing'],
                'voice_profile': voice_result['voice_profile'],
                'optimized_text': voice_result['optimized_text'],
                'voice_tone': voice_tone
            },
            'session_id': session_id,
            'timestamp': voice_result['timestamp'],
            'mock_mode': voice_result.get('mock', False),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@integrated_chat_bp.route('/conversation-flow', methods=['POST'])
def manage_conversation_flow():
    """
    Manage complete conversation flow with context and voice synthesis
    """
    try:
        data = request.get_json()
        messages = data.get('messages', [])  # Array of user messages
        session_id = data.get('session_id', 'default')
        context = data.get('context', {})
        include_voice = data.get('include_voice', True)
        
        if not messages or not isinstance(messages, list):
            return jsonify({
                'error': 'Messages array is required',
                'status': 'error'
            }), 400
        
        conversation_flow = []
        
        for i, message in enumerate(messages):
            if not message.strip():
                continue
                
            # Process each message in sequence
            ai_response = conversation_ai.process_message(
                user_message=message.strip(),
                session_id=session_id,
                context=context
            )
            
            avatar_instructions = get_avatar_instructions(ai_response)
            
            flow_item = {
                'sequence': i + 1,
                'user_message': message.strip(),
                'ai_response': ai_response,
                'avatar_instructions': avatar_instructions,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add voice synthesis if requested
            if include_voice:
                voice_result = voice_service.synthesize_with_timing(
                    text=ai_response['text'],
                    voice_tone=avatar_instructions['voice_tone']
                )
                
                if voice_result['success']:
                    flow_item['voice_synthesis'] = {
                        'audio_base64': voice_result['audio_base64'],
                        'duration_estimate': voice_result['duration_estimate'],
                        'lip_sync_timing': voice_result['lip_sync_timing']
                    }
            
            conversation_flow.append(flow_item)
        
        return jsonify({
            'conversation_flow': conversation_flow,
            'session_id': session_id,
            'total_messages': len(conversation_flow),
            'include_voice': include_voice,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

def get_avatar_instructions(response):
    """
    Generate avatar animation instructions based on AI response
    Enhanced version with voice coordination
    """
    instructions = {
        'expression': 'helpful',
        'gesture': 'none',
        'voice_tone': 'professional',
        'animation_duration': 3.0
    }
    
    intent = response.get('intent', 'general')
    confidence = response.get('confidence', 0.5)
    entities = response.get('entities', {})
    
    # Map intents to avatar behaviors
    if intent == 'greeting':
        instructions.update({
            'expression': 'helpful',
            'gesture': 'welcoming',
            'voice_tone': 'warm',
            'animation_duration': 3.5
        })
    elif intent == 'problem_solving':
        instructions.update({
            'expression': 'thinking',
            'gesture': 'explaining',
            'voice_tone': 'focused',
            'animation_duration': 4.0
        })
    elif intent == 'explanation' or intent == 'how_to':
        instructions.update({
            'expression': 'explaining',
            'gesture': 'pointing',
            'voice_tone': 'clear',
            'animation_duration': 5.0
        })
    elif intent == 'confirmation':
        instructions.update({
            'expression': 'understanding',
            'gesture': 'nodding',
            'voice_tone': 'confirming',
            'animation_duration': 2.5
        })
    elif intent == 'gratitude':
        instructions.update({
            'expression': 'celebrating',
            'gesture': 'celebration',
            'voice_tone': 'excited',
            'animation_duration': 3.0
        })
    elif intent in ['denial', 'problem_solving']:
        instructions.update({
            'expression': 'understanding',
            'gesture': 'supportive',
            'voice_tone': 'empathetic',
            'animation_duration': 3.5
        })
    
    # Adjust based on confidence level
    if confidence < 0.3:
        instructions['expression'] = 'thinking'
        instructions['voice_tone'] = 'uncertain'
    elif confidence > 0.8:
        instructions['voice_tone'] = 'confident'
    
    # Adjust based on emotional entities
    emotions = entities.get('emotions', [])
    if emotions:
        if any(emotion in ['frustrated', 'angry', 'stressed'] for emotion in emotions):
            instructions['voice_tone'] = 'empathetic'
            instructions['expression'] = 'understanding'
        elif any(emotion in ['happy', 'pleased', 'grateful'] for emotion in emotions):
            instructions['voice_tone'] = 'excited'
            instructions['expression'] = 'celebrating'
    
    # Adjust based on urgency
    urgency_indicators = entities.get('urgency_indicators', [])
    if urgency_indicators:
        instructions['voice_tone'] = 'focused'
        instructions['animation_duration'] = 2.0  # Faster for urgent issues
    
    return instructions

