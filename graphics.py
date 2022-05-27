import pygame as pg
import errors as er
from button import Button, GridButton
from itertools import product


class Engine:
    def __init__(self, width=550, height=425):
        self.colors = {'dark_bg':     (43, 43, 43),
                       'light_bg':    (49, 51, 53),
                       'line':        (60, 63, 65),
                       'text':        (175, 177, 179),
                       'text_bright': (200, 202, 204)}
        self.font = 'Calibri'
        self.width = width
        self.height = height
        self.display = None
        self.buttons = []
        self.coord_start = 25
        self.coord_spacing = 40

    def initialize(self):
        pg.init()
        self.display = pg.display.set_mode(size=(self.width, self.height))
        self.draw_lines()
        self.start_menu()
        self.create_grid_buttons()
        self.create_speed_buttons()

    def draw_lines(self):
        # Fill background
        self.display.fill(self.colors['dark_bg'], pg.Rect(0, 0, self.width, self.height))
        box_size = (120, 120)
        coordinates = [i for i in product([10, 250], [250, 10])]
        # Fill light boxes
        for x, y in coordinates:
            self.display.fill(self.colors['light_bg'], pg.Rect(x, y, *box_size))
        # Fill center
        self.display.fill(self.colors['light_bg'], pg.Rect(130, 130, *box_size))
        for i in range(0, 10):
            location = i * 40 + 10
            width = 3 if i % 3 else 5
            # Vertical lines
            self.display.fill(self.colors['line'], pg.Rect(location, 10, width, 365))
            # Horizontal lines
            self.display.fill(self.colors['line'], pg.Rect(10, location, 360, width))

    def start_menu(self):
        left_edge = 400
        top_edge = 15
        button_size = (130, 50)
        spacing = 65
        button_color = self.colors['light_bg']
        button_names = ('New Puzzle', 'Solve', 'Clear', 'Quit')
        max_len = max([len(i) for i in button_names])

        for name in button_names:
            rect = pg.Rect(left_edge, top_edge, *button_size)
            self.display.fill(button_color, rect)
            self.draw_font(name, rect=rect, top_buff=12, left_buff=max((max_len-len(name))*6, 6))
            self.buttons.append(Button(rect, name.lower()))
            top_edge += spacing

    def create_grid_buttons(self):
        y = 15
        for i in range(9):
            x = 15
            for j in range(9):
                width = 35
                height = 35
                x_pos = x
                y_pos = y
                if j % 3:
                    x_pos -= 2
                    width += 2
                if i % 3:
                    y_pos -= 2
                    height += 2
                self.buttons.append(GridButton(pg.Rect(x_pos, y_pos, width, height), i, j, (x, y)))
                x += 40
            y += 40

    def create_speed_buttons(self, build_list=True):
        button_size = (65, 30)
        button_color = self.colors['light_bg']

        rect = pg.Rect(15, 380, *button_size)
        self.display.fill(button_color, rect)
        self.draw_font(f'Slowest', (18, 383), size=15)
        if build_list:
            self.buttons.append(Button(rect, 'slowest'))

        rect = pg.Rect(85, 380, *button_size)
        self.display.fill(button_color, rect)
        self.draw_font(f'Slow', (88, 383), size=15)
        if build_list:
            self.buttons.append(Button(rect, 'slow'))

        rect = pg.Rect(155, 380, *button_size)
        self.display.fill(button_color, rect)
        self.draw_font(f'Normal', (158, 383), size=15)
        if build_list:
            self.buttons.append(Button(rect, 'normal'))

        rect = pg.Rect(225, 380, *button_size)
        self.display.fill(button_color, rect)
        self.draw_font(f'Fast', (228, 383), size=15)
        if build_list:
            self.buttons.append(Button(rect, 'fast'))

        if build_list:
            button_color = (25, 25, 25)
        rect = pg.Rect(295, 380, *button_size)
        self.display.fill(button_color, rect)
        self.draw_font(f'Fastest', (298, 383), size=15)
        if build_list:
            self.buttons.append(Button(rect, 'fastest'))

        self.flip()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONUP:
                if button_pushed := self.handle_buttons(*event.pos):
                    if button_pushed.get_name() == 'quit':
                        self.quit()
                    return button_pushed
            elif event.type == pg.KEYDOWN:
                return self.handle_keys(event.key)
            elif event.type == pg.VIDEOEXPOSE:
                self.flip()

    def handle_buttons(self, x, y):
        for button in self.buttons:
            if button.get_rect().collidepoint(x, y):
                return button

    @staticmethod
    def handle_keys(key):
        if key == pg.K_1:
            return 1
        if key == pg.K_2:
            return 2
        if key == pg.K_3:
            return 3
        if key == pg.K_4:
            return 4
        if key == pg.K_5:
            return 5
        if key == pg.K_6:
            return 6
        if key == pg.K_7:
            return 7
        if key == pg.K_8:
            return 8
        if key == pg.K_9:
            return 9
        if key in [pg.K_0, pg.K_BACKSPACE, pg.K_RETURN, pg.K_DELETE, pg.K_SPACE, pg.K_ESCAPE]:
            return 0

    def update(self, position=None, surface=None, rect=None, color=None, convert=False, top_buff=3, left_buff=3):
        if convert:
            if position is None:
                raise er.ArgumentError('If convert is True, position must be specified')
            position = self.get_position(*position)
        if rect is None:
            if position is None:
                raise er.ArgumentError('Either position or rect must be defined')
            rect = pg.Rect(position[0], position[1], 25, 25)
        if position is None:
            position = (rect.left + left_buff, rect.top + top_buff)
        if color is None:
            color = self.display.get_at(position)
        self.display.fill(color, rect)
        if surface:
            self.display.blit(surface, position)
        pg.display.update(rect)
        return self.event_loop()

    def draw_font(self, string, position=None, size=25, color=None,
                  bold=False, convert=False, rect=None, bg_color=None,
                  top_buff=3, left_buff=3):

        position = self.get_position(position[0], position[1]) if convert else position
        font = pg.font.SysFont(self.font, size, bold=bold)
        if not color:
            color = self.colors['text']
        text_surface = font.render(string, False, color)
        if not rect:
            return self.update(position, text_surface)
        return self.update(surface=text_surface, rect=rect, color=bg_color, top_buff=top_buff, left_buff=left_buff)

    @staticmethod
    def flip():
        pg.display.flip()

    def draw_puzzle(self, puzzle):
        # Clear 'Solved!' message
        self.maze_solved(True)
        y = self.coord_start
        for row in puzzle:
            x = self.coord_start
            for num in row:
                if num:
                    self.draw_font(str(num), (x, y), color=self.colors['text_bright'], bold=True)
                else:
                    self.update((x, y))
                x += self.coord_spacing
            y += self.coord_spacing

    def puzzle_information(self, num, clues, puzzles):
        full_rect = pg.Rect(390, 300, 150, 70)
        self.display.fill(self.colors['line'], full_rect)
        rect = pg.Rect(395, 305, 140, 60)
        self.display.fill(self.colors['dark_bg'], rect)
        self.draw_font(f'Puzzle: {num} of {puzzles}', (398, 308), size=18)
        self.draw_font(f'Clues: {clues}', (398, 328), size=18)
        pg.display.update(full_rect)

    def maze_solved(self, clear=False):
        position = (408, 275)
        rect = pg.Rect(*position, 150, 25)
        if clear:
            self.update(position, rect=rect)
            return
        self.draw_font('Solved!', rect=rect)

    def get_position(self, i, j):
        # Reverse input order to match coordinate plane
        return j * self.coord_spacing + self.coord_start, i * self.coord_spacing + self.coord_start

    def get_color(self, position, convert=False):
        position = position if not convert else self.get_position(position[0], position[1])
        return self.display.get_at(position)

    @staticmethod
    def quit():
        pg.quit()
        exit('\nProgram Quit... Good Bye!')
