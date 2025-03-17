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

    print("Received PGN:", pgn)  # You can process this further

    # Process PGN using python-chess
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return jsonify({"error": "Invalid PGN format"}), 400

    moves_list = []
    node = game
    while node.variations:
        node = node.variation(0)
        moves_list.append(node.move.uci())
        
    print("Parsed Game:", game)
    print("Extracted Moves:", moves_list)

    return jsonify({"message": "PGN received successfully", "moves": moves_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
