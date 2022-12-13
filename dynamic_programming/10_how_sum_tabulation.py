# same problem but we use tabulation/iterative method now

# this type of problem have a repeating pattern solution, this function can be a template!
def how_sum(target, nums):
    """
    We need only one possible combination of the construction.
    """

    # since we need to return lists, lets just build a 2d array
    # instead of trying to work with 1d array
    # and chaining at the end (this is possible but error prone)

    arr = [None for k in range(target + 1)]  # create a default
    # why is None a better base case than 0 here?
    # because we expect the output to be a list
    # for (0, [...]) the result is []
    # to assume the -ve result we can use None
    arr[0] = []  # we can reach 1
    for i, val in enumerate(arr):
        if val is None:  # if we can reach this value no point in looking forward
            continue
        for num in nums:
            if i + num <= target:
                # if i+num is equal to target we can just stop,
                # but in some other problems we might need to iterate till the end
                # so we iterate till end anyway
                arr[i + num] = [*val, num]
    return arr[target]


print(how_sum(7, [2, 3]))
print(how_sum(300, [7, 14]))
