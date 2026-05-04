import csv
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: python scourgify.py input.csv output.csv")

try:
    with open(sys.argv[1], newline="") as infile:
        reader = csv.DictReader(infile)

        with open(sys.argv[2], "w", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=["first", "last", "house"])
            writer.writeheader()

            for row in reader:
                last, first = row["name"].split(", ")
                writer.writerow({
                    "first": first,
                    "last": last,
                    "house": row["house"]
                })

except FileNotFoundError:
    sys.exit("Could not read input file")
