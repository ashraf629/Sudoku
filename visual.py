import curses
import solve
import copy
import time

class board:
    def __init__(self,entries,green=[],yellow=[],red=[]):
        self.entries, self.green, self.yellow, self.red = entries, green, yellow, red

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def printPuzzle(stdscr, puzzle):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    for i in range(9):
        if i % 3 == 0: stdscr.addstr("+-------+-------+-------+\n")
        for j in range(9):
            if (i,j) in puzzle.green: colour = 1
            elif (i,j) in puzzle.yellow: colour = 2
            elif (i,j) in puzzle.red: colour = 3
            else: colour = 4
            if j % 3 == 0: stdscr.addstr('| ')
            stdscr.addstr(str(puzzle.entries[i][j])+' ',curses.color_pair(colour))
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

def createTimeline(puzzle):
    zeros = findZeros(puzzle)
    stack = [board(puzzle,red=zeros)]
    timeline = []
    while stack:
        current = stack.pop()
        timeline.append(current)
        if len(current.red)==0:
            break
        x,y = current.red[0]
        possible = solve.possibilities(current.entries,x,y)
        for n in possible:
            next = copy.deepcopy(current.entries)
            next[x][y] = n
            stack.append(board(next,current.green+current.yellow,[(x,y)],current.red[1:]))
    timeline.append(board(timeline[-1].entries,green=timeline[-1].green+timeline[-1].yellow))
    return timeline

def getUserInput(stdscr):
    userInput = ''
    char = stdscr.getch()
    print(curses.KEY_ENTER)
    while char not in [curses.KEY_ENTER,10]:
        print(char)
        userInput += chr(char)
        stdscr.addstr(chr(char))
        stdscr.refresh()
        char = stdscr.getch()
    return userInput

def main(stdscr):
    puzzle = '000000657702400100350006000500020009210300500047109008008760090900502030030018206'
    puzzle = [[int(puzzle[9*i+j]) for j in range(9)] for i in range(9)]
    sleepTime = 0.5
    
    stdscr.nodelay(True)
    timeline = createTimeline(puzzle)
    for puzzle in timeline:
        stdscr.addstr("Press s to skip to the end")
        stdscr.refresh()
        userInput = stdscr.getch()
        if userInput == ord('s'): break
        time.sleep(sleepTime)
        stdscr.clear()
        printPuzzle(stdscr,puzzle)
    
    stdscr.keypad(True)
    stdscr.nodelay(False)
    frame = len(timeline)
    while True:
        stdscr.clear()
        stdscr.addstr(f"Number of frames = {len(timeline)}\n")
        stdscr.addstr("Use left and right arrow keys to navigate through frames\n")
        stdscr.addstr("Press c to choose a specific frame\n")
        stdscr.addstr("Press any other key to exit\n")
        printPuzzle(stdscr,timeline[frame-1])
        stdscr.refresh()
        userInput = stdscr.getch()

        if userInput in [curses.KEY_LEFT, curses.KEY_SLEFT, curses.KEY_B1]:
            if frame > 1: frame -= 1
        elif userInput in [curses.KEY_RIGHT, curses.KEY_SRIGHT, curses.KEY_B3]:
            if frame < len(timeline): frame += 1
        elif userInput == ord('c'):
            stdscr.clear()
            stdscr.addstr(f"Enter a number from 1 to {len(timeline)} to view frame\n")
            stdscr.refresh()
            userInput = getUserInput(stdscr)
            while not (is_int(userInput) and 0 < int(userInput) < len(timeline) + 1):
                stdscr.clear()
                stdscr.addstr(f"Please enter a number from 1 to {len(timeline)}\n")
                stdscr.refresh()
                userInput = getUserInput(stdscr)
            frame = int(userInput)
        else:
            break

if __name__ == "__main__":
    curses.wrapper(main)