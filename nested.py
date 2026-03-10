nested = [[1,2], [3,4], [5,6]]

flat = [num for sub in nested for num in sub]

print(flat)