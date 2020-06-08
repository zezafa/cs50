# Python script that prints a list of students for a given house in alphabetical order
import cs50
import csv
from sys import argv

# 1 Access database
db = cs50.SQL("sqlite:///students.db")

# 2 Accept the name of a house as a command-line argument
if len(argv) == 2:
    houseQuery = argv[1]
    # 2 Query the students table in the db for all students in the specified house
    table = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first ASC", houseQuery)
    # 3 Print out full name and birth year
    for row in table:
        if row["middle"] == None:
            print(row["first"] + " " + row["last"] + ", born " + str(row["birth"]))
        else:
            print(row["first"] + " " + row["middle"] + " " + row["last"] + ", born " + str(row["birth"]))
else:
    print("Usage: python roster.py house_name")
    exit(1)