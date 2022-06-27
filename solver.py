import array
import itertools

schema = []

def readSchema():
    global schema
    with open('schema.txt') as file:
        lines = file.readlines()
        blocchi = []
        for i in range(5):
            blocchi.append(lines[9*i+i:9*(i+1)+i])
        schema = [ [ [ int(elem) for elem in row.strip().split(' ') ] for row in block ] for block in blocchi ]

def formatRow(row):
    s = ''
    for i,x in enumerate(row):
        s += f'{x}'
        if i in [2,5]:
            s += ' | '
        else:
            s += ' '
    return s


def printSchema():
    for i, (row1, row2) in enumerate(itertools.chain(zip(schema[0], schema[1]), zip(schema[-1][3:6],schema[-1][3:6]), zip(schema[2],schema[3]))):
        r1 = formatRow(row1)
        r2 = formatRow(row2)
        center = map(str, schema[-1][i-6][3:6]) if i >= 6 and i < 15 else None
        if i<6:
            print(r1 + '|       |' + r2)
        elif i>=6 and i<9:
            print(r1 + '| ' + ' '.join(center) + ' | ' + r2)
        elif i>=9 and i<12:
            print(' '*16 + r1 + ' '*16)
        elif i>=12 and i<15:
            print(r1 + '| ' + ' '.join(center) + ' | ' + r2)
        else:
            print(r1 + '|       |' + r2)

        if i%3==2 and i not in [8,11,20]:
            print('-'*23+'       '+'-'*23)
        if i in [8,11]:
            print(' '*15 + '-'*23)
        

def isValid(n, block, row, col):
    grid = schema[block]

    #recuperato lo schema verifico sia valido internamente

    for i in grid[row]:
        if i == n:
            return False

    for i in [r[col] for r in grid]:
        if i == n:
            return False

    r_offset = (row//3)*3
    c_offset = (col//3)*3
    for i in itertools.chain(*[r[c_offset:c_offset+3] for r in grid[r_offset:r_offset+3]]):
        if i == n:
            return False

    if isSharedPart(block,r_offset,c_offset):
        new_row = row-6 if block in [0,1] else row+6
        new_col = col-6 if block in [0,2] else col+6
        return isValid(n,4,new_row,new_col)

    return True


def isSharedPart(block, r_off, c_off):
    if (block in [0,1] and r_off==6) or (block in [2,3] and r_off==0):
        if (block in [0,2] and c_off==6) or (block in [1,3] and c_off==0):
            return True
    return False

def solve(block, row, col):
    if col == 9:
        row += 1
        if row == 9:
            block += 1
            if block == 5:
                return True
            else:
                row = 0
                col = 0
        else:
            col = 0

    if schema[block][row][col] != 0:
        return solve(block,row,col+1)

    for i in range(1,10):
         if isValid(i, block, row, col):
            schema[block][row][col] = i

            if solve(block,row,col+1):
                return True

            schema[block][row][col] = 0
            
    return False

def main():
    readSchema()
    if solve(0,0,0):
        printSchema()
    else:
        print('There are no solutions!')

if __name__ == '__main__':
    main()
        


    

