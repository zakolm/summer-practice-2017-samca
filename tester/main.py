from program_input import *
from algorithm_lee import *

#if check_field:
#number_menu = -1
#while (number_menu > 2 or number_menu < 0):
#    print('0- Выход.\n'+
#          '1- Создать файл.\n'+
#          '2- Выбрать файл.')
#    number_menu = int(input('>>>'))
#print(number_menu)
#if number_menu == 2:
rc, field_robot, count_W, count_H = file('file')#input('Введите название файла: '))
#print(field_robot)
if rc:
    algorithm_lee(field_robot, count_W, count_H)
#print(field)
else:
    file = open('f_out.txt', 'w')
    file.write('Incorrect input data')
    #print('Incorrect input data')
