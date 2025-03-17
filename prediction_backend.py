import pickle
import chess.pgn
import io
import numpy as np
import chess_utils
import joblib

def gaussian_kernel(distances):
    weights = np.exp(-75 * (distances ** 2))
    return weights / np.sum(weights)

nn_model = joblib.load("models/knn_model.pkl")


def predict_elo(pgn_text, move_limit=35):
    """
    Predicts the Elo ratings for White and Black based on a given PGN game.

    Parameters:
        pgn_text (str): The PGN game string.
        move_limit (int, optional): The number of moves to consider. Defaults to 35.

    Returns:
        tuple: Predicted Elo ratings for White and Black.
    """
    # Parse the PGN
    pgn_io = io.StringIO(pgn_text)
    game = chess.pgn.read_game(pgn_io)

    if game is None:
        raise ValueError("Invalid PGN input")

    # Convert game to feature vector
    game_vector = chess_utils.game_to_vec(game, move_limit).reshape(1, -1)

    # Predict Elo
    predicted_elo = nn_model.predict(game_vector)
    white_elo, black_elo = predicted_elo.flatten()

    return white_elo, black_elo
