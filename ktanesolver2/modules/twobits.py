from ..edgework import edgework

class twobits(edgework):
    __querybank = [
      ['kb','dk','gv','tk','pv','kp','bv','vt','pz','dt'],
       ['ee','zk','ke','ck','zp','pp','tp','tg','pd','pt'],
        ['tz','eb','ec','cc','cz','zv','cv','gc','bt','gt'],
         ['bz','pk','kz','kg','vd','ce','vb','kd','gg','dg'],
          ['pb','vv','ge','kv','dz','pe','db','cd','td','cb'],
           ['gb','tv','kk','bg','bp','vp','ep','tt','ed','zg'],
            ['de','dd','ev','te','zd','bb','pc','bd','kc','zb'],
             ['eg','bc','tc','ze','zc','gp','et','vc','tb','vz'],
              ['ez','ek','dv','cg','ve','dp','bk','pg','gk','gz'],
               ['kt','ct','zz','vg','gd','cp','be','zt','vk','dc']
      ]
    
    def __check(self, q):
        if not isinstance(q, (str, int)): raise TypeError("Query must be in str or int")
        if isinstance(q, int): q = str(q).zfill(2)
        
        if len(q) !=2: raise IndexError("Query must be length of 2")
        elif q[0].isalpha() or q[1].isalpha(): raise ValueError("Query cannot be a letter, must be all numbers")
        elif int(q[0]) not in range(0,10) or int(q[1]) not in range(0,10): raise ValueError("Query must be in range of 00-99")
        return q

    def __init__(self, edgework: edgework):
        '''
        Intialize a new twobits instance

        Args:
            edgework (edgework): The edgework of the bomb
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
    
    def __calculate(self):
        n = ord(self._snletter[0]) - ord('A') + 1 if len(self._snletter) > 0 else 0
        n += int(self._sndigit[-1])*self.batt
        if 'RCA' in self._uniqueports and not 'RJ-45' not in self._uniqueports: n *= 2
        n = str(n%100) if n>99 else '0'+str(n) if n<10 else str(n)
        return n

    def solve(self, query:str|int|None=None):
        '''
        Solve the Two Bits module

        Args:
            query (str|int|None): The query code that appears on the module. Leave this parameter None if this is the first query

        Returns:
            str: The query/submit code
        '''
        if query is not None:
            self.__query = self.__check(query)
            r,c = int(self.__query[0]), int(self.__query[1])
        else:
            a = self.__calculate()
            r,c = int(a[0]), int(a[1])
        return self.__querybank[r][c]