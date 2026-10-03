from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from game import Game


app = FastAPI(title="Chess Game API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


games = {}


class MoveRequest(BaseModel):
    game_id: str
    start: str
    end: str


@app.post("/game/new")
def new_game():

    game = Game()

    game_id = str(len(games) + 1)

    games[game_id] = game

    return {
        "game_id": game_id,
        "turn": game.turn,
        "message": "Game created"
    }


@app.get("/game/{game_id}")
def get_game(game_id: str):

    if game_id not in games:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    game = games[game_id]

    board = []

    for row in range(8):

        row_data = []

        for col in range(8):

            piece = game.board.board[row][col]

            if piece is None:
                row_data.append(None)

            else:
                row_data.append({
                    "type": piece.type,
                    "color": piece.color
                })

        board.append(row_data)

    return {
        "game_id": game_id,
        "turn": game.turn,
        "board": board,
        "game_over": game.game_over,
        "winner": game.winner
    }


@app.post("/game/move")
def make_move(move: MoveRequest):

    if move.game_id not in games:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    game = games[move.game_id]

    try:
        result = game.move(
            move.start.lower(),
            move.end.lower()
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid position"
        )

    if not result:
        return {
            "success": False,
            "message": "Illegal move",
            "turn": game.turn
        }

    return {
        "success": True,
        "message": "Move successful",
        "start": move.start,
        "end": move.end,
        "turn": game.turn,
        "game_over": game.game_over,
        "winner": game.winner
    }


# -------------------------
# Frontend
# -------------------------

app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)