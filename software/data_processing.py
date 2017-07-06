
#--------------------------------------------------------------------------
#---------------------------------Волновой алгоритм------------------------
#--------------------------------------------------------------------------
def wave_algorithm(field, nr, nc):
    # начальный уровень волны
    wave = 2
    start = wave
    # перерисуем карту 
    for i in range(nr):
        for j in range(nc):
            if field[i][j] == 1:
                field[i][j] = '#'
            if field[i][j] == 3:
                y = i # координаты
                x = j # выхода
                field[i][j] = 0

    # ~~~~~~~~~~~~~~~~Распространение волны~~~~~~~~~~
    
    stop = False # предполагаем, что существует непомеченная клетка
    while field[y][x] == 0 and not stop:
        stop = True # предполагаем, что все свободные клетки уже помечены
        for i in range(nr):
            for j in range(nc):
                if field[i][j] == wave: # клетка (i,j) помечена числом wave
                    # проходим по всем непомеченным клеткам-соседям
                    if free(field, nr, nc, i, j+1):
                        field[i][j+1] = wave + 1
                        stop = False
                    
                    if free(field, nr, nc, i-1, j):
                        field[i-1][j] = wave + 1
                        stop = False
                        
                    if free(field, nr, nc, i, j-1):
                        field[i][j-1] = wave + 1
                        stop = False

                    if free(field, nr, nc, i+1, j):
                        field[i+1][j] = wave + 1
                        stop = False
        wave += 1
        
    # ~~~~~~~~~~~~~~~~Восстановление волны~~~~~~~~~~
    
    if field[y][x] == 0:
        exist = False
        track = None
    else:
        exist = True
        track = [['-'] * nc for i in range(nr)]
        track[y][x] = '@'
        
        # пока текущий уровень волны не станет равным начальному
        # учитывается минимальное количество поворотов
        while wave != start:
            # движение вправо
            if way_back(field, nr, nc, y, x+1, wave):
                while way_back(field, nr, nc, y, x+1, wave):
                    wave = field[y][x+1]
                    track[y][x+1] = '@'
                    x += 1
            # движение вверх     
            if way_back(field, nr, nc, y-1, x, wave):
                while way_back(field, nr, nc, y-1, x, wave):
                    wave = field[y-1][x]
                    track[y-1][x] = '@'
                    y -= 1 
            # движение влево     
            if way_back(field, nr, nc, y, x-1, wave):
                while way_back(field, nr, nc, y, x-1, wave):
                    wave = field[y][x - 1]
                    track[y][x-1] = '@'
                    x -= 1         
            # движение вниз
            if way_back(field, nr, nc, y+1, x, wave):
                while way_back(field, nr, nc, y+1, x, wave):
                    wave = field[y+1][x]
                    track[y+1][x] = '@'
                    y += 1
                    
    return track, exist

# определение свободного пути
def free(field, nr, nc, i, j):
    if i >= 0 and i <= nr - 1 \
    and j >= 0 and j <= nc - 1 \
    and field[i][j] == 0:
        return True
    return False
    
# определение обратного движения по волне
def way_back(field, nr, nc, i, j, wave):
    if i >= 0 and i <= nr - 1 \
    and j >= 0 and j <= nc - 1 \
    and field[i][j] == wave - 1:
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

#------------------------------------------------------------------------------
#-------------------------------------Создание команд--------------------------
#------------------------------------------------------------------------------
    
def list_of_commands(track, nr, nc, start_i, start_j, finish_i, finish_j):
    commands = []
    i = start_i
    j = start_j
    
    # пока не достигнем финиша
    track[i][j]= '-'
    while i != finish_i or j != finish_j:
        # движение вправо
        if way_forward(track, nr, nc, i, j + 1): 
            while way_forward(track, nr, nc, i, j + 1):
                commands.append(1)
                track[i][j + 1] = '-'
                j += 1
            if way_forward(track, nr, nc, i + 1, j):
                commands.append(2)
            if way_forward(track, nr, nc, i - 1, j):
                commands.append(3)
        # движение вверх     
        if way_forward(track, nr, nc, i - 1, j):
            while way_forward(track, nr, nc, i - 1, j):
                commands.append(1)
                track[i - 1][j] = '-'
                i -= 1
            if way_forward(track, nr, nc, i, j + 1):
                commands.append(2)
            if way_forward(track, nr, nc, i, j - 1):
                commands.append(3)
        # движение влево     
        if way_forward(track, nr, nc, i, j - 1):
            while way_forward(track, nr, nc, i, j - 1):
                commands.append(1)
                track[i][j - 1] = '-'
                j -= 1
            if way_forward(track, nr, nc, i - 1 , j):
                commands.append(2)
            if way_forward(track, nr, nc, i + 1, j):
                commands.append(3)
        # движение вниз
        if way_forward(track, nr, nc, i + 1, j):
            while way_forward(track, nr, nc, i + 1, j):
                commands.append(1)
                track[i + 1][j] = '-'
                i += 1
            if way_forward(track, nr, nc, i, j - 1):
                commands.append(2)
            if way_forward(track, nr, nc, i, j + 1):
                commands.append(3)
                
    return commands

# определение направления движения
def way_forward(field, nr, nc, i, j):
    if i >= 0 and i <= nr - 1 \
    and j >= 0 and j <= nc - 1 \
    and field[i][j] == '@':
        return True
    return False



