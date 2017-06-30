'''
'''
import os
def file(name):
    name += '.txt'
    if os.path.exists(name):
        file = open(name, 'r')
        field = []; check_H = []
        count_W = 0

        for line in file:
            row = []; count_H = 0
            for element in line:
                if element != '\n':
                    row.append((int(element)))
                    count_H += 1
            field.append(row)
            check_H.append(count_H)
            count_W += 1
        return True, field, count_W, count_H
    else:
        #print('File does not exist\n')
        #FILE.write('File does not exist\n')
        return False, -1, -1, -1

'''def check_field():
    if len(check_H) == check_H.count(count_H):
        #print("It's okey")
        return True
    else:
        return False'''
