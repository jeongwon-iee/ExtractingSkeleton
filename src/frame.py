# 새의 시작점, 높이, 넓이 초기화, 계산
class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Point:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def row_plus(self):
        return Point(self.row + 1, self.column)

    def column_plus(self):
        return Point(self.row, self.column + 1)

    def all_plus(self):
        return Point(self.row + 1, self.column + 1)

    def row_minus(self):
        return Point(self.row - 1, self.column)

    def column_minus(self):
        return Point(self.row, self.column - 1)

    def all_minus(self):
        return Point(self.row - 1, self.column - 1)

    def row_minus_column_plus(self):
        return Point(self.row - 1, self.column + 1)

    def row_plus_column_minus(self):
        return Point(self.row + 1, self.column - 1)

    def is_equal(self, point):
        if self.row == point.row and self.column == point.column:
            return True
        return False


class Frame:
    def __init__(self, image):
        self.width = image.width
        self.height = image.height
        self.pixels = image.pixels
        self.visited = [[0] * self.width for row in range(self.height)]
        self.starting_point = self.find_starting_point()
        self.end_point = self.find_end_point()
        self.shape_size = Size(self.calculate_height(), self.calculate_width())

    def find_starting_point(self):
        for row in range(self.height):
            for column in range(self.width):
                if self.pixels[row][column] == 1:
                    return Point(row, column)

    def find_end_point(self):
        for row in range(self.height - 1, 0, -1):
            for column in range(self.width - 1, 0, -1):
                if self.pixels[row][column] == 1:
                    return Point(row, column)

    def calculate_height(self):
        self.end_point.row - self.starting_point.row + 1

    def calculate_width(self):
        end = start = 0
        for column in range(self.width):
            for row in range(self.height):
                if self.pixels[row][column] == 1:
                    end = column
        for column in range(self.width -1, 0, -1):
            for row in range(self.height - 1, 0, -1):
                if self.pixels[row][column] == 1:
                    start = column
        return end - start + 1
