
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

connected_users = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    message = data['message']
    username = data['username']
    send({'message': message, 'username': username}, broadcast=True)

@socketio.on('user_connected')
def handle_user_connected(data):
    username = data['username']
    connected_users.append(username)
    emit('user_connected', {'username': username}, broadcast=True)

@socketio.on('user_disconnected')
def handle_user_disconnected(data):
    username = data['username']
    connected_users.remove(username)
    emit('user_disconnected', {'username': username}, broadcast=True)

@app.route('/users')
def get_users():
    return jsonify({'users': connected_users})

@app.route('/messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
