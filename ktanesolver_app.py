import os
from ktanesolver2 import modules, edgework
from ktanesolver2.tools.modulefuncdict import *

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    clear_screen()
    print("-"*40)
    print(""*20+"KTANE SOLVER"+""*20)
    print("-"*40)

def header_modules(name):
    print(f"MODULE - {name}")

input_text = ""
batt = 0; ind = []; ports = []; sn = 0; total_modules = 0; needy = 0; init_flag = False
egw = None
solved = 0; strikes = 0; autosolve = True
error_text = ""

while 1:
    header()
    if not init_flag:
        print("EDGEWORKS ")
        batt = input("Battery: ")
        hold = input("Battery Holder: ")
        ind = input("Indicators: ").split()
        n_ports = input("Number of Port Plates: ")
        ports = [input(f"{' '*len('Number of Port Plates')}  ").split() for a in range(int(n_ports))]
        sn = input("Serial Number: ")
        total_modules = input("Total Modules: ")
        needy = input("Needy: ")
        egw = edgework(int(batt), int(hold), ind, ports, sn, int(total_modules), int(needy), strikes)
        init_flag = True
    else:
        print("MAIN MENU")
        print("Solves - "+str(solved)+(chr(27)+"[94m\t[AUTO]"+chr(27)+"[0m" if autosolve else ""))
        print(f"Strikes - {egw.strikes}\n")
        print(chr(27)+'[91m[ERROR]'+chr(27)+'[0m - '+error_text+'\n\n' if error_text!='' else '', end="")

        input_text = input().lower().replace('\'', '')
        if len(input_text)>0:
            if input_text[0]!='-': input_text = input_text.replace(' ','')
            else: input_text = input_text.split()

            if input_text[0] == "-exit":
                break
            if input_text[0] == '-strike':
                if len(input_text)>2:
                    print(chr(27)+"[93mWARNING"+chr(27)+"[0m: Only 1 argument expected (number of strikes). This argument can be left with none to default at 1")
                    input()
                else:
                    egw.striked(int(input_text[1]) if len(input_text)>1 else 1)
            if input_text[0] == '-autosolve':
                state = True
                if len(input_text)>2:
                    print(chr(27)+"[93mWARNING"+chr(27)+"[0m: Only 1 argument expected (bool). This argument can be left with none to default at True")
                    input()
                if len(input_text)==2:
                    if input_text[1] not in ['false', 'true', '0', '1', 'on', 'off']:
                        print(chr(27)+"[93mWARNING"+chr(27)+"[0m: Autosolve only accepts: 'false', 'true', '0', '1', 'off', or 'on'")
                        input()
                    else:
                        state = ['false', 'true', '0', '1', 'off', 'on'].index(input_text[1])%2==1
                autosolve = state
            if input_text[0] == '-solve':
                if len(input_text)>2:
                    print(chr(27)+"[93mWARNING"+chr(27)+"[0m: Only 1 argument expected (int). This argument can be left with none to default at 1")
                    input()
                solved+=int(input_text[1]) if len(input_text)>1 else 1
            if not isinstance(input_text, list):
                if input_text in modules.__dict__ and callable(globals()[input_text+'_function']):
                    res = globals()[input_text+'_function'](egw, solved)
                    if res is not None:  
                        error_text = " ".join([a.capitalize() for a in res.split(' ')])
                        continue
                    else:
                        error_text = ''
                        input()
                    if autosolve: solved += 1
clear_screen()