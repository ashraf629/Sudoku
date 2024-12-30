import curses
import solve
import copy
import time

def printPuzzle(stdscr, puzzle):
    stdscr.clear()
    puzzle,green,yellow,red = puzzle
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    for i in range(9):
        if i % 3 == 0: stdscr.addstr("+-------+-------+-------+\n")
        for j in range(9):
            if (i,j) in green:
                colour = 1
            elif (i,j) in yellow:
                colour = 2
            elif (i,j) in red:
                colour = 3
            else:
                colour = 4
            if j % 3 == 0: stdscr.addstr('| ')
            stdscr.addstr(str(puzzle[i][j])+' ',curses.color_pair(colour))
        stdscr.addstr('|\n')
    stdscr.addstr("+-------+-------+-------+\n")
    stdscr.refresh()

def findZeros(puzzle):
    out = []
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                out.append((i,j))
    return out

def main(stdscr):
    puzzle = [[5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]]
    zeros = findZeros(puzzle)
    stack = [(puzzle,[],[],zeros)]
    while stack:
        current = stack.pop()
        puzzle,green,yellow,zeros = current
        printPuzzle(stdscr,current)
        time.sleep(0.1)
        if not zeros:
            printPuzzle(stdscr,(puzzle,[],[],[]))
            break
        x,y = zeros[0]
        possible = solve.possibilities(puzzle,x,y)
        for n in possible:
            next = copy.deepcopy(puzzle)
            next[x][y] = n
            stack.append((next,green+yellow,[(x,y)],zeros[1:]))
    stdscr.getch()

curses.wrapper(main)