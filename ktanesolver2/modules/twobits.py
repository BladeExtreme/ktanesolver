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
        if not isinstance(q, str): raise TypeError("Query has an invalid type")
        elif len(q) !=2: raise IndexError("Query must be length of 2")
        elif q[0].isalpha() or q[1].isalpha(): raise ValueError("Query cannot be a letter, must be all numbers")
        return q

    def __init__(self, edgework: edgework, query: str | None = None):
        '''
        Intialize a new twobits instance

        Args:
            edgework (edgework): The edgework of the bomb
            query (str)|(None): The query code that appears on the module. If this is the first query, leave it empty
        '''
        super().__init__(edgework.batt, edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        try:
            self.__query = self.__check(query)
        except:
            self.__query = None
    
    def __calculate(self):
        n = ord(self._snletter[0]) - ord('A') + 1 if len(self._snletter) > 0 else 0
        n += int(self._sndigit[-1])*self.batt
        if 'RCA' in self._uniqueports and not 'RJ-45' not in self._uniqueports: n *= 2
        n = str(n%100) if n>99 else '0'+str(n) if n<10 else str(n)
        return n

    def interactive(self, query: str):
        '''
        A quicker way to query the code without initializing a new instance. Assuming you've done the first query
        This can only be used when the edgework has been intialized to this instance

        Args:
            query (str)|(None): The query code that appears on the module.
        Returns:
            str: The query/submit code
        '''
        self.__query = self.__check(query)
        return self.solve()

    def solve(self):
        '''
        Solve the Two Bits module

        Returns:
            str: The query/submit code
        '''
        if self.__query != None:
            r, c = int(self.__query[0]), int(self.__query[1])
        else:
            a = self.__calculate()
            r, c = int(a[0]), int(a[1])
        return self.__querybank[r][c]
