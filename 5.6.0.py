matrix = [[' ', 0, 1, 2],
          [0, '-', '-', '-'],
          [1, '-', '-', '-'],
          [2, '-', '-', '-']
          ]

stop = 0


# Функция для вывода стартового поля и поля с последующими изменениями
def M(matrix):
    for i in matrix:
        for j in i:
            print(j, end=' ')
        print()


# Функция для определения условий победы одного из игроков
# Каждый вариант победы уникален, поэтому не смог придумать как сократить код
def vin(matrix):
    if matrix[1][1] == matrix[1][2] == matrix[1][3]:
        if matrix[1][1] == "X":
            return f'Победил {player1}!'
        elif matrix[1][1] == 0:
            return f'Победил {player2}!'
    elif matrix[2][1] == matrix[2][2] == matrix[2][3]:
        if matrix[2][1] == "X":
            return f'Победил {player1}!'
        elif matrix[2][1] == 0:
            return f'Победил {player2}!'
    elif matrix[3][1] == matrix[3][2] == matrix[3][3]:
        if matrix[3][1] == "X":
            return f'Победил {player1}!'
        elif matrix[3][1] == 0:
            return f'Победил {player2}!'
    elif matrix[1][1] == matrix[2][1] == matrix[3][1]:
        if matrix[1][1] == "X":
            return f'Победил {player1}!'
        elif matrix[1][1] == 0:
            return f'Победил {player2}!'
    elif matrix[1][2] == matrix[2][2] == matrix[3][2]:
        if matrix[1][2] == "X":
            return f'Победил {player1}!'
        elif matrix[1][2] == 0:
            return f'Победил {player2}!'
    elif matrix[1][3] == matrix[2][3] == matrix[3][3]:
        if matrix[1][3] == "X":
            return f'Победил {player1}!'
        elif matrix[1][3] == 0:
            return f'Победил {player2}!'
    elif matrix[1][1] == matrix[2][2] == matrix[3][3]:
        if matrix[1][1] == "X":
            return f'Победил {player1}!'
        elif matrix[1][1] == 0:
            return f'Победил {player2}!'
    elif matrix[1][3] == matrix[2][2] == matrix[3][1]:
        if matrix[1][3] == "X":
            return f'Победил {player1}!'
        elif matrix[1][3] == 0:
            return f'Победил {player2}!'


print("Добро пожаловать в игру 'Крестики-нолики'!")
print()

print("Правила игры:")
print("1.Первый, выстроивший в ряд 3 своих символа по вертикали, горизонтали или "
      "\nбольшой диагонали, выигрывает.")
print("2.Если игроки заполнили все 9 ячеек и оказалось, что ни в одной вертикали,",
      "\nгоризонтали или большой диагонали нет трёх одинаковых знаков - ничья.")
print("3.Первый ход делает игрок, ставящий крестики.")
print()

player1 = input("Игрок 1, введите ваше имя: ")
print("Ваш символ - X")
print()

player2 = input("Игрок 2, введите ваше имя: ")
print("Ваш символ - 0")
print()

print("Ваше игровое поле")
M(matrix)

while True:
    index_1 = list(input(f"{player1}, введите номер ячейки для символа в формате строка-пробел-столбец: "))
# Попробовал реализовать повторный запрос при вызове индекса за пределами списка,
# но нормально не заработало. Подскажите в чём здесь ошибка.
#    if (int(index_1[0])) > 2 or (int(index_1[2])) > 2:
#        print()
#        print("Номер ячейки введён некорректно, повторите ввод.")
#        print()
#        continue
    matrix[int(index_1[0]) + 1][int(index_1[2]) + 1] = "X"
    M(matrix)
    if vin(matrix):
        print()
        print(*vin(matrix))
        break
    stop += 1
    if stop == 9:
        print()
        print("Увы, ничья.")
        break
    index_2 = list(input(f"{player2}, введите номер ячейки для символа в формате строка-пробел-столбец: "))
#    if (int(index_1[0])) > 2 or (int(index_1[2])) > 2:
#        print()
#        print("Номер ячейки введён некорректно, повторите ввод.")
#        print()
#        continue
    matrix[int(index_2[0]) + 1][int(index_2[2]) + 1] = 0
    M(matrix)
    if vin(matrix):
        print()
        print(*vin(matrix))
        break
    stop += 1
    if stop == 9:
        print()
        print("Увы, ничья.")
        break
