from flask import Blueprint, request, jsonify, send_file
import os
import tempfile
import base64
from src.models.voice_synthesis import VoiceSynthesis

voice_bp = Blueprint('voice', __name__)

# Initialize voice synthesis service
voice_service = VoiceSynthesis()

@voice_bp.route('/synthesize', methods=['POST'])
def synthesize_text():
    """
    Convert text to speech using Mia's voice
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice_tone = data.get('voice_tone', 'professional')
        output_format = data.get('output_format', 'mp3_44100_128')
        return_audio = data.get('return_audio', True)
        
        if not text:
            return jsonify({
                'error': 'Text is required',
                'status': 'error'
            }), 400
        
        # Synthesize speech
        result = voice_service.synthesize_speech(
            text=text,
            voice_tone=voice_tone,
            language=data.get('language', 'en')
        )
        
        if not result['success']:
            return jsonify({
                'error': result.get('error', 'Voice synthesis failed'),
                'status': 'error'
            }), 500
        
        response_data = {
            'text': result['text'],
            'optimized_text': result['optimized_text'],
            'voice_id': result.get('voice_id', 'unknown'),
            'voice_tone': result['voice_tone'],
            'language': result.get('language', 'en'),
            'audio_format': result.get('audio_format', 'mp3'),
            'duration_estimate': result['duration_estimate'],
            'audio_size': result['audio_size'],
            'timestamp': result['timestamp'],
            'status': 'success'
        }
        
        if return_audio:
            response_data['audio_base64'] = result['audio_base64']
        
        if result.get('mock'):
            response_data['mock_mode'] = True
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@voice_bp.route('/synthesize-with-timing', methods=['POST'])
def synthesize_with_timing():
    """
    Convert text to speech with lip-sync timing information
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice_tone = data.get('voice_tone', 'professional')
        
        if not text:
            return jsonify({
                'error': 'Text is required',
                'status': 'error'
            }), 400
        
        # Synthesize speech with timing
        result = voice_service.synthesize_with_timing(
            text=text,
            voice_tone=voice_tone
        )
        
        if not result['success']:
            return jsonify({
                'error': result.get('error', 'Voice synthesis failed'),
                'status': 'error'
            }), 500
        
        return jsonify({
            'text': result['text'],
            'optimized_text': result['optimized_text'],
            'voice_profile': result['voice_profile'],
            'voice_tone': result['voice_tone'],
            'audio_format': result['audio_format'],
            'duration_estimate': result['duration_estimate'],
            'audio_base64': result['audio_base64'],
            'lip_sync_timing': result['lip_sync_timing'],
            'timestamp': result['timestamp'],
            'mock_mode': result.get('mock', False),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@voice_bp.route('/conversation-response', methods=['POST'])
def synthesize_conversation_response():
    """
    Synthesize voice for AI conversation response with avatar coordination
    """
    try:
        data = request.get_json()
        ai_response = data.get('ai_response', {})
        session_id = data.get('session_id', 'default')
        
        # Extract text and voice instructions from AI response
        text = ai_response.get('text', '').strip()
        avatar_instructions = ai_response.get('avatar_instructions', {})
        voice_tone = avatar_instructions.get('voice_tone', 'professional')
        
        if not text:
            return jsonify({
                'error': 'AI response text is required',
                'status': 'error'
            }), 400
        
        # Synthesize speech with timing for avatar coordination
        voice_result = voice_service.synthesize_with_timing(
            text=text,
            voice_tone=voice_tone
        )
        
        if not voice_result['success']:
            return jsonify({
                'error': voice_result.get('error', 'Voice synthesis failed'),
                'status': 'error'
            }), 500
        
        # Combine voice synthesis with avatar instructions
        response = {
            'session_id': session_id,
            'ai_response': ai_response,
            'voice_synthesis': {
                'text': voice_result['text'],
                'optimized_text': voice_result['optimized_text'],
                'voice_profile': voice_result['voice_profile'],
                'voice_tone': voice_result['voice_tone'],
                'audio_base64': voice_result['audio_base64'],
                'duration_estimate': voice_result['duration_estimate'],
                'lip_sync_timing': voice_result['lip_sync_timing']
            },
            'avatar_coordination': {
                'expression': avatar_instructions.get('expression', 'helpful'),
                'gesture': avatar_instructions.get('gesture', 'none'),
                'animation_duration': avatar_instructions.get('animation_duration', 3.0),
                'voice_duration': voice_result['duration_estimate'],
                'sync_timing': voice_result['lip_sync_timing']
            },
            'timestamp': voice_result['timestamp'],
            'mock_mode': voice_result.get('mock', False),
            'status': 'success'
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@voice_bp.route('/voices', methods=['GET'])
def get_available_voices():
    """
    Get list of available voice profiles for Mia
    """
    try:
        voices = voice_service.get_available_voices()
        
        return jsonify({
            'voices': voices,
            'current_voice': voice_service.current_voice,
            'count': len(voices),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@voice_bp.route('/voice-profile', methods=['POST'])
def set_voice_profile():
    """
    Set the current voice profile for Mia
    """
    try:
        data = request.get_json()
        voice_key = data.get('voice_key', '').strip()
        
        if not voice_key:
            return jsonify({
                'error': 'Voice key is required',
                'status': 'error'
            }), 400
        
        success = voice_service.set_voice_profile(voice_key)
        
        if not success:
            available_voices = [v['key'] for v in voice_service.get_available_voices()]
            return jsonify({
                'error': f'Invalid voice key. Available voices: {available_voices}',
                'status': 'error'
            }), 400
        
        return jsonify({
            'message': f'Voice profile set to {voice_key}',
            'current_voice': voice_service.current_voice,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@voice_bp.route('/test-connection', methods=['GET'])
def test_voice_connection():
    """
    Test ElevenLabs API connection and voice synthesis
    """
    try:
        result = voice_service.test_connection()
        
        return jsonify({
            'connection_test': result,
            'service_status': 'operational' if result['success'] else 'degraded',
            'mock_mode': result['mock_mode'],
            'timestamp': voice_service.synthesize_speech('test', return_base64=False)['timestamp'],
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@voice_bp.route('/audio-file/<path:filename>', methods=['GET'])
def serve_audio_file(filename):
    """
    Serve generated audio files
    """
    try:
        # Security check - only serve files from temp directory
        if not filename.startswith('/tmp/'):
            return jsonify({
                'error': 'Invalid file path',
                'status': 'error'
            }), 400
        
        if not os.path.exists(filename):
            return jsonify({
                'error': 'Audio file not found',
                'status': 'error'
            }), 404
        
        return send_file(
            filename,
            as_attachment=True,
            download_name=f'mia_voice_{os.path.basename(filename)}'
        )
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@voice_bp.route('/presets', methods=['GET'])
def get_voice_presets():
    """
    Get predefined voice tone presets for different scenarios
    """
    try:
        presets = {
            'greeting': {
                'voice_tone': 'warm',
                'description': 'Warm, welcoming tone for greetings',
                'use_case': 'Initial user interaction'
            },
            'problem_solving': {
                'voice_tone': 'focused',
                'description': 'Clear, focused tone for technical explanations',
                'use_case': 'Troubleshooting and problem solving'
            },
            'explanation': {
                'voice_tone': 'clear',
                'description': 'Clear, educational tone for instructions',
                'use_case': 'Step-by-step guidance'
            },
            'understanding': {
                'voice_tone': 'empathetic',
                'description': 'Empathetic, supportive tone for user concerns',
                'use_case': 'Acknowledging user frustration'
            },
            'celebration': {
                'voice_tone': 'excited',
                'description': 'Enthusiastic tone for successful outcomes',
                'use_case': 'Problem resolution celebration'
            },
            'professional': {
                'voice_tone': 'professional',
                'description': 'Standard professional tone for general support',
                'use_case': 'Default interaction mode'
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

@voice_bp.route('/batch-synthesize', methods=['POST'])
def batch_synthesize():
    """
    Synthesize multiple text snippets in batch for efficiency
    """
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        voice_tone = data.get('voice_tone', 'professional')
        
        if not texts or not isinstance(texts, list):
            return jsonify({
                'error': 'Texts array is required',
                'status': 'error'
            }), 400
        
        results = []
        for i, text in enumerate(texts):
            if text.strip():
                result = voice_service.synthesize_speech(
                    text=text.strip(),
                    voice_tone=voice_tone,
                    return_base64=True
                )
                results.append({
                    'index': i,
                    'text': text,
                    'synthesis_result': result
                })
        
        return jsonify({
            'batch_results': results,
            'total_processed': len(results),
            'voice_tone': voice_tone,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

