import copy
from ..edgework import edgework

class switches(edgework):
    def __check(self, s, t):
        if not isinstance(s, list): raise TypeError("state must be in list")
        elif len(s)!=5: raise IndexError("Length of state must be 5")
        elif (not all([isinstance(a, bool) for a in s])) and (not all([isinstance(a, int) for a in s])): raise TypeError("Element of state must be in bool/int")
        elif not isinstance(t, list): raise TypeError("target must be in list")
        elif len(t)!=5: raise IndexError("Length of target must be 5")
        elif (not all([isinstance(a, bool) for a in t])) and (not all([isinstance(a, int) for a in t])): raise TypeError("Element of target must be in bool/int")
        if all([isinstance(a, int) for a in s]):
            for a in range(len(s)):
                if s[a] not in [0,1]: raise ValueError("Element of state must be 0 or 1")
        if all([isinstance(a, int) for a in t]):
            for a in range(len(t)):
                if t[a] not in [0,1]: raise ValueError("Element of target must be 0 or 1")
        return [1 if bool(a)==True else 0 for a in s],[1 if bool(a)==True else 0 for a in t]
    
    def __init__(self, edgework:edgework, state:list[bool], target:list[bool]):
        '''
        Initialize a new switches instance

        Args:
            edgework (edgework): The edgework of the bomb
            state (list (bool)): The state of the switch where it's up or down. Put True/1 for up and False/0 for down
            target (list (bool)): The target state of the switch indicated by the lights. Put True/1 for up and False/0 for down
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__state, self.__target = self.__check(state, target)
    
    def __calculate(self):
        illegal = [
            [0,0,1,0,0],
            [0,1,0,1,1],
            [0,1,1,1,1],
            [1,0,0,1,0],
            [1,0,0,1,1],
            [1,0,1,1,1],
            [1,1,0,0,0],
            [1,1,1,0,0],
            [1,1,1,1,0]
        ]
        queue = [[self.__state, [], sum([1 for b in range(len(self.__state)) if self.__state[b]==self.__target[b]])]]
        visited = set()

        while queue:
            state, path, score = queue.pop(0)
            if state==self.__target: return path
            if tuple(state) in visited: continue
            if state in illegal: continue
            visited.add(tuple(state))
            for a in range(5):
                new_state = copy.deepcopy(state)
                new_state[a] = int(not new_state[a])
                new_score = sum([1 for b in range(len(new_state)) if new_state[b]==self.__target[b]])
                queue.append([new_state, path+[a+1], new_score])
                queue = sorted(queue, key=lambda x: x[-1], reverse=True)
        return None
            

    def solve(self):
        '''
        Solve the Switches module

        Returns:
            tuple (int): The switch order to click in the sequence
        '''
        return tuple(self.__calculate())