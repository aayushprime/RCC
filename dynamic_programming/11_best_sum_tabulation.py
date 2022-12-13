# same problem, find the best (shortest) combination to form the target


def best_sum(target, nums):
    arr = [None for _ in range(target + 1)]
    arr[0] = []  # base case
    for i, val in enumerate(arr):
        if val is None:
            continue
        for num in nums:  # all same like before
            if num + i <= target:  # if we are in bounds
                # we are the first to reach there,
                # no other way to reach there has been found yet
                if arr[num + i] is None:
                    # then just put the array there!
                    arr[num + i] = val + [num]
                else:
                    # then this position already has a way to get there
                    # check if its length is smaller than what we are proposing
                    if len(arr[num + i]) > len(val + [num]):
                        arr[num + i] = val + [num]
    return arr[target]


print(best_sum(8, [2, 3, 5]))
print(best_sum(100, [1, 2, 5, 25]))  # instant
