# Python script to import data from CSV spreadsheet into a SQLite database

import csv
import cs50
from sys import argv

# 1 Access database
db = cs50.SQL("sqlite:///students.db")

# 2 Access CSV file
if (len(argv) == 2):
    with open(argv[1], "r") as students:
        reader = csv.DictReader(students)
        # 3 Insert data into students.db database
        for row in reader:
            if len(row["name"].split(" ")) == 3:
                # import with first, midle, last name
                first, middle, last = row["name"].split(" ")
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                            first, middle, last, row["house"], row["birth"])
            else:
                # import with first and last name (assumption)
                first, last = row["name"].split(" ")
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                            first, None, last, row["house"], row["birth"])
else:
    print("Usage: python import.py characters.csv")
    exit(1)