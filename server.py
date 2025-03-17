import os
from flask import Flask, request, jsonify
import chess.pgn
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Flask Backend is Running!"

@app.route('/upload_pgn', methods=['POST'])
def receive_pgn():
    data = request.get_json()
    pgn = data.get("pgn", "")

    if not pgn:
        return jsonify({"error": "No PGN data received"}), 400

    # Convert literal "\n" sequences to actual newline characters
    pgn = pgn.replace("\\n", "\n")
    print("Received PGN:", pgn, flush=True)

    # Process PGN using python-chess
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return jsonify({"error": "Invalid PGN format"}), 400

    # Extract moves using mainline_moves
    moves_list = [move.uci() for move in game.mainline_moves()]
        
    print("Parsed Game:", game, flush=True)
    print("Extracted Moves:", moves_list, flush=True)

    return jsonify({"message": "PGN received successfully", "moves": moves_list})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
