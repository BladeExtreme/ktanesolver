from ..edgework import edgework

class blindalley(edgework):
    __indtable = {
        'BOB': [1,6],
        'CAR': [2,1],
        'CLR': [9,6],
        'FRK': [8,2],
        'FRQ': [4,7],
        'IND': [4,1],
        'MSA': [9,8],
        'NSA': [2,5],
        'SIG': [5,7],
        'SND': [5,9],
        'TRN': [4,7]
    }
    __porttable = {
        'PARALLEL': 8,
        'PS/2': 6,
        'RCA': 9,
        'RJ-45': 2,
        'SERIAL': 6
    }
    __pos = {
        0: 'Top Left', 1: 'Top Middle',
        3: 'Middle Left', 4: 'Middle', 5: 'Middle Right',
        6: 'Bottom Left', 7: 'Bottom Middle', 8: 'Bottom Right'
    }
    
    def __init__(self, edgework:edgework):
        '''
        Initialize a new blindalley instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
    
    def __calculate(self):
        quadrant = [0 for a in range(9)]
        for a in self.__indtable:
            if a in self._unlitind: quadrant[self.__indtable[a][0]-1] += 1
            if a+'*' in self._litind: quadrant[self._indtable[a][1]-1] += 1
        for a in self.__porttable:
            if a in self._uniqueports: quadrant[self.__porttable[a]-1] += 1
        return [self.__pos[a] for a in range(len(quadrant)) if quadrant[a]==max(quadrant)]

    def solve(self) -> tuple[str]:
        '''
        Solve the Blind Alley module

        Returns:
            tuple [str]: The list of positions to press
        '''
        return tuple(self.__calculate())