__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import json
import psycopg2

import pandas as pd
import tensorflow as tf


with open("postgres_cred.json", "r") as file:
    CREDENTIALS = json.load(file)


def insert_numbers(number):
    with psycopg2.connect(**CREDENTIALS) as conn:
        cursor = conn.cursor()
        cursor.execute("create table if not exists t16 (number int);")
        cursor.execute("truncate table t16;")
        query = """
        insert into t16
        values (%(n)s)
        """
        values = (
            {"n": n}
            for n in range(number)
        )
        cursor.executemany(query, values)


def read_values():
    with psycopg2.connect(**CREDENTIALS) as conn:
        numbers = pd.read_sql("select * from t16", conn)

    return numbers.values.squeeze()


def get_graph(numbers):
    graph = tf.Graph()
    with graph.as_default():
        input_tf = tf.constant(numbers, dtype=tf.int32, name="input_tf")
        mask = tf.cast(tf.mod(input_tf, 2), dtype=tf.bool, name="mask")
        only_odd = tf.boolean_mask(input_tf, mask, name="only_odd")
        squared = tf.square(only_odd, name="squared")

    return graph


def main():
    argparser = argparse.ArgumentParser(description="Parser")
    argparser.add_argument(
        "--number-of-numbers", "-n", action="store",
        type=int, dest="num_of_num"
    )
    num_of_num = argparser.parse_args().num_of_num

    insert_numbers(num_of_num)

    numbers = read_values()

    graph = get_graph(numbers)

    with tf.Session(graph=graph) as sess:
        tf.global_variables_initializer().run()
        result = sess.run(graph.get_tensor_by_name("squared:0"))
        print("result: ", result)


if __name__ == "__main__":
    main()

