from time import sleep

import button


class Solver:
    def __init__(self, engine=None):
        self.__engine = engine
        self.__puzzle = [[]]
        self.__solutions = []
        self.__sleep_time = 0
        self.__speeds = ({'name': 'Slowest', 'delay': 0.1},
                         {'name': 'Slow',    'delay': 0.05},
                         {'name': 'Normal',  'delay': 0.025},
                         {'name': 'Fast',    'delay': 0.0125},
                         {'name': 'Fastest', 'delay': 0})

    def set_puzzle(self, puzzle):
        self.__puzzle = puzzle
        self.__solutions = []

    def get_puzzle(self):
        return self.__puzzle

    def get_num_sol(self):
        return len(self.__solutions)

    def solve(self, attempt=None, i=0, j=0, single=True):
        if not single and self.get_num_sol() > 1:
            return
        if not attempt:
            attempt = [x for x in build_attempt(self.__puzzle)]
        if j < 8:
            new_pos = [i, j+1]
        else:
            new_pos = [i + 1, 0]
        try:
            if attempt[i][j] != 0:
                if single:
                    return self.solve(attempt, new_pos[0], new_pos[1], single)
                else:
                    self.solve(attempt, new_pos[0], new_pos[1], single)
        except IndexError:
            if single:
                self.__puzzle = attempt
                return True
            else:
                self.__solutions.append([x for x in build_attempt(attempt)])
                return

        valid_nums = check_sections(attempt, i, j)
        original = attempt[i][j]
        for num in valid_nums:
            attempt[i][j] = num
            if single:
                self.update(i, j, num)
            if (i, j) != (8, 8):
                if self.solve(attempt, new_pos[0], new_pos[1], single):
                    if single:
                        return True
                    else:
                        self.solve(attempt, new_pos[0], new_pos[1], single)
            else:
                if single:
                    self.__puzzle = attempt
                    return True
                else:
                    self.__solutions.append([x for x in build_attempt(attempt)])

        if single:
            self.update(i, j)
            attempt[i][j] = 0
            return False
        else:
            attempt[i][j] = original

    def update(self, i, j, num=None):
        if num is None:
            pressed = self.__engine.update((i, j), convert=True)
        else:
            pressed = self.__engine.draw_font(str(num), (i, j), convert=True)
        self.set_sleep(pressed)
        if self.__sleep_time:
            sleep(self.__sleep_time)

    def set_sleep(self, pressed):
        if not isinstance(pressed, button.Button):
            return
        for speed in self.__speeds:
            if pressed.get_name() == speed['name'].lower():
                self.__engine.create_speed_buttons(False)
                self.__sleep_time = speed['delay']
                self.__engine.draw_font(speed['name'], size=15, rect=pressed.get_rect(), bg_color=(25, 25, 25))
                break


def build_attempt(puzzle):
    for i in range(9):
        lst = []
        for j in range(9):
            lst.append(puzzle[i][j])
        yield lst


def check_sections(puzzle, i, j):
    puzzle[i][j] = 0
    col = [puzzle[i][x] for x in range(9)]
    row = [puzzle[x][j] for x in range(9)]
    block = []
    for x in range(9):
        for y in range(9):
            if x // 3 == i // 3 and y // 3 == j // 3:
                block += [puzzle[x][y]]
    return [k for k in range(1, 10) if all(k not in z for z in [row, col, block])]
