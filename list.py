def rotate_list(lst, k):
    k = k % len(lst)
    return lst[k:] + lst[:k]

print(rotate_list([1,2,3,4,5], 2))