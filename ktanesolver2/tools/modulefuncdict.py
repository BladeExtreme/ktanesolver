import os
import inspect
from ..modules import *

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def header(name):
    clear_screen()
    print("-"*40)
    print(""*20+"KTANE SOLVER"+""*20)
    print("-"*40)
    print(f"MODULE - {name.upper()}")

def whosonfirst_function(edgework, solved):
    try:
        instructions = '''INSTRUCTIONS:
- For display, enter the word that appears on the the module's display
- For buttons, enter each button for each input. There are 6 six inputs. The orders should be like as below (starting from 1 to 6)
- NOTE: Not following the order could cause a wrong answer!

Order:
1   2
3   4
5   6

'''
        for x in range(3):
            text = "who\'s on first"
            header(text)
            print(instructions)
            print(f"Stage {x+1} of 3")

            disp = input("Display: ").lower()
            print("Buttons: ",end =""); buttons = [input()]
            for a in range(5):
                buttons += [input(f"{' '*len('Buttons: ')}").lower()]
            m = whosonfirst(edgework, disp, buttons)
            print(f"\nSOLVE - {m.solve()[1]}\n")
            input()
    except: return text

def keypad_function(edgework, solved):
    try:
        instructions = '''INSTRUCTIONS:
 - Enter the word for each symbol that appears on the module
 - The name for each symbol can be seen on the image:
'''
        text = "keypad"
        header(text)
        input_text = input("Symbols: ").lower().split()
        m = keypad(edgework, input_text)
        print(f"\nSOLVE - {m.solve()}")
    except: return text

def simonsays_function(edgework, solved):
    try:
        text = "simon says"
        header(text)
        color_seq = tuple(input("Color Sequence: ").lower().split())
        while 'exit' not in color_seq:
            m = simonsays(edgework, color_seq)
            print(f"\nSOLVE - {m.solve()}\n")
            color_seq = tuple(input("Color Sequence: ").lower().split())
    except: return text

def maze_function(edgework, solved):
    try:
        text = "maze"
        header(text)
        m = maze(edgework, tuple(input("Maze Indicator: ").split()), input("Player: "), input("Target: "))
        print(f"\nSOLVE - ")
        for a in m.solve():
            print("  "+a.capitalize())
    except: return text

def wires_function(edgework, solved):
    try:
        text = "wires"
        header(text)
        m = wires(edgework, input("Wire Colors: ").split())
        print(f"\nSOLVE - {m.solve()}")
    except: return text

def button_function(edgework, solved):
    try:
        text = "button"
        header(text)
        m = button(edgework, input("Color: "), input("Label: "))
        print(f"\nSOLVE - {m.solve()}")
    except: return text