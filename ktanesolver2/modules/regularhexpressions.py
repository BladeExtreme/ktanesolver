import re
from ..edgework import edgework

class regularhexpressions(edgework):
    __table = [
        [r".*O.*H.*", r"....", r".*[^O]N.*", r"A.*", r".*O.*E.*", r".*(ER|RE).*"],
        [r".*R[^E].*", r"[^ASTERISK]+", r".*[AEIOU].[AEIOU].*", r".*(OW|WO).*", r".*M[^O].*", r".*W(HA|HI|A).*"],
        [r".*O", r".*OT.*", r"....?", r".*[OU][MN].*", r".*E", r".*F.*T.*"],
        [r".....", r".*[^O]T.*", r"D.*", r".*I.*T.*", r".*(FI|IF).*", r".*F[^O].*"],
        [r"[^BRACKET]+", r".*[^AEIOU][^AEIOU].*", r".*(NO|ON).*", r".*U[^G].*", r".*OL?[DT].*", r".*[AEIOU][AEIOU].*"],
        [r".*HT.*", r".....?", r".*[BT][OE].*", r".*H", r".*OW.*", r"......"],
        [r".*[^H]T.*", r"H.*", r".*B.*T.*", r"..", r".*B[^O].*", r"[^REFUTE]+"],
        [r".*[^AEIOU][^AEIOU].", r".*(OT|TO).*", r".*O[^W].*", r"[^STRAIGHT]+", r".*[AEIOU]", r".*[AEIOU].*", r".*TH.*"],
        [r"(..)?.", r".*L[AEIOU].*", r".*P", r".*ON.*", r"..?", r".*[^E]A.*"],
        [r"W.*", r".*F.*R.*", r"...", r".*I[^N].*", r"[^ELIMINATE]+", r"[^AEIOU][^AEIOU].*"],
        [r".*(HT|TH).*", r".*E[^A].*", r"[^QUESTION]+", r".*[AEIOU]", r".*DI.*", r".*O[^T].*"],
        [r".[AEIOU].", r".*Y", r".*OR.*", r"...?", r".*[^S]T.*", r"U.*"]
    ]
    
    def __check(self, w,r,c):
        if not isinstance(w, dict): raise TypeError("words must be in dict")
        elif not all([isinstance(a, str) for a in w.keys()]): raise TypeError("The key of 'words' must be in str")
        elif not all([isinstance(a, str) for a in w.values()]): raise  TypeError("The values of 'words' must be in str")
        elif len(w)!=8: raise IndexError("Length of words must be exactly 8")
        elif not all([a in {'$','*','+','-','.','?','^','|'} for a in w.keys()]): raise ValueError("One of the regex symbol is invalid")
        elif (not isinstance(r, int)) or (not isinstance(c, int)): raise TypeError("Row and Column must be in int")
        elif r>11 or c>5 or r<0 or c<0: raise ValueError("Row and Column values cannot be bigger than 11 and 5, respectively and lower than 0")
        new_w = {}
        for _,__ in zip(w.keys(), w.values()):
            new_w[_.upper()] = __.upper()
        return new_w, r, c

    def __init__(self, edgework:edgework, words:dict, row:int, column:int):
        '''
        Initialize a new adjacentletters instance

        Library:
            re

        Args:
            edgework (edgework): The edgework of the bomb
            words (dict (keys=str, values=str)): The words that appear on each symbol. The symbol will act as the key in the dict, and the words that represent the symbol will be the value of those keys
            row (int): The initial row. The number that appear beside the "R" when moving the symbol to the top
            column (int): The initial column. The number that appear beside the "C" when moving the symbol to the top
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__words, self.__row, self.__col = self.__check(words, row, column)
    
    def __calculate(self):
        row_offset = (self.total_modules%11)+1
        col_offset = ((self.batt+len(self.ind))%5)+1
        row = (self.__row+row_offset)%12; col = (self.__col+col_offset)%6
        rowlist = sorted([row, self.__row]); collist = sorted([col, self.__col])
        regex_to_use = [self.__table[rowlist[0]][collist[0]], self.__table[rowlist[0]][collist[1]], self.__table[rowlist[1]][collist[1]], self.__table[rowlist[1]][collist[0]]]
        valid_symbols = []
        
        for a in regex_to_use:
            pattern = re.compile(a)
            for b,c in zip(self.__words.keys(), self.__words.values()):
                if bool(pattern.fullmatch(c)):
                    valid_symbols.append(b)
                    break
        return valid_symbols

    def solve(self):
        '''
        Solve the Regular Hexpressions module

        Returns:
            list (str, size=4): The symbols that needs to be submitted. The list is ordered where the first index is the topmost symbol and the last index is the bottom symbol
        '''
        valid_symbols = self.__calculate()
        return valid_symbols