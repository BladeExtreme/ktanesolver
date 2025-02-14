from ..edgework import edgework

class algebra(edgework):
    def __check(self, f):
        if not callable(f): raise TypeError("function must be callable/function")
        elif not set([a for a in f.__code__.co_varnames])==set(['x','y','z']): raise TypeError("function must be callable/function")
        return f
    
    def __init__(self, edgework:edgework):
        '''
        Initialize a new algebra instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__x, self.__y, self.__z = 0,0,0
        self.__findxyz()
    
    def __findxyz(self):
        x = sum([int(a) for a in self._sndigit])
        if self.hold>=3: x+=2
        if 'RJ-45' in self._uniqueports: x-=1
        if 'BOB*' in self._litind: x+=4
        if any([a in "AIUEO" for a in self._snletter]): x-=3

        y = len(self.ind)-len([a for b in self.ports for a in b])
        if self.hold<=2: y-=2
        if 'SERIAL' in self._uniqueports: y+=3
        if 'FRQ' in self._unlitind: y-=5
        if sum([int(a) for a in self._sndigit]) in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]: y+=4

        z = self.total_modules+(((self.batt-self.hold)*2 )* (self.batt-((self.batt-self.hold)*2)))
        if self.hold==0: z+=3
        if "PARALLEL" in self._uniqueports: z-=6
        if "MSA*" in self._litind: z+=2
        if sum([int(a) for a in self._sndigit])%3==0: z+=1

        self.__x, self.__y, self.__z = x, y, z

    def __calculate(self):
        return self.__function(self.__x, self.__y, self.__z)

    def solve(self, function:callable):
        '''
        Solve the Algebra module

        Args:
            function (callable): The function that appears on the module. Move the equation so that one side is only the a/b/c. The function should only be the equations. Parameter must be 'x','y','z' despite one of the variables may not appear in the module. All parameter name must be in lower case.

        Returns:
            int|float: The correct answer to the algebra problem
        '''
        self.__function = self.__check(function)
        return self.__calculate()