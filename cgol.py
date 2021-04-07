import sys

# Python 3.4.10 (default, Nov 14 2019, 22:17:56) 
# [GCC 5.4.0 20160609] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import sys                                                                                         
# >>> sys.hexversion
# 50596592

# require at least python 3.4.10

minimum_python_version = 50596592 # 

if (sys.hexversion < minimum_python_version):
    exit("Minimum Python version for this program is 3.4.10 (50596592)")


import time
import os

from ctypes import *

if (os.name == 'nt'):
    import msvcrt
elif (os.name == 'posix'):
    import tty

# Colorama
# https://pypi.org/project/colorama/#description
# Makes ANSI escape character sequences (for producing colored terminal text and cursor positioning) work under MS Windows.

#from colorama import init
from colorama import *
init()

debug = 0

""" Convert bytes to int? - StackOverflow

https://stackoverflow.com/questions/34009653/convert-bytes-to-int

Assuming you're on at least 3.2, there's a built in for this:

int.from_bytes( bytes, byteorder, *, signed=False )

...

The argument bytes must either be a bytes-like object or an iterable producing bytes.

The byteorder argument determines the byte order used to represent the integer. If byteorder 
is "big", the most significant byte is at the beginning of the byte array. If byteorder is 
"little", the most significant byte is at the end of the byte array. To request the native 
byte order of the host system, use sys.byteorder as the byte order value.

The signed argument indicates whether two’s complement is used to represent the integer.
 """

def int_from_bytes(i):
    return int.from_bytes(i, "big")

def clear_screen():
    if (os.name == 'nt'):
        os.system('cls')
    elif (os.name == 'posix'):
        os.system('clear')
    
def int_from_bytes(i):
    return int.from_bytes(i, "big")

def home_cursor():

    print(Cursor.POS(1, 1), end = '')

    return

    # if (os.name == 'nt'):
    #     ###########################################################################
    #     # This code is from: "Terminal control/Cursor positioning - Rosetta Code
    #     # "https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python

    #         STD_OUTPUT_HANDLE = -11

    #         class COORD(Structure):
    #             pass

    #         COORD._fields_ = [("X", c_short), ("Y", c_short)]

    #         def print_at(r, c, s):
    #             h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    #             windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

    #             c = s.encode("windows-1252")
    #             windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)

    #         print_at(0, 0, "")
    #     # end code from "Terminal control/Cursor positioning - Rosetta Code
    #     ###########################################################################
    # elif (os.name == 'posix'):
    #     # https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python
    #     # Using ANSI escape sequence, where ESC[y;xH moves curser to row y, col x:
    #     print("\033[0;0")

        


    #     #print('%s%s%s%s' % (pos(MINY, MINX), Fore.WHITE, Back.BLACK, Style.NORMAL), end='')
        
    # else:
    #     exit(-1)


# START code from https://code.activestate.com/recipes/134892/
# GETCH()-LIKE UNBUFFERED CHARACTER READING FROM STDIN ON BOTH WINDOWS AND UNIX (PYTHON RECIPE)
# A small utility class to read single characters from standard input, on both Windows and UNIX systems. It provides a getch() function-like instance.
# Created by Danny Yoo on Fri, 21 Jun 2002 (PSF)



class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

# END code from https://code.activestate.com/recipes/134892/

def get_keyboard_key():
    key = getch()
    if ( type(key) == type(b'q') ):
        return chr(int.from_bytes(key, "big"))
    elif ( type(key) == type('q') ):
        return(key)
    else:
        print('Unexpected input [', key, ']', "of type ", type(key))
        exit(-1)

    #debug_info_print()

    #exit(-1) # debug
    return key
    
def init_field(fsize):
    """
    Docstring for init_field(size)
    """
    field = fsize * [0]
    for x in range(0, fsize):
        field[x] = fsize * [0]
    return field

def display_field(dfField, size):
    # if dfField is None:
    #     error("In display_field: dfField is None")
    #     return

    #if(debug != 1):
    #    clear_screen()
# moved up # from ctypes import *

    home_cursor()

    #print('> <-- cursor homed  ', end=' ')
    #exit(-1)

    for col in range(1, size):
        if ((col % 10) == 0):
            print(int(col / 10), end = ' ')
            #print(col, end = ' ')

        else:
            print(' ', end = ' ')
    print('')
    print('  ', end=' ')
    for col in range(0, size):
        print(col % 10, end = ' ')

    print('')

    for row in range(0, len(dfField)):
        row_string = str(row)
        print(row_string.rjust(2), end = ' ')
        for col in range(0, len(dfField[row]) ):
            # print( len(dfField[row]), end = '' )

            # ◌ □ ■  ▪▫ . . ┼ ˖

            if dfField[col][row] == 0:
                print('˖ ', end = '')
                #print(dfField[col][row], end = ' ')
            else:
                print('■ ', end = '')
                #print(dfField[col][row], end = ' ')
        print('')

def process_field(in_field, out_field):
    # ASSUMES: square grid
    grid_len = len(in_field[0])

    if (debug == 1):
        print('grid_len', grid_len)

    for row in range(0, grid_len):
        for col in range(0, grid_len):

            if (debug == 1):
                print('(process_field ***new cell***)[c,r=', col, row, ']')

            neighbors = 0

            out_field[col][row] = 0  # assume death

            #range(-1,1+1):
            for yoff in [-1, 0, 1]:
                 #range(-1,1+1):
                for xoff in [-1, 0, 1]:
                    y = row + yoff
                    yf = y
                    x = col + xoff
                    xf = x
                    #print('xoff,yoff=', xoff, yoff)
                    #print('x, xf, y, yf=', x, xf, y, yf)
                    if ( not ( (yoff == 0) and (xoff == 0) ) ):
######################### optimize this with modulo arithmatic:
                        if (y < 0):
                            yf = len(in_field[0]) - 1
                        elif (y >= len(in_field[0])):
                            yf = 0

                        if (x < 0):
                            xf = len(in_field[0]) - 1
                        elif(x >= len(in_field[0])):
                            xf = 0
                        #print('x, xf, y, yf=', x, xf, y, yf)
                        # print('in_field[xf, yf]=', in_field[xf, yf])
                        #print('in_field[xf][yf]=', in_field[xf][yf])
                        #exit()

                        if (debug == 1):
                            print('Added neighbor: x, y, xf, yf, in_field[xf][yf],neighbors', x, y, xf, yf, in_field[xf][yf],neighbors )

                        neighbors = neighbors + in_field[xf][yf]
            if (debug == 1):
                print('* Cell contents and TOTAL neighbors:', in_field[col][row],neighbors )

            if (in_field[col][row] == 0):
                if (neighbors == 3):
                    out_field[col][row] = 1
                    if (debug == 1):
                        print('**************')
                        print('*** Birth! :D ***')
                        print('**************')
            # in_field[col][row] == 1
            elif ( (neighbors == 2) or (neighbors == 3) ):
                if (debug == 1):
                    print('**************')
                    print('*** Remain ***')
                    print('**************')
                out_field[col][row] = 1
            else:
                out_field[col][row] = 0
                if (debug == 1):
                    print('**************')
                    print('*** Death :( ***')
                    print('**************')

            #print('.')
    #return

def copy_field(in_field, out_field):
    # ASSUMES: square grid
    grid_len = len(in_field[0])

    if (debug == 1):
        print('grid_len', grid_len)

    for row in range(0, grid_len):
        for col in range(0, grid_len):
            in_field[col][row] = out_field[col][row]

    return

def edit_field(in_field, out_field):
    _MODE_INIT = 1
    _MODE_EDIT = 2
    _MODE_RUN  = 3

    mode = _MODE_INIT

    return


def main():
    # check OS
    if not (os.name in ['nt', 'posix'] ):
        print(os.name,' is not supported, exiting.')

    size = 15 # Code assumes square grid!

    if (debug == 1):
        print('=========================================================================')
        print('=========================================================================')
        print('=========================================================================')
        print('=========================================================================')
    else:
        clear_screen()

    afield = init_field(size)
    bfield = init_field(size)

# random start position ??

# Glider:
    afield[1][3] = 1
    afield[3][3] = 1
    afield[2][4] = 1
    afield[3][4] = 1
    afield[2][5] = 1

    inputchar = ' '
    #debugcounter = 0
    while (True):
        display_field(afield, size)
        print('Choose:')
        print('e - edit starting position')
        print('r - run simulation (^C to quit)')
        print('q - quit')

        #print(debugcounter, end=' ')

        inputchar = get_keyboard_key()
        # inputchar = 'q'

        if (inputchar == 'e'):
            edit_field(afield, bfield)
            copy_field(afield, bfield)
        elif (inputchar == 'q'):
            #crap = 1 / 0
            #print('You entered[', inputchar, ']')
            sys.exit(1)
        elif (inputchar == 'r'):
            # print('You entered[', inputchar, ']')
            while (True):
                # print('while loop [', inputchar, ']')
                display_field(afield, size)
                time.sleep(0.085)
                process_field(afield, bfield)
                copy_field(afield, bfield)
                #afield = bfield

                # print(afield[0] is afield[1])
                # print(afield[0][0] is afield[1][0])
        # debugging:
        # else:
        #    print('You entered[', inputchar, '] with ord() [', ord(inputchar), ']')



if (__name__ == '__main__'):
    main()
# else:
#     print("Since __name__ is not \"__main__\" I'll not execute the code")

""" Conway's Game of Life - Wikipedia

https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Rules[edit]
The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
These rules, which compare the behavior of the automaton to real life, can be condensed into the following:

Any live cell with two or three live neighbours survives.
Any dead cell with three live neighbours becomes a live cell.
All other live cells die in the next generation. Similarly, all other dead cells stay dead.
The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick. Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.

 """


# 5c842acef43ef9332b56b787a7f56785 *cgol.py
