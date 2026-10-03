from game import Game

def print_board(game):
    print("\n a b c d e f g h")

    for row in range(8):
        rank = 8 - row
        line = []

        for col in range(8):
            piece = game.board.board[row][col]

            if piece is None:
                symbol = "."
            else:
                symbols = {
                    "king": "K",
                    "queen": "Q",
                    "rook": "R",
                    "bishop": "B",
                    "knight": "N",
                    "pawn": "P"
                }

                symbol = symbols[piece.type]

                if piece.color == "black":
                    symbol = symbol.lower()

            line.append(symbol)

        print(rank, " ".join(line), rank)

    print("  a b c d e f g h")
    print("نوبت:", game.turn)

def main():
    game = Game()

    print("================================")
    print("        CHESS GAME")
    print("================================")

    print_board(game)

    while not game.game_over:

        print()

        move = input(
            f"{game.turn} move (e2 e4): "
        ).strip()

        if not move:
            continue

        parts = move.split()

        if len(parts) != 2:
            print("❌ فرمت اشتباه است.")
            print("مثال: e2 e4")
            continue

        start = parts[0].lower()
        end = parts[1].lower()

        try:
            result = game.move(start, end)
            
        except ValueError:
            print("❌ مختصات نامعتبر است.")
            continue

        if result:
            print(f"✅ {start} → {end}")
            print_board(game)

    print("\n================================")
    print("          GAME OVER")
    print("================================")

    if game.winner:
        print("🏆 برنده:", game.winner)
    else:
        print("🤝 مساوی")
    
if __name__ == "__main__":
    main()