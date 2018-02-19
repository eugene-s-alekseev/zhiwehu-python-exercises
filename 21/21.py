__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import itertools

import numpy as np


class Move:
    def __init__(self):
        self.location = np.array([0, 0])

    def up(self):
        self.location += np.array([1, 0])

    def down(self):
        self.location += np.array([-1, 0])

    def right(self):
        self.location += np.array([0, 1])

    def left(self):
        self.location += np.array([0, -1])

    @property
    def location_(self):
        return self.location

    @property
    def distance_(self):
        return np.linalg.norm(self.location)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--up", type=int, action="store", dest="up")
    parser.add_argument("--down", type=int, action="store", dest="down")
    parser.add_argument("--right", type=int, action="store", dest="right")
    parser.add_argument("--left", type=int, action="store", dest="left")
    args = vars(parser.parse_args())
    args = [
        [arg for _ in range(args[arg])]
        for arg in args
    ]
    args = list(itertools.chain.from_iterable(args))

    move = Move()

    for m in args:
        getattr(move, m)()

    print(move.distance_)


if __name__ == "__main__":
    main()