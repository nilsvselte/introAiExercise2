# Sudoku problems.
# The CSP.ac_3() and CSP.backtrack() methods need to be implemented

from csp import CSP, alldiff


def print_solution(solution):
    """
    Convert the representation of a Sudoku solution, as returned from
    the method CSP.backtracking_search(), into a Sudoku board.
    
    """
    width = 9
    for row in range(width):
        for col in range(width):
            print(solution[f'X{row+1}{col+1}'], end=" ")
            if col == 2 or col == 5:
                print('|', end=" ")
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')


sodukos = ['./sudoku_easy.txt','./sudoku_medium.txt','./sudoku_hard.txt','./sudoku_very_hard.txt']

# Choose Sudoku problem
def sudoku(difficulty):
    grid = open(difficulty).read().split()

    width = 9
    box_width = 3

    domains = {}
    for row in range(width):
        for col in range(width):
            if grid[row][col] == '0':
                domains[f'X{row+1}{col+1}'] = set(range(1, 10))
            else:
                domains[f'X{row+1}{col+1}'] = {int(grid[row][col])}

    edges = []
    for row in range(width):
        edges += alldiff([f'X{row+1}{col+1}' for col in range(width)])
    for col in range(width):
        edges += alldiff([f'X{row+1}{col+1}' for row in range(width)])
    for box_row in range(box_width):
        for box_col in range(box_width):
            cells = []
            edges += alldiff(
                [
                    f'X{row+1}{col+1}' for row in range(box_row * box_width, (box_row + 1) * box_width)
                    for col in range(box_col * box_width, (box_col + 1) * box_width)
                ]
            )

    csp = CSP(
        variables=[f'X{row+1}{col+1}' for row in range(width) for col in range(width)],
        domains=domains,
        edges=edges,
    )



    def run_normal():
        print(csp.ac_3())
        print_solution(csp.backtracking_search())

    def run_domains():
        csp.ac_3();
        items = [str(item) for item in csp.domains.items()]
        for item in items:
            print(item)
    def measure_runtimes():
        import time
        start = time.time()
        csp.ac_3()
        print("AC-3 runtime: ", time.time()-start)
        start = time.time()
        csp.backtracking_search()
        print("Backtracking runtime: ", time.time()-start)

    def measure_number_of_times_backtrack_called():
        print("number of times backtrack called",csp.backtracking_search(True)[1])
        print("number of times accrutally backtracked called",csp.backtracking_search(True)[2])

    # Change to run normal for running normally and run_domains for printing domains etc.
    measure_number_of_times_backtrack_called()

for soduko in sodukos:
    print("difficulty: ",soduko)
    sudoku(soduko)

# Expected output after implementing csp.ac_3() and csp.backtracking_search():
# True
# 7 8 4 | 9 3 2 | 1 5 6
# 6 1 9 | 4 8 5 | 3 2 7
# 2 3 5 | 1 7 6 | 4 8 9
# ------+-------+------
# 5 7 8 | 2 6 1 | 9 3 4
# 3 4 1 | 8 9 7 | 5 6 2
# 9 2 6 | 5 4 3 | 8 7 1
# ------+-------+------
# 4 5 3 | 7 2 9 | 6 1 8
# 8 6 2 | 3 1 4 | 7 9 5
# 1 9 7 | 6 5 8 | 2 4 3
