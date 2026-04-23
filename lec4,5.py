import random

def main():
    level = get_level()
    score = 0

    for _ in range(10):
        x,y = generate_integer(level),generate_integer(level)
        answer, tries, correct = x + y, 0, False

        while tries < 3 and not correct:
            try:
                if int(input(f"{x} + {y} = ")) == answer:
                    correct, score = True, score + 1
                else:
                    print("EEE")
                    tries += 1
            except ValueError:
                print("EEE")
                tries += 1

        if not correct:
            print(answer)

    print(f"Score: {score}")

def get_level():
    while True:
        try:
            num = int(input("level:"))
            if num in (1,2,3):
                return num
        except ValueError:
            continue

def generate_integer(level):
    if level == 1:
        return random.randint(0,9)
    return random.randint(10**(level-1),10**level-1)

if __name__ == "__main__":
    main()

