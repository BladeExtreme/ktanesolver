import copy
from ..edgework import edgework

class binarypuzzle(edgework):
    def __check(self, g):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif len(g) != 6: raise IndexError("Length of grid must be 6")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Element of grid must be in list")
        elif not all([len(a) == 6 for a in g]): raise IndexError("Length of element of grid must be 6")
        elif not all([a is None or isinstance(a, (int, str)) for b in g for a in b]): raise TypeError("Type of each grid sublists must be int or str or none")
        elif not all([a is None or a in [0, 1] for b in g for a in b]): raise ValueError("Type of each grid sublists must be 0 or 1 or none")
        return [[a if a is None else int(a) for a in b] for b in g]

    def __init__(self, edgework: edgework, grid: list[list[int | None]]):
        '''
        Initialize a new x01 instance

        Args:
            edgework (edgework): The edgework of the bomb
            grid (list [list [int|None]]): The grid of the current puzzle that appears on the module. Each list must consist of the number 0 or 1 (either in int or str) or None.
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__grid = self.__check(grid)

    def __calculate(self):
        def backtracking(seq, row_memory, col_memory, row=0, potential=[0, 1]):
            rotated = [list(col) for col in zip(*seq)]  # Transpose to get columns

            for b in range(len(seq)):
                for a in range(0, len(seq[b]) - 2):
                    if (len(set(seq[b][a:a+3])) == 1 and None not in seq[b][a:a+3]) or \
                       (len(set(rotated[b][a:a+3])) == 1 and None not in rotated[b][a:a+3]):
                        return None

                if seq[b].count(0) > 3 or seq[b].count(1) > 3:
                    return None
                if rotated[b].count(0) > 3 or rotated[b].count(1) > 3:
                    return None

            if all(all(cell is not None for cell in row) for row in seq):
                return seq

            if seq[row].count(None) == 0:
                row += 1
                if row >= len(seq): 
                    return seq

            for a in potential:
                new_seq = copy.deepcopy(seq)
                new_row_memory = copy.deepcopy(row_memory)
                new_col_memory = copy.deepcopy(col_memory)

                none_index = new_seq[row].index(None)
                new_seq[row][none_index] = a

                updated_col = [new_seq[r][none_index] for r in range(len(new_seq))]

                if new_seq[row] in [mem[0] for mem in new_row_memory]:
                    continue
                if updated_col in [mem[0] for mem in new_col_memory]:
                    continue

                new_row_memory.append([new_seq[row], row])
                new_col_memory.append([updated_col, none_index])

                result = backtracking(new_seq, new_row_memory, new_col_memory, row)
                if result is not None:
                    return result
            return None
        return backtracking(seq=self.__grid, row_memory=[], col_memory=[])

    def solve(self):
        '''
        Solve the Binary Puzzle module

        Returns:
            list (list [int]): The correct grid to solve the module. This grid's orientation is the same as the module, meaning first list represents topmost row, second list represent second top row and so on
        '''
        return self.__calculate()
