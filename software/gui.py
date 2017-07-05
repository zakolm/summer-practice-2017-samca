from tkinter import *
import tkinter.messagebox as box
from tkinter.filedialog import *
import fileinput
from random import *
import random
import copy

from data_processing import *

cell_size = 34 # размер клетки

x0 = 5 # отступ от левого края
y0 = 5 # отступ от вернего края

start_is_painted = False
finish_is_painted = False
track_is_painted = False
a = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~Обработка событий~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# класс Робота 
class Robot():
    # рисование начального состояния
    def __init__(self, r, c, i, j):
        self.r = r # номер сторки 
        self.c = c # номер столбца
        if j == c + 1:
            self.turn_right()
        if i == r - 1:
            self.turn_up()
        if j == c - 1:
            self.turn_left()
        if i == r + 1:
            self.turn_down()
        self.start_orient = self.orient
        self.paint("darkmagenta")

    # движение по нужному направлению
    def moves(self):
        if(bot.orient == "l"):
            self.c -= 1
            canv.move(self.trian, -cell_size, 0)
            self.turn_left()
        elif bot.orient == "r":
            self.c += 1
            canv.move(self.trian,cell_size, 0)
            self.turn_right()
        elif bot.orient == "u":
            self.r -= 1
            canv.move(self.trian, 0, -cell_size)
            self.turn_up()
        else:
            self.r += 1
            canv.move(self.trian, 0, cell_size)
            self.turn_down()
            
    # удаление элемента робот с канваса      
    def delete(self):
        canv.delete(self.trian)

    def turn_left(self):
        self.orient = "l"
        self.x1 = x0 + self.c * cell_size         
        self.y1 = y0 + self.r * cell_size + cell_size / 2
        self.x2 = self.x1 + cell_size 
        self.y2 = self.y1 - cell_size/2
        self.x3 = self.x2
        self.y3 = self.y2 + cell_size     
    
    def turn_right(self):
        self.orient = "r"
        self.y1 = y0 + self.r * cell_size + cell_size / 2
        self.x1 = x0 + self.c * cell_size + cell_size
        self.y2 = y0 + self.r * cell_size
        self.x2 = x0 + self.c * cell_size
        self.x3 = self.x2
        self.y3 = self.y2 + cell_size
        
    def turn_up(self):
        self.orient = "u"
        self.y1 = y0 + self.r  * cell_size
        self.x1 = x0 + self.c * cell_size + cell_size / 2
        self.y2 = self.y1 + cell_size
        self.x2 = self.x1 - cell_size / 2
        self.y3 = self.y2
        self.x3 = self.x2 +cell_size
         
    def turn_down(self):
        self.orient = "d"
        self.y1 = y0 + self.r *cell_size + cell_size
        self.x1 = x0 + self.c * cell_size + cell_size/2
        self.y2 = y0 + self.r *cell_size
        self.x2 = self.x1 - cell_size/2
        self.y3 = self.y2
        self.x3 = self.x2 +  cell_size

    def paint(self, color = 'mediumpurple'):
        self.trian = canv.create_polygon([self.x1, self.y1], [self.x2, self.y2], [self.x3, self.y3], fill = color)


# класс одной клетки
class Cell():
    def __init__(self, r, c): # при создании указываем номер строки и столбца
        self.r = r # номер сторки 
        self.c = c # номер столбца 
        self.color = "white" # базовый цвет 
        self.id = canv.create_rectangle(-100, 0, -100, 0, fill = self.color) # id клетки
        self.paint()
        
    # рисуем клетку на холсте   
    def paint(self):
        # координаты левого верхнего угла
        x1 = x0 + self.c * cell_size         
        y1 = y0 + self.r * cell_size 
        # координаты правого нижнего угла
        x2 = x1 + cell_size  
        y2 = y1 + cell_size
        # настройка
        canv.coords(self.id, x1, y1, x2, y2) # меняем координаты клетки по её id
        canv.itemconfig(self.id, fill = self.color) # меняем свойства

# кнопка создать новую карту
def btn_create_grid():
    global nr, nc, a
    global start_is_painted; start_is_painted = False
    global finish_is_painted; finish_is_painted = False
    global track_is_painted; track_is_painted = False
    # удалим все объекты на холсте
    canv.delete("all")
    # считываем размеры
    length = root.entry_length.get()
    height = root.entry_height.get()
    # исключения
    nr = height
    nc = length
    if(nr == "" or nc == ""):
        box.showinfo("Ошибка", "Невозможно создать карту. \nУкажите длину и ширину карты!")
    else:
        try:
            nr = int(height)
            nc = int(length)
        
            if nr < 4:
                nr = 4
                root.entry_height.delete(0, last = END)
                root.entry_height.insert(0, str(nr))
            elif nr > 11:
                nr = 11
                root.entry_height.delete(0, last = END)
                root.entry_height.insert(0, str(nr))
            if nc < 4:
                nc = 4
                root.entry_length.delete(0, last = END)
                root.entry_length.insert(0, str(nc)) 
            elif nc > 19:
                nc = 19
                root.entry_length.delete(0, last = END)
                root.entry_length.insert(0, str(nc))
                    
            # создаём двумерный массив из объектов класса клетки и рисуем объекты
            a = []
            for r in range(nr): 
                a.append([])
                for c in range(nc):
                    a[r].append(Cell(r, c))
            check_status_buttons()
            # возможность добавления преграды сразу после создания сетки
            canv.bind('<Button-1>', click_add_block)    
        except ValueError:
            box.showinfo("Ошибка", "Невозможно создать карту. \nУкажите длину и ширину карты целыми арабскими числами!")
    
# кнопка добавить преграду
def btn_add_block():
    check_track()
    check_status_buttons()
    canv.bind('<Button-1>', click_add_block)

# обрабока клика для добавления преграды
def click_add_block(event):
    global start_is_painted, finish_is_painted
    x = event.x
    y = event.y
    row, column, click_in_grid = find_col_row(x, y)
    if click_in_grid == 2:       
        if a[row][column].color != "blue":
            if a[row][column].color == "limegreen":
                 start_is_painted = False
            if a[row][column].color == "orangered":
                 finish_is_painted = False    
            a[row][column].color = "blue"
        else:
            a[row][column].color = "white"
        a[row][column].paint()
    check_status_buttons()

# кнопка указать начало
def btn_add_start():
    check_track()
    check_status_buttons()
    canv.bind("<Button-1>", click_add_start)

# обработка клика для указания начала
def click_add_start(event):
    global start_is_painted
    global row_before_start, column_before_start
    x = event.x
    y = event.y
    row, column, click_in_grid = find_col_row(x, y)
    if click_in_grid == 2:
        if not start_is_painted:
            change_color(row, column, "limegreen", "white")
            if a[row][column].color != "blue" and a[row][column].color != "orangered":
                start_is_painted = True
            row_before_start = row
            column_before_start = column
        else:
            if( a[row][column].color != "blue" and a[row][column].color != "orangered" and (row_before_start !=row or column_before_start != column)):
                a[row][column].color = "limegreen"
                a[row][column].paint()
                if(a[row_before_start][column_before_start].color != "blue" and a[row_before_start][column_before_start].color != "orangered"):
                    a[row_before_start][column_before_start].color = "white"
                    a[row_before_start][column_before_start].paint()
                    row_before_start = row
                    column_before_start = column
            elif a[row][column].color == "limegreen":
                a[row][column].color = "white"
                a[row][column].paint()
                start_is_painted = False
    check_status_buttons()

# кнопка указать конец
def btn_add_finish():
    check_track()
    check_status_buttons()
    canv.bind("<Button-1>", click_add_finish)
    
# обработка клика для указания конца
def click_add_finish(event):
    global finish_is_painted
    global row_before_finish, column_before_finish
    x = event.x
    y = event.y
    row, column, click_in_grid = find_col_row(x, y)
    if click_in_grid == 2:
        if not finish_is_painted:
            change_color(row, column, "orangered", "white")
            if a[row][column].color != "blue" and a[row][column].color != "limegreen":
                finish_is_painted = True
            row_before_finish = row
            column_before_finish = column
        else:
            if( a[row][column].color != "blue" and a[row][column].color != "limegreen" and (row_before_finish != row or column_before_finish != column)):
                a[row][column].color = "orangered"
                a[row][column].paint()
                if(a[row_before_finish][column_before_finish].color != "blue") and a[row_before_finish][column_before_finish].color != "limegreen":
                    a[row_before_finish][column_before_finish].color = "white"
                    a[row_before_finish][column_before_finish].paint()
                    row_before_finish = row
                    column_before_finish = column
            elif a[row][column].color == "orangered":
                a[row][column].color = "white"
                a[row][column].paint()
                finish_is_painted = False
    check_status_buttons()

# найти к какому квадрату приналежит клик
def find_col_row(x, y):
    click_in_grid = 0
    for r in range(nr):
        y1 = y0 + r * cell_size 
        y2 = y1 + cell_size
        if(  y1 < y < y2 ): 
            click_in_grid += 1
            break
    for c in range(nc):
        x1 = x0 + c * cell_size 
        x2 = x1 + cell_size
        if( x1 < x < x2):
            click_in_grid += 1
            break
    return r, c, click_in_grid

# поменять цвет клетки
def change_color(row, column, color1, color2):
    if a[row][column].color == color2:
        a[row][column].color = color1
    elif a[row][column].color == color1:
        a[row][column].color = color2
    a[row][column].paint()
    
# преобразовать нарисованную сетку в матрицу
def grid_to_array():
    MAP = [[0] * nc for r in range(nr)]
    for r in range(nr):
        for c in range(nc):
            if a[r][c].color == "blue":
                MAP[r][c] = 1
            if a[r][c].color == "limegreen":
                MAP[r][c] = 2
            if a[r][c].color == "orangered":
                MAP[r][c] = 3
    return MAP

# кнопка сохранить карту
def btn_save_map():
    MAP = grid_to_array()
    sa = asksaveasfilename()
    file = open(sa + '.botmap', 'w')
    for r in range(nr):
        for c in range(nc):
            file.write(str(MAP[r][c]))
        file.write('\n')
    file.close()

 # кнопка загрузить карту
def btn_load_map():
    global nr, nc
    global MAP
    global start_is_painted; start_is_painted = True
    global finish_is_painted; finish_is_painted = True
    global track_is_painted; track_is_painted = False
    global a
    # очистка
    canv.delete("all")
    root.entry_height.delete(0, last = END)
    root.entry_length.delete(0, last = END)   
    # сохраняем карту в матрицу
    MAP = []
    nr = -1
    op = askopenfilename(defaultextension = ".botmap", filetypes= [('BOTMAP arrays', '.botmap')])
    if op:
        
        for line in fileinput.input(op):
            nr += 1
            MAP.append([])
            nc = -1
            for element in line:
                nc += 1
                if element != '\n':
                    MAP[nr].append(int(element))
        nr += 1

        root.entry_height.insert(0, str(nr))
        root.entry_length.insert(0, str(nc))
        # отрисовка карты на сетке
        array_to_grid()
    else:
        start_is_painted = False
        finish_is_painted = False
        a = None
    check_status_buttons()

# преобразование матрицы в сетку
def array_to_grid():
    global a
    global row_before_start, column_before_start
    global row_before_finish, column_before_finish
    a = []
    for r in range(nr): 
        a.append([])
        for c in range(nc):            
            a[r].append(Cell(r, c))    
            if MAP[r][c] == 1:
                a[r][c].color = "blue"
            if MAP[r][c] == 2:
                a[r][c].color = "limegreen"
                row_before_start = r
                column_before_start = c   
            if MAP[r][c] == 3:
                a[r][c].color = "orangered"
                row_before_finish = r
                column_before_finish = c
            a[r][c].paint()

# кнопка проложить путь
def btn_do_track():
    global track_is_painted
    global bot
    check_track()
    field = grid_to_array()
    track, exist = wave_algorithm(field, nr, nc)
    if exist:
        for r in range(nr):
            for c in range(nc):
                if track[r][c] == '@':
                    if a[r][c].color != 'orangered' and a[r][c].color != 'limegreen':
                        a[r][c].color = 'yellow'
                    a[r][c].paint()
        if track_is_painted:
            bot.delete()
        track_is_painted = True
        orient_i,  orient_j = starting_position_of_the_robot(track)
        bot = Robot(row_before_start, column_before_start, orient_i, orient_j)
    else:
        box.showinfo("Ошибка", "Невозможно проложить путь. \nПуть полностью ограждён!")
    check_status_buttons()
    canv.bind('<Button-1>', pass_click)

# координаты направления робота
def starting_position_of_the_robot(track):
    if way_forward(track, nr, nc, row_before_start, column_before_start + 1):
        orient_i = row_before_start
        orient_j = column_before_start + 1
    if way_forward(track, nr, nc, row_before_start - 1, column_before_start):
        orient_i = row_before_start - 1
        orient_j = column_before_start 
    if way_forward(track, nr, nc, row_before_start, column_before_start - 1):
        orient_i = row_before_start
        orient_j = column_before_start - 1
    if way_forward(track, nr, nc, row_before_start + 1, column_before_start):
        orient_i = row_before_start + 1
        orient_j = column_before_start
    return  orient_i,  orient_j
        
# пустой клик, чтобы не допускать редактирование после построения маршрута
def pass_click(event):
    pass

# удалить, если есть маршрут
def check_track():
    global track_is_painted
    if track_is_painted:
        for r in range(nr):
            for c in range(nc):
                if a[r][c].color == 'yellow':
                    a[r][c] = Cell(r, c)
                if a[r][c].color == 'limegreen':
                    a[r][c] = Cell(r, c)
                    a[r][c].color = "limegreen"
                a[r][c].paint()
        bot.delete()
    track_is_painted = False
    
# проверка наличия кoнца и начала
def check_exist_begin_end():
    if start_is_painted and finish_is_painted:
        return True
    return False

# проверка наличия кoнца и начала
def check_click_in_grid(event):
    x = event.x
    y = event.y
    r, c, click_in_grid = find_col_row(x, y)
    if click_in_grid == 2:
        return True
    return False

# проверка активности кнопок
def check_status_buttons():
    if check_exist_begin_end():
        root.btn_track.config(state = NORMAL, bg = "dodgerblue")
        root.btn_save.config(state = NORMAL, bg = "dodgerblue")
    else:
        root.btn_track.config(state = DISABLED, bg = "lavender")
        root.btn_save.config(state = DISABLED, bg = "lavender")
    if a == None:
        root.btn_finish.config(state = DISABLED, bg = "lavender")
        root.btn_border.config(state = DISABLED, bg = "lavender")
        root.btn_start.config(state = DISABLED, bg = "lavender")
    else:
        root.btn_start.config(state = NORMAL, bg = "dodgerblue")
        root.btn_finish.config(state = NORMAL, bg = "dodgerblue")
        root.btn_border.config(state = NORMAL, bg = "dodgerblue")
    if track_is_painted:
        root.btn_go.config(state = NORMAL, bg = "dodgerblue")
        root.btn_stop.config(state = NORMAL, bg = "dodgerblue")
        root.btn_forward.config(state = NORMAL, bg = "dodgerblue")
        root.btn_back.config(state = NORMAL, bg = "dodgerblue")
        root.btn_right.config(state = NORMAL, bg = "dodgerblue")
        root.btn_left.config(state = NORMAL, bg = "dodgerblue")
        if bot.r == row_before_start and bot.c == column_before_start and bot.orient == bot.start_orient:
            root.btn_go.config(state = NORMAL, bg = "dodgerblue")
            root.btn_stop.config(state = NORMAL, bg = "dodgerblue")
        else:
            root.btn_go.config(state = DISABLED, bg = "lavender")
            root.btn_stop.config(state = DISABLED, bg = "lavender")            
    else:
        root.btn_go.config(state = DISABLED, bg = "lavender")
        root.btn_stop.config(state = DISABLED, bg = "lavender")
        root.btn_forward.config(state = DISABLED, bg = "lavender")
        root.btn_back.config(state = DISABLED, bg = "lavender")
        root.btn_right.config(state = DISABLED, bg = "lavender")
        root.btn_left.config(state = DISABLED, bg = "lavender")
    
        
# вывод матрицы
def display(array):
    print()
    for line in array:
        for element in line:
            print('{:<3}'.format (element), end = ' ')
        print()
    print()              

# кнопка сгенерировать карту.  
def  btn_generate_map():
    global row_before_start
    global column_before_start
    global row_before_finish
    global column_before_finish
    global nr, nc
    global MAP
    # очистка.  
    canv.delete("all")
    root.entry_height.delete(0, last = END)
    root.entry_length.delete(0, last = END)
    # заполнение карты рандомно.  
    exist = False
    nr = random.randint(5,11)
    nc = random.randint(5,19)

    # закоментирован долгий цикл
    ''' 
    distance = 1
    MAP = [[0] * nc for r in range(nr)]
    
    row_before_start = 0
    column_before_start = 1     
    row_before_finish = 1
    column_before_finish = 0
   
    while True:
        print(exist, distance)
        if exist and distance > nr * nc / 4:
            break
        
        #MAP[row_before_start][column_before_start] = 0
        #MAP[row_before_finish][column_before_finish] = 0
        distance = 1
        for i in range(nr):
            for j in range(nc):
                MAP[i][j] = randint(0, 1)
        
        row_before_start = randint(0, nr - 1)
        column_before_start = randint(0, nc - 1)
        
        row_before_finish = randint(0, nr - 1)
        column_before_finish = randint(0, nc - 1)
        
        MAP[row_before_start][column_before_start] = 2
        MAP[row_before_finish][column_before_finish] = 3
        display(MAP)
        track, exist = wave_algorithm(MAP, nr, nc)
        
        if exist:
            display(track)
            for i in range(nr):
                for j in range(nc):
                    if track[i][j] == '@':
                        distance += 1
            
    array_to_grid()
    check_status_buttons()
'''                 
    nr = random.randint(5,11)
    nc = random.randint(5,19)
    data = [random.choice((0, 1)) for _ in range(nc*nr)]
    data[:] = [data[i:i + nc] for i in range(0, nc*nr, nc)]
    #points = []#[0 for i in range(4)]
    #print(nr,nc,'\n',data)
    while (not exist):
        data1 = copy.deepcopy(data)
        a = random.randint(0, nr-1)
        b = random.randint(0, nc-1)
        c = random.randint(0, nr-1)
        d = random.randint(0, nc-1)
        if (a != c or b != d):
            data1[a][b] = 2; data1[c][d] = 3
            track, exist = wave_algorithm(data1, nr, nc)
    data[a][b] = 2; data[c][d] = 3
    # Не знаю почему с массивом не работает. Потом еще посмотреть! 
    '''for i in range(4):
            if i%2:
                points.append(random.randint(0,nc-1))
            else:
                points.append(random.randint(0,nr-1))
    if ( points[0] != points[2] or points[1] != points[3] ):
        data1[points[0]][points[1]] = 2; data1[points[2]][points[3]] = 3
        track, exist = algorithm_lee(data1, nr, nc)
    data[points[0]][points[1]] = 2; data[points[2]][points[3]] = 3'''
    
    # Вывод на экран карты.  
    global MAP; MAP = copy.deepcopy(data)
    global start_is_painted; start_is_painted = True
    global finish_is_painted; finish_is_painted = True
    global track_is_painted; track_is_painted = False
    
    array_to_grid()
    check_status_buttons()

# массив целых чисел в строку
def array_of_int_to_string(array):
    string = ''
    for i in range(len(array)):
        string += str(array[i]) + ' '
    return string

# кнопка старт
def btn_start_moving():
    # преобразуем нарисованное в матрицу
    field = grid_to_array()
    # составляем команды
    track, exist = wave_algorithm(field, nr, nc)
    commands = list_of_commands(track, nr, nc, row_before_start, column_before_start, row_before_finish, column_before_finish)
    input_to_status(commands)

    # прокладываем путь по командам
    for h in commands:
        bot.paint()
        if h == 1:
            bot.paint()
            bot.moves()
        # 2 - право для робота
        else:
            bot.delete()
            if h == 2:                             
                if bot.orient == "u":
                    bot.turn_right()
                elif bot.orient == "d":
                    bot.turn_left()
                elif bot.orient == "l":
                    bot.turn_up()
                else:
                    bot.turn_down()
            # 3 - лево для робота
            if h == 3:                            
                if bot.orient == "u":
                    bot.turn_left()
                elif bot.orient == "d":
                    bot.turn_right()
                elif bot.orient == "l":
                    bot.turn_down()
                else:
                    bot.turn_up()
            bot.paint("mediumpurple")
        bot.delete()
    bot.paint("darkmagenta")
    check_status_buttons()
    canv.bind('<Button-1>', pass_click)
    
def input_to_status(commands):
    root.text_status.delete(0.0, END)
    d = 0 
    for h in commands:
        d += 1
        if h == 1:
            root.text_status.insert(END, '{:>3} '.format(str(d))  + chr(708) +" прямо \n")
        elif h == 2:
            root.text_status.insert(END, '{:>3} '.format(str(d)) + chr(707) +" поворот направо\n")
        else:
            root.text_status.insert(END, '{:>3} '.format(str(d)) + chr(706)+ " поворот налево \n")
            
# кнопка стоп
def btn_stop_moving():
    pass

# кнопка вперед
def btn_move_forward():
    bot.delete()
    bot.turn_up()
    bot.moves()
    bot.paint("darkmagenta")
    check_status_buttons()

# кнопка назад(вниз по карте)  
def btn_move_back():
    bot.delete()
    bot.turn_down()
    bot.moves()
    bot.paint("darkmagenta")
    check_status_buttons()

# кнопка вправо
def btn_turn_right():
    bot.delete()
    bot.turn_right()
    bot.moves()
    bot.paint("darkmagenta")
    check_status_buttons()
    
# кнопка влево
def btn_turn_left():
    bot.delete()
    bot.turn_left()
    bot.moves()
    bot.paint("darkmagenta")
    check_status_buttons()
    
# горячая клавиша - выход из программы
def exit_(event):
    root.destroy()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~Расположение элементов~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
root = Tk()

root.title("Guide robot")
root.geometry('1000x600')
root.resizable(width=False, height=False)

# горячая клавиша - выход
root.bind('<Escape>',exit_)

# кнопка проложить путь
root.btn_track = Button(root, text = 'Проложить путь', width = 13, height = 3, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_do_track)
root.btn_track.place(x = 30, y = 20)

# метка высоты
root.lbl_height = Label(root, text = "Высота", font = 'arial 10')
root.lbl_height.place(x = 200, y = 60)

# поле высоты 
root.entry_height = Entry(root, width = 6)
root.entry_height.place(x = 255, y = 63)

# метка длины
root.lbl_length = Label(root, text = "Длина", font = 'arial 10')
root.lbl_length.place(x = 317, y = 60)

# поле длины
root.entry_length = Entry(root,  width = 6)
root.entry_length.place(x = 365, y = 63)

# кнопка создать новую карту
root.btn_new_map = Button(root, text = "Создать новую карту", width = 22, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_create_grid)
root.btn_new_map.place(x = 200, y = 20)

# кнопка указать начало
root.btn_start = Button(root, text = "Указать\n начало", width = 8, height = 2, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 9', command = btn_add_start)
root.btn_start.place(x = 200, y = 90)

# кнопка указать конец
root.btn_finish = Button(root, text = "Указать\n конец", width = 8, height = 2, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 9', command = btn_add_finish)
root.btn_finish.place(x = 270, y = 90)

# кнопка добавить преграду
root.btn_border = Button(root, text = "Добавить\n преграду", width = 8, height = 2, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 9', command = btn_add_block)
root.btn_border.place(x = 340, y = 90)

# кнопка сохранить карту
root.btn_save = Button(root, text = "Сохранить карту", width = 15, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 9', command = btn_save_map)
root.btn_save.place(x = 200, y = 135)

# кнопка загрузить карту
root.btn_take_map = Button(root, text = "Загрузить карту", width = 22, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_load_map)
root.btn_take_map.place(x = 450, y = 20)

# кнопка сгенерировать карту
root.btn_generate = Button(root, text = "Сгенерировать карту", width = 22, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_generate_map)
root.btn_generate.place(x = 450, y = 60)

# метка статус
root.lbl_status = Label(root, text = "Статус", font = 'arial 14')
root.lbl_status.place(x = 800, y = 20)

# поле статуса
root.text_status = Text(root, height = 15, width = 25, font = 'Arial 14', wrap = WORD)
root.text_status.place(x = 700, y = 60)

# кнопка вперёд
root.btn_forward = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_move_forward)
root.btn_forward.place(x = 815, y = 430)

# кнопка назад
root.btn_back = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_move_back)
root.btn_back.place(x = 815, y = 465)

# кнопка направо
root.btn_right = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_turn_right)
root.btn_right.place(x = 864, y = 465)

# кнопка налево
root.btn_left = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_turn_left)
root.btn_left.place(x = 766, y = 465)

# кнопка старт
root.btn_go = Button(root, text = "Старт", width = 9, height = 2, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_start_moving)
root.btn_go.place(x = 745, y = 520)

# кнопка стоп
root.btn_stop = Button(root, text = "Стоп", width = 9, height = 2, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_stop_moving)
root.btn_stop.place(x = 845, y = 520)

# холст
canv = Canvas(root, width = 650, height = 380,  bd = 0, relief = "ridge")
canv.place(x = 20, y = 190)

# начальный статус кнопок
check_status_buttons()

# запускаем событийный цикл
root.mainloop()

