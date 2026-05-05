from datetime import date
import inflect
import sys

def main():
    birth = input("Date of Birth: ")

    try:
        year, month, day = birth.split("-")
        birth_date = date(int(year), int(month), int(day))
    except ValueError:
        sys.exit("Invalid date")

    today = date.today()

    # Difference in days
    days = (today - birth_date).days

    # Convert days to minutes
    minutes = days * 24 * 60

    # Convert number to words
    p = inflect.engine()
    words = p.number_to_words(minutes, andword="")

    print(words.capitalize() + " minutes")


if __name__ == "__main__":
    main()