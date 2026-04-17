items = {}
while True:
    try:
        item = input().strip().lower()

        if item in items:
            items[item] += 1
        else:
            items[item] = 1

    except EOFError:
        break
for name in sorted(items):
    print( items[name], name.upper() )
