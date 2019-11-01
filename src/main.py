import src.vector_extractor as vec
import os
import sys


def get_file_count():
    dir = '../image/crows'
    return len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])


def main():
    count = get_file_count()
    path = '../image/crows'
    theta = 2
    for filename in os.listdir(path):
        filepath = path + "/" + filename
        vector = vec.get_vectors(filepath, theta)
        print(filename)


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    main()
