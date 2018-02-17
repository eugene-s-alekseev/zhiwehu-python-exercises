__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse

import tensorflow as tf


def check_even_digits(number):
    string_number = tf.expand_dims(tf.as_string(number), axis=-1)
    sparse_splitted = tf.string_split(string_number, delimiter="")
    splitted_dense = tf.sparse_to_dense(
        sparse_splitted.indices,
        sparse_splitted.dense_shape,
        sparse_splitted.values,
        default_value="0"
    )
    digits = tf.string_to_number(splitted_dense)
    rems = tf.mod(digits, 2)
    odds = tf.reduce_sum(rems)
    return tf.cond(
        tf.equal(odds, 0),
        lambda: tf.constant(True, dtype=tf.bool),
        lambda: tf.constant(False, dtype=tf.bool)
    )



def main():
    argparser = argparse.ArgumentParser(description="Parser that handles input arguments")
    argparser.add_argument("--bounds", "-b", action="store", dest="bounds", nargs=2)
    lower, higher = argparser.parse_args().bounds
    lower, higher = int(lower), int(higher)

    numbers = tf.range(lower, higher, name="numbers", dtype=tf.int32)
    mask = tf.map_fn(check_even_digits, numbers, name="mask", dtype=tf.bool)
    numbers_with_even_digits = tf.boolean_mask(numbers, mask, name="numbers_with_even_digits")

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        nums = sess.run(numbers_with_even_digits)

    nums = nums.tolist()
    nums = list(map(str, nums))
    print(", ".join(nums))


if __name__ == "__main__":
    main()

