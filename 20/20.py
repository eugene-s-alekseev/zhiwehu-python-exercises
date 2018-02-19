__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import itertools
import sys

import numpy as np
import pandas as pd

import pyspark
import tensorflow as tf


def get_div_by_7_pure_python(n):
    result = itertools.filterfalse(lambda x: x % 7, range(n))
    result = list(result)
    return result


def get_div_by_7_numpy(n):
    array = np.array(range(n))
    array = array[array % 7 == 0]
    array = array.tolist()
    return array


def get_div_by_7_pandas(n):
    array = pd.Series(list(range(n)))
    array = array[array % 7 == 0]
    array = array.tolist()
    return array


def get_div_by_7_tensorflow(n):
    with tf.Session() as sess:
        x = tf.placeholder(shape=(None,), dtype=tf.int32, name="input_data")
        mask = tf.map_fn(
            lambda y: tf.mod(y, 7) == 0,
            x,
            dtype=tf.bool
        )
        result = tf.boolean_mask(x, mask, name="result")

        tf.global_variables_initializer().run()
        feed_dict = {
            x: list(range(n))
        }
        res = sess.run(
            result,
            feed_dict=feed_dict
        )
        res = res.tolist()

    return res


def get_div_by_7_spark(n):
    conf = pyspark.SparkConf().setAppName("20").setMaster("local")
    sc = pyspark.SparkContext(conf=conf)
    collection = sc.parallelize(list(range(n)))
    only_div_by_7 = collection.filter(lambda x: x % 7 == 0)
    result = only_div_by_7.collect()
    return result


def check_all_the_same(*values):
    return values.count(values[0]) == len(values)


def main():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("--number", "-n", action="store", type=int, dest="number")
    number = parser.parse_args().number
    functions = (
        get_div_by_7_pure_python,
        get_div_by_7_numpy,
        get_div_by_7_pandas,
        get_div_by_7_tensorflow,
        get_div_by_7_spark
    )
    results = list(map(lambda f: f(number), functions))
    if check_all_the_same(results):
        sys.stdout.write("{}That's allright{}".format("#"*6, "#"*6))
    else:
        sys.stdout.write("{0}Something went wrong{0}".format("#"*6, "#"*6))


if __name__ == "__main__":
    main()

