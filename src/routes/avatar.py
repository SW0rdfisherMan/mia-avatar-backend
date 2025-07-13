from flask import Blueprint, request, jsonify
import json
from datetime import datetime

avatar_bp = Blueprint('avatar', __name__)

# Avatar state management
avatar_sessions = {}

@avatar_bp.route('/status', methods=['GET'])
def get_avatar_status():
    """
    Get current avatar status and capabilities
    """
    try:
        return jsonify({
            'avatar': {
                'name': 'Mia',
                'version': '1.0.0',
                'status': 'active',
                'capabilities': [
                    'conversational_ai',
                    'facial_expressions',
                    'voice_synthesis',
                    'gesture_animation',
                    'tech_support'
                ],
                'supported_expressions': [
                    'neutral',
                    'understanding',
                    'helpful',
                    'thinking',
                    'explaining',
                    'speaking',
                    'attentive',
                    'celebrating'
                ],
                'supported_gestures': [
                    'welcoming',
                    'explaining',
                    'pointing',
                    'nodding',
                    'celebration',
                    'supportive',
                    'thinking_pose'
                ],
                'voice_options': [
                    'professional',
                    'warm',
                    'focused',
                    'clear',
                    'confirming',
                    'excited',
                    'empathetic'
                ]
            },
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/expression', methods=['POST'])
def set_expression():
    """
    Set avatar facial expression
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        expression = data.get('expression', 'neutral')
        intensity = data.get('intensity', 1.0)
        duration = data.get('duration', 3.0)
        
        # Validate expression
        valid_expressions = [
            'neutral', 'understanding', 'helpful', 'thinking', 
            'explaining', 'speaking', 'attentive', 'celebrating'
        ]
        
        if expression not in valid_expressions:
            return jsonify({
                'error': f'Invalid expression. Valid options: {valid_expressions}',
                'status': 'error'
            }), 400
        
        # Update avatar session
        if session_id not in avatar_sessions:
            avatar_sessions[session_id] = {
                'current_expression': 'neutral',
                'current_gesture': 'none',
                'voice_tone': 'professional',
                'last_update': datetime.now()
            }
        
        avatar_sessions[session_id].update({
            'current_expression': expression,
            'expression_intensity': intensity,
            'expression_duration': duration,
            'last_update': datetime.now()
        })
        
        return jsonify({
            'message': f'Expression set to {expression}',
            'session_id': session_id,
            'expression': expression,
            'intensity': intensity,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/gesture', methods=['POST'])
def set_gesture():
    """
    Set avatar gesture/body language
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        gesture = data.get('gesture', 'none')
        duration = data.get('duration', 2.0)
        
        # Validate gesture
        valid_gestures = [
            'none', 'welcoming', 'explaining', 'pointing', 
            'nodding', 'celebration', 'supportive', 'thinking_pose'
        ]
        
        if gesture not in valid_gestures:
            return jsonify({
                'error': f'Invalid gesture. Valid options: {valid_gestures}',
                'status': 'error'
            }), 400
        
        # Update avatar session
        if session_id not in avatar_sessions:
            avatar_sessions[session_id] = {
                'current_expression': 'neutral',
                'current_gesture': 'none',
                'voice_tone': 'professional',
                'last_update': datetime.now()
            }
        
        avatar_sessions[session_id].update({
            'current_gesture': gesture,
            'gesture_duration': duration,
            'last_update': datetime.now()
        })
        
        return jsonify({
            'message': f'Gesture set to {gesture}',
            'session_id': session_id,
            'gesture': gesture,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/voice-tone', methods=['POST'])
def set_voice_tone():
    """
    Set avatar voice tone for speech synthesis
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        voice_tone = data.get('voice_tone', 'professional')
        
        # Validate voice tone
        valid_tones = [
            'professional', 'warm', 'focused', 'clear', 
            'confirming', 'excited', 'empathetic', 'uncertain', 'confident'
        ]
        
        if voice_tone not in valid_tones:
            return jsonify({
                'error': f'Invalid voice tone. Valid options: {valid_tones}',
                'status': 'error'
            }), 400
        
        # Update avatar session
        if session_id not in avatar_sessions:
            avatar_sessions[session_id] = {
                'current_expression': 'neutral',
                'current_gesture': 'none',
                'voice_tone': 'professional',
                'last_update': datetime.now()
            }
        
        avatar_sessions[session_id].update({
            'voice_tone': voice_tone,
            'last_update': datetime.now()
        })
        
        return jsonify({
            'message': f'Voice tone set to {voice_tone}',
            'session_id': session_id,
            'voice_tone': voice_tone,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/animation-sequence', methods=['POST'])
def play_animation_sequence():
    """
    Play a coordinated animation sequence (expression + gesture + voice)
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        sequence = data.get('sequence', {})
        
        # Default sequence structure
        default_sequence = {
            'expression': 'neutral',
            'expression_intensity': 1.0,
            'gesture': 'none',
            'voice_tone': 'professional',
            'duration': 3.0,
            'transition_speed': 1.0
        }
        
        # Merge with provided sequence
        animation_sequence = {**default_sequence, **sequence}
        
        # Update avatar session
        if session_id not in avatar_sessions:
            avatar_sessions[session_id] = {
                'current_expression': 'neutral',
                'current_gesture': 'none',
                'voice_tone': 'professional',
                'last_update': datetime.now()
            }
        
        avatar_sessions[session_id].update({
            'current_expression': animation_sequence['expression'],
            'expression_intensity': animation_sequence['expression_intensity'],
            'current_gesture': animation_sequence['gesture'],
            'voice_tone': animation_sequence['voice_tone'],
            'animation_duration': animation_sequence['duration'],
            'transition_speed': animation_sequence['transition_speed'],
            'last_update': datetime.now()
        })
        
        return jsonify({
            'message': 'Animation sequence started',
            'session_id': session_id,
            'sequence': animation_sequence,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/session/<session_id>', methods=['GET'])
def get_avatar_session(session_id):
    """
    Get current avatar state for a session
    """
    try:
        if session_id not in avatar_sessions:
            return jsonify({
                'error': 'Session not found',
                'status': 'error'
            }), 404
        
        session_data = avatar_sessions[session_id]
        
        return jsonify({
            'session_id': session_id,
            'avatar_state': session_data,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/session/<session_id>', methods=['DELETE'])
def clear_avatar_session(session_id):
    """
    Clear avatar session and reset to defaults
    """
    try:
        if session_id in avatar_sessions:
            del avatar_sessions[session_id]
        
        return jsonify({
            'message': f'Avatar session {session_id} cleared',
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/presets', methods=['GET'])
def get_animation_presets():
    """
    Get predefined animation presets for common scenarios
    """
    try:
        presets = {
            'greeting': {
                'expression': 'helpful',
                'gesture': 'welcoming',
                'voice_tone': 'warm',
                'duration': 3.0,
                'description': 'Friendly greeting animation'
            },
            'problem_solving': {
                'expression': 'thinking',
                'gesture': 'thinking_pose',
                'voice_tone': 'focused',
                'duration': 4.0,
                'description': 'Thoughtful problem-solving pose'
            },
            'explaining': {
                'expression': 'explaining',
                'gesture': 'pointing',
                'voice_tone': 'clear',
                'duration': 5.0,
                'description': 'Animated explanation gesture'
            },
            'understanding': {
                'expression': 'understanding',
                'gesture': 'nodding',
                'voice_tone': 'empathetic',
                'duration': 2.5,
                'description': 'Empathetic understanding response'
            },
            'celebration': {
                'expression': 'celebrating',
                'gesture': 'celebration',
                'voice_tone': 'excited',
                'duration': 3.0,
                'description': 'Positive outcome celebration'
            },
            'listening': {
                'expression': 'attentive',
                'gesture': 'none',
                'voice_tone': 'professional',
                'duration': 2.0,
                'description': 'Attentive listening pose'
            }
        }
        
        return jsonify({
            'presets': presets,
            'count': len(presets),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@avatar_bp.route('/preset/<preset_name>', methods=['POST'])
def apply_preset(preset_name):
    """
    Apply a predefined animation preset
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        # Get preset configuration
        presets = {
            'greeting': {
                'expression': 'helpful',
                'gesture': 'welcoming',
                'voice_tone': 'warm',
                'duration': 3.0
            },
            'problem_solving': {
                'expression': 'thinking',
                'gesture': 'thinking_pose',
                'voice_tone': 'focused',
                'duration': 4.0
            },
            'explaining': {
                'expression': 'explaining',
                'gesture': 'pointing',
                'voice_tone': 'clear',
                'duration': 5.0
            },
            'understanding': {
                'expression': 'understanding',
                'gesture': 'nodding',
                'voice_tone': 'empathetic',
                'duration': 2.5
            },
            'celebration': {
                'expression': 'celebrating',
                'gesture': 'celebration',
                'voice_tone': 'excited',
                'duration': 3.0
            },
            'listening': {
                'expression': 'attentive',
                'gesture': 'none',
                'voice_tone': 'professional',
                'duration': 2.0
            }
        }
        
        if preset_name not in presets:
            return jsonify({
                'error': f'Preset not found. Available presets: {list(presets.keys())}',
                'status': 'error'
            }), 404
        
        preset_config = presets[preset_name]
        
        # Update avatar session
        if session_id not in avatar_sessions:
            avatar_sessions[session_id] = {
                'current_expression': 'neutral',
                'current_gesture': 'none',
                'voice_tone': 'professional',
                'last_update': datetime.now()
            }
        
        avatar_sessions[session_id].update({
            'current_expression': preset_config['expression'],
            'current_gesture': preset_config['gesture'],
            'voice_tone': preset_config['voice_tone'],
            'animation_duration': preset_config['duration'],
            'preset_applied': preset_name,
            'last_update': datetime.now()
        })
        
        return jsonify({
            'message': f'Preset {preset_name} applied successfully',
            'session_id': session_id,
            'preset': preset_name,
            'configuration': preset_config,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

