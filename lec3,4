months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

while True:
    date = input("Date: ").strip()

    try:
        if "/" in date:
            parts = date.split("/")
            if len(parts) != 3:
                raise ValueError
            m = int(parts[0])
            d = int(parts[1])
            y = int(parts[2])

        else:
            if "," not in date:
                raise ValueError

            month, rest = date.split(" ", 1)
            d, y = rest.replace(",", "").split()

            if month not in months:
                raise ValueError

            m = months.index(month) + 1
            d = int(d)
            y = int(y)

        if 1 <= m <= 12 and 1 <= d <= 31:
            print(f"{y:04}-{m:02}-{d:02}")
            break
        else:
            raise ValueError

    except:
        print("Invalid date")
