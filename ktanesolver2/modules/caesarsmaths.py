from word2number import w2n
from ..edgework import edgework

class caesarsmaths(edgework):
    def __check(self, e,g,r):
        if not isinstance(e, list): raise TypeError("encrypted must be in list")
        elif not all([isinstance(a, str) for a in e]): raise TypeError("Element of encrypted must be in str")
        elif not isinstance(g, int): raise TypeError("green_leds must be in int")
        elif not isinstance(r, int): raise TypeError("red_leds must be in int")
        elif g<0 or g>3: raise ValueError("green_leds must be in range 0-3")
        elif r<0 or r>3: raise ValueError("red_leds must be in range 0-3")
        return [a.upper() for a in e],g,r
    
    def __init__(self, edgework:edgework, encrypted:list[str], green_leds:int, red_leds:int):
        '''
        Initialize a new caesarsmaths instance

        Args:
            edgework (edgework): The edgework of the bomb
            encrypted (list[str]): The list of encrypted message that appears on the module. The first index of this list represents the encypted message on the topmost row and so on
            green_leds (int): The number of green leds that appears on the module
            red_leds (int): The number of red leds that appears on the module
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__encrypted, self.__green_leds, self.__red_leds = self.__check(encrypted, green_leds, red_leds)
    
    def __calculate(self):
        a = sum([int(a) for a in self._sndigit]); b = self.batt+3; c = self.__green_leds; d = self.__red_leds
        shiftkey = (((6*a) * (b**c)) - d)%26
        decrypted = "".join(["".join([chr(((ord(a)-ord('A')-shiftkey)%26)+ord('A')) for a in b]) for b in self.__encrypted])

        # print(decrypted, shiftkey, "a="+str(a), "b="+str(b), "c="+str(c), "d="+str(d))
        operation = lambda x,y: None; n=[]
        number_list = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]

        if "CALCULATE" in decrypted: decrypted = decrypted.replace("CALCULATE", " ")
        if "PERFORM" in decrypted: decrypted = decrypted.replace("PERFORM", " ")
        if "FIND" in decrypted: decrypted = decrypted.replace("FIND", " ")
        if "MINUS" in decrypted or "SUBTRACT" in decrypted:
            if "MINUS" in decrypted: decrypted = decrypted.replace("MINUS", " ")
            elif "SUBTRACT" in decrypted: decrypted = decrypted.replace("SUBTRACT", " ")
            if "FROM" in decrypted: decrypted = decrypted.replace("FROM", " ")
            operation = lambda x,y: x-y
        elif "PLUS" in decrypted or "ADD" in decrypted:
            if "PLUS" in decrypted: decrypted = decrypted.replace("PLUS", " ")
            elif "ADD" in decrypted: decrypted = decrypted.replace("ADD", " ")
            if "TO" in decrypted: decrypted = decrypted.replace("TO", " ")
            operation = lambda x,y: x+y
        elif "DIVIDE" in decrypted:
            decrypted = decrypted.replace("DIVIDE", " "); decrypted = decrypted.replace("BY", " ")
            operation = lambda x,y: x//y
        elif "MULTIPLY" in decrypted or "TIMES" in decrypted:
            if "MULTIPLY" in decrypted: decrypted = decrypted.replace("MULTIPLY", " ")
            elif "TIMES" in decrypted: decrypted = decrypted.replace("TIMES", " ")
            decrypted = decrypted.replace("BY", " ")
            operation = lambda x,y: x*y
        
        decrypted = decrypted.split(" ")
        decrypted.remove("")
        for a in range(len(decrypted)):
            try:
                n.append(w2n.word_to_num(decrypted[a]))
            except:
                for b in range(len(number_list)):
                    if number_list[b] in decrypted[a]:
                        decrypted[a] = decrypted[a].replace(number_list[b], " ")
                        n.append(w2n.word_to_num(decrypted[a]+" "+number_list[b]))
                        break

        return operation(n[0], n[1])

    def solve(self):
        '''
        Solve the Caesar's Maths module

        Returns:
            int: The correct answer after the calculation
        '''
        return self.__calculate()