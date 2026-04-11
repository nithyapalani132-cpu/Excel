due=50
while due > 0:
    print("Amount Due:", due)
    a = int(input("Insert coin: "))
    if a not in(25, 10, 5):
        continue
    due -= a
    change = -due
print("Change owed:", change)
