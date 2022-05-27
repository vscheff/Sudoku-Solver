from random import randint
from json import load
import solve as s
import graphics as g
import button as b


class Control:

    def __init__(self, filename='puzzle_store.json'):
        with open(filename, 'r') as inFile:
            self.puzzles = load(inFile)
        self.puzzle = {}
        self.num_puzzles = len(self.puzzles['puzzles'])
        self.engine = g.Engine()
        self.s = s.Solver(self.engine)
        self.user_attempt = []
        self.bad_coords = []

    def initialize(self):
        self.engine.initialize()

    def main_loop(self):
        while True:
            if not (pressed := self.engine.event_loop()):
                continue
            if not isinstance(pressed, b.Button):
                continue
            self.s.set_sleep(pressed)
            if pressed.get_name() == 'new puzzle':
                self.select_maze()
                continue
            if self.puzzle:
                if pressed.get_name() == 'solve':
                    self.select_maze(new=False)
                    self.solve_maze()
                elif pressed.get_name() == 'clear':
                    self.select_maze(new=False)
                elif isinstance(pressed, b.GridButton) and any(i.count(0) > 0 for i in self.s.get_puzzle()):
                    self.handle_input(pressed)

    def select_maze(self, new=True):
        if new:
            rand = randint(0, len(self.puzzles['puzzles']) - 1)
            self.puzzle = self.puzzles['puzzles'][rand]
            self.engine.puzzle_information(rand + 1, self.puzzle['clues'], self.num_puzzles)
        self.s.set_puzzle(self.puzzle['puzzle'])
        self.user_attempt = [i for i in s.build_attempt(self.puzzle['puzzle'])]
        self.engine.draw_puzzle(self.puzzle['puzzle'])

    def handle_input(self, pressed):
        i = pressed.get_i()
        j = pressed.get_j()
        if self.puzzle['puzzle'][i][j] == 0:
            valid_nums = s.check_sections(self.user_attempt, i, j)
            bg_color = self.engine.get_color((i, j), convert=True)
            position = pressed.get_position()
            bg_rect = pressed.get_rect()
            self.engine.update(rect=bg_rect, color=(25, 25, 25))
            while True:
                key_pressed = self.engine.event_loop()
                if key_pressed is None:
                    continue
                elif not isinstance(key_pressed, int):
                    continue
                elif key_pressed == 0:
                    self.engine.update(position, rect=bg_rect, color=bg_color)
                    self.user_attempt[i][j] = 0
                    self.check_coords()
                    break
                color = None
                if key_pressed not in valid_nums:
                    color = (225, 25, 0)
                    self.bad_coords.append((i, j))
                self.engine.update(rect=bg_rect, color=bg_color)
                self.engine.draw_font(str(key_pressed), (i, j), color=color, convert=True)
                self.user_attempt[i][j] = key_pressed
                self.check_coords()
                break

    def check_coords(self):
        for (i, j) in self.bad_coords:
            puzzle = [x for x in s.build_attempt(self.user_attempt)]
            if self.user_attempt[i][j] in s.check_sections(puzzle, i, j):
                self.engine.draw_font(str(self.user_attempt[i][j]), (i, j), convert=True)
                self.bad_coords.remove((i, j))

    def solve_maze(self):
        if self.s.solve():
            self.engine.maze_solved()
        else:
            print('\nNo Solution!')
