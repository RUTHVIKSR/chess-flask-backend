import os
from flask import Flask, request, jsonify
import chess.pgn
from flask_cors import CORS
import io
import prediction_backend  # Import the prediction module

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
    
    try:
        # Predict Elo ratings using the model
        white_elo, black_elo = prediction_backend.predict_elo(pgn)
        
        print(f"Predicted Elo: White - {white_elo}, Black - {black_elo}", flush=True)

        return jsonify({
            "message": "PGN processed successfully",
            "white_elo": white_elo,
            "black_elo": black_elo
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
