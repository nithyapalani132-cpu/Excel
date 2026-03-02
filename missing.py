def missing_number(lst, n):
    return n*(n+1)//2 - sum(lst)

print(missing_number([1,2,4,5], 5))