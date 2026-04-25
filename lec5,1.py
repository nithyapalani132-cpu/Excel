def main():
    text = input("Input: ")
    print("Output:", shorten(text))


def shorten(word):
    vowels = "AEIOUaeiou"
    result = ""

    for letter in word:
        if letter not in vowels:
            result += letter

    return result


if __name__ == "__main__":
    main()