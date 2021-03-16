import time
import os
import msvcrt
import sys

# temp for test?
from ctypes import *
#

debug = 0

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
    #    os.system('cls')

# moved up # from ctypes import *

 ###########################################################################
 # This code is from: "Terminal control/Cursor positioning - Rosetta Code
 # "https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python

    STD_OUTPUT_HANDLE = -11

    class COORD(Structure):
        pass

    COORD._fields_ = [("X", c_short), ("Y", c_short)]

    def print_at(r, c, s):
        h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

        c = s.encode("windows-1252")
        windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)

    print_at(0, 0, "")
 # end code from "Terminal control/Cursor positioning - Rosetta Code
 ###########################################################################

    print('    ', end=' ')

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

def edit_field(in_field, out_field, mode):

    return


def main():

    size = 45 # Code assumes square grid!

    if (debug == 1):
        print('=========================================================================')
        print('=========================================================================')
        print('=========================================================================')
        print('=========================================================================')
    else:
        os.system('cls')

    afield = init_field(size)
    bfield = init_field(size)

# random start position ??

# Glider:
    afield[1][3] = 1
    afield[3][3] = 1
    afield[2][4] = 1
    afield[3][4] = 1
    afield[2][5] = 1

    # main loop modes
    _MODE_INIT = 1
    _MODE_EDIT = 2
    _MODE_RUN  = 3
    # editor modes


    mode = _MODE_INIT
    inputchar = ' '
    debugcounter = 0
    while (True):
        display_field(afield, size)
        print('Choose:')
        print('e - edit starting position')
        print('r - run simulation')
        print('q - quit')

        print(debugcounter, end=' ')

        inputchar = msvcrt.getch()
        if (inputchar == b'e'):
            edit_field(afield, bfield)
            copy_field(afield, bfield)
        elif (inputchar == b'q'):
            #crap = 1 / 0
            #print('You entered[', inputchar, ']')
            sys.exit(1)
        elif (inputchar == b'r'):
            print('You entered[', inputchar, ']')
            while (True):
                print('while loop [', inputchar, ']')
                display_field(afield, size)
                #time.sleep(0.085)
                process_field(afield, bfield)
                copy_field(afield, bfield)
                #afield = bfield

                # print(afield[0] is afield[1])
                # print(afield[0][0] is afield[1][0])



main()

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


