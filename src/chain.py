from frame import Point


class Chain:
    def __init__(self):
        self.chains = []
        self.point = Point(0, 0)
        self.isReturning = False
        self.isEnd = False
        self.return_index = -1
        self.return_count = 0

    def set_point(self, point):
        self.point = point

    def add_chain(self, chain, point):
        self.chains.append(chain)
        self.point = point

    def print_chains(self):
        for chain in self.chains:
            print(chain, end=' ')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_x(self, number):
        self.x = self.x + number

    def add_y(self, number):
        self.y = self.y + number

    def minus_x(self, number):
        self.x = self.x - number

    def minus_y(self, number):
        self.y = self.y - number


class Coordinate:
    def __init__(self):
        self.current = Point(300, 300)
        self.coordinates = []

    def append(self, coordinate):
        self.coordinates.append(coordinate)

    def print_coordinates(self):
        for coordinate in self.coordinates:
            print("(%d, %d)" % (coordinate.x, coordinate.y), end=' ')

    def print_x(self):
        for coordinate in self.coordinates:
            print("%d" % coordinate.x, end=' ')
        print()

    def print_y(self):
        for coordinate in self.coordinates:
            print("%d" % coordinate.y, end=' ')
        print()
