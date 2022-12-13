def can_sum(target, numbers):
    """
    Return true if numbers can be combined to form target (addition)
    """
    arr = [0 for _ in range(target + 1)]
    for pos in arr:
        # for each number in our table, add a number from
        # numbers array and add the counter on `number` positions from us
        for num in numbers:
            if pos + num <= target:  # check for bounds
                arr[pos + num] += 1

    return arr[target] != 0  # if arr[target] has a non zero value then


# tests
print(can_sum(7, [2, 4]))
print(can_sum(7, [5, 3, 4, 7]))
print(can_sum(300, [7, 14]))

# the above function counts the ways to add up to the target number
# instead if we only want to know if it is possible to make the number by some combination


def can_sum(target, numbers):
    # 1 more than target because we need array till target, which counting 0 is target+1 spaces
    arr = [False for _ in range(target + 1)]
    arr[0] = True  # base case, if the number is 0 its already made up
    for i in range(target):
        # iterate till target,
        if not arr[i]:  # if we can't reach this number no point in looking forward
            continue
        for num in numbers:
            # for each slot in the table, look at each number and look forward and mark it possible
            if num + i <= target:
                arr[num + i] = True
    return arr[target]


print(can_sum(7, [2, 4]))
print(can_sum(7, [5, 3, 4, 7]))
print(can_sum(300, [7, 14]))
