from ..edgework import edgework

class booleanvenndiagram(edgework):
    def __check(self, l):
        func = l.__code__
        if not callable(l): raise TypeError("logic must be in function")
        elif not all([b in ['a','b','c'] for b in [a for a in func.co_varnames]]): raise NameError("Parameter of logic function must be only 'a', 'b', and 'c'")
        return l
    
    def __init__(self, edgework:edgework, logic:callable):
        '''
        Initialize a new booleanvenndiagram instance

        Args:
            edgework (edgework): The edgework of the bomb
            logic (function): The logic function that appears on the module. Parameter of this function must have parameters named: 'a', 'b', 'c'. Representing a, b, and c on the module.
        NOTE:
            If you're confused how to translate the logical symbol to python here's a guide:\n
            x ∧ y = x and y\n
            x v y = x or y\n
            x ⊻ y = x ^ y\n
            x → y = not x or y\n
            x ← y = x or not y\n
            x | y = not (x and y)\n
            x ↓ y = not (x or y)\n
            x ↔ y = not (x ^ y)\n
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__logic = self.__check(logic)
    
    def __calculate(self):
        ans = []
        for _ in range(0,8):
            temp = [True if x=='1' else False for x in format(_, "03b")]; a = temp[0]; b = temp[1]; c = temp[2]
            if self.__logic(a=a, b=b, c=c): ans.append("".join([['a','b','c'][z] for z in range(0,3) if temp[z]]))
        return ans

    def solve(self):
        '''
        Solve the Boolean Venn Diagram

        Returns:
            list (str): The part of circles you need to press. Multiple letter indicates part of two circles where those two combined/connected
        '''
        return self.__calculate()