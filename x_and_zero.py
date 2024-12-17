"""
Игра крестики-нолики
"""

import re
import random

# Переменные для цветного вывода в консоль
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[31m'
CYAN = '\033[96m'
ENDC = '\033[0m'

# Счётчик ходов
count_turns = 0

# Игровое поле
matrix = [['', 0, 1, 2],
          [0, '', '', ''],
          [1, '', '', ''],
          [2, '', '', '']]


# Функция для отображения игрового поля
def playground():
    print()
    # Для каждой строки
    for id_row, row in enumerate(matrix):
        # Для каждого элемента в строке
        for id_col, col in enumerate(row):
            # Если первый элемент в первой строе
            if id_col == 0 and id_row == 0:
                print(f"{CYAN}{'-' * 13: >17}{ENDC}")
                print(f"   ", end=f"{CYAN} | {ENDC}")
            # Если первый элемент во всех строках кроме первой
            elif id_col == 0:
                print(f"{CYAN}|{ENDC} {col: ^1}", end=f"{CYAN} | {ENDC}")
            # Если последний элемент в любой строке
            elif id_col == 3:
                print(f"{col: ^1} {CYAN}|{ENDC}")
                print(f"{CYAN}{'-' * 17}{ENDC}")
            # Если второй или третий элемент в любой строке
            else:
                print(f"{col: ^1}", end=f"{CYAN} | {ENDC}")


# Функция проверки победных комбинаций
def win_check(matrix: list, point):
    if any([matrix[1][1] == matrix[2][2] == matrix[3][3] == point,
            matrix[1][3] == matrix[2][2] == matrix[3][1] == point,
            matrix[1][1] == matrix[1][2] == matrix[1][3] == point,
            matrix[2][1] == matrix[2][2] == matrix[2][3] == point,
            matrix[3][1] == matrix[3][2] == matrix[3][3] == point,
            matrix[1][1] == matrix[2][1] == matrix[3][1] == point,
            matrix[1][2] == matrix[2][2] == matrix[3][2] == point,
            matrix[1][3] == matrix[2][3] == matrix[3][3] == point]):
        return "Победа"


# Функция хода игроков
def turns(names: dict):
    global count_turns
    # Холит первый игрок, затем второй
    for name, point in names.items():
        choice = input(f"Ход игрока: {name}\nВведите номер ячейки: ")
        # Проверка на слово "Стоп"
        choice = stop_check(choice)
        if choice == "стоп":
            return f"Игра окончена, ничья!"
        # Проверка на корректность вводимых данных
        choice = turns_check(choice)
        if choice == "стоп":
            return f"Игра окончена, ничья!"
        # Если в ячейке пусто, ставим "Х" или "0" (в зависимости от игрока)
        elif not matrix[choice[0] + 1][choice[1] + 1]:
            matrix[choice[0] + 1][choice[1] + 1] = point
        # Если в ячейке уже есть значение, запрос новых координат
        else:
            choice = input(f"В ячейке уже есть значение, повторите ввод: ")
            # Проверка на слово "Стоп"
            choice = stop_check(choice)
            if choice == "стоп":
                return f"Игра окончена, ничья!"
            # Проверка воодимых данных на корректность
            choice = turns_check(choice)
            # Ставим "Х" или "0" (в зависимости от игрока)
            matrix[choice[0] + 1][choice[1] + 1] = point
        # Вывод игрового поля с изменениями
        playground()
        # Наращивание счётчика ходов
        count_turns += 1
        # Проверка на победную комбинацию
        if win_check(matrix, point) == "Победа":
            return f"Игра окончена, победил {name}!"
        # Проверка на заполненность игрового поля
        elif count_turns == 9:
            return f"Игра окончена, ничья!"
        # Подсказка о возможнеости закончить игру
        print("Если вы хотите закончить игру, введите 'Стоп'\n")
    return "Продолжаем"


# Функция проверки воодимых данных на корректность
def turns_check(choice: str):
    # Убираем все пробелы
    choice = re.sub(r"\s", r"", choice)
    # Пока не получим комбинацию из двух цифр от 0 до 2
    while not re.search(r'[0-2][0-2]', choice):
        choice = input(f"Неверный формат номера ячейки, повторите ввод: ")
        # Проверка на слово "Стоп"
        choice = stop_check(choice)
        if choice == "стоп":
            break
    if choice == "стоп":
        return choice
    else:
        # Когда получили нужную комбинацию, преобразуем её в список из двух цифр
        return list(map(int, list(choice)))


# Функция проверки на слово "Стоп"
def stop_check(choice: str):
    # Убираем все пробелы
    choice = re.sub(r"\s", r"", choice)
    # Преобразование к нижнему регистру
    choice = choice.lower()
    if choice == "стоп":
        return f"стоп"
    return choice


# Функция логики игры
def main():
    # Приветствие и правила игры
    print(f"\n{GREEN}Добро пожаловать в игру 'Крестики-нолики'!{ENDC}\n\n"
          f"Для победы нужно расположить три одинаковых символа:\n"
          f"1) в ряд по горизонтали\n"
          f"2) в ряд по вертикали\n"
          f"3) по любой диагонали\n"
          f"Если ходы закончились, но ни одно из условий победы не достигнуто - ничья.\n")

    # Запрос имён игроков
    name1 = input("Введите имя первого игрока: ")
    while not name1:
        name1 = input("Ошибка ввода, введите заново имя первого игрока: ")
    name2 = input("Введите имя второго игрока: ")
    while not name2:
        name2 = input("Ошибка ввода, введите заново имя второго игрока: ")

    names = [name1, name2]
    # Перемешивание списка имён, для случайного выбора игрока, делающего первый ход
    random.shuffle(names)
    # Присваивание каждому имени цвета и символа
    names = {f"{RED}{names[0]}{ENDC}": f"{RED}X{ENDC}",
             f"{YELLOW}{names[1]}{ENDC}": f"{YELLOW}0{ENDC}"}
    for name, point in names.items():
        print(f"{name} ваш символ - {point}")

    # Вывод игрового поля
    print(f"\n{'Ваше игровое поле': ^17}", end='')
    playground()
    print(f"{GREEN}Для выбора ячейки введите номер строки и номер столбца.\n"
          f"Например, '0 2' или '11'\n{ENDC}")

    while True:
        # Запуск ходов игроков
        result = turns(names)
        if "победил" in result:
            print(result)
            break
        elif "ничья" in result:
            print(result)
            break


# Запуск игры
if __name__ == "__main__":
    main()
