from ..edgework import edgework

class binaryled(edgework):
    __table = [
        [17,15,6,2,24,8,26,25,21,24,1,15,18,8],
        [18,15,19,31,12,6,19,21,11,16,19,2,1,29],
        [8,25,1,15,20,15,9,3,6,24,1,24,5,26],
        [21,27,6,12,27,20,7,1,19,15,3,13,9,28],
        [3,21,14,22,7,28,16,27,22,17,26,2,31,15],
        [8,22,30,19,1,25,31,16,9,7,6,13,9,7],
        [5,18,12,7,5,12,31,16,10,15,17,9,12,25],
        [4,20,18,25,20,4,24,29,17,16,12,16,29,19]
    ]
    __cut_at = [
        [3,5,7],
        [8,11,4],
        [1,9,2],
        [12,8,7],
        [5,10,8],
        [10,0,6],
        [5,2,9],
        [5,9,10]
    ]
    
    def __check(self, f):
        if not isinstance(f, list): raise TypeError("sequence must be in list")
        elif not all([isinstance(a, (list,int,str)) for a in f]): raise TypeError("Element of sequence must be in int (base 10 value), list or (str)")
        elif len(f)<self.__threshold: raise IndexError(f"Length of sequence must be at least {self.__threshold}")
        seq = []
        for a in f:
            if isinstance(a, str):
                if len(a)!=5: raise IndexError(f"Length of element of sequence must be 5. {a}")
                elif not all([x in '01' for x in a]): raise ValueError(f"Element of element of sequence must be in 0 or 1. {a}")
                seq.append(int(a, 2))
            elif isinstance(a, int):
                if a>31: raise ValueError(f"Element of sequence cannot be greater than 31. {a}")
                seq.append(a)
            elif isinstance(a, list):
                if len(a)!=5: raise IndexError(f"Length of element of sequence must be 5. {a}")
                elif not all([isinstance(x, (str,int,bool)) for x in a]): raise TypeError(f"Element of element of sequence must be in str, int or bool. {a}")
                if all([isinstance(x,str) for x in a]):
                    if any([x not in '01' for x in a]): raise ValueError(f"Element of element of sequence must be in 0 or 1. {a}")
                    seq.append(int("".join(a), 2))
                elif all([isinstance(x,int) for x in a]):
                    if any([x not in range(2) for x in a]): raise ValueError(f"Element of element of sequence must be in 0 or 1. {a}")
                    seq.append(int("".join([str(x) for x in a]), 2))
                elif all([isinstance(x,bool) for x in a]):
                    if any([x not in [True, False] for x in a]): raise ValueError(f"Element of element of sequence must be in True or False. {a}")
                    seq.append(int("".join([str(int(x)) for x in a]), 2))
                else:
                    raise TypeError(f"Element of element of sequence must be consistent in str, int or bool. {a}")
        return seq
    
    def __init__(self, edgework:edgework, sequence:list[list[str | int | bool] | int], threshold:int=4):
        '''
        Initialize a new binaryled instance

        Args:
            edgework (edgework): The edgework of the bomb
            sequence (list [list [str|int|bool]]|int): The sequence of the led in the form of a list of ones and zeros or a list of numbers converted to base 10. Specifically for ones and zeros, content of list can be the type of str, int or bool. However, a list must have a consistent type ([1,0,1,0,1], [False, True, True, True, False], ['1','0','1','0','1'])
            threshold (int): The threshold of how many minimum of LED sequences to be accepted, cannot be below 3. By default it's 4
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if not isinstance(threshold, int): raise TypeError("threshold must be int")
        elif threshold<3: raise ValueError("threshold cannot be below 3")
        else: self.__threshold = threshold
        self.__sequence = self.__check(sequence)
    
    def __calculate(self):
        rows = {a:[] for a in self.__sequence}

        for a in range(len(self.__sequence)):
            for b in range(len(self.__table)):
                if self.__sequence[a] in self.__table[b]:
                    rows[self.__sequence[a]].append(b)
                    continue
        
        intersection_rows = set(tuple([a for a in rows.values()][0]))
        for a in rows.values():
            intersection_rows = intersection_rows.intersection(tuple(a))
        
        if len(intersection_rows)==1:
            return {['Green','Red','Blue'][a]:[bin(self.__table[list(intersection_rows)[0]][self.__cut_at[list(intersection_rows)[0]][a]-1])[2:].zfill(5), bin(self.__table[list(intersection_rows)[0]][self.__cut_at[list(intersection_rows)[0]][a]])[2:].zfill(5)+"#", bin(self.__table[list(intersection_rows)[0]][self.__cut_at[list(intersection_rows)[0]][a]+1])[2:].zfill(5)] for a in range(3)}
        else:
            temp = {list(intersection_rows)[x]:{a:[] for a in self.__sequence} for x in range(len(intersection_rows))}
            for a in intersection_rows:
                for b in range(len(self.__table[a])):
                    if self.__table[a][b] in self.__sequence:
                        temp[a][self.__table[a][b]].append(b)
            row_to_use = -1
            for a in intersection_rows:
                if row_to_use==-1:
                    num_set = {x for y in temp[a].values() for x in y}
                    min_num, max_num = min(num_set), max(num_set)
                    for start in range(min_num, max_num - 1):
                        consecutive = {start, start + 1, start + 2}
                        if consecutive.issubset(num_set):
                            row_to_use = a
                            break
                    else:
                        continue
            return {['Green','Red','Blue'][a]:[bin(self.__table[row_to_use][self.__cut_at[row_to_use][a]-1])[2:].zfill(5), bin(self.__table[row_to_use][self.__cut_at[row_to_use][a]])[2:].zfill(5)+"#", bin(self.__table[row_to_use][self.__cut_at[row_to_use][a]+1])[2:].zfill(5)] for a in range(3)}

    def solve(self):
        '''
        Solve the Binary LED module

        Returns:
            dict (str, list): The correct wire to cut at the corresponding time
        '''
        return self.__calculate()