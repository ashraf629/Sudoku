from copy import deepcopy

def possibilities(puzzle,i,j):
    notPossible = set()
    for x in range(9):
        if x == j: continue
        if puzzle[i][x] == 0: continue
        notPossible.add(puzzle[i][x])
    
    for x in range(9):
        if x == i: continue
        if puzzle[x][j] == 0: continue
        notPossible.add(puzzle[x][j])
    
    for x in range(i - i%3,i - i%3 + 3):
        for y in range(j - j%3,j - j%3 + 3):
            if (x,y) == (i,j): continue
            if puzzle[x][y] == 0:
                continue
            notPossible.add(puzzle[x][y])
    
    possible = list(range(1,10))
    for n in notPossible:
        possible.remove(n)
    return possible

def try_solve(puzzle):
    # returns solved puzzle if possible, returns False otherwise
    stack = [puzzle]
    while stack:
        current = stack.pop()
        foundZero = False
        for i in range(9):
            for j in range(9):
                if current[i][j] == 0:
                    x,y = i,j
                    foundZero = True
                    break
            if foundZero: break
        if not foundZero: return current
        possible = possibilities(current,x,y)
        for n in possible:
            next = deepcopy(current)
            next[x][y] = n
            stack.append(next)
    return False

if __name__ == '__main__':
    TESTCASES = 100
    with open('sudoku.csv') as file:
        # source https://www.kaggle.com/datasets/bryanpark/sudoku
        file.readline()
        quizzes = []
        solutions = []
        s = file.readline()
        for _ in range(TESTCASES):
            if not s: break
            quiz,sol = s.split(',')[0],s.split(',')[1].strip()
            puzzle = solution = [[0 for _ in range(9)] for _ in range(9)]
            for x in range(81):
                puzzle[x//9][x%9] = int(quiz[x])
                solution[x//9][x%9] = int(sol[x])
            quizzes.append(puzzle)
            solutions.append(solution)
            s = file.readline()
        for x in range(TESTCASES):
            assert solutions[x] == try_solve(quizzes[x])
