import copy
from ..edgework import edgework

class splittingtheloot(edgework):
    __diamond_table = [
        [20,19,13,26,23,34,12,14,35,16],
        [10,21,13,25,24,11,11,30,19,39],
        [39,38,25,30,24,23,28,34,15,36],
        [14,18,33,22,31,32,22,37,36,31],
        [40,20,26,12,32,33,28,15,38,17],
        [19,29,18,16,17,21,35,27,27,37]
    ]
    
    def __check(self,l,m):
        if not isinstance(l, list): raise TypeError("loots must be in list")
        elif len(l)!=7: raise IndexError("Length of loots must be 7")
        elif not all([isinstance(a, (str, int)) for a in l]): raise TypeError("Element of loots must be in str or int")
        elif not all([a[0].lower() not in "ABCDEFGHIJ" for a in l if isinstance(a,str)]): raise ValueError("Letter must come first in loots")
        elif not isinstance(m, (str, int)): raise TypeError("marked must be in str or int")
        elif str(m).upper() not in [str(a).upper() for a in l]: raise ValueError("marked must be in loots")
        l_temp = []; d_temp = {}
        for _ in l:
            if isinstance(_, int): l_temp.append(_)
            else:
                if _[0].upper() in "ABCDEFGHIJ":
                    d_temp[_.upper()] = self.__diamond_table[int(_[1])-1][ord(_[0].upper())-ord('A')]
                else: l_temp.append(int(_))
        
        team_division = {'l': [[],[]], 'd': [[],[]]}
        if isinstance(m, int): team_division['l'][0].append(m)
        else:
            if m[0].upper() in "ABCDEFGHIJ": team_division['d'][0].append(self.__diamond_table[int(m[1])-1][ord(m[0].upper())-ord('A')])
            else: team_division['l'][0].append(int(m))
        
        d_temp2 = copy.deepcopy(d_temp)
        if isinstance(m, int): l_temp.remove(m)
        else:
            if m[0].upper() in "ABCDEFGHIJ": d_temp2.pop(m.upper())
            else: l_temp.remove(int(m))
        
        return d_temp2, l_temp, team_division, d_temp
    
    def __init__(self, edgework:edgework, loots:list[str|int], marked:int|str):
        '''
        Initialize a new splittingtheloot instance

        Args:
            edgework (edgework): The edgework of the bomb
            loots (list [str|int]): The loots that appears on the module. Value of each loots can be in str or int and it does not have to be consistent. NOTE: All loots must be included, including the marked one
            marked (int|str): The already marked loot.
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__diamonds, self.__loots, self.__team, self.__full_diamonds = self.__check(loots, marked)

    def __calculate(self):
        def backtrack(idx, diamonds, loots, splits):
            if sum(splits['l'][0])+sum(splits['d'][0])==sum(splits['l'][1])+sum(splits['d'][1]):
                return splits
            
            if len(splits['d'][0])==3 or len(splits['d'][1])==3:
                return None

            for letter, value in diamonds.items():
                new_splits = copy.deepcopy(splits)
                new_diamonds = copy.deepcopy(diamonds)
                if sum(new_splits['l'][0])+sum(new_splits['d'][0])>=sum(new_splits['l'][1])+sum(new_splits['d'][1]):
                    new_splits['d'][1].append(value); added = 1
                else:
                    new_splits['d'][0].append(value); added = 0
                new_diamonds.pop(letter)
                result = backtrack(idx + 1, new_diamonds, loots, new_splits)
                if result is not None: return result

            for value in loots:
                new_splits = copy.deepcopy(splits)
                new_loots = copy.deepcopy(loots)
                if sum(new_splits['l'][0])+sum(new_splits['d'][0])>=sum(new_splits['l'][1])+sum(new_splits['d'][1]):
                    new_splits['l'][1].append(value); added = 1
                else:
                    new_splits['l'][0].append(value); added = 0
                new_loots.remove(value)
                result = backtrack(idx + 1, diamonds, new_loots, new_splits)
                if result is not None: return result

            return None    
        return backtrack(0, self.__diamonds, self.__loots, self.__team)



    def solve(self):
        '''
        Solve the Splitting the Loot module

        Returns:
            tuple (list [str]): One of the possible solution to split the loot between two team evenly. The index does not represent any specific team, but they are grouped to be two teams each
        '''
        result = self.__calculate()
        reverse_diamonds = {}
        for a,b in self.__full_diamonds.items():
            reverse_diamonds[b] = a
        team1 = [str(a).zfill(2) for a in result['l'][0]]; team2 = [str(a).zfill(2) for a in result['l'][1]]
        team1 = team1+[reverse_diamonds.get(a) for a in result['d'][0]]; team2 = team2+[reverse_diamonds.get(a) for a in result['d'][1]]
        return (team1, team2)
        return result