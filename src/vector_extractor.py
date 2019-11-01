import operator as op
from functools import reduce
from chain import Point
import math
import scipy.signal
import peakutils
import chain_extractor as ch
import test as test

class Theta:
    def __init__(self, radian, head, tail):
        self.radian = radian # head와 tail의 각도
        self.head = head # head로 추정되는 지점의 index
        self.tail = tail # tail로 추정되는 지점의 index

    def reverse(self):
        self.radian -= math.radians(180)
        temp = self.head
        self.head = self.tail
        self.tail = temp


class Vector:
    def __init__(self, center, head, tail, wings):
        self.center = center
        self.head = head
        self.tail = tail
        self.wing1 = wings[0]
        if len(wings) < 2:
            self.wing2 = wings[0]
        else:
            self.wing2 = wings[1]

    def get_coordinates(self):
        coordinates = []
        coordinates.append(self.center)
        coordinates.append(self.head)
        coordinates.append(self.tail)
        coordinates.append(self.wing1)
        coordinates.append(self.wing2)
        return coordinates


class Calculator:
    @classmethod
    def ncr(cls, n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return int(numer / denom)

    @classmethod
    def center_point(cls, coordinates): # 좌표 리스트 input하면 center 좌표값 output으로
        cent_x = cent_y = 0
        for coordinate in coordinates:
            cent_x += coordinate.x
            cent_y += coordinate.y
        return Point(cent_x // len(coordinates), cent_y // len(coordinates))

    @classmethod
    def get_distances(cls, coordinates, center): # 좌표값, 센터값 input하면 center로부터의 거리 구해서 return
        distance = []
        for coordinate in coordinates:
            dx = coordinate.x - center.x
            dy = coordinate.y - center.y
            distance.append(math.sqrt((dx ** 2) + (dy ** 2)))
        return distance

    @classmethod
    def smooth_distance(cls, distances):
        return scipy.signal.savgol_filter(distances, 51, 3)

    @classmethod
    def radians_between_dots(cls, theta, coordinates, maximas):
        thetas = []
        for i in range(len(maximas)):
            for j in range(i + 1, len(maximas)):
                if i == j:
                    continue
                point1 = coordinates[maximas[i]] # 기준점
                point2 = coordinates[maximas[j]] # 대조점
                if point2.y > point1.y:
                    thetas.append(Theta(math.atan2(point2.y - point1.y, point2.x - point1.x), maximas[j], maximas[i]))
                else:
                    thetas.append(Theta(math.atan2(point1.y - point2.y, point1.x - point2.x), maximas[i], maximas[j]))

        if theta > 0:
            return thetas
        return Calculator.reverse(thetas)

    @classmethod
    def reverse(cls, thetas):
        for theta in thetas:
            theta.reverse()
        return thetas


def calculate_maximas(coordinates, center):
    distances = Calculator.get_distances(coordinates, center)
    filtered_distance = Calculator.smooth_distance(distances)
    maximas = peakutils.indexes(filtered_distance, thres=0.02 / max(filtered_distance), min_dist=100)
    return maximas


def calculate_slope(theta, coordinates, maximas):
    radians = Calculator.radians_between_dots(theta, coordinates, maximas)

    difference = abs(theta - radians[0].radian)
    slope = radians[0]
    for radian in radians:
        if difference > abs(theta - radian.radian):
            difference = abs(theta - radian.radian)
            slope = radian

    # difference가 theta와 지나치게 차이나는 경우 +- 5
    # if difference > theta + math.degrees(5) or difference < theta - math.degrees(5):


    return slope


def calculate_center(slope, coordinates):
    x = coordinates[slope.head].x + coordinates[slope.tail].x
    y = coordinates[slope.head].y + coordinates[slope.tail].y
    return Point(x / 2, y / 2)


def extract_wings(coordinates, slope, maximas):
    indices = []
    for maxima in maximas:
        if maxima == slope.head or maxima == slope.tail:
            continue
        indices.append(maxima)
    wings = []
    for index in indices:
        wings.append(coordinates[index])
    return wings


def get_vectors(filename, theta):
    bird = ch.get_coordinates(filename)
    geographical_center = Calculator.center_point(bird)
    geographical_maximas = calculate_maximas(bird, geographical_center)

    if len(geographical_maximas) < 1:
        null_point = Point(-1, -1)
        null_wings = [null_point, null_point]
        return Vector(null_point, null_point, null_point, null_wings)

    # bird 재조정
    bird = ch.rotate_coordinates(bird, geographical_maximas[0] // 2)
    geographical_center = Calculator.center_point(bird)
    geographical_maximas = calculate_maximas(bird, geographical_center)

    if len(geographical_maximas) < 2:
        null_point = Point(-1, -1)
        null_wings = [null_point, null_point]
        return Vector(null_point, null_point, null_point, null_wings)

    # 새의 각도, 중심
    bird_slope = calculate_slope(theta, bird, geographical_maximas)
    bird_center = calculate_center(bird_slope, bird)
    bird_head = bird[bird_slope.head]
    bird_tail = bird[bird_slope.tail]
    bird_wings = extract_wings(bird, bird_slope, geographical_maximas)

    # 벡터화
    vector = Vector(bird_center, bird_head, bird_tail, bird_wings)

    test.test_drawing(bird, vector)

    return vector


def main():
    theta = 2.879799
    vector = get_vectors("../image/crows/crow1.png", theta)


if __name__ == "__main__":
    main()
