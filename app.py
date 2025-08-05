from flask import Flask, render_template, request, jsonify
import tictactoe as ttt

app = Flask(__name__)

board = ttt.initial_state()
ai_turn = False

@app.route("/")
def index():
    global board, ai_turn
    winner = ttt.winner(board)
    game_over = ttt.terminal(board)
    return render_template("index.html", board=board, winner=winner, game_over=game_over)

@app.route("/move", methods=["POST"])
def move():
    global board, ai_turn
    if not ttt.terminal(board):
        row = int(request.json["row"])
        col = int(request.json["col"])
        if (row, col) in ttt.actions(board):
            board = ttt.result(board, (row, col))
            ai_turn = True

            if not ttt.terminal(board):
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False

            winner = ttt.winner(board)
            game_over = ttt.terminal(board)
            return jsonify({
                "board": board,
                "winner": winner,
                "game_over": game_over
            })
    return jsonify({"error": "Invalid move"})

@app.route("/reset", methods=["POST"])
def reset():
    
    global board, ai_turn
    board = ttt.initial_state()
    ai_turn = False
    return jsonify({"board": board})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
