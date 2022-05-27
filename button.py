class Button:
    def __init__(self, rect, name):
        self.__rect = rect
        self.__name = name

    def get_rect(self):
        return self.__rect

    def get_name(self):
        return self.__name


class GridButton(Button):

    def __init__(self, rect, i, j, position):
        Button.__init__(self, rect, f'grid{i}{j}')
        self.__i = i
        self.__j = j
        self.__position = position

    def get_i(self):
        return self.__i

    def get_j(self):
        return self.__j

    def get_position(self):
        return self.__position
