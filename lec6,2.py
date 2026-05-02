import sys
import csv
from tabulate import tabulate

if len(sys.argv) != 2:
    sys.exit("Too few or too many command-line arguments")

filename = sys.argv[1]

if not filename.endswith(".csv"):
    sys.exit("Not a CSV file")


try:
    with open(filename, "r") as file:
        reader = csv.reader(file)
        table = list(reader)


        headers = table[0]
        data = table[1:]

        print(tabulate(data, headers=headers, tablefmt="grid"))

except FileNotFoundError:
    sys.exit("File does not exist")