__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import unittest

import tensorflow as tf


def get_graph(number):
    graph = tf.Graph()
    with graph.as_default():
        input_tf = tf.constant(number, name="number")
        str_repr = tf.as_string(input_tf, name="str_repr")
        length = tf.size(tf.string_split([str_repr], ""), name="length")
        output_array = tf.TensorArray(dtype=tf.int32, size=4)

        i = tf.constant(0, dtype=tf.int32)
        intermed = tf.constant(0, dtype=tf.int32)
        cond = lambda i, _, __: i < 4
        body = lambda i, intermed, output_array: (
            i + 1,
            input_tf * tf.pow(10, length*i) + intermed,
            output_array.write(
                i,
                input_tf * tf.pow(10, length*i) + intermed
            )
        )

        _, _, out = tf.while_loop(cond=cond, body=body, loop_vars=[i, intermed, output_array])

        stacked = out.stack()
        result = tf.reduce_sum(stacked, name="result")

    return graph


def main():
    argparser = argparse.ArgumentParser(description="Parser that handles input arguments")
    argparser.add_argument("--number", "-n", action="store", type=int, dest="number")
    number = argparser.parse_args().number

    graph = get_graph(number)

    with tf.Session(graph=graph) as sess:
        tf.global_variables_initializer().run()
        output = sess.run(graph.get_tensor_by_name("result:0"))

    print(output)


if __name__ == "__main__":
    main()