import copy
from ..edgework import edgework

class binarypuzzle(edgework):
    def __check(self, g):
        if not isinstance(g, list): raise TypeError("grid must be in list")
        elif len(g)!=6: raise IndexError("Length of grid must be 6")
        elif not all([isinstance(a, list) for a in g]): raise TypeError("Element of grid must be in list")
        elif not all([len(a)==6 for a in g]): raise IndexError("Length of element of grid must be 6")
        elif not all([a is None or isinstance(a, (int, str)) for b in g for a in b]): raise TypeError("Type of each grid sublists must be int or str or none")
        elif not all([a is None or a in [0,1] for b in g for a in b]): raise ValueError("Type of each grid sublists must be 0 or 1 or none")
        return [[a if a is None else int(a) for a in b] for b in g]
    
    def __init__(self, edgework:edgework, grid:list[list[int|None]]):
        '''
        Initialize a new x01 instance

        Args:
            edgework (edgework): The edgework of the bomb
            grid (list [list [int|None]]): The grid of the current puzzle that appears on the module. Each list must consist of the number 0 or 1 (either in int or str) or None. Anything than 0 or 1 will assigned as None (except for 0,1).
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__grid = self.__check(grid)
    
    def __calculate(self):
        def backtracking(seq, memory, row=0, potential=[0,1]):
            rotated = [list(row)[::-1] for row in list(zip(*seq))]
            for b in range(len(seq)):
                for a in range(0,len(seq[b])-2):
                    if(len(set(seq[b][a:a+3]))==1) and (seq[b][a] is not None) and (seq[b][a+1] is not None) and (seq[b][a+2] is not None): return None
                    if(len(set(rotated[b][a:a+3]))==1) and (rotated[b][a] is not None) and (rotated[b][a+1] is not None) and (rotated[b][a+2] is not None): return None
                if len([a for a in seq[b] if a==0])>3 or len([a for a in seq[b] if a==1])>3: return None
                if len([a for a in rotated[b] if a==0])>3 or len([a for a in rotated[b] if a==1])>3: return None
            if len([a for b in seq for a in b if a is None])==0: return seq
            if seq[row].count(None) == 0:
                row += 1
                if row >= len(seq): return seq

            for a in potential:
                new_seq = copy.deepcopy(seq); new_memory = copy.deepcopy(memory)
                
                none_index = new_seq[row].index(None)
                new_seq[row][none_index] = a
                
                if new_seq[row] in [m[0] for m in new_memory]:
                    continue

                new_memory.append([new_seq[row], row])
                result = backtracking(new_seq, new_memory, row)
                if result is not None:
                    return result
            return None
        return backtracking(seq=self.__grid, memory=[])

    def solve(self):
        '''
        Solve the Binary Puzzle module

        Returns:
            list (list [int]): The correct grid to solve the module. This grid's orientation is the same as the module, meaning first list represents topmost row, second list represent second top row and so on
        '''
        return self.__calculate()