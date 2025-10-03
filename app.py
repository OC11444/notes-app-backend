from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)

# Allow CORS for local dev and GitHub Pages domain
CORS(
    app,
    resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "https://OC11444.github.io",
        "https://OC11444.github.io/notes-app-frontend"
    ]}}
)

# Simple in-memory storage (replace with DB for production)
notes = []

@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json(silent=True) or {}
    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content required'}), 400

    new_note = {
        'id': (max([n['id'] for n in notes]) + 1) if notes else 1,
        'title': data['title'],
        'content': data['content'],
        'created_at': datetime.now().isoformat()
    }
    notes.append(new_note)
    return jsonify(new_note), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json(silent=True) or {}
    note = next((n for n in notes if n['id'] == note_id), None)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    note['title'] = data.get('title', note['title'])
    note['content'] = data.get('content', note['content'])
    note['updated_at'] = datetime.now().isoformat()
    return jsonify(note)

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    if not any(n['id'] == note_id for n in notes):
        return jsonify({'error': 'Note not found'}), 404
    notes = [n for n in notes if n['id'] != note_id]
    return jsonify({'message': 'Note deleted'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Respect PORT env var for cloud platforms (Render/Fly/etc.)
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
