from ..edgework import edgework

class chess(edgework):
    __table = [[0 for a in range(6)] for b in range(6)]

    def __check(self, c):
        if not isinstance(c, list): raise TypeError("coords must be in list")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Elements of coords must be in str")
        elif len(c) != 6: raise IndexError("Length of coords must be 6")
        c = [a.replace("-","") for a in c]
        if not all([a[0].lower() in ['a','b','c','d','e','f'] and int(a[1]) in range(1,7) for a in c]): raise ValueError("Column of coords must be A-F and Row of coords must be 1-6 only")
        arr = []
        for a in c:
           temp = {'col': None, 'row': None}
           temp['col'] = int(ord(a[0].upper())-65); temp['row'] = int(a[1])-1
           arr.append(temp)
        return arr
    
    def __init__(self, edgework:edgework, coords:list):
        '''
        Initialize a new chess instance

        Args:
            edgework (edgework): The edgework of the bomb
            coords (list [str,...]): The coordinates of chess in list. Index 0 represents position 1. Coordinates should be in one string, remove all dashes. ('c-1' becomes 'c1')
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__coords = self.__check(coords)
        self.__piece = [0,0,0,0,0,0]

    def __moves(self, table, row, col, piece):
        if piece=='r':
            possible_rows = [a for a in range(1,6) if row+a in range(len(table))]; [possible_rows.append(-1*a) for a in range(1,6) if row-a in range(len(table))]
            possible_cols = [a for a in range(1,6) if col+a in range(len(table[0]))]; [possible_cols.append(-1*a) for a in range(1,6) if col-a in range(len(table))]
            for a in set(possible_rows):
                table[row+a][col] = 1 if table[row+a][col]==0 else table[row+a][col]
                if isinstance(table[row+a][col], str): break
            for a in set(possible_cols):
                table[row][col+a] = 1 if table[row][col+a]==0 else table[row][col+a]
                if isinstance(table[row][col+a], str): break
        elif piece=='b':
            possible_rows = [[a for a in range(1,6) if row+a in range(len(table))],[-1*a for a in range(1,6) if row-a in range(len(table))]]
            possible_cols = [[a for a in range(1,6) if col+a in range(len(table[0]))],[-1*a for a in range(1,6) if col-a in range(len(table[0]))]]
            for i in range(2):
                for x in range(2):
                    for y in range(min([len(possible_rows[i]),len(possible_cols[x])])):
                        a = possible_rows[i][y]; b = possible_cols[x][y]
                        table[row+a][col+b] = 1 if table[row+a][col+b]==0 else table[row+a][col+b]
                        if isinstance(table[row+a][col+b], str): break
        elif piece=='k':
            possible_rows = [a for a in range(0,2) if row+a in range(len(table))]; [possible_rows.append(-1*a) for a in range(0,2) if row-a in range(len(table))]
            possible_cols = [a for a in range(0,2) if col+a in range(len(table[0]))]; [possible_cols.append(-1*a) for a in range(0,2) if col-a in range(len(table[0]))]
            for a in set(possible_rows):
                for b in set(possible_cols):
                    table[row+a][col+b] = 1 if table[row+a][col+b]==0 else table[row+a][col+b]
                    if isinstance(table[row+a][col+b], str) and (a!=0 and b!=0): break
        elif piece=='n':
            possible_rows = [a for a in [2,1,-1,-2] if row+a in range(len(table))]; possible_cols = [[a for a in [2,-2] if col+a in range(len(table[0]))], [a for a in [1,-1] if col+a in range(len(table[0]))]]
            for a in set(possible_rows):
                for b in set(possible_cols[abs(a)-1]):
                    table[row+a][col+b] = 1 if table[row+a][col+b]==0 else table[row+a][col+b]
        elif piece=='q':
            table = self.__moves(table, row, col, 'r')
            table = self.__moves(table, row, col, 'b')
        return table

    def __calculate(self):
        self.__piece[3] = 'r'
        self.__piece[4] = 'q' if (self.__coords[4]['col']+self.__coords[4]['row'])%2==1 else 'r'
        self.__piece[0] = 'k' if self.__piece[4] == 'q' else 'b'
        self.__piece[1] = 'r' if int(self._sndigit[-1])%2==1 else 'n'
        self.__piece[2] = 'q' if self.__piece.count('r')<2 else 'k'
        self.__piece[5] = 'q' if self.__piece.count('q')==0 else 'n' if self.__piece.count('n')==0 else 'b'

        for a in range(len(self.__piece)): self.__table[self.__coords[a]['row']][self.__coords[a]['col']] = self.__piece[a]
        for a in range(len(self.__piece)):
            self.__table = self.__moves(self.__table, self.__coords[a]['row'], self.__coords[a]['col'], self.__piece[a])
        for a in self.__table:
            if 0 in a: return self.__table.index(a), a.index(0)
    
    def solve(self):
        '''
        Solve the Chess module

        Returns:
            tuple (int, int, str): The empty spot of the chess board. Index 0 represents the row from 0, index 1 represents the column from 0, and index 2 is the coordinate that should be submitted
        '''
        ans = self.__calculate()
        return tuple([ans[0], ans[1], "".join([['A','B','C','D','E','F'][ans[1]],str(ans[0]+1)])])