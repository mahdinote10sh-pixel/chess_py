class King:
    def __init__(self, color):
        self.type = "king"
        self.color = color 
        self.has_moved = False

white_king = King("white")
black_king = King("black")

class Queen:
    def __init__(self, color):
        self.type = "queen"
        self.color = color 
        self.has_moved = False

white_queen = Queen("white")
black_queen = Queen("black")

class Rook:
    def __init__(self, color):
        self.type = "rook"
        self.color = color
        self.has_moved = False

white_rooks = [Rook("white") for _ in range(2)]
black_rooks = [Rook("black") for _ in range(2)]

class Knight:
    def __init__(self, color):
        self.type = "knight"
        self.color = color
        self.has_moved = False

white_knights = [Knight("white") for _ in range(2)]
black_knights = [Knight("black") for _ in range(2)]
        
class Bishop:
    def __init__(self, color):
        self.type = "bishop"
        self.color = color
        self.has_moved = False

white_bishops = [Bishop("white") for _ in range(2)]
black_bishops = [Bishop("black") for _ in range(2)]

class Pawn:
    def __init__(self, color):
        self.type = "pawn"
        self.color = color
        self.has_moved = False

white_pawns = [Pawn("white") for _ in range(8)]
black_pawns = [Pawn("black") for _ in range(8)]

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)] 

        self.setup_board()

    def setup_board(self):

        #white
        self.board[7][0] = Rook("white")        
        self.board[7][1] = Knight("white")            
        self.board[7][2] = Bishop("white")            
        self.board[7][3] = Queen("white")   
        self.board[7][4] = King("white")  
        self.board[7][5] = Bishop("white")    
        self.board[7][6] = Knight("white")
        self.board[7][7] = Rook("white")

        for col in range(8):
            self.board[6][col] = Pawn("white")

        #black
        self.board[0][0] = Rook("black")
        self.board[0][1] = Knight("black")   
        self.board[0][2] = Bishop("black") 
        self.board[0][3] = Queen("black")
        self.board[0][4] = King("black")
        self.board[0][5] = Bishop("black")
        self.board[0][6] = Knight("black")
        self.board[0][7] = Rook("black")

        for col in range(8):
            self.board[1][col] = Pawn("black")

    def get_square(self, position):
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])

        return self.board[row][col]

board = Board()


# for row in range(8):
    # for col in range(8):
        # print(col+1, ". ", board.board[row][col])

for row in range(8, 0, -1):
    for col in range(8):
        position = chr(ord('a')+col) + str(row)
        print(position, ":", board.get_square(position))
