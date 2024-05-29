from ..edgework import edgework

class orientationcube(edgework):
    __poston = {'f':0, 'r':1, 'b':2, 'l':3}
    __tabledict = {
        0: [['clockwise'],['left','counter-clockwise'],['counter-clockwise'],['left','clockwise']],
        1: [['counter-clockwise'],['clockwise','right'],['clockwise'],['clockwise','left']],
        2: [['counter-clockwise', 'left'],['left', 'clockwise'],['clockwise','left'],['left','counter-clockwise']],
        3: [['clockwise','left','left'],['right','clockwise','right'],['counter-clockwise','left','left'],['right','counter-clockwise','right']],
        4: [
            ['clockwise',[['clockwise'],['right','clockwise'],None,['right','counter-clockwise']]],
            ['clockwise',[['left','clockwise'],['clockwise'],['left','counter-clockwise'],None]],
            ['clockwise',[None,['left','clockwise'],['clockwise'],['left','counter-clockwise']]],
            ['clockwise',[['left', 'counter-clockwise'],None,['left','clockwise'],['clockwise']]]],
        5: [['counter-clockwise'],['clockwise','right'],['clockwise'],None]
    }
    
    def __check(self, p):
        if not isinstance(p, str): raise TypeError("Position must be str")
        elif p not in ['front','right','back','left']: raise ValueError(f"This position is invalid \'{p}\'")
        return p[0]
    
    def __init__(self, edgework:edgework, position: str):
        '''
        Initialize a new orientationcube instance

        Args:
            edgework (edgework): The edgework of the bomb
            position (str): The position of the eye in the module. Accepts only 'front', 'right', 'back', 'left'
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__position = self.__check(position)
    
    def __calculate(self):
        tabletouse = 0 if 'R' in self._snletter else 1 if ('TRN*' in  self._litind) or ('CAR' in self._unlitind or 'CAR*' in self._litind) \
        else 2 if 'PS/2' in self._uniqueports or self.strikes > 0 else 3 if '7' in self._sndigit or '8' in self._sndigit else 4 if self.batt >= 3 or self.__position=='l' \
        else 5
        return self.__tabledict[tabletouse][self.__poston[self.__position]]

    def solve(self, new_position:str|None=None):
        '''
        Solve the Orientation Cube module

        Args:
            new_position (str|None): By default None. If the eye position change, insert the new position to the parameter
        Returns:
            Tuple (str, ...): The correct order of presses to be submitted
        '''
        if new_position==None:
            ans = self.__calculate()
            if isinstance(ans[-1], list):
                self.__nextpos = ans[-1]
                return 're-enter new position'
            return tuple(ans)
        else:
            return tuple(self.__nextpos[self.__poston[self.__check(new_position)]])