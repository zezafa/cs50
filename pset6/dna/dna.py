#dna.py - identifies a person based on their DNA (input: CSV file cointaining STR counts; output: most likely person)

import csv
from sys import argv

# Read the first command-line argument to find the CSV file containing STR csv database and second argument as DNA seq to identify

if (len(argv) == 3):
    # Open csv database
    with open(argv[1], 'r', newline='\n') as csvfile:
        #fieldsnames = ['name', 'AGATC' , 'AATG', 'TATC']
        # Read csv database into memory
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

else:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

csvfile = open(argv[1], 'r', newline='\n')
reader = csv.DictReader(csvfile)

# Open text file sequence and read its contents into memory
f = open(argv[2], 'r')
seq = f.read()

i = 0

list = {}

for STR in headers[1:]:
    list[STR] = []

while (i < len(seq)):
    for STR in headers[1:]:
        if (seq[i:i + len(STR)] == STR):
            j = i
            counter = 0
            while (seq[j:j + len(STR)] == STR):
                j += len(STR)
                counter += 1
            list[STR].append(counter)
    i += 1


for STR in headers[1:]:
    if list[STR] == []:
        list[STR] = 0
    else:
        list[STR] = max(list[STR])


for row in reader:
    match = 1
    for STR in headers[1:]:
        # Apperantly row[STR] needs to be casted to int
        if (int(row[STR]) == list[STR]):
            match +=1
    #print(match)
    if match == len(headers):
        print(row['name'])
        exit(0)

print("No match.")