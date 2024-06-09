from ..edgework import edgework
from ..tools.semadict import _sematranslate

class semaphore(edgework):
    def __check(self, f):
        if not isinstance(f, list) and not isinstance(f, dict): raise TypeError("flags must be in either list or dict")
        if isinstance(f, dict):
            if not all([a in ['letter', 'number'] for a in f.keys()]): raise KeyError("Keys of flags must be only 'letter' and 'number'")
            elif len(f.keys()) != 2: raise IndexError("Length of flags' keys must be 2")
            elif not all([all([isinstance(a, list) for a in f['letter']]), all([isinstance(a, list) for a in f['number']])]): raise TypeError("Values of flags must be in list")
            elif not all([all([isinstance(a, str) for a in [c for d in f['letter'] for c in d]]), all([isinstance(a, str) for a in [c for d in f['number'] for c in d]])]): raise TypeError("Element of flags' values must be in str")
            return f['letter'], f['number']
        elif isinstance(f, list):
            if not all([isinstance(a, list) for a in f]): raise TypeError("Element of flags must be in list")
            elif not all([len(a)==2 for a in f]): raise IndexError("Length of flags' elements must be 2")
            elif not all([isinstance(a, str) for a in [b for c in f for b in c]]): raise TypeError("Each element must contain str")
            temp = {'letter': [], 'number': []}
            flgst = 0 if tuple(sorted(set(f[0]))) == tuple(sorted({'N', 'E'})) else 1
            for a in f[1:]:
                if(tuple(sorted(set(a)))==tuple(sorted({'N', 'NE'})) and flgst==0) or (tuple(sorted(set(a)))==tuple(sorted({'N', 'E'})) and flgst==1):
                    flgst+=1; flgst%=2
                else:
                    if (tuple(sorted(set(a))) == tuple(sorted({'N', 'E'})) and flgst==1) or (tuple(sorted(set(a))) == tuple(sorted({'N', 'NE'}))): pass
                    elif flgst==0: temp['letter'].append(set(a))
                    elif flgst==1: temp['number'].append(set(a))
            return temp['letter'], temp['number']
    
    def __init__(self, edgework:edgework, flags:list|dict):
        '''
        Initialize a new semaphore instance

        Args:
            edgework (edgework): The edgework of the bomb
            flags (list [[str, str], ...]): The order direction of flags that appears on the module
            flags (dict {'letter': [[str, str], ...]}): The direction of flags that appears on the module during each signal/state. Valid keys are only 'letter' and 'number'
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__letter, self.__digit = self.__check(flags)
        self.__islist = True if isinstance(flags, list) else False
        self.__pureflags = flags if self.__islist else None
    
    def __searchindex(self, ans, state):
        flgst = 0 if tuple(sorted(set(self.__pureflags[0]))) == tuple(sorted({'N', 'E'})) else 1
        for a in range(1, len(self.__pureflags[1:])):
            if(tuple(sorted(set(self.__pureflags[a])))==tuple(sorted({'N', 'NE'})) and flgst==0) or (tuple(sorted(set(self.__pureflags[a])))==tuple(sorted({'N', 'E'})) and flgst==1):
                flgst+=1; flgst%=2
            elif flgst==state and ans==_sematranslate(self.__pureflags[a], flgst):
                return self.__pureflags[a], a

    def __calculate(self):
        newletter = _sematranslate(self.__letter.copy(), 0); newdigit = _sematranslate(self.__digit.copy(), 1)
        ans = ''
        for a in range(len(newletter)):
            if newletter[a] not in self._snletter:
                ans = newletter[a]
                if self.__islist: return self.__searchindex(ans, 0)
                return self.__letter[a], 'letter'
        for a in range(len(newdigit)):
            if newdigit[a] not in self._sndigit:
                ans = newdigit[a]
                if self.__islist: return self.__searchindex(ans, 1)
                return self.__digit[a], 'digit'

    def solve(self):
        '''
        Solve the Semaphore module

        Returns:
            list (str, str): The direction of the odd one out flag
            str|int: The state of the flag ('letter' or 'digit') OR the index of the list where the flag is the odd one out
        '''
        ans = self.__calculate()
        return tuple(ans)
