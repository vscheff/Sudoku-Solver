from random import randint
from itertools import product
from solve import Solver, check_sections
from json import load, dump


def main():
    # json is populated with pre-computed, valid sudoku puzzles represented as 2D arrays of ints
    with open('puzzle_store.json', 'r') as inFile:
        puzzle_dic = load(inFile)
    save_flag = False  # We only overwrite the previous puzzle store if we compute >1 puzzle
    try:
        for i in range(int(input('Mazes: '))):
            puzzle, clues = construct_valid(i + 1)
            puzzle_dic['puzzles'].append({'puzzle': puzzle, 'clues': clues})
            save_flag = True
    # Save any computed puzzles in case the user decides to terminate the program prematurely
    except KeyboardInterrupt:
        if save_flag:
            save_puzzles(puzzle_dic)
        exit('Program quit... Good bye!')
    save_puzzles(puzzle_dic)
    exit('Program quit... Good bye!')


# Saves computed puzzles to a json file
# @ param puzzles - dictionary of puzzles to be dumped to json
def save_puzzles(puzzles):
    with open('puzzle_store.json', 'w') as outFile:
        dump(puzzles, outFile, indent=1)
    print(f'\nNumber of mazes: {len(puzzles["puzzles"])}')


# Constructs valid sudoku puzzles with a local minima number of clues
# @ param puz_num - ordinal value of the puzzle
def construct_valid(puz_num):
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    puzzle = recursive_construct(0, 0, puzzle)
    print('\nCreated this random puzzle:')
    print_puzzle(puzzle)
    coords = [i for i in product([i for i in range(9)], [j for j in range(9)])]
    clues = 81
    solver = Solver()
    while len(coords) > 0:
        i, j = coords.pop(randint(0, len(coords) - 1))
        original = puzzle[i][j]
        puzzle[i][j] = 0
        solver.set_puzzle(puzzle)
        print(f'\nPuzzle: {puz_num}, Coordinate: {81 - len(coords)}, Clues: {clues}'
              f'\nTrying to remove #{original} in coordinate ({i}, {j}):')
        print_puzzle(puzzle)
        solver.solve(single=False)
        if solver.get_num_sol() != 1:
            puzzle[i][j] = original
            print('bad')
        else:
            clues -= 1
            print('good')

    print(f'\nSolvable puzzle with {clues} clues below: ')
    print_puzzle(puzzle)
    return puzzle, clues


def recursive_construct(i, j, puzzle):
    if i == 9:
        return puzzle
    if j < 8:
        new_pos = [i, j + 1]
    else:
        new_pos = [i + 1, 0]
    valid_nums = check_sections(puzzle, i, j)
    while len(valid_nums) > 0:
        rand = valid_nums.pop(randint(0, len(valid_nums) - 1))
        puzzle[i][j] = rand
        if solution := recursive_construct(new_pos[0], new_pos[1], puzzle):
            return solution
    puzzle[i][j] = 0
    return False


def print_puzzle(puzzle):
    for i in puzzle:
        print(i)


if __name__ == '__main__':
    main()
