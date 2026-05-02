import sys

def main():
    if len(sys.argv) < 2:
        print("Too few command-line arguments")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("Too many command-line arguments")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.endswith(".py"):
        print("Not a Python file")
        sys.exit(1)

    try:
        with open(filename, "r") as file:
            count = 0
            for line in file:
                stripped = line.lstrip()
                if stripped == "" or stripped.startswith("#"):
                    continue
                count += 1
        print(count)

    except FileNotFoundError:
        print("File does not exist")
        sys.exit(1)

if __name__ == "__main__":
    main()