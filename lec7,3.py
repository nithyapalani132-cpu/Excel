import re

def main():
    time = input("Hours: ")
    print(convert(time))


def convert(s):
    pattern = r"^([1-9]|1[0-2])(?::([0-5][0-9]))? (AM|PM) to ([1-9]|1[0-2])(?::([0-5][0-9]))? (AM|PM)$"
    match = re.fullmatch(pattern, s)

    if not match:
        raise ValueError

    h1, m1, p1, h2, m2, p2 = match.groups()

    h1 = int(h1)
    h2 = int(h2)
    m1 = int(m1) if m1 else 0
    m2 = int(m2) if m2 else 0

    if p1 == "AM" and h1 == 12:
        h1 = 0
    elif p1 == "PM" and h1 != 12:
        h1 += 12

    if p2 == "AM" and h2 == 12:
        h2 = 0
    elif p2 == "PM" and h2 != 12:
        h2 += 12

    return f"{h1:02}:{m1:02} to {h2:02}:{m2:02}"


if __name__ == "__main__":
    main()