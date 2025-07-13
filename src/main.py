import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.conversation import conversation_bp
from src.routes.knowledge import knowledge_bp
from src.routes.avatar import avatar_bp
from src.routes.voice import voice_bp
from src.routes.integrated_chat import integrated_chat_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'mia_avatar_secret_key_2024'

# Enable CORS for all routes to allow frontend communication
CORS(app, origins="*")

# Register API blueprints
app.register_blueprint(conversation_bp, url_prefix='/api/conversation')
app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
app.register_blueprint(avatar_bp, url_prefix='/api/avatar')
app.register_blueprint(voice_bp, url_prefix='/api/voice')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve static files and handle SPA routing"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Mia AI Backend", "version": "1.0.0"}

if __name__ == '__main__':
    print("🤖 Starting Mia AI Backend Server...")
    print("🌟 Beautiful, intelligent tech support avatar ready!")
    app.run(host='0.0.0.0', port=5001, debug=True)

