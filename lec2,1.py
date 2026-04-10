n = input("camelCase: ")
for ch in n:
    if ch.isupper():
        print("_" + ch.lower(), end="")
    else:
        print(ch, end="")