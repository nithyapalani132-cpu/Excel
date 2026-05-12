
def main():
    print(validate(input("IPv4 Address: ")))

def validate(ip):
    parts = ip.split(".")

    # must have exactly 4 parts
    if len(parts) != 4:
        return False

    for part in parts:
        # only digits allowed
        if not part.isdigit():
            return False

        # no leading zeros
        if len(part) > 1 and part.startswith("0"):
            return False

        number = int(part)

        # range check
        if number < 0 or number > 255:
            return False

    return True

if __name__ == "__main__":
    main()