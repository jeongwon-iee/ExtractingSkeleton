from chain import Chain, Coordinate, Point
from frame import Frame
from image import ImageConverter


def is_neighbor(frame, point, chain, number):
    # 0인 경우 끝냄
    if frame.pixels[point.row][point.column] == 0:
        return False

    # point가 가장자리인 경우 끝냄
    if point.row == 0 or point.row == frame.height:
        return True
    if point.column == 0 or point.column == frame.width:
        return True

    # 자신이 1이고 주위에 0이 하나라도 있는 경우 True 반환
    if chain.isReturning is False:
        if frame.visited[point.row][point.column] == 1:
            return False
        if point.column > 0:
            if frame.pixels[point.row][point.column - 1] == 0:
                return True
        if point.column < frame.width:
            if frame.pixels[point.row][point.column + 1] == 0:
                return True
        if point.row > 0:
            if frame.pixels[point.row - 1][point.column] == 0:
                return True
        if point.row < frame.height:
            if frame.pixels[point.row + 1][point.column] == 0:
                return True
        return False

    if chain.isReturning is True:
        if frame.visited[point.row][point.column] == 0:
            chain.isReturning = False
            chain.return_count = 0
            return True
        prev = chain.chains[chain.return_index - chain.return_count]
        next = (prev + 4) % 8
        # print("[%d %d %d]" % (prev, next, number), end=' ')
        if number == next:
            return True
    return False


def find_neighbor_border(frame, point, chain):
    # check east
    if is_neighbor(frame, point.column_plus(), chain, 0):
        chain.add_chain(0, point.column_plus())
        print("0", end=' ')
        return chain

    # check southeast
    if is_neighbor(frame, point.all_plus(), chain, 1):
        chain.add_chain(1, point.all_plus())
        print("1", end=' ')
        return chain

    # check south
    if is_neighbor(frame, point.row_plus(), chain, 2):
        chain.add_chain(2, point.row_plus())
        print("2", end=' ')
        return chain

    # check southwest
    if is_neighbor(frame, point.row_plus_column_minus(), chain, 3):
        chain.add_chain(3, point.row_plus_column_minus())
        print("3", end=' ')
        return chain

    # check west
    if is_neighbor(frame, point.column_minus(), chain, 4):
        chain.add_chain(4, point.column_minus())
        print("4", end=' ')
        return chain

    # check northwest
    if is_neighbor(frame, point.all_minus(), chain, 5):
        chain.add_chain(5, point.all_minus())
        print("5", end=' ')
        return chain

    # check north
    if is_neighbor(frame, point.row_minus(), chain, 6):
        chain.add_chain(6, point.row_minus())
        print("6", end=' ')
        return chain

    # check northeast
    if is_neighbor(frame, point.row_minus_column_plus(), chain, 7):
        chain.add_chain(7, point.row_minus_column_plus())
        print("7", end=' ')
        return chain

    # no neighbor
    chain.set_point(point)
    return chain


def is_dead_end(frame, point):
    count = 0
    for row in range(point.row - 1, point.row + 2):
        for column in range(point.column - 1, point.column + 2):
            # 검사할 위치가 자기 자신인 경우 continue
            if row == point.row and column == point.column:
                continue
            # 검사할 구간이 배경인 경우 continue
            if frame.pixels[row][column] == 0:
                continue
            # 검사할 구간을 방문한 적이 없는 경우
            if frame.visited[row][column] == 0:
                return False
            # 검사하는 구간이 1이면서 방문한 적이 있는 경우
            count += 1
    # 검사하는 구간에 방문하지 않은 1이 하나라도 없는 경우 False 반환
    if count > 0:
        return True
    return False


def hang_chain(frame, chain):
    # 검사할 지점 visited 체크
    frame.visited[chain.point.row][chain.point.column] = 1

    # 다음 체인 탐색
    chain = find_neighbor_border(frame, chain.point, chain)

    # 다음 체인이 시작점과 같은 경우 재귀함수 종료
    if chain.point.is_equal(frame.starting_point):
        return chain

    if chain.isReturning is True:
        chain.return_count += 1
        return hang_chain(frame, chain)

    # 새로 추가한 체인이 막다른 체인인지 검사
    if is_dead_end(frame, chain.point) is True:
        chain.isReturning = True
        chain.returning_index = chain.chains[len(chain.chains) - 1]



def calculate_coordinates(chain, coordinates):
    x = coordinates.current.x
    y = coordinates.current.y
    coordinates.coordinates = []
    for index in range(len(chain.chains)):
        if chain.chains[index] == 0:
            x += 1
        elif chain.chains[index] == 1:
            x += 1
            y -= 1
        elif chain.chains[index] == 2:
            y -= 1
        elif chain.chains[index] == 3:
            x -= 1
            y -= 1
        elif chain.chains[index] == 4:
            x -= 1
        elif chain.chains[index] == 5:
            x -= 1
            y += 1
        elif chain.chains[index] == 6:
            y += 1
        elif chain.chains[index] == 7:
            x += 1
            y += 1

        if x < 0:
            coordinates.current.add_x(50)
            return calculate_coordinates(chain, coordinates)
        if y < 0:
            coordinates.current.add_y(50)
            return calculate_coordinates(chain, coordinates)

        coordinates.append(Point(x, y))
    return coordinates


def get_coordinates(filename):
    return calculate_coordinates(extract_chains(filename), Coordinate()).coordinates


def extract_chains(filename):
    image = ImageConverter(filename)
    frame = Frame(image)
    chain = find_neighbor_border(frame, frame.starting_point, Chain())
    return hang_chain(frame, chain)


def rotate_coordinates(coordinates, index):
    new_coordinates = []
    for i in range(index, len(coordinates)):
        new_coordinates.append(coordinates[i])
    for i in range(index):
        new_coordinates.append(coordinates[i])
    return new_coordinates


def main():
    chains = extract_chains("../image/crows/crow20.png"), Coordinate()


if __name__ == '__main__':
    main()


#%%
