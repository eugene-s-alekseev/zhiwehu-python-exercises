__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import itertools

import numpy as np
import tensorflow as tf


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


def get_location(steps):
    directions = {
        "up": np.array([1, 0]),
        "down": np.array([-1, 0]),
        "right": np.array([0, 1]),
        "left": np.array([0, -1])
    }
    move_tf = tf.placeholder(shape=[2], dtype=tf.float32, name="move")
    location_tf = tf.Variable(initial_value=[0, 0], dtype=tf.float32, name="location")
    step_tf = tf.assign_add(location_tf, move_tf, name="make_step")
    distance_tf = tf.norm(location_tf, name="distance")
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        for step in steps:
            feed_dict = {move_tf: directions[step]}
            sess.run(step_tf, feed_dict=feed_dict)
        result = sess.run(distance_tf)

    return result


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

    print(get_location(args))

if __name__ == "__main__":
    main()