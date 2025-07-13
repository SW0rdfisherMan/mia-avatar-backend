from flask import Blueprint, request, jsonify
import json
import re
import random
from datetime import datetime
from src.models.conversation_ai import ConversationAI
from src.models.tech_support_knowledge import TechSupportKnowledge

conversation_bp = Blueprint('conversation', __name__)

# Initialize AI components
conversation_ai = ConversationAI()
tech_knowledge = TechSupportKnowledge()

@conversation_bp.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint for conversing with Mia
    Handles user input and returns AI response with avatar instructions
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
        
        # Process the conversation
        response = conversation_ai.process_message(
            user_message=user_message,
            session_id=session_id,
            context=context
        )
        
        # Get avatar instructions based on response type
        avatar_instructions = get_avatar_instructions(response)
        
        return jsonify({
            'response': response['text'],
            'confidence': response['confidence'],
            'intent': response['intent'],
            'entities': response['entities'],
            'avatar_instructions': avatar_instructions,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@conversation_bp.route('/intent', methods=['POST'])
def analyze_intent():
    """
    Analyze user intent without generating a full response
    Useful for understanding user needs quickly
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        intent_analysis = conversation_ai.analyze_intent(user_message)
        
        return jsonify({
            'intent': intent_analysis['intent'],
            'confidence': intent_analysis['confidence'],
            'entities': intent_analysis['entities'],
            'category': intent_analysis['category'],
            'urgency': intent_analysis['urgency'],
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@conversation_bp.route('/context', methods=['POST'])
def update_context():
    """
    Update conversation context for better responses
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        context_updates = data.get('context', {})
        
        conversation_ai.update_context(session_id, context_updates)
        
        return jsonify({
            'message': 'Context updated successfully',
            'session_id': session_id,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@conversation_bp.route('/session/<session_id>', methods=['GET'])
def get_session_history(session_id):
    """
    Get conversation history for a session
    """
    try:
        history = conversation_ai.get_session_history(session_id)
        
        return jsonify({
            'session_id': session_id,
            'history': history,
            'message_count': len(history),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@conversation_bp.route('/session/<session_id>', methods=['DELETE'])
def clear_session(session_id):
    """
    Clear conversation history for a session
    """
    try:
        conversation_ai.clear_session(session_id)
        
        return jsonify({
            'message': f'Session {session_id} cleared successfully',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@conversation_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback on AI responses for continuous improvement
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        message_id = data.get('message_id')
        rating = data.get('rating')  # 1-5 scale
        feedback_text = data.get('feedback', '')
        
        conversation_ai.record_feedback(
            session_id=session_id,
            message_id=message_id,
            rating=rating,
            feedback_text=feedback_text
        )
        
        return jsonify({
            'message': 'Feedback recorded successfully',
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
    """
    instructions = {
        'expression': 'helpful',
        'gesture': 'none',
        'voice_tone': 'professional',
        'animation_duration': 3.0
    }
    
    intent = response.get('intent', 'general')
    confidence = response.get('confidence', 0.5)
    
    # Map intents to avatar behaviors
    if intent == 'greeting':
        instructions.update({
            'expression': 'helpful',
            'gesture': 'welcoming',
            'voice_tone': 'warm'
        })
    elif intent == 'problem_solving':
        instructions.update({
            'expression': 'thinking',
            'gesture': 'explaining',
            'voice_tone': 'focused'
        })
    elif intent == 'explanation':
        instructions.update({
            'expression': 'explaining',
            'gesture': 'pointing',
            'voice_tone': 'clear'
        })
    elif intent == 'confirmation':
        instructions.update({
            'expression': 'understanding',
            'gesture': 'nodding',
            'voice_tone': 'confirming'
        })
    elif intent == 'celebration':
        instructions.update({
            'expression': 'celebrating',
            'gesture': 'celebration',
            'voice_tone': 'excited'
        })
    elif intent == 'concern':
        instructions.update({
            'expression': 'understanding',
            'gesture': 'supportive',
            'voice_tone': 'empathetic'
        })
    
    # Adjust based on confidence level
    if confidence < 0.3:
        instructions['expression'] = 'thinking'
        instructions['voice_tone'] = 'uncertain'
    elif confidence > 0.8:
        instructions['voice_tone'] = 'confident'
    
    return instructions

