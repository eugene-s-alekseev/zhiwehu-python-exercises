__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = 1.0

import argparse

import tensorflow as tf

def main():
    argparser = argparse.ArgumentParser(description="Parser that handles input parameters")
    argparser.add_argument("--numbers", "-n", action="store", dest="numbers", nargs="*")
    args = argparser.parse_args()
    numbers = [int(number, 2) for number in args.numbers]

    graph = tf.Graph()

    with graph.as_default():
        input_numbers = tf.constant(numbers)
        remainders = input_numbers % 5
        inverse_mask = tf.cast(remainders, dtype=tf.bool)
        mask = tf.logical_not(inverse_mask)
        divisible_by_5 = tf.boolean_mask(input_numbers, mask)

        init = tf.global_variables_initializer()

    with tf.Session(graph=graph) as sess:
        sess.run(init)
        output = sess.run(divisible_by_5)

    output = output.tolist()
    output = map(bin, output)
    output = [str(number)[2:] for number in output]

    print(", ".join(output))

if __name__ == "__main__":
    main()