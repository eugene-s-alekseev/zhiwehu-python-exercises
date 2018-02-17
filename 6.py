__author__ = "Eugene Alekseev"

import argparse
import re

import tensorflow as tf


def main():
    parser = argparse.ArgumentParser(description="Parser to handle input numbers")
    parser.add_argument("--numbers", "-n", action="store", nargs="*", dest="numbers")
    args = parser.parse_args()
    numbers = [int(re.findall("\d+", number)[0]) for number in args.numbers]
    print("Check: ", numbers)

    with tf.name_scope("inputs"):
        c = tf.constant(50., name="c")
        h = tf.constant(30., name="h")
        d = tf.constant(numbers, dtype=tf.float32, name="d")
    q = tf.sqrt((2 * c * d) / h, name="sqrt")
    output = tf.round(q, "rounded")

    writer = tf.summary.FileWriter("tensorboard")

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        print(sess.run(output))


if __name__ == "__main__":
    main()