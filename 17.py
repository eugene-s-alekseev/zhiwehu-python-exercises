__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import json
import psycopg2
import random

import pandas as pd
import tensorflow as tf

with open("postgres_cred.json", "r") as file:
    CREDENTIALS = json.load(file)


def fill_table(table, n_transactions=50, lower_range=1., upper_range=500.):
    pairs = [
        {
            "type": random.choice(["W", "D"]),
            "value": random.uniform(lower_range, upper_range)
        }
        for _ in range(n_transactions)
    ]
    with psycopg2.connect(**CREDENTIALS) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        create table if not exists {0} (type char(1), value numeric(7, 2));
        """.format(table))
        cursor.execute("""
        truncate table {0};
        """.format(table))
        query = """
        insert into {0} values (%(type)s, %(value)s)
        """.format(table)
        cursor.executemany(query, pairs)


def get_table(table):
    with psycopg2.connect(**CREDENTIALS) as conn:
        transactions = pd.read_sql("select * from {0}".format(table), conn)

    return transactions["type"].values, transactions["value"].values


def build_graph(types_, values_):
    graph = tf.Graph()
    with graph.as_default():
        tf_types = tf.constant(types_, dtype=tf.string)
        tf_values = tf.constant(values_, dtype=tf.float32)
        signs = tf.map_fn(
            lambda x: tf.cond(
                tf.equal(x, "D"),
                lambda: tf.constant(1.),
                lambda: tf.constant(-1.)
            ),
            tf_types,
            dtype=tf.float32
        )
        result = tf.reduce_sum(signs*tf_values, name="result")

    return graph


def main():
    fill_table("t17")
    types, values = get_table("t17")

    graph = build_graph(types, values)

    with tf.Session(graph=graph) as sess:
        tf.global_variables_initializer().run()
        result = sess.run(graph.get_tensor_by_name("result:0"))

    print(result)


if __name__ == "__main__":
    main()