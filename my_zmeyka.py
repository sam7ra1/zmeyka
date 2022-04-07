# Импорт нужных модулей
import pygame
import random
import sqlite3
import datetime

# Инициализация pygame и шрифтов
pygame.init()
pygame.font.init()

#Размеры окна
width, height = 600, 400

# Создается экран с определенными размерами и названием программы
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Zmeyka')

clock = pygame.time.Clock()

# Размер змейки, скорость, цель для уровня 1
snake_size = 10
snake_speed = 20
goal = 100
level = 1

# Вспомогательные переменные
flag = False
username = ''


#Создание класса кнопки
class Button:
    def __init__(self, width, height, function):
        # На вход принимаются ширина, высота и название функции, которую вызывает кнопка
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)
        self.function = function

    def draw(self, x, y, message):
        # Отрисовка кнопки
        mouse = pygame.mouse.get_pos()
        # Получение позиции мышки
        click = pygame.mouse.get_pressed()
        # Проверяет нажатие на кнопку

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            # Отрисовка кнопки в определенной позиции с размерами из функции выше
            # При наведении на кнопку, ее цвет меняется на активный
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                # При нажатии на кнопку задержка 3 секунды
                # Вызывается функция, которую передавали в параметрах класса
                # Затем запускается функция самой игры
                pygame.time.delay(300)
                self.function()
                game()
        else:
            # Отрисовка кнопки, когда на нее не наводят курсор
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        # Текст на кнопке
        text = pygame.font.Font('Rany.otf', 30).render(message, True, (255, 0, 0))
        screen.blit(text, (x + 10, y + 10))


def level1():
    # Функция на кнопки level_1
    pass


def level2():
    # Функция для кнопки level_2
    global snake_size, snake_speed, goal, level
    # Переопределяются параметры размера змеи, ее скорости и цели
    snake_size = 20
    snake_speed = 15
    goal = 70
    level = 2


def setting_username():
    global username
    running = True
    # Фон меню - картинка
    menu_background = pygame.image.load('Lobby.jpg')
    # Изменение размера картинки под размеры окна
    menu_background = pygame.transform.scale(menu_background, (width, height))

    # Изначально ввод с клавиатуры не считывается
    need_input = False
    input_text = ''

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if need_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # При нажатии на Enter сохраняется ник
                    username = input_text
                    # Ввод текста снова не считывается
                    need_input = False
                    input_text = ''
                    lobby()
                elif event.key == pygame.K_BACKSPACE:
                    # Стирается последний символ при нажатии на Backspace
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        # Если длина текста меньше 10, то к нему добавляется символ с клавиатуры
                        input_text += event.unicode
        # Установка фона и определение кнопок
        screen.blit(menu_background, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            # Чтобы активировать ввод текста, нужно нажать на Tab
            need_input = True

        # Создание текста
        text1 = pygame.font.Font(None, 30).render('Нажмите TAB, чтобы ввести username,', True, (0, 128, 255))
        screen.blit(text1, (110, 100))
        text2 = pygame.font.Font(None, 30).render('затем нажмите Enter', True, (0, 128, 255))
        screen.blit(text2, (205, 130))
        text3 = pygame.font.Font(None, 30).render(input_text, True, (255, 255, 255))
        screen.blit(text3, (230, 170))

        pygame.display.update()
        clock.tick(60)


# Создание меню игры
def lobby():
    global username
    running = True
    menu_background = pygame.image.load('Lobby.jpg')
    menu_background = pygame.transform.scale(menu_background, (width, height))
    # Создание кнопок
    level_1 = Button(300, 100, level1)
    level_2 = Button(300, 100, level2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Установка фона и определение кнопок
        screen.blit(menu_background, (0, 0))
        level_1.draw(200, 50, 'First level')
        level_2.draw(200, 200, 'Second level')
        # Обновление экрана
        pygame.display.update()
        clock.tick(60)


#Создание таблицы лидеров
def leaderboard(username, score, level):
    # Подключение к БД
    con = sqlite3.connect("leaderboard.sqlite")
    cur = con.cursor()
    info = cur.execute('SELECT * FROM leaderboard WHERE username=?', (username,))
    # Проверка, есть ли username уже в таблице
    n = info.fetchone()
    if n is None:
        # Если ника в ДБ нет, то создается новая строчка с ником, счетом, уровнем и временем прохождения
        sqlite_insert = """INSERT INTO leaderboard
                        (username, created_date, score, level)
                        VALUES
                        (?, ?, ?, ?);"""
        data_tuple = (username, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), score, level)
        cur.execute(sqlite_insert, data_tuple)
    else:
        # Если username в таблице есть и игрок ставит рекорд, то обновляется счет и уровень
        sql = cur.execute("""SELECT score FROM leaderboard WHERE username = ?""", (username,)).fetchone()
        if score > sql[0]:
            sqlite_update = """UPDATE leaderboard SET score = ?, level = ? WHERE username = ?"""
            cur.execute(sqlite_update, (score, level, username))
    # Сохранение изменений
    con.commit()
    con.close()


# Отрисовка змейки
def the_snake(snake_size, snake_list):
    for x in snake_list:
        # Рисуются прямоугольники, везде, где находится змейка
        pygame.draw.rect(screen, (222, 118, 37), [x[0], x[1], snake_size, snake_size])


# Вывод счета на экран
def score(score):
    value = pygame.font.Font(None, 40).render("Score: " + str(score), True, (0, 255, 0))
    screen.blit(value, (0, 0))


# Вывод сообщения на экран после игры
def message(message, x, y, color):
    msg = pygame.font.Font(None, 30).render(message, True, color)
    screen.blit(msg, (x, y))


# Основная функция, которая создает игру
def game():
    flag = False
    # Вспомогательные переменные, созданные для проверок
    last_key = ''
    game_over = False
    to_close = False
    # Начальные координаты змейки
    x1 = width / 2
    y1 = height / 2
    # Изменение координат относительно x и y
    x1_change = 0
    y1_change = 0
    # Создание списка, где хранится расположение змейки
    snake_list = []
    # Начальная длина
    length = 1
    # Генерация еды для змейки
    boost_x = round(random.randrange(0, width - snake_size) / snake_size) * snake_size
    boost_y = round(random.randrange(0, height - snake_size) / snake_size) * snake_size

    while not game_over:
        # Если змейка игрока врезалась:
        while to_close:
            screen.fill((109, 103, 169))
            # Вывод информации о поражении или победе в зависимости от длины змейки
            if int(length) < goal:
                message("You Lost! Press R to Play Again,", 150, 130, (255, 0, 0))
                message("L to enter lobby or Q to Quit", 150, 150, (255, 0, 0))
            else:
                message("You Won! Press R to Play Again,", 150, 130, (0, 255, 0))
                message("L to enter lobby or Q to Quit", 150, 150, (0, 255, 0))
            score(length - 1)
            # Обновление экрана
            pygame.display.update()

            for event in pygame.event.get():
                # Проверяются действия игрока
                if event.type == pygame.KEYDOWN:
                    # Клавиша q - закрыть окно с игрой
                    if event.key == pygame.K_q:
                        game_over = True
                        to_close = False
                    # Клавиша l - вернуться в лобби
                    if event.key == pygame.K_l:
                        lobby()
                    # Клавиша r - начать новую игру
                    if event.key == pygame.K_r:
                        game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Закрытие игры, если нажать на крестик
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Проверка клавиатуры игрока
                # Проверяется, нажалась ли кнопка вверх
                if event.key == pygame.K_UP and last_key != 'down':
                    # Если текущее положение змейки не противоположно новому, то она меняет направление
                    y1_change = -snake_size
                    x1_change = 0
                    last_key = 'up'
                    # Запоминается направление змейки для проверки выше
                elif event.key == pygame.K_LEFT and last_key != 'right':
                    # Дальше все то же самое
                    x1_change = -snake_size
                    y1_change = 0
                    last_key = 'left'
                elif event.key == pygame.K_RIGHT and last_key != 'left':
                    x1_change = snake_size
                    y1_change = 0
                    last_key = 'right'
                elif event.key == pygame.K_DOWN and last_key != 'up':
                    y1_change = snake_size
                    x1_change = 0
                    last_key = 'down'

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            # Поражение, если змейка достигла границы
            if not flag:
                flag = True
                # Вызов функции leaderboard
                leaderboard(username, length - 1, level)
            to_close = True
        # Текущие координаты змейки
        x1 += x1_change
        y1 += y1_change
        screen.fill((109, 103, 169))
        # Отрисовка еды
        pygame.draw.rect(screen, (0, 255, 0), [boost_x, boost_y, snake_size, snake_size])
        # Координаты частей змейки
        head = [x1, y1]
        snake_list.append(head)
        # Удаление лишних координат части змейки
        if len(snake_list) > length:
            del snake_list[0]

        for x in snake_list[:-1]:
            # Игрок проиграл
            if x == head:
                if not flag:
                    flag = True
                    # Вызов функции leaderboard
                    leaderboard(username, length - 1, level)
                to_close = True
        # Отрисовка змейки и отображение счета
        the_snake(snake_size, snake_list)
        score(length - 1)
        # Обновление экрана
        pygame.display.update()

        if x1 == boost_x and y1 == boost_y:
            # Проверка, подобрала ли змейка буст. Тогда генерируется новый буст и длина змейки увеличивается на 1
            length += 1
            boost_x = round(random.randrange(0, width - snake_size) / snake_size) * snake_size
            boost_y = round(random.randrange(0, height - snake_size) / snake_size) * snake_size
        # Скорость змейки
        clock.tick(snake_speed)
    # Завершение работы
    pygame.quit()
    quit()


# Вызов функции меню, чтобы игра запустилась
setting_username()
