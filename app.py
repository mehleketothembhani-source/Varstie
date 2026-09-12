import os
from flask import Flask, jsonify, request, session, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/csrf')
def get_csrf():
    return jsonify({"csrf_token": "sample_csrf_token"})

@app.route('/api/me')
def get_me():
    # Return 401 unauthenticated by default for new sessions
    return jsonify({"error": "Unauthorized"}), 401

@socketio.on('join_video_room')
def handle_join_room(data):
    room_id = data.get('room_id')
    emit('participant_joined', {"sid": request.sid, "name": "Student"}, broadcast=True, include_self=False)

@socketio.on('signal')
def handle_signal(data):
    target = data.get('to')
    emit('signal', {"from": request.sid, "data": data.get('data')}, room=target)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
