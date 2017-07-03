#~~~~~~~~~~~~~~~~~~~~~~
# ВОЛНОВОЙ АЛГОРИТМ
#~~~~~~~~~~~~~~~~~~~~~~

import time

def algorithm_lee(field, row, column):
    global n; n = row 
    global m; m = column
    global MAP; MAP = field # копирование исходной матрицы

    # Начальный уровень волны
    d = 2
    start = d
    
    # Перерисуем карту 
    for i in range(n):
        for j in range(m):
            if field[i][j] == 1:
                MAP[i][j] = '#'
            if field[i][j] == 3:
                y = i # Координаты
                x = j # выхода
                MAP[i][j] = 0

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~Распространение волны~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    t1 = time.clock()# запуск секундомера
    #display(MAP)
    stop = False # предполагаем, что существует непомеченная клетка
    while MAP[y][x] == 0 and not stop:
        stop = True # предполагаем, что все свободные клетки уже помечены
        for i in range(n):
            for j in range(m):
                if MAP[i][j] == d: # клетка (i,j) помечена числом d
                    # проходим по всем непомеченным клеткам-соседям
                    if free(i, j+1):
                        MAP[i][j+1] = d + 1
                        stop = False
                    
                    if free(i-1, j):
                        MAP[i-1][j] = d + 1
                        stop = False
                        
                    if free(i, j-1):
                        MAP[i][j-1] = d + 1
                        stop = False

                    if free(i+1, j):
                        MAP[i+1][j] = d + 1
                        stop = False
        d += 1
        
    t2 = time.clock() - t1 # остановка секундомера
    
    #display(MAP)
    #print('Время распространения волны = {:5.6f} секунд '. format(t2))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~Восстановление волны~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Строим маршрут
    if MAP[y][x] == 0:
        exist = False
        WAY = None
    else:
        exist = True
        WAY = [['-'] * m for i in range(n)]
        WAY[y][x] = '@'

        t = MAP[y][x] # уровень волны
        while t != start:
            if route(y, x+1, t):
                t = MAP[y][x+1]
                WAY[y][x+1] = '@'
                x += 1
            
            if route(y-1, x, t):
                t = MAP[y-1][x]
                WAY[y-1][x] = '@'
                y -= 1
                
            if route(y, x-1, t):
                t = MAP[y][x - 1]
                WAY[y][x-1] = '@'
                x -= 1

            if route(y+1, x, t):
                t = MAP[y+1][x]
                WAY[y+1][x] = '@'
                y += 1
        #display(WAY)

    return WAY, exist

#------------------------------------------------------------------------------
#-------------------------------------zzzZZZzzz--------------------------------
#------------------------------------------------------------------------------
# Определение свободного пути
def free(i, j):
    if i >= 0 and i <= n - 1 \
    and j >= 0 and j <= m - 1 \
    and MAP[i][j] == 0:
        return True
    return False
    
# Определение движения для обратного маршрута
def route(i, j, t):
    if i >= 0 and i <= n - 1 \
    and j >= 0 and j <= m - 1 \
    and MAP[i][j] == t - 1:
        return True
    return False

# Вывод матрицы
def display(array):
    print()
    for line in array:
        for element in line:
            print('{:<3}'.format (element), end = ' ')
        print()
    print()


