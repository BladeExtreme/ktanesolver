from ..edgework import edgework

class gamepad(edgework):
    def __check(self, s):
        if not isinstance(s, str): raise TypeError("screen must be in str")
        elif len(s) !=5: raise IndexError("Length of screen must be 5")
        elif s[2] != ':': raise ValueError("The divider must be colon")
        return int(s[0:2]), int(s[3:]), [int(s[0]), int(s[1]), int(s[3]), int(s[4])]
    
    def __init__(self, edgework:edgework, screen:str):
        '''
        Initialize a new gamepad instance

        Args:
            edgework (edgework): The edgework of the bomb
            screen (str): The numbers that appears on the module, the two numbers are divided by a colon (':')
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__x, self.__y, self.__abcd = self.__check(screen)
    
    def __calculate(self):
        prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        perfect_squares = [1, 4, 9, 16, 25, 36, 49, 64, 81]
        highly_composite_numbers = [1, 2, 4, 6, 12, 24, 36, 48, 60]
        a = []

        if self.__x in prime: a.append("▲▲▼▼")
        elif self.__x % 12 == 0: a.append("▲A◀◀")
        elif self.__abcd[0]+self.__abcd[1] == 10 and int(self._sndigit[-1]) % 2 == 1: a.append("AB◀▶")
        elif (self.__x-3)%6 == 0 or (self.__x-5)%10 == 0: a.append("▼◀A▶")
        elif self.__x%7 == 0 and self.__y%7 != 0: a.append("◀◀▲B")
        elif self.__abcd[2]*self.__abcd[3] == self.__x: a.append("A▲◀◀")
        elif self.__x in perfect_squares: a.append("▶▶A▼")
        elif (self.__x+1)%3 == 0 or any([a for a in self._unlitind if "SND" == a]): a.append("▶AB▲")
        elif self.__x>=60 and self.__x<=90 and self.batt==0: a.append("BB▶◀")
        elif self.__x%6 == 0: a.append("ABA▶")
        elif self.__x%4 == 0: a.append("▼▼◀▲")
        else: a.append("A◀B▶")
        a.append(" ")
        if self.__y in prime: a.append("◀▶◀▶")
        elif self.__y%8 == 0: a.append("▼▶B▲")
        elif self.__abcd[2]-self.__abcd[3] == 4 and 'STEREO RCA' in self._uniqueports: a.append("▶A▼▼")
        elif (self.__y-2)%4 == 0 or any([a for a in self._litind if 'FRQ*' == a]): a.append("B▲▶A")
        elif self.__y%7 == 0 and self.__x%7 != 0: a.append("◀◀▼A")
        elif self.__y in perfect_squares: a.append("▲▼B▶")
        elif self.__y == self.__abcd[0]*self.__abcd[1]: a.append("A▲◀▼")
        elif (self.__y+1)%4 == 0 or 'PS/2' in self._uniqueports: a.append("▲BBB")
        elif self.__abcd[2]>self.__abcd[3] and self.batt >= 2: a.append("AA▲▼")
        elif self.__y%5 == 0: a.append("BAB◀")
        elif self.__y%3 == 0: a.append("▶▲▲◀")
        else: a.append("B▲A▼")

        a = [a for b in a for a in b]
        if self.__x%11 == 0:
            temp = a[0]; a[0] = a[1]; a[1] = temp
            temp = a[5]; a[5] = a[7]; a[7] = temp
        if self.__abcd[0]-1 == self.__abcd[3]:
            temp = a[2]; a[2] = a[3]; a[3] = temp
            temp = a[6]; a[6] = a[8]; a[8] = temp
        if self.__x in highly_composite_numbers or self.__y in highly_composite_numbers:
            temp = a[0:4]; a[0:4] = a[5:]; a[5:] = temp
        if self.__x in perfect_squares and self.__y in perfect_squares:
            a = a[::-1]
        return "".join(a)

    def solve(self):
        '''
        Solve the Gamepad module

        Return
            str: The command to be submitted
        '''
        ans = self.__calculate()
        return ans