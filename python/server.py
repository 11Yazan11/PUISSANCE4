import threading
from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit

# Constants
PORT = 3001
TICK_RATE = 60


# Flask app and SocketIO setup
app = Flask(__name__, static_folder='public')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
current_map = 'default'



# Routes
@app.route('/game')
def serve_index():
    return send_from_directory(app.static_folder, 'client.py')

# Socket.IO events for /game namespace
@socketio.on('connect', namespace='/game')
def on_connect():
    player_id = request.sid
    print(f'A player joined the game: {player_id}')


@socketio.on('disconnect', namespace='/game')
def disconnect():
    player_id = request.sid  # Get the player ID from the disconnect data
    print(f'A player left the game: {player_id}')



# Game loop
def game_loop():
    while True:
        socketio.sleep(1 / TICK_RATE)

# Start the server
if __name__ == '__main__':
    threading.Thread(target=game_loop, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=PORT)