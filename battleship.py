"""
Игра морской бой

Игровое поле 6х6, список кораблей содержится в переменной LIST_SHIP (один 3 палубный, два 2 палубных, четыре 1 палубных).
Игрок играет с ИИ. Сперва корабли расставляет игрок. Если место закончилось, а корабли остались, расстановка запускается заново.
Доска ИИ собирается автоматически. Если место закончилось, а корабли остались, расстановка запускается заново.
*Ситуация с повторной расстановкой кораблей на доске возникает из-за текущих параметров "размер поля" и "список кораблей".
При стандартных параметрах игры такой ситуации не будет.
"""

import re
import random
from time import sleep


# Список кораблей на игровом поле
LIST_SHIP = ["ship3",
             "ship2", "ship2",
             "ship1", "ship1", "ship1", "ship1"]


# Исключение при выборе игроком координат вне игрового поля
class BoardOutException(Exception):
    pass


# Класс цветов консоли
class bcolors:
    ENDC = '\033[0m'  # Обозначение места окончания примения форматирования
    RED = '\033[91m'  # Обозначение ошибок при вводе данных, а также попаданий по кораблям игрока
    GREEN = '\033[92m'  # Веделения важных входных данных
    YELLOW = '\033[93m'  # Выделение промахов
    BlUE = '\033[94m'  # Конец игры
    MAGENTA = '\033[95m'  # Цвет доски ИИ
    MAGENTA_GROUND = '\033[45m'  # Цвет кораблей ИИ
    CYAN = '\033[96m'  # Цвет доски игрока
    CYAN_GROUND = '\033[44m'  # Цвет кораблей игрока
    WHITE = '\033[97m'  # Цвет номеров строк и столбцов
    # {bcolors.CYAN}{....}{bcolors.ENDC}


# Класс корабля. Хранятся: стартовая точка, направлени и длинна
class Ship:

    def __init__(self, start_point, vector, len_ship):
        self.len_ship = len_ship
        self.start_point = start_point
        self.vector = vector
        self.health_ship = len_ship

    # Метод, возвращающий список координат корабля
    def dots(self):
        list_dot = [self.start_point]
        if self.len_ship > 1:
            for i in range(1, self.len_ship):
                if self.vector == "н":
                    list_dot.append((self.start_point[0] + i, self.start_point[1]))
                elif self.vector == "в":
                    list_dot.append((self.start_point[0] - i, self.start_point[1]))
                elif self.vector == "л":
                    list_dot.append((self.start_point[0], self.start_point[1] - i))
                elif self.vector == "п":
                    list_dot.append((self.start_point[0], self.start_point[1] + i))
        return list_dot


# Класс игровой доски
class Board:
    # Список для хранения названия строк и столбцов
    list_symbol_numbers = None
    # Двумерный список для хранения данных о караблях и результатах выстрелов
    matrix_data = None
    # Параметр, который регулирует отображение кораблей на игровой доске (True - показываются, False - скрыты)
    hid = None
    # Множество всех координат игрового поля
    set_dot_matrix = None

    def __init__(self, size, color_ground, hid):
        # Задаётся размер игрового поля
        self.size = size
        # В зависимости от размера игрового поля изменяется количество строк и столбцов
        self.list_symbol_numbers = [i for i in range(self.size)]
        # Создание двумерного списока для хранения данных о караблях и результатах выстрелов
        self.matrix_data = [[f'o' for j in range(self.size)] for i in range(self.size)]
        # Создание множества всех координат игрового поля
        self.set_dot_matrix = set([(i, j) for i in range(6) for j in range(6)])
        # Нужно отображать корабли или нет
        self.hid = hid
        # Цвет игрового поля
        self.color_ground = color_ground

    # Добавление корабля на игровую доску
    def add_ships(self, ship: str, player):
        # Если вызван метод добавления корабля, но на поле нет свободных точек
        if not self.set_dot_matrix:
            return False
        len_ship = int(ship[-1])
        start_point = None
        vector = None
        # Если корабль добавляет Игрок
        if "User" in str(player.__class__):
            start_point = input(f"\nВведите координаты точки, где нужно бросить якорь "
                                f"{bcolors.GREEN}{len_ship}{bcolors.ENDC} палубному кораблю.\n"
                                f"Сперва номер строки, затем номер столбца. Без пробелов.\n"
                                f"Например, {bcolors.GREEN}00{bcolors.ENDC} или {bcolors.GREEN}34{bcolors.ENDC}.\n")
            # Пока нет правильной стартовой координаты
            while not re.search(r'^[0-5][0-5]$', start_point, flags=re.MULTILINE):
                start_point = input(f"{bcolors.RED}Ошибка!{bcolors.ENDC} "
                                    f"Введите номер строки и номер столбца. Без пробелов:\n")
            start_point = tuple(map(int, list(start_point)))
            # Пока стартовая координата не примет допустимое значение
            while start_point not in self.set_dot_matrix:
                start_point = input(f"{bcolors.RED}Ошибка!{bcolors.ENDC} "
                                    f"Рядом раположен другой корабль, повторите ввод.\n")
                # Пока нет правильных координат
                while not re.search(r'^[0-5][0-5]$', start_point, flags=re.MULTILINE):
                    start_point = input(f"{bcolors.RED}Ошибка!{bcolors.ENDC} "
                                        f"Введите номер строки и номер столбца. Без пробелов:\n")
                start_point = tuple(map(int, list(start_point)))
            # Выбор направления расположения корабля
            if len_ship > 1:
                vector = input(f"Как нужно расположить корабль относительно точки сброса якоря?\n"
                               f"(Вверх - {bcolors.GREEN}в{bcolors.ENDC}, "
                               f"Вниз - {bcolors.GREEN}н{bcolors.ENDC}, "
                               f"Влево - {bcolors.GREEN}л{bcolors.ENDC}, "
                               f"Вправо - {bcolors.GREEN}п{bcolors.ENDC})\n")
                # Пока не выбрано допустимое направление корабля
                while not re.search(r'[внлп]', vector):
                    vector = input(f"{bcolors.RED}Ошибка!{bcolors.ENDC} Нет такого направления. Повторите ввод.\n")
                ship = Ship(start_point, vector, len_ship)
                # Пока не выбрано направление в границах игрового поля, не затрагивающее другие корабли и их области
                while not check_ship_points(ship.dots(), self.set_dot_matrix):
                    vector = input(f"{bcolors.RED}Ошибка!{bcolors.ENDC} Корабль выходит за границы игрового поля или "
                                   f"пересекатся с другим кораблём. Повторите ввод.\n")
                    # Пока не выбрано допустимое направление корабля
                    while not re.search(r'[внлп]', vector):
                        vector = input(f"{bcolors.RED}Ошибка!{bcolors.ENDC} Нет такого направления. Повторите ввод.\n")
                    ship = Ship(start_point, vector, len_ship)
            else:
                vector = ""
                ship = Ship(start_point, vector, len_ship)
        # Если корабль добавлеят ИИ
        elif "Mark" in str(player.__class__):
            # Случайные: генерация стартовой координаты, выбор направления корабля
            chars = [i for i in range(6)]
            start_point = (random.choice(chars), random.choice(chars))
            # Пока стартовая координата не примет допустимое значение
            while start_point not in self.set_dot_matrix:
                start_point = (random.choice(chars), random.choice(chars))
            if len_ship > 1:
                vectors = 'внлп'
                vector = random.choice(vectors)
                ship = Ship(start_point, vector, len_ship)
                # Пока не выбрано допустимое направление корабля
                # В зависимости от результатов проверки на выход координат корабля
                # за пределы поля или пересечение с другими кораблями
                while not check_ship_points(ship.dots(), self.set_dot_matrix):
                    vectors.replace(vector, "")
                    vector = random.choice(vectors)
                    ship = Ship(start_point, vector, len_ship)
            else:
                vector = ""
                ship = Ship(start_point, vector, len_ship)
        # Удаление из множества точек поля координат корабля
        for dot_for_set in ship.dots():
            self.set_dot_matrix.discard(dot_for_set)
        # Удаление из множества точек поля координат контура корабля
        for dot_for_set in contour(start_point, vector, len_ship):
            self.set_dot_matrix.discard(dot_for_set)
        return ship, ship.dots()

    # Выстрел по игровой доске
    def shot(self, dot, color):
        if self.matrix_data[dot[0]][dot[1]] == 'o':
            self.matrix_data[dot[0]][dot[1]] = f'T'
            return False
        elif self.matrix_data[dot[0]][dot[1]] == 'T':
            return "Другие координаты"
        else:
            self.matrix_data[dot[0]][dot[1]] = f'{color} X {bcolors.ENDC}'
            return "Попадание"

    # Вывод игрового поля в консоль
    def view_playground(self):
        print()
        print(f"{self.color_ground}{' ' * 4}{'-' * (self.size * 4 + 1)}{bcolors.ENDC}\n"
              f"{self.color_ground}    |{bcolors.ENDC}", end="")
        # Вывод строки с номерами колонок
        for number in self.list_symbol_numbers:
            if number == self.list_symbol_numbers[-1]:
                print(f" {bcolors.WHITE}{self.list_symbol_numbers[number]}{bcolors.ENDC} "
                      f"{self.color_ground}|{bcolors.ENDC}")
            else:
                print(f" {bcolors.WHITE}{self.list_symbol_numbers[number]}{bcolors.ENDC}"
                      f" {self.color_ground}|{bcolors.ENDC}", end="")
        print(f"{self.color_ground}{'-' * (self.size * 4 + 5)}{bcolors.ENDC}")
        # Вывод матицы с данными
        # Для каждой строки
        for id_row, row in enumerate(self.matrix_data):
            print(f"{self.color_ground}|{bcolors.ENDC} {bcolors.WHITE}{self.list_symbol_numbers[id_row]}"
                  f"{bcolors.ENDC} ", end="")
            # Для каждого элемента в строке
            for id_col, col in enumerate(row):
                # Если корабли показывать не нужно, в отображении заменить их на 'o'
                if not self.hid:
                    if col == '\x1b[45m   \x1b[0m':
                        col = 'o'
                # Если первый элемент во всех строках кроме первой
                if id_col == 0:
                    print(f"{self.color_ground}|{bcolors.ENDC}{col: ^3}", end=f"{self.color_ground}|{bcolors.ENDC}")
                # Если последний элемент в любой строке
                elif id_col == self.list_symbol_numbers[-1]:
                    print(f"{col: ^3}{self.color_ground}|{bcolors.ENDC}")
                    print(f"{self.color_ground}{'-' * (self.size * 4 + 5)}{bcolors.ENDC}")
                # Если второй или третий элемент в любой строке
                else:
                    print(f"{col: ^3}", end=f"{self.color_ground}|{bcolors.ENDC}")


# Родительский класс для игроков с методом вывода результата выстрела
class Player:

    def ask(self):
        pass

    # Доска оппонента, координата выстрела, цвет оппонента
    def move(self, board,  dot, colors):
        move_dot = board.shot(dot, colors)
        # Вывод и возврат соответствующих результатов выстрела по доске
        if move_dot == "Попадание":
            if colors == '\x1b[44m':
                colors = bcolors.RED
            else:
                colors = bcolors.GREEN
            print(f'\n{colors}Выстрел по координатам {dot[0]}-{dot[1]}. Попадание!{bcolors.ENDC}\n')
            return "Попадание"
        elif move_dot == "Другие координаты":
            print(f'\n{bcolors.YELLOW}Выстрел по координатам {dot[0]}-{dot[1]} '
                  f'уже производился или\nэто контур потопленного корабля, введите другие координаты.{bcolors.ENDC}\n')
            return "Другие координаты"
        else:
            print(f'\n{bcolors.YELLOW}Выстрел по координатам {dot[0]}-{dot[1]}. Промах!{bcolors.ENDC}\n')
            return "Промах"


# Класс Игрока
class User(Player):

    def __init__(self):
        self.list_ship = LIST_SHIP.copy()
        self.set_dot_ask = set([(i, j) for i in range(6) for j in range(6)])

    # Запрос координат выстрела у игрока
    def ask(self):
        try:
            point = input(f"\nВведите координаты выстрела\n"
                          f"Сперва номер строки, затем номер столбца. Без пробелов.\n")
            if not re.search(r'^[0-5][0-5]$', point, flags=re.MULTILINE):
                raise BoardOutException
            point = tuple(map(int, list(point)))
        except BoardOutException:
            point = input(f"{bcolors.RED}Ошибка!{bcolors.ENDC} Неверные координаты выстрела. Введите их заново\n")
        return point


# Класс ИИ
class Mark1(Player):

    def __init__(self):
        self.list_ship = LIST_SHIP.copy()
        # Множество координат для случайных ходов ИИ
        self.set_dot_ask = set([(i, j) for i in range(6) for j in range(6)])

    def ask(self):
        if self.set_dot_ask:
            chars = [i for i in range(6)]
            # Генерирование случайной координаты
            point = (random.choice(chars), random.choice(chars))
            # Пока не сгенерируется допустимая координата
            while point not in self.set_dot_ask:
                point = (random.choice(chars), random.choice(chars))
            # Убираем сгенерированную координату, чтобы запретить повторный выстрел в неё
            self.set_dot_ask.discard(point)
            return point


# Обводка кунтура кораблей, в пределах которого нельзя размещать другие корабли
def contour(point: tuple, vector: str, size: int):
    list_countour = None
    if size == 1:
        list_countour = [[point[0] + 1, point[1] - 1],
                         [point[0], point[1] - 1],
                         [point[0] - 1, point[1] - 1],
                         [point[0] - 1, point[1]],
                         [point[0] - 1, point[1] + 1],
                         [point[0], point[1] + 1],
                         [point[0] + 1, point[1] + 1],
                         [point[0] + 1, point[1]]]
    else:
        if vector == 'п':
            list_countour = [[point[0] + 1, point[1] - 1],
                             [point[0], point[1] - 1],
                             [point[0] - 1, point[1] - 1],
                             [point[0], point[1] + size]]
            for i in range(size + 1):
                list_countour.append([point[0] - 1, point[1] + i])
                list_countour.append([point[0] + 1, point[1] + i])
        elif vector == 'л':
            list_countour = [[point[0] - 1, point[1] + 1],
                             [point[0], point[1] + 1],
                             [point[0] + 1, point[1] + 1],
                             [point[0], point[1] - size]]
            for i in range(size + 1):
                list_countour.append([point[0] - 1, point[1] - i])
                list_countour.append([point[0] + 1, point[1] - i])
        elif vector == 'в':
            list_countour = [[point[0] + 1, point[1] - 1],
                             [point[0] + 1, point[1]],
                             [point[0] + 1, point[1] + 1],
                             [point[0] - size, point[1]]]
            for i in range(size + 1):
                list_countour.append([point[0] - i, point[1] - 1])
                list_countour.append([point[0] - i, point[1] + 1])
        elif vector == 'н':
            list_countour = [[point[0] - 1, point[1] - 1],
                             [point[0] - 1, point[1]],
                             [point[0] - 1, point[1] + 1],
                             [point[0] + size, point[1]]]
            for i in range(size + 1):
                list_countour.append([point[0] + i, point[1] - 1])
                list_countour.append([point[0] + i, point[1] + 1])
    # Убираются точки, выходящие за пределы игрового поля
    # и преобразование списка координат в множество
    set_countour = check_contour(list_countour)
    return set_countour


# Убираются координаты контура за пределами игрового поля
def check_contour(list_countour: list):
    check_set_countour = set()
    for dot in list_countour:
        if 0 <= dot[0] <= 5 and 0 <= dot[1] <= 5:
            check_set_countour.add(tuple(dot))
    return check_set_countour


# Проверка на наличие выходящих за пределы игрового поля или уже занятых координат
def check_ship_points(ship_dot: list, set_dot_matrix: set):
    list_bad_dot = []
    for dot in ship_dot:
        if (dot[0] < 0 or dot[0] > 5) or (dot[1] < 0 or dot[1] > 5) or dot not in set_dot_matrix:
            list_bad_dot.append(dot)
    if list_bad_dot:
        return False
    return True


# Создание игрового поля игрока и ИИ
def create_playground(players: list):
    # У каждого игрока обновляется список кораблей.
    # Значение "Ship3" (цифра задаёт длинну корабля) заменяется на кортеж:
    # экземпляр класса Ship, координаты корабля
    for id_player, player in enumerate(players):
        for id_ship, ship in enumerate(player[0].list_ship):
            new_ship = player[1].add_ships(ship, player[0])
            # Если расставлены не все корабли, а кординаты на поле закончились, начать расстановку кораблей заново
            if not new_ship:
                if "User" in str(player[0]):
                    print(f"\n{bcolors.RED}Ошибка!{bcolors.ENDC} Некуда поставить корабль. "
                          f"Начните расстановку заново.")
                    user = User()
                    playground_user = Board(6, bcolors.CYAN, True)
                    create_playground([[user, playground_user, bcolors.CYAN_GROUND]])
                # При запуске новой расстановки у ИИ не работает так как надо.
                # При незаконченной расстановке кораблей на поле, после уничтожения всех кораблей игра не заканчивается.
                # Требуется доработка или увеличение размера поля.
                elif "Mark" in str(player[0]):
                    mark1 = Mark1()
                    playground_mark1 = Board(6, bcolors.MAGENTA, False)
                    # playground_mark1 = Board(6, bcolors.MAGENTA, True)
                    create_playground([[mark1, playground_mark1, bcolors.CYAN_GROUND]])
                break
            # Добавление кординат корабля в матрицу данных и вывод поля Игрока с добавленным кораблём
            else:
                player[0].list_ship[id_ship] = new_ship
                for dots in new_ship[1]:
                    player[1].matrix_data[dots[0]][dots[1]] = f"{player[2]}   {bcolors.ENDC}"
                if "User" in str(player[0]):
                    print(f"\n{'Ваше игровое поле': ^29}", end='')
                    player[1].view_playground()


def main():
    # Приветствие и правила игры
    print(f"\n{bcolors.GREEN}Добро пожаловать в игру 'Морской бой'!{bcolors.ENDC}\n\n"
          f"Размер игрового поля - 6 х 6\n"
          f"1 корабль на 3 клетки\n"
          f"2 корабля на 2 клетки\n"
          f"4 корабля на 1 клетку\n"
          f"При попадании игрок делает ещё один выстрел\n\n"
          f"Для победы нужно сбить все корабли раньше оппонента.")

    # Создание классов игроков
    user = User()
    mark1 = Mark1()
    # Создание игровых полей (Размер поля, цвет игрока, нужно ли показывать корабли)
    playground_user = Board(6, bcolors.CYAN, True)
    playground_mark1 = Board(6, bcolors.MAGENTA, False)
    # playground_mark1 = Board(6, bcolors.MAGENTA, True)
    print(f"\n{'Ваше игровое поле': ^29}", end='')
    # Вывод образца игрового поля
    playground_user.view_playground()
    players = [[user, playground_user, bcolors.CYAN_GROUND], [mark1, playground_mark1, bcolors.MAGENTA_GROUND]]
    # Расстановка кораблей на игровых полях
    create_playground(players)
    print(f"\n{'Игровое поле оппонента': ^29}", end='')
    players[1][1].view_playground()
    print(f"\n\n{bcolors.GREEN}{'НАЧАТЬ ИГРУ': ^29}{bcolors.ENDC}\n\n")
    # Создание пустых переменных для дальнейшего стабильного обращения к атрибутам и методам
    # в зависимости от игрока делающего ход
    player_1 = None
    player_2 = None
    while True:
        for player in players:
            if "User" in str(player[0]):
                player_1 = player
                player_2 = players[1]
            elif "Mark" in str(player[0]):
                sleep(1)
                player_1 = player
                player_2 = players[0]
            # Запрашивается координата выстрела
            dot = player_1[0].ask()
            # Проверка на то, куда попал выстрел
            turn = player_1[0].move(player_2[1], dot, player_2[2])
            while turn == "Промах" or turn == "Попадание" or turn == "Другие координаты":
                # Если промах, вывод игровго поля оппонента с результатом выстрела
                # и передача хода другому игроку
                if turn == "Промах":
                    player_1[0].set_dot_ask.discard(dot)
                    if "User" in str(player[0]):
                        print(f"{'Игровое поле оппонента': ^29}", end='')
                    elif "Mark" in str(player[0]):
                        print(f"{'Выше игровое поле': ^29}", end='')
                    player_2[1].view_playground()
                    break
                # Если попадание, вывод игровго поля оппонента с результатом выстрела
                # и запрос координат для нового выстрела
                elif turn == "Попадание":
                    # Удаление координат выстрела из множества координат игрового поля и из координат корабля
                    player_1[0].set_dot_ask.discard(dot)
                    for id_ship, ship in enumerate(player_2[0].list_ship):
                        for id_point_ship, point_ship in enumerate(ship[1]):
                            if dot == point_ship:
                                ship[1].pop(id_point_ship)
                                # Если в корабле не осталось координат, занчит он потоплен.
                                # Удаление корабля из списка кораблей игрока.
                                # Обвод контура вокруг уничтоженного корабля
                                if not ship[1]:
                                    player_2[0].list_ship.pop(id_ship)
                                    for dot_dead_ship in contour(ship[0].start_point, ship[0].vector, ship[0].len_ship):
                                        player_2[1].matrix_data[dot_dead_ship[0]][dot_dead_ship[1]] = 'T'
                                        if "Mark" in str(player_1[0]):
                                            player_1[0].set_dot_ask.discard(dot_dead_ship)
                                    if player_1[2] == '\x1b[45m':
                                        colors = bcolors.RED
                                    else:
                                        colors = bcolors.GREEN
                                    print(f"{colors}Корабль потоплен!{bcolors.ENDC}\n")
                                break
                    # Если список кораблей у оппонента пустой, то победил игрок делающий ход.
                    # Завершение игры
                    if not player_2[0].list_ship:
                        if "User" in str(player[0]):
                            print(f'{bcolors.BlUE}\n\n{"ИГРА ОКОНЧЕНА!": ^29}\n{"ВЫ ПОБЕДИЛИ!": ^29}\n{bcolors.ENDC}')

                        elif "Mark" in str(player[0]):
                            print(f"{'Игровое поле оппонента': ^29}", end='')
                            player_1[1].hid = True
                            player_1[1].view_playground()
                            print(f'{bcolors.BlUE}\n\n{"ИГРА ОКОНЧЕНА!": ^29}\n{"ПОБЕДИЛ Mark1!": ^29}\n{bcolors.ENDC}')
                        break
                    # Вывод игрового поля после выстрела и новый выстрел того же игрока
                    if "User" in str(player[0]):
                        print(f"{'Игровое поле оппонента': ^29}", end='')
                    elif "Mark" in str(player[0]):
                        sleep(1)
                        print(f"{'Выше игровое поле': ^29}", end='')
                    player_2[1].view_playground()
                    dot = player_1[0].ask()
                    turn = player_1[0].move(player_2[1], dot, player_2[2])
                # Если выбраны координаты с кораблём или промахом, запрос новых координат
                elif turn == "Другие координаты":
                    dot = player_1[0].ask()
                    turn = player_1[0].move(player_2[1], dot, player_2[2])
            # Завершение игры
            if not player_2[0].list_ship:
                break
        # Завершение игры
        if not player_2[0].list_ship:
            break


if __name__ == "__main__":
    main()
