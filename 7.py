import argparse

import tensorflow as tf


__author__ = "Eugene Alekseev"
__copyright__ = "Copyright 2017, Eugene Alekseev"
__license__ = "Apache 2.0"
__version__ = "0.1"
__maintainer__ = "Eugene Alekseev"
__email__ = "email@gmail.com"
__status__ = "production"


class IllegalNumberOfCommandArguments(Exception):
    def __init__(self, message):
        self.message = message


def main():
    parser = argparse.ArgumentParser(description="7.py argument parser")
    parser.add_argument("--numbers", "-n", action="store", nargs="*", dest="numbers")
    args = parser.parse_args()
    if len(args.numbers) != 2:
        raise IllegalNumberOfCommandArguments("There must be exactly two arguments")

    numbers = [int(number) for number in args.numbers]

    default_graph = tf.Graph()

    with default_graph.as_default():
        with tf.name_scope("inputs"):
            i_tf = tf.range(numbers[0], name="first")
            j_tf = tf.range(numbers[1], name="second")

        with tf.name_scope("outputs"):
            cross_product = tf.multiply(
                tf.reshape(i_tf, (numbers[0], 1)),
                tf.reshape(j_tf, (1, numbers[1])),
                name="cross_product"
            )

        tf.summary.histogram("cross_product", cross_product)

        merged = tf.summary.merge_all()

        saver = tf.summary.FileWriter("tensorboard")

        init = tf.global_variables_initializer()

    with tf.Session(graph=default_graph) as sess:
        sess.run(init)
        summary, result = sess.run([merged, cross_product])
        print(result)
        saver.add_summary(summary)

if __name__ == "__main__":
    main()