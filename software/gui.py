from tkinter import *
import tkinter.messagebox as box
from tkinter.filedialog import *
import fileinput
import random
import copy

from data_processing import *

cell_size = 34 # размер клетки

x0 = 5 # отступ от левого края
y0 = 5 # отступ от вернего края

start_is_painted = False
finish_is_painted = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~Обработка событий~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
            if( (not 3< nr < 12) or (not 3 < nc < 20)):
                box.showinfo("Предупреждение", "Невозможно создать карту заданного размера.\nМинимальный размер 4х4!\nМаксимальный размер 11х19 ")
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
            # возможность добавления преграды сразу после создания сетки
            canv.bind('<Button-1>', click_add_block)    
        except:
            box.showinfo("Ошибка", "Невозможно создать карту. \nУкажите длину и ширину карты целыми арабскими числами!")

# кнопка добавить преграду
def btn_add_block():
    check_track()
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
            if a[row][column].color == "red":
                 finish_is_painted = False    
            a[row][column].color = "blue"
        else:
            a[row][column].color = "white"
        a[row][column].paint()

# кнопка указать начало
def btn_add_start():
    check_track()
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
            if a[row][column].color != "blue" and a[row][column].color != "red":
                start_is_painted = True
            row_before_start = row
            column_before_start = column
        else:
            if( a[row][column].color != "blue" and a[row][column].color != "red" and (row_before_start !=row or column_before_start != column)):
                a[row][column].color = "limegreen"
                a[row][column].paint()
                if(a[row_before_start][column_before_start].color != "blue" and a[row_before_start][column_before_start].color != "red"):
                    a[row_before_start][column_before_start].color = "white"
                    a[row_before_start][column_before_start].paint()
                    row_before_start = row
                    column_before_start = column
            elif a[row][column].color == "limegreen":
                a[row][column].color = "white"
                a[row][column].paint()
                start_is_painted = False   

# кнопка указать конец
def btn_add_finish():
    check_track()
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
            change_color(row, column, "red", "white")
            if a[row][column].color != "blue" and a[row][column].color != "limegreen":
                finish_is_painted = True
            row_before_finish = row
            column_before_finish = column
        else:
            if( a[row][column].color != "blue" and a[row][column].color != "limegreen" and (row_before_finish != row or column_before_finish != column)):
                a[row][column].color = "red"
                a[row][column].paint()
                if(a[row_before_finish][column_before_finish].color != "blue") and a[row_before_finish][column_before_finish].color != "limegreen":
                    a[row_before_finish][column_before_finish].color = "white"
                    a[row_before_finish][column_before_finish].paint()
                    row_before_finish = row
                    column_before_finish = column
            elif a[row][column].color == "red":
                a[row][column].color = "white"
                a[row][column].paint()
                finish_is_painted = False

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
            if a[r][c].color == "red":
                MAP[r][c] = 3
    return MAP

# кнопка сохранить карту
def btn_save_map():
    if check_exist_begin_end():
        MAP = grid_to_array()
        sa = asksaveasfilename()
        file = open(sa + '.botmap', 'w')
        for r in range(nr):
            for c in range(nc):
                file.write(str(MAP[r][c]))
            file.write('\n')
        file.close()
    else:
        box.showinfo("Ошибка", "Невозможно сохранить карту.\nСоздайте карту с точкой отправки и точкой прибытия перед сохранением.")
 
 # кнопка загрузить карту
def btn_load_map():
    global nr, nc
    global MAP
    global start_is_painted; start_is_painted = True
    global finish_is_painted; finish_is_painted = True
    global track_is_painted; track_is_painted = False
    # очистка
    canv.delete("all")
    root.entry_height.delete(0, last = END)
    root.entry_length.delete(0, last = END)   
    # сохраняем карту в матрицу
    MAP = []
    nr = -1
    op = askopenfilename(defaultextension = ".botmap", filetypes= [('BOTMAP arrays', '.botmap')])
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
                a[r][c].color = "red"
                row_before_finish = r
                column_before_finish = c
            a[r][c].paint()

# кнопка проложить путь
def btn_do_track():
    if check_exist_begin_end():
        global track_is_painted; track_is_painted = True
        field = grid_to_array()
        track, exist = wave_algorithm(field, nr, nc)
        if exist:
            for r in range(nr):
                for c in range(nc):
                    if track[r][c] == '@':
                        if a[r][c].color != 'red' and a[r][c].color != 'limegreen':
                            a[r][c].color = 'yellow'
                        a[r][c].paint()
        else:
            box.showinfo("Ошибка", "Невозможно проложить путь. \nПуть полностью ограждён!")
    else:
        box.showinfo("Ошибка", "Невозможно проложить путь. \nУкажите начальную и конечную точку маршрута!")
    canv.bind('<Button-1>', pass_click)

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
                    a[r][c].color = 'white'
                    a[r][c].paint()
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
    # очистка.  
    canv.delete("all")
    root.entry_height.delete(0, last = END)
    root.entry_length.delete(0, last = END)
    # заполнение карты рандомно.  
    exist = False
    global nr, nc;
    nr = random.randint(4,11); nc = random.randint(4,19)
    data = [random.choice((0, 1)) for _ in range(nc*nr)]
    data[:] = [data[i:i + nc] for i in range(0, nc*nr, nc)]
    #points = []#[0 for i in range(4)]
    #print(nr,nc,'\n',data)
    while (not exist):
        data1 = copy.deepcopy(data)
        a = random.randint(0,nr-1)
        b = random.randint(0,nc-1)
        c = random.randint(0,nr-1)
        d = random.randint(0,nc-1)
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

# кнопка старт
def btn_start_moving():
    if check_exist_begin_end():
        global track_is_painted; track_is_painted = True
        # преобразуем нарисованное в матрицу
        field = grid_to_array()
        # ищем координаты старта и финиша
        for i in range(nr):
            for j in range(nc):
                if field[i][j] == 2:
                    start_i = i
                    start_j = j
                if field[i][j] == 3:
                    finish_i = i
                    finish_j = j
                    break
        # составляем команды
        track, exist = wave_algorithm(field, nr, nc)
        if exist:
            commands = list_of_commands(track, nr, nc, start_i, start_j, finish_i, finish_j)
            root.text_status.insert(1.0, array_of_int_to_string(commands))
        else:
            box.showinfo("Ошибка", "Невозможно проложить путь. \nПуть полностью ограждён!")
    else:
        box.showinfo("Ошибка", "Невозможно проложить путь. \nУкажите начальную и конечную точку маршрута!")
    canv.bind('<Button-1>', pass_click)

def array_of_int_to_string(array):
    string = ''
    for i in range(len(array)):
        string += str(array[i]) + ' '
    return string

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~Расположение элементов~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
root = Tk()

root.title("Guide robot")
root.geometry('1000x600')

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
root.btn_start = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12')# command = btn_start_moving)
root.btn_start.place(x = 815, y = 430)

# кнопка назад
root.btn_start = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12')# command = btn_start_moving)
root.btn_start.place(x = 815, y = 465)

# кнопка направо
root.btn_start = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12')# command = btn_start_moving)
root.btn_start.place(x = 864, y = 465)

# кнопка налево
root.btn_start = Button(root, width = 4, height = 1, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12')# command = btn_start_moving)
root.btn_start.place(x = 766, y = 465)

# кнопка старт
root.btn_start = Button(root, text = "Старт", width = 9, height = 2, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12', command = btn_start_moving)
root.btn_start.place(x = 745, y = 520)

# кнопка стоп
root.btn_start = Button(root, text = "Стоп", width = 9, height = 2, bg = 'dodgerblue', fg = 'aliceblue', font = 'arial 12') #command = btn_start_moving)
root.btn_start.place(x = 845, y = 520)

# холст
canv = Canvas(root, width = 650, height = 380,  bd = 0, relief = "ridge")
canv.place(x = 20, y = 190)

# запускаем событийный цикл
root.mainloop()

