from chess_engine import Board, King, Queen, Rook, Knight, Bishop, Pawn

class Game:

    def __init__(self):
        self.board = Board()
        self.turn = "white"
        self.last_move = None
        self.game_over = False
        self.winner = None

# -------- مختصات --------

    def position_to_index(self, position):
        col = ord(position[0].lower()) - ord("a")
        row = 8 - int(position[1])

        if not (0 <= row  < 8 and 0 <= col < 8):
            raise ValueError("Invalid position")

        return row, col

    def index_to_position(self, row, col):
        return chr(ord("a") + col) + str(8 - row)

# -------- گرفتن مهره --------

    def get_piece(self, position):
        row, col = self.position_to_index(position)
        return self.board.board[row][col]

# -------- بررسی مسیر --------

    def clear_path(self, start_row, start_col, end_row, end_col):

        row_step = (end_row > start_row) - (end_row < start_row)
        col_step = (end_col > start_col) - (end_col < start_col)

        row = start_row + row_step
        col = start_col + col_step

        while (row, col) != (end_row, end_col):

            if self.board.board[row][col] is not None:
                return False

            row += row_step
            col += col_step

        return True

# -------- حرکت عادی مهره --------

    def is_basic_move_legal(self, start, end):

        start_row, start_col = self.position_to_index(start)
        end_row, end_col = self.position_to_index(end)

        piece = self.board.board[start_row][start_col]
        target = self.board.board[end_row][end_col]

        if piece is None:
            return False

        if piece.color != self.turn:
            return False

        if target is not None and target.color == piece.color:
            return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        piece_type = piece.type

        # Pawn
        if piece_type == "pawn":

            direction = -1 if piece.color == "white" else 1

            if col_diff == 0 and row_diff == direction:
                return target is None

            if col_diff == 0 and row_diff == 2 * direction:

                if piece.has_moved:
                    return False

                middle_row = start_row + direction

                return (
                    target is None
                    and self.board.board[middle_row][start_col] is None
                )

            if abs(col_diff) == 1 and row_diff == direction:
                return target is not None and target.color != piece.color

            return False

        # Knight
        if piece_type == "knight":

            return (
                (abs(row_diff), abs(col_diff)) in 
                [(1, 2), (2, 1)]

            )

        # Bishop
        if piece_type == "bishop":

            if abs(row_diff) != abs(col_diff):
                return False

            return self.clear_path(
                start_row,
                start_col,
                end_row,
                end_col
            )

        # Rook
        if piece_type == "rook":

            if row_diff != 0 and col_diff != 0:
                return False

            return self.clear_path(
                start_row,
                start_col,
                end_row,
                end_col
            )

        # Queen
        if piece_type == "queen":

            straight = row_diff == 0 or col_diff == 0
            diagonal = abs(row_diff) == abs(col_diff)

            if not (straight or diagonal):
                return False

            return self.clear_path(
                start_row,
                start_col,
                end_row,
                end_col
            )

        # King 
        if piece_type == "king":

            return max(abs(row_diff), abs(col_diff)) == 1

        return False

    # -------- پیدا کردن شاه --------- 
    def find_king(self, color):

        for row in range(8):
            for col in range(8):

                piece = self.board.board[row][col]

                if (
                    piece is not None
                    and piece.type == "king"
                    and piece.color == color
                ):
                    return row, col

        return None

    # ---- آیا خانه تحت حمله است؟ ---
    def is_square_legal(self, row, col, by_color):

        for start_row in range(8):
            for start_col in range(8):

                piece = self.board.board[start_row][start_col]

                if piece is None:
                    continue

                if piece.color != by_color:
                    continue

                start = self.index_to_position(start_row, start_col)
                end = self.index_to_position(row, col)

                if self.is_attack_legal(start, end):
                    return True

        return False

    def is_attack_legal(self, start, end):

        start_row, start_col = self.position_to_index(start)
        end_row, end_col = self.position_to_index(end)

        piece = self.board.board[start_row][start_col]

        if piece is None:
            return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if piece.type == "pawn":

            direction = -1 if piece.color == "white" else 1

            return (
                abs(col_diff) == 1
                and row_diff == direction
            )

        if piece.type == "knight":

            return (
                abs(row_diff),
                abs(col_diff)
            ) in [(1, 2), (2, 1)]

        if piece.type == "king":

            return max(abs(row_diff), abs(col_diff)) == 1

        if piece.type == "bishop":

            return (
                abs(row_diff) == abs(col_diff)
                and self.clear_path(
                    start_row,
                    start_col,
                    end_row,
                    end_col
                )
            )

        if piece.type == "rook": 

            return (
                (row_diff == 0 or col_diff == 0)
                and self.clear_path(
                    start_row,
                    start_col,
                    end_row,
                    end_col
                )
            )
        
        if piece.type == "queen":

            straight = row_diff == 0 or col_diff == 0
            diagonal = abs(row_diff) == abs(col_diff)

            return (
                (straight or diagonal)
                and self.clear_path(
                    start_row,
                    start_col,
                    end_row,
                    end_col
                )
            )

        return False

    # --- آیا شاه کیش شده؟ --- 
    def is_in_check(self, color):

        king_position = self.find_king(color)

        if king_position is None:
            return True

        king_row, king_col = king_position

        enemy = "black" if color == "white" else "white"

        return self.is_square_legal(
            king_row,
            king_col,
            enemy
        )

    # --- شبیه سازی حرکت ---
    def simulate_move(self, start, end):

        start_row, start_col = self.position_to_index(start)
        end_row, end_col = self.position_to_index(end)

        piece = self.board.board[start_row][start_col]
        captured = self.board.board[end_row][end_col]

        self.board.board[end_row][end_col] = piece
        self.board.board[start_row][start_col] = None

        return (
            start_row,
            start_col,
            end_row,
            end_col,
            piece,
            captured
        )

    def undo_move(self, data):
        (
            start_row,
            start_col,
            end_row,
            end_col,
            piece,
            captured
        ) = data

        self.board.board[start_row][start_col] = piece
        self.board.board[end_row][end_col] = captured

    # --- حرکت قانونی واقعی --- 
    def is_legal_move(self, start, end):

        piece = self.get_piece(start)

        if piece is None:
            return False

        if piece.color != self.turn:
            return False

        if not self.is_basic_move_legal(start, end):
            return False

        move_data = self.simulate_move(start, end)

        illegal = self.is_in_check(piece.color)

        self.undo_move(move_data)

        return not illegal

    # --- حرکت مهره ---
    def move(self, start, end):

        if self.game_over:
            return False

        if not self.is_legal_move(start, end):
            return False

        start_row, start_col = self.position_to_index(start)
        end_row, end_col = self.position_to_index(end)

        piece = self.board.board[start_row][start_col]

        self.board.board[end_row][end_col] = piece
        self.board.board[start_row][start_col] = None

        piece.has_moved = True

        self.last_move = {
            "start": start,
            "end": end,
            "piece": piece
        }

        self.promote_pawn(end)

        self.change_turn()

        self.check_game_status()

        return True

    # --- ارتقای سرباز ---
    def promote_pawn(self, position):

        row, col = self.position_to_index(position)

        piece = self.board.board[row][col]

        if piece is None or piece.type != "pawn":
            return 

        if (
            piece.color == "white"
            and row == 0
        ) or (
            piece.color == "black"
            and row == 7
        ):

            self.board.board[row][col] = Queen(piece.color)

    # --- تغییر نوبت --- 
    def change_turn(self):

        self.turn = (
            "black"
            if self.turn == "white" 
            else "white"
        )

    # --- آیا بازیکن حرکت قانونی دارد؟ --- 
    def has_legal_moves(self, color):

        old_turn = self.turn
        self.turn = color

        for row in range(8):
            for col in range(8):

                piece = self.board.board[row][col]

                if piece is None:
                    continue

                if piece.color != color:
                    continue

                start = self.index_to_position(row, col)

                for end_row in range(8):
                    for end_col in range(8):

                        end = self.index_to_position(
                            end_row,
                            end_col
                        )

                        if self.is_legal_move(start, end):

                            self.turn = old_turn
                            return True

        self.turn = old_turn

        return False

    # --- کیش، مات یا پات ---
    def check_game_status(self):

        color = self.turn

        if self.has_legal_moves(color):
            return

        if self.is_in_check(color):

            self.game_over = True

            self.winner = (
                "black"
                if color == "white"
                else "white"
            )

        else:
            self.game_over = True
            self.winner = "draw"