__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import json
import os
import psycopg2
import random

import pyspark

with open(os.path.abspath(os.path.join("..", "postgres_cred.json")), "r") as file:
    CREDENTIALS = json.load(file)

POSTGRES_TABLE = "t19"


def generate_data(table, nrows, upper_age):
    data = [
        {
            "name": random.choice(["Alice", "Bob", "Clyde"]),
            "age": random.randint(18, upper_age),
            "score": random.uniform(0, 1)
        }
        for _ in range(nrows)
    ]
    with psycopg2.connect(**CREDENTIALS) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        create table if not exists {table} (name varchar(20), age int, score float);
        """.format(table=table))
        cursor.execute("""
        truncate table {table};
        """.format(table=table))
        query = """
        insert into {table}
        values (%(name)s, %(age)s, %(score)s)
        """.format(table=table)
        cursor.executemany(query, data)


def main():
    argparser = argparse.ArgumentParser(description="Parser")
    argparser.add_argument("--table", "-t", action="store", dest="table")
    argparser.add_argument("--nrows", "-n", action="store", dest="nrows", type=int)
    argparser.add_argument("--upper-age", "-u", action="store", dest="upper_age", type=int)
    args = argparser.parse_args()
    generate_data(args.table, args.nrows, args.upper_age)

    sc = pyspark.SparkContext("local", "context")
    sqlContext = pyspark.sql.SQLContext(sc)
    properties = {
        "user": CREDENTIALS["user"],
        "password": CREDENTIALS["password"]
    }
    df = pyspark.sql.DataFrameReader(sqlContext).jdbc(
        url="jdbc:postgresql://localhost:5432/zhiwehu",
        table=POSTGRES_TABLE,
        properties=properties
    )

    df.registerTempTable("t19")

    sorted = sqlContext.sql("""
    select *
    from t19
    order by name, age, score
    """).show()


if __name__ == "__main__":
    main()