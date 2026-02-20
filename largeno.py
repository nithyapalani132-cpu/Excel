def find_largest(nums):
    largest = nums[0]
    for num in nums:
        if num > largest:
            largest = num
    return largest

print(find_largest([10, 25, 3, 99, 45]))