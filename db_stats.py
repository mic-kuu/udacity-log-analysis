#!/usr/bin/env python3
import psycopg2


def print_headline(text):
    """Helper funtion for printing the tests' headlines"""
    print("\n", "-" * 80, "\n| ", text, "\n", "-" * 80, "\n")


# intial work - open connection to the correct db
db = psycopg2.connect("dbname=news")
c = db.cursor()

# Task 1: Top articles
c.execute("select * from top_articles;")
rows = c.fetchall()

print_headline("1: The most popular three articles of all time")

for idx, row in enumerate(rows):
    print(" [ {index} ]\t\"{article}\"\t\t{views} views".format(
        index=idx + 1,
        article=row[0],
        views=row[1]))


# Task 2: Top authors
c.execute("select * from top_authors;")
rows = c.fetchall()

print_headline("2: The most popular article authors of all time")

for idx, row in enumerate(rows):
    print(" [ {index} ]\t\"{author}\"{space}{views} views".format(
        index=idx + 1,
        author=row[0],
        views=row[1],
        space=("\t" * 3, "\t" * 4)[bool(len(row[0]) < 22)]))


# Task 3: Error percentage
c.execute("select * from request_stats;")
rows = c.fetchall()

print_headline("3: Days on which more than 1% of requests lead to errors")

for idx, row in enumerate(rows):
    print(" [ {index} ]\t{day}\t\t\t\t\t{failure_percentage}%".format(
        index=idx + 1,
        day=row[0],
        failure_percentage=round(row[1] * 100, 2)))

db.close()
