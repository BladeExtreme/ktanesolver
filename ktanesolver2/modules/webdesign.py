import re
from ..edgework import edgework

class webdesign(edgework):
    def __check(self, s,c):
        if not isinstance(s, str): raise TypeError("script must be in str")
        elif not isinstance(c, bool): raise TypeError("color_present must be in bool")
        return s.lower().replace(' ',''),c
    
    def __init__(self, edgework:edgework, script:str, color_present:bool):
        '''
        Initialize a webdesign instance

        Args:
            edgework (edgework): The edgework of the bomb
            script (str): The script that appears on the module
            color_present (bool): The state of the buttons if color exist on them
        '''
        super().__init__(edgework.batt ,edgework.hold, edgework.ind, edgework.ports, edgework.sn, edgework.total_modules, edgework.needy, edgework.strikes)
        self.__script, self.__state = self.__check(script, color_present)
    
    def __findthreshold(self):
        threshold = ''
        element_dict = {
            'body': False,
            'a': False,
            'h3': False,
            'blockquote': False,
            'div': False,
            'span': False,
            'img': False,
            'ul': False,
            'ol': False,
            'img': False,
            'b': False,
            'i': False,
            'iframe': False,
        }
        id_dict = {
            '#header': False,
            '#comments': False,
            '#msg': False,
            '#cover': False,
            '#content': False,
            '#sidebar': False,
            '#main': False,
            '#fullview': False,
            '#rating': False,
            '#sidebar': False,
            '#download': False,
        }
        classes_dict = {
            '.post': False,
            '.title': False,
            '.author': False,
            '.share': False,
            '.username': False,
            '.large': False,
            '.avatar': False,
            '.channel': False,
            '.rating': False,
            '.fullscreen': False,
            '.menu': False,
            '.reply': False
        }
        segments = [
            [
                ['body', 'a', 'h3', 'blockquote'], ['#header', '#comments'], ['.post', '.title', '.author']
            ], [
                ['div', 'span', 'img', 'a'], ['#msg', '#cover', '#content', '#sidebar'], ['.post', '.title', '.share']
            ], [
                ['div', 'img'], ['#main', '#comments', '#fullview'], ['.username', '.share', '.large']
            ], [
                ['ul', 'ol', 'img', 'b', 'i'], ['#sidebar'], ['.avatar', '.username']
            ], [
                ['div', 'iframe', 'b', 'i'], ['#main', '#rating', '#comments'], ['.username', '.share', '.channel']
            ], [
                ['body', 'iframe'], ['#rating', '#comments'], ['.rating', '.fullscreen']
            ], [
                ['div', 'h3', 'img', 'iframe'], ['#sidebar', '#download'], ['.menu', '.author']
            ], [
                ['body', 'div', 'img', 'blockquote'], ['#header', '#content', '#sidebar'], ['.avatar', '.reply']
            ]
        ]
        threshold_list = ["00FF00","8040C0","BADA55","03E61E","60061E","501337","B020E5","BEA61E"
        ]
        score = [0 for a in range(8)]

        for a in element_dict.keys(): element_dict[a] = True if bool(re.search(a+'#', self.__script[0][0])) or bool(re.search(a+'.', self.__script)) else element_dict[a]
        for a in id_dict.keys(): id_dict[a] = True if bool(re.search(a, self.__script)) else id_dict[a]
        for a in classes_dict.keys(): classes_dict[a] = True if bool(re.search(a, self.__script)) else classes_dict[a]
        
        for a in range(len(segments)):
            if any([element_dict[x] for x in segments[a][0]]): score[a]+=1
            if any([id_dict[x] for x in segments[a][1]]): score[a]+=1
            if any([classes_dict[x] for x in segments[a][2]]): score[a]+=1
        threshold = threshold_list[score.index(max(score))]

        return {b:threshold[a:a+2] for a,b in zip(range(0,len(threshold),2),['r','g','b'])}
    
    def __findtarget(self):
        target_idx = ['blue','yellow','red','green','white','orange','purple','magenta','gray']
        target_list = ['0000FF','FFFF00','FF0000','00FF00','FFFFFF','FFA500','800080','FF00FF','808080']
        target_list_ans = []

        for a in target_idx:
            target_list_ans += [x for x in re.finditer(a, self.__script)]
        result = target_list[target_idx.index(sorted(target_list_ans, key=lambda x: x.span()[0])[0].group())]
        
        return {b:result[a:a+2] for a,b in zip(range(0,len(result),2),['r','g','b'])}

    def __calculate(self):
        threshold = self.__findthreshold()
        target = self.__findtarget()
        lines = self.__script.count(';')
        score = 0; score += lines

        if int(target['r'], 16)<int(threshold['r'], 16): score+=3
        if int(target['g'], 16)>=int(threshold['g'], 16): score+=3
        if int(target['b'], 16)>int(threshold['b'], 16): score+=3
        
        score += (len(re.findall('margin:', self.__script))+len(re.findall('padding:', self.__script)))*2
        score += (len([a for a in re.finditer('border-radius:(\d+)(?:px|%)', self.__script) if not bool(re.search('0px', a.group())) and not bool(re.search('50%', a.group()))]) + \
                  len([a for a in re.finditer('border:(\d+)(?:px|%)', self.__script) if not bool(re.search('0px', a.group())) and not bool(re.search('50%', a.group()))]))
        score -= len([a for a in re.finditer('z-index:', self.__script) if not bool(re.search('position', a.group()))])
        for x in [a for a in re.finditer('font-family:(.*?)(?=\;)', self.__script)]:
            if bool(re.search("comicsansms", x.group())): score -=5
            else: score += 1
        for x in [a for a in re.finditer('box-shadow:(.*?)(?=\;)', self.__script)]+[a for a in re.finditer('text-shadow:(.*?)(?=\;)', self.__script)]:
            if bool(re.search("none", x.group())): continue
            else: score += 2
        
        score+= score if self.__state else -3
        while score<=0: score+=16
        
        score_str = str(score)
        while len(score_str)!=1:
            score_str = str(sum([int(a) for a in score_str]))
        
        if score_str in '2357': return 'Accept'
        elif score_str in '68': return 'Consider'
        else: return 'Reject'

    def solve(self) -> str:
        '''
        Solve the Web Design module

        Returns:
            str: The button that is correct to be pressed
        '''
        return self.__calculate()