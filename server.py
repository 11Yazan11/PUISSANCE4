from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'game_data.db'

def init_db():
    """Initialize the database and create a players table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    """Register a new player."""
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
        conn.commit()
        return jsonify({"message": f"Player '{username}' registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()

@app.route('/player/<username>', methods=['GET'])
def get_player(username):
    """Get player details by username."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, score FROM players WHERE username = ?", (username,))
    player = cursor.fetchone()
    conn.close()
    
    if player:
        return jsonify({"id": player[0], "username": player[1], "score": player[2]})
    else:
        return jsonify({"error": "Player not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
