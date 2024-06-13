from ..edgework import edgework
from ..tools.colordict import _colorcheck

class coloredswitches(edgework):
    def __check2(self, w):
        if not isinstance(w, list): raise TypeError("switches must be in list")
        elif len(w)!=5: raise IndexError("Length of switches must be 5")
        elif not all([isinstance(a, dict) for a in w]): raise TypeError("Element of switches must be in dict")
        elif not all([all([b in ['color','state'] for b in a]) for a in w]): raise KeyError("Keys of each element of switches must consists of the following only: 'color' and 'state'")
        elif not all([all([isinstance(b['color'], str) and isinstance(b['state'], bool) or isinstance(b['state', int]) for b in a]) for a in w]): raise TypeError("Value of each element of switches must be str for 'color' and bool for 'state'")
        arr = [_colorcheck(a) for a in w]; arr2 = [0 if isinstance(a['state'], bool) and a==False else 1 if isinstance(a['state'], bool) and a==True else a['state'] for a in w]
        return arr, arr2

    def __check(self,s,c):
        if not isinstance(s, list): raise TypeError("switchstate must be in list")
        elif not isinstance(c, list): raise TypeError("color must be in list")
        elif not len(s)==len(c)==5: raise IndexError("Length of switchstate and color must be 5")
        elif not all([isinstance(a, bool) or isinstance(a, int) for a in s]): raise TypeError("Element of switchstate must be in bool or int")
        elif not all([isinstance(a, str) for a in c]): raise TypeError("Element of color must be in str")
        s = [0 if isinstance(a, bool) and a==False else 1 if isinstance(a, bool) and a==True else a for a in s]; c = ['purple' if a[0]=='m' else a for a in c]
        return s,[_colorcheck(a) for a in c]
    
    def __init__(self, edgework:edgework, switchstate:list|None=None, color:list|None=None, switches:list|None=None):
        '''
        Initialize a new coloredswitches instance

        Args:
            edgework (edgework): The edgework of the bomb
            switchstate (list (bool|int)): The state of the switch where it's up or down. Put True/1 for up and False/0 for down. CAUTION: switchstate must be in sync with color
            color (list (str)): The color of the switches in a list. Index 0 is the most left. CAUTION: color must be in sync with switchstate
            switches (list (dict)): The color and state of the switch in dict. Each dict must have the following keys only: 'color' and 'state'
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__target = None
        if switches is not None: self.__state, self.__color = self.__check2(switches)
        elif switchstate is not None and color is not None: self.__state, self.__color = self.__check(switchstate, color)
        else:
            raise TypeError("coloredswitches.__init__() missing 1 or 2 required positional arguments: 'switchstate' and 'color'; 'switches'")
    
    def __calculate(self):
        mapswitch = {
            0: [1], 1: [3], 2: [2,3], 3: [5 if self.__color[4] in ['green', 'blue'] else -1, 3], 4: [5], 5: [1 if self.__color[0] in ['cyan', 'red', 'purple'] else -1, 4 if self.__color[3]=='purple' else -1, 5],
            6: [4], 7: [5 if self.__color[4]=='purple' else -1, 2], 8: [2], 9: [4 if self.__color[3]=='green' else -1, 3, 2], 10: [2], 11: [2],
            12: [4], 13: [5], 14: [1], 15: [1], 16: [5], 17: [2],
            18: [1 if self.__color[0] in ['orange', 'blue', 'cyan'] else -1, 5], 19: [4], 20: [3 if self.__color[2] in ['red','cyan','purple'] else -1, 4], 21: [3 if self.__color[2] in ['orange', 'blue'] else -1, 5], 22: [3 if self.__color[2]=='green' else -1, 5], 23: [4],
            24: [1], 25: [4 if self.__color[3]=='orange' else -1, 5 if self.__color[4] in ['blue','purple','green'] else -1, 1], 26: [1 if self.__color[0] in ['purple', 'green', 'red'] else -1, 2], 27: [5 if self.__color[4] in ['red', 'cyan', 'orange'] else -1, 1], 28: [4 if self.__color[3] in ['orange', 'purple', 'green'] else -1, 5], 29: [4 if self.__color[3] in ['red','blue','cyan'] else -1, 2 if self.__color[1] in ['purple', 'orange'] else -1, 5],
            30: [2 if self.__color[1] in ['red', 'green'] else -1, 4], 31: [3]
        }
        vis = []; target = self.__target if self.__target is not None else 3; start = int("".join([str(x) for x in self.__state]), 2)
        query = [start]; history = [-1]; origin = [0]
        if target==3:
            for a in range(target):
                vis.append(query[0])
                nextmove = [a-1 for a in mapswitch[query[0]] if a!=-1]
                temp = [int(a) for a in format(query[0], '05b')]
                for b in nextmove:
                    temp2 = temp.copy(); temp2[b]=(temp2[b]+1)%2; temp2 = int("".join([str(x) for x in temp2]), 2)
                    if temp2 not in vis:
                        query.append(temp2); history.append(b); origin.append(query[0]); break
                query.pop(0)
            return [history[a]+1 for a in range(1, len(history))], [int(a) for a in format(query[-1], '05b')]
        else:
            while int("".join([str(x) for x in target]), 2) not in vis:
                vis.append(query[0])
                nextmove = [a-1 for a in mapswitch[query[0]] if a!=-1]
                temp = [int(a) for a in format(query[0], '05b')]
                for b in nextmove:
                    temp2 = temp.copy(); temp2[b]=(temp2[b]+1)%2; temp2 = int("".join([str(x) for x in temp2]), 2)
                    if temp2 not in vis:
                        query.append(temp2); history.append(b); origin.append(query[0])
                query.pop(0)
            track = [[int("".join([str(x) for x in target]), 2), -1]]
            while track[0][0]!=start:
                track.insert(0, [origin[vis.index(track[0][0])], history[vis.index(track[0][0])]+1])
            return [track[a][1] for a in range(len(track)-1)], 0

    def solve(self, target:list|None=None):
        '''
        Solve the Colored Switches module

        Args:
            target (list (bool|int)): The target state of the switches, indicated by LED below the switches. All low position LED are represented with 0/False while high position LED are resented with 1/True.
        Returns:
            tuple (tuple (int, int)): The switch order to click in the sequence. Index 0 are sequence starting from 0, index 1 are sequence starting from 1 instead.
        '''
        if target is not None:
            if not isinstance(target, list): raise TypeError("target must be in list")
            elif not len(target)==5: raise IndexError("Length of target must be 5")
            elif not all([isinstance(a, bool) or isinstance(a, int) for a in target]): raise TypeError("Element of target must be in bool or int")
            self.__target = [0 if isinstance(a,bool) and a==False else 1 if isinstance(a,bool) and a==True else a for a in target]
        ans, self.__state = self.__calculate()
        return tuple([tuple([a-1 for a in ans]), tuple(ans)])