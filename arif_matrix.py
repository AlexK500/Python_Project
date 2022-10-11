# Дан двухмерный массив 5×6. Определить среднее арифметическое
# каждо- го столбца, определить максимум и минимум каждой строки.




def input_matrix():
    print('Введите количество строк в матрице:')
    nstr = int(input().strip())
    # nstr = 2
    print('Введите количество столбцов в матрице:')
    nstb = int(input().strip())
    # nstb = 2
    mas = [[0]*nstr for _ in range(nstr)]
    for i in range(nstr):
        print(f'Введите {i + 1}-ю строку из {nstr} через пробел')
        mas[i] = [int(j) for j in input().strip().split(" ")]
    if len(mas[i]) != nstb:
        print(f'Количество введенных значений {len(mas[i])} отличается от заявленных {nstb}, попробуйте еще раз.')
        input_matrix()
    return mas



def print_matrix(mtrx):
    for i in range(0, len(mtrx)):
        for i2 in range(0, len(mtrx[i])):
            print(mtrx[i][i2], end=' ')
        print(" --> ", f"min = {min(mtrx[i])}", f"max = {max(mtrx[i])}")

def main():
    mas = []
    mas = input_matrix()
    print_matrix(mas)
    sr_arif(mas)


def sr_arif(mas):
    arf = []
    sr = []
    for i in range(0, len(mas[0])):
        for i2 in range(0, len(mas)):
            arf.append(mas[i2][i])
        sr.append({i:sum(arf)/len(mas)})
        arf = []
    for i in range(0, len(mas[0])):
        print(sr[i][i], end=' ')

if __name__=='__main__':
    main()