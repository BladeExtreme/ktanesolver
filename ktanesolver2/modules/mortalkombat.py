from ..edgework import edgework

class mortalkombat(edgework):
    __prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    __charactermoves = {
        'johnnycage': ['⇦⇨A', '⇦⇨B', '⇩⇩C', ['⇩⇩⇦C⇧B', '⇦⇦⇦BB⇧', '⇩⇦⇧⇩AB']],
        'kano': ['⇧⇩C', '⇨⇨B', '⇩⇦A', ['A⇩B⇧⇦C', '⇧⇧⇨⇨CB', 'ABC⇦⇦⇧']],
        'liukang': ['⇨⇨C', '⇨⇧A', '⇦⇩B', ['⇩⇨B⇦B⇩', '⇨⇨⇩A⇧C', '⇨⇨⇦⇦⇧A']],
        'raiden': ['⇦⇦B', '⇩⇨A', '⇩⇧C', ['AA⇦⇧⇨B', '⇩⇧⇩⇧BB', 'C⇧⇦AB⇩']],
        'scorpion': ['⇦⇦A', '⇦⇨C', '⇧⇧B', ['⇨⇨⇨BBB', '⇧⇧⇩⇦AC', 'A⇨B⇩C⇩']],
        'sonyablade': ['⇧⇨A', '⇩⇦C', '⇨⇦B', ['⇨⇦⇦⇨CB', '⇩⇧⇨B⇦A', '⇧⇧⇩⇦AC']],
        'subzero': ['⇨⇧B', '⇨⇨A', '⇨⇩C', ['⇦⇧⇨⇩CC', '⇨⇩⇦⇧AA', '⇧⇨A⇦⇧B']]
    }
    __whattouse = {
        'johnnycage': [None, [0,2,1], [1,0,2], [2,1,0], [1,2,0], [0,1,2], [2,0,1]],
        'kano': [[2,0,1], None, [1,0,2], [0,1,2], [2,1,0], [1,2,0], [0,2,1]],
        'liukang': [[1,2,0],[0,1,2],None,[2,0,1],[0,2,1],[1,0,2],[2,1,0]],
        'raiden': [[2,1,0],[1,2,0],[0,2,1],None,[2,0,1],[1,0,2],[0,1,2]],
        'scorpion': [[0,1,2],[2,0,1],[1,0,2],[2,1,0],None,[1,2,0],[0,2,1]],
        'sonyablade': [[2,1,0],[1,2,0],[0,2,1],[0,1,2],[2,0,1],None,[1,0,2]],
        'subzero': [[0,2,1],[1,0,2],[2,1,0],[0,1,2],[2,0,1],[1,2,0],None]
    }
    __char2idx = {
        'johnnycage': 0, 'kano': 1, 'liukang': 2,
        'raiden': 3, 'scorpion': 4, 'sonyablade': 5,
        'subzero': 6
    }
    
    def __namecheck(self, a):
        if a in ['johnny', 'cage', 'johnnycage']: return 'johnnycage'
        elif a in ['kano']: return 'kano'
        elif a in ['liu', 'kang', 'liukang']: return 'liukang'
        elif a in ['raiden']: return 'raiden'
        elif a in ['scorpion']: return 'scorpion'
        elif a in ['sonya', 'blade', 'sonyablade']: return 'sonyablade'
        elif a in ['subzero']: return 'subzero'
        else: raise ValueError(f"Character is invalid {a}")


    def __check(self, p, e):
        if not isinstance(p, str): raise TypeError("Player must be in str")
        elif not isinstance(e, str): raise TypeError("Enemy must be in str")
        p = p.replace(" ", ""); e = e.replace(" ",""); p = p.lower(); e = e.lower()
        p = p.replace("-", ""); e = e.replace("-","")
        p = self.__namecheck(p); e = self.__namecheck(e)

        if p==e: raise ValueError("Player's character cannot be same as Enemy's character")
        return p,e
    
    def __init__(self, edgework:edgework, player:str, enemy:str):
        '''
        Initialize a new mortalkombat instance

        Args:
            edgework (edgework): The edgework of the bomb
            player (str): The name of the player that appears on the module
            enemy (str): The name of the enemy that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__player, self.__enemy = self.__check(player, enemy)
    
    def __calculate(self):
        ans = [self.__charactermoves[self.__player][a] for a in self.__whattouse[self.__player][self.__char2idx[self.__enemy]]]
        ans.append(self.__charactermoves[self.__player][-1])
        if self.__player == 'johnnycage':
            if self.__enemy in ['kano', 'liukang', 'raiden']:
                if 'PARALLEL' in self._uniqueports or 'SERIAL' in self._uniqueports: ans[-1] = ans[-1][0]
                elif int(self._sndigit[-1])%2 == 1: ans[-1] = ans[-1][1]
            else:
                if any([a in ['CAR*', 'CLR*', 'MSA*'] for a in self._litind]) or any([a in ['BOB', 'NSA', 'FRK'] for a in self._unlitind]): ans[-1][0]
                elif self.batt%2==0: ans[-1][1]
        elif self.__player == 'kano':
            if self.__enemy in ['johnnycage', 'liukang', 'raiden']:
                if self.batt-(self.batt-self.hold)*2 > (self.batt-self.hold)*2: ans[-1] = ans[-1][0]
                elif len(self._unlitind)==0: ans[-1]=ans[-1][1]
            else:
                if any([a in ['A','I','U','E','O'] for a in self._snletter]): ans[-1] = ans[-1][0]
                elif 'DVI-D' in self._uniqueports or 'RJ-45' in self._uniqueports: ans[-1] = ans[-1][1]
        elif self.__player == 'liukang':
            if self.__enemy in ['johnnycage', 'kano', 'raiden']:
                if len(self._litind)>0: ans[-1] = ans[-1][0]
                elif 'STEREO RCA' in self._uniqueports or 'PS/2' in self._uniqueports: ans[-1] = ans[-1][1]
            else:
                if sum([int(a) for a in self._sndigit]) in self.__prime: ans[-1] = ans[-1][0]
                elif self.batt-(self.batt-self.hold)*2 == 0: ans[-1] = ans[-1][1]
        elif self.__player == 'raiden':
            if self.__enemy in ['johnnycage', 'kano', 'liukang']:
                if self.batt<=4: ans[-1] = ans[-1][0]
                elif any([a in ['L','P','T'] for a in self._snletter]): ans[-1] = ans[-1][1]
            else:
                if len(self.ind)==0: ans[-1] = ans[-1][0]
                elif [a for b in self.ports for a in b].count("SERIAL") > 1: ans[-1] = ans[-1][1]
        elif self.__player == 'scorpion':
            if self.__enemy in ['johnnycage', 'kano', 'liukang']:
                if len([a for b in self.ports for a in b])>3: ans[-1] = ans[-1][0]
                elif (self.batt-self.hold)*2 > self.batt-(self.batt-self.hold)*2: ans[-1] = ans[-1][1]
            else:
                if int(self._sndigit[-1])%2==0: ans[-1] = ans[-1][0]
                elif any([a in ['BOB*', 'FRK*'] for a in self._litind]) or any([a in ['FRQ', 'CAR'] for a in self._unlitind]): ans[-1] = ans[-1][1]
        elif self.__player == 'sonyablade':
            if self.__enemy in ['johnnycage', 'kano', 'liukang']:
                if len(self.ind) > len([a for b in self.ports for a in b]): ans[-1] = ans[-1][0]
                elif int(self._sndigit[0]) > self.batt: ans[-1] = ans[-1][1]
            else:
                if self.batt > int(self._sndigit[0]): ans[-1] = ans[-1][0]
                elif len([a for b in self.ports for a in b]) > len(self.ind): ans[-1] = ans[-1][1]
        elif self.__player == 'subzero':
            if self.__enemy in ['johnnycage', 'kano', 'liukang']:
                if sum([int(a) for a in self._sndigit])%3==0: ans[-1] = ans[-1][0]
                elif self.batt==0: ans[-1] = ans[-1][1]
            else:
                if len(self._litind)==0: ans[-1] = ans[-1][0]
                elif 'PARALLEL' in self._uniqueports or 'STEREO RCA' in self._uniqueports: ans[-1] = ans[-1][1]
        if isinstance(ans[-1], list): ans[-1] = ans[-1][2]
        return ans

    def solve(self):
        return tuple(self.__calculate())