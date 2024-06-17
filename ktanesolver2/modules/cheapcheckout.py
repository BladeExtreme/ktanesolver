from ..edgework import edgework

class cheapcheckout(edgework):
    __table = {
            'bananas': {'name': 'bananas', 'price':  0.87, 'category': 'fruit'},
            'broccoli': {'name': 'broccoli', 'price':  1.39, 'category': 'vegetable'},
            'candy canes': {'name': 'candy canes', 'price':  3.51, 'category': 'sweet'},
            'canola oil': {'name': 'canola oil', 'price':  2.28, 'category': 'oil'},
            'cereal': {'name': 'cereal', 'price':  4.19, 'category': 'grain'},
            'cheese': {'name': 'cheese', 'price':  4.49, 'category': 'dairy'},
            'chicken': {'name': 'chicken', 'price':  1.99, 'category': 'protein'},
            'chocolate bar': {'name': 'chocolate bar', 'price':  2.10, 'category': 'sweet'},
            'chocolate milk': {'name': 'chocolate milk', 'price':  5.68, 'category': 'dairy'},
            'coffee beans': {'name': 'coffee beans', 'price':  7.85, 'category': 'other'},
            'cookies': {'name': 'cookies', 'price':  2.00, 'category': 'sweet'},
            'deodorant': {'name': 'deodorant', 'price':  3.97, 'category': 'care product'},
            'fruit punch': {'name': 'fruit punch', 'price':  2.08, 'category': 'sweet'},
            'grape jelly': {'name': 'grape jelly', 'price':  2.98, 'category': 'sweet'},
            'grapefruit': {'name': 'grapefruit', 'price':  1.08, 'category': 'fruit'},
            'gum': {'name': 'gum', 'price':  1.12, 'category': 'sweet'},
            'honey': {'name': 'honey', 'price':  8.25, 'category': 'sweet'},
            'soda': {'name': 'soda', 'price':  2.05, 'category': 'sweet'},
            'spaghetti': {'name': 'spaghetti', 'price':  2.92, 'category': 'grain'},
            'steak':  {'name': 'steak', 'price':  4.97, 'category': 'protein'},
            'sugar': {'name': 'sugar', 'price':  2.08, 'category': 'sweet'},
            'tea': {'name': 'tea', 'price':  2.35, 'category': 'water'},
            'tissues':  {'name': 'tissues', 'price':  3.94, 'category': 'care product'},
            'ketchup': {'name': 'ketchup', 'price':  3.59, 'category': 'other'},
            'lemons':  {'name': 'lemons', 'price':  1.74, 'category': 'fruit'},
            'lettuce': {'name': 'lettuce', 'price':  1.10, 'category': 'vegetable'},
            'lollipops': {'name': 'lollipops', 'price':  2.61, 'category': 'sweet'},
            'lotion': {'name': 'lotion', 'price':  7.97, 'category': 'care product'},
            'mayonnaise': {'name': 'mayonnaise', 'price':  3.99, 'category': 'oil'},
            'mints': {'name': 'mints', 'price':  6.39, 'category': 'sweet'},
            'mustard': {'name': 'mustard', 'price':  2.36, 'category': 'other'},
            'oranges': {'name': 'oranges', 'price':  0.80, 'category': 'fruit'},
            'paper towels': {'name': 'paper towels', 'price':  9.46, 'category': 'care product'},
            'pasta sauce': {'name': 'pasta sauce', 'price':  2.30, 'category': 'vegetable'},
            'peanut butter': {'name': 'peanut butter', 'price':  5.00, 'category': 'protein'},
            'pork': {'name': 'pork', 'price':  4.14, 'category': 'protein'},
            'potato chips': {'name': 'potato chips', 'price':  3.25, 'category': 'oil'},
            'potatoes': {'name': 'potatoes', 'price':  0.68, 'category': 'vegetable'},
            'shampoo': {'name': 'shampoo', 'price':  4.98, 'category': 'care product'},
            'socks': {'name': 'socks', 'price':  6.97, 'category': 'other'},
            'tomatoes': {'name': 'tomatoes', 'price':  1.80, 'category': 'fruit'},
            'toothpaste': {'name': 'toothpaste', 'price':  2.50, 'category': 'care product'},
            'turkey': {'name': 'turkey', 'price':  2.98, 'category': 'protein'},
            'water bottles': {'name': 'water bottles', 'price':  9.37, 'category': 'water'},
            'white bread': {'name': 'white bread', 'price':  2.43, 'category': 'grain'},
            'white milk': {'name': 'white milk', 'price':  3.62, 'category': 'dairy'}
        }
    __daysoftheweek = {
        'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7
    }
    
    def __check(self, m, i, d):
        if not isinstance(m, float): raise TypeError("money must be in float")
        elif m<0.0: raise ValueError("money cannot be negative")
        elif not isinstance(i, list): raise TypeError("items must be in list")
        elif len(i)!=6: raise IndexError("Length of items must be 6")
        elif not isinstance(d, str): raise TypeError("day must be in str")
        elif d.lower() not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','mon','tue','wed','thu','fri','sat','sun']: raise ValueError("day must be the name of any day or the first three letters of it")
        elif not all([isinstance(a, dict) for a in i]): raise TypeError("Element of items must be in dict")
        inonweight = [a for a in i if all([b in ['item'] for b in a])]; iweight = [b for b in i if any([c in ['weight'] for c in b])]
        if len(inonweight)!=4 or len(iweight)!=2: raise IndexError("Amount of non-weighted items must be 4, and weighted items must be 2")
        elif not all([isinstance(x['item'], str) for x in inonweight]): raise TypeError("Value of non-weighted items must be in str")
        elif not all([isinstance(x['item'],str) and isinstance(x['weight'], float) for x in iweight]): raise TypeError("Value of weighted items must be in str for the item name, and float for the weight")
        elif not all([x['weight']>0 for x in iweight]): raise ValueError("Value of weight cannot be negative")
        return m, [{'item': a['item'].lower()} for a in inonweight]+[{'item': a['item'].lower(), 'weight': a['weight']} for a in iweight], self.__daysoftheweek[d[0:3].lower()]
    
    def __check1(self, m, i, w, d):
        if not isinstance(m, float): raise TypeError("money must be in float")
        elif m<0.0: raise ValueError("money cannot be negative")
        elif not isinstance(i, list): raise TypeError("itemnames must be in list")
        elif len(i)!=6: raise IndexError("Length of itemnames must be 6")
        elif not isinstance(w, list): raise TypeError("itemnames must be in list")
        elif len(w)!=2: raise IndexError("Length of weights must be 2")
        elif not isinstance(d, str): raise TypeError("day must be in str")
        elif d.lower() not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','mon','tue','wed','thu','fri','sat','sun']: raise ValueError("day must be the name of any day or the first three letters of it")
        elif not all([isinstance(a, str) for a in i]): raise TypeError("Element of itemnames must be in str")
        elif not all([isinstance(a, float) for a in w]): raise TypeError("Element of weights must be in float")
        elif not all([a>0 for a in w]): raise ValueError("Element of weights cannot be negative")
        return m, [{'item': i[a].lower()} for a in range(0,4)]+[{'item': i[a].lower(), 'weight': w[4-a]} for a in range(4,6)], self.__daysoftheweek[d[0:3].lower()]
    
    def __init__(self, edgework:edgework, money:float, day:str, itemnames:list|None=None, weights:list|None=None, items:list|None=None):
        '''
        Initialize a new cheapcheckout instance

        Args:
            edgework (edgework): The edgework of the bomb
            money (float): The money paid by the customer
            itemnames (list (str)): All of the item names. CAUTION: itemnames must be in sync with weights (only for the last 2 index)
            weights (list (float)): The weight of the weighted items. CAUTION: weights must be in sync with itemnames (weights are synced with the last 2 index of itemnames)
            items (list (dict)): The item lists on the module. Each dict must have a key of: 'item' or 'weight', if the item does have a weight indicated. If the item doesn't have a weight, then only the key 'item' is needed
            day (str): The day of the bomb generated
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        if items is not None:
            self.__money, self.__items, self.__day = self.__check(money, items, day)
        elif itemnames is not None and weights is not None:
            self.__money, self.__items, self.__day = self.__check1(money, itemnames, weights, day)
        else:
            raise TypeError("cheapcheckout.__init__() missing 1 or 2 required positional arguments: 'itemnames', 'weights' | 'items'")
        self.__ans = self.__calculate()
    
    def __round(self, a):
        return int(a*100)/100 if int(a*100)*2-int((a*100)/0.5)==0 else (int(a*100)+1)/100
    def __digitalroot(self, a):
        while int("".join([(x) for x in str(a) if x!='.']))>=10:
            a = sum([int(x) for x in str(a) if x!='.'])
        return a

    def __calculate(self):
        realitems = [self.__table[self.__items[a]['item']].copy() for a in range(0,4)]; realitems += [{'name': self.__table[self.__items[a]['item']].copy()['name'], 'price': self.__round(self.__table[self.__items[a]['item']].copy()['price']*self.__items[a]['weight']*0.25) if self.__day==5 else self.__round(self.__table[self.__items[a]['item']].copy()['price']*self.__items[a]['weight']), 'category': self.__table[self.__items[a]['item']].copy()['category']} for a in range(4,6)]
        if self.__day==7:
            for a in range(0, 4):
                if 's' in realitems[a]['name']: realitems[a]['price'] += 2.15
        elif self.__day==1:
            for a in [0,2,5]:
                realitems[a]['price'] -= realitems[a]['price']*0.15
                realitems[a]['price'] = self.__round(realitems[a]['price'])
        elif self.__day==2:
            for a in range(0,4):
                realitems[a]['price'] += self.__digitalroot(realitems[a]['price'])
                realitems[a]['price'] = self.__round(realitems[a]['price'])
        elif self.__day==3:
            for a in range(len(realitems)):
                highest = max([int(x) for x in str(realitems[a]['price']) if x!='.'])
                lowest = min([int(x) for x in str(realitems[a]['price']) if x!='.'])
                temp = str(realitems[a]['price']); temp.replace(lowest, 'X'); temp.replace(highest, lowest); temp.replace('X', highest)
                realitems[a]['price'] = float(temp)
        elif self.__day==4:
            for a in range(0, len(realitems), 2):
                realitems[a]['price'] = self.__round(realitems[a]['price']*0.5)
        elif self.__day==6:
            for a in range(len(realitems)):
                if realitems[a]['category'] == 'sweet':
                    realitems[a]['price'] -= realitems[a]['price']*0.35
                    realitems[a]['price'] = self.__round(realitems[a]['price'])
        return self.__round(sum([a['price'] for a in realitems]))

    def solve(self, newmoney:float|None=None):
        '''
        Solve the Cheap Checkout module

        Args:
            newmoney (float|None): The new money given by the customer. By default it's None
        Returns:
            str: If the answer is negative, it will return 'not enough money' indicating the current given money is not enough for the total price of the items. Otherwise, it will return the correct change after the transaction.
        '''
        if newmoney is not None:
            if not isinstance(newmoney, float): raise TypeError("newmoney must be in float")
            elif newmoney<0: raise ValueError("newmoney cannot be negative")
            self.__money = newmoney
        if self.__round(self.__money-self.__ans)<0: return 'not enough money'
        else: return str(self.__round(self.__money-self.__ans))+'0' if len(str(self.__round(self.__money-self.__ans)))==3 else str(self.__round(self.__money-self.__ans))