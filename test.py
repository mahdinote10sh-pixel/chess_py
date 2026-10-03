from game import Game


game = Game()

print("=== شروع تست شطرنج ===")

# 1. وضعیت اولیه
print("\n1. وضعیت اولیه:")
print("نوبت:", game.turn)
print("e2:", game.get_piece("e2").type)
print("e1:", game.get_piece("e1").type)

# 2. حرکت e2 -> e4
print("\n2. حرکت e2 -> e4:")
result = game.move("e2", "e4")
print("نتیجه:", result)
print("نوبت بعد:", game.turn)

# 3. حرکت e7 -> e5
print("\n3. حرکت e7 -> e5:")
result = game.move("e7", "e5")
print("نتیجه:", result)
print("نوبت بعد:", game.turn)

# 4. حرکت اسب g1 -> f3
print("\n4. حرکت g1 -> f3:")
result = game.move("g1", "f3")
print("نتیجه:", result)
print("نوبت بعد:", game.turn)

# 5. یک حرکت غیرقانونی
print("\n5. تست حرکت غیرقانونی e1 -> e5:")
result = game.move("e1", "e5")
print("نتیجه:", result)

# 6. نمایش وضعیت نهایی چند خانه
print("\n=== وضعیت نهایی ===")

for position in ["e4", "e5", "f3", "g1"]:
    piece = game.get_piece(position)

    if piece:
        print(position, "->", piece.color, piece.type)
    else:
        print(position, "-> خالی")

print("\nبازی تمام شده؟", game.game_over)
print("برنده:", game.winner)

print("\n=== تست تمام شد ===")
