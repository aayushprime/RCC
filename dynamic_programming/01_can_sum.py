# logical problem to solve after, fibonacci and gridTraveler(Move only down and right)
# While calling recursively, do not check for the children's validity! Instead handle it in the base case.
# This is because resoning about base cases is easier than reasoning about children.


# take a number and a list of numbers and tell if it is possible to add up the numbers in the list to get the number

# can_sum(7, [2,4]) = False; 2 and 4 cannot make 7
# can_sum(7, [5,3,4,7]) = True; 4 and 3 can make 7


def can_sum(target, numbers):
    if target == 0:
        return True
    if (
        target < 0
    ):  # notice here that we are checking about the validity of the input to the function
        return False
    for num in numbers:
        remaining = target - num
        if (
            can_sum(remaining, numbers) == True
        ):  # here we are ignoring the validity of the children
            return True
    return False


print(can_sum(7, [2, 4]))
print(can_sum(7, [5, 3, 4, 7]))
# print(can_sum(300, [7, 14])) # too slow

# memoization of the above function
# we recognize that we can remember the result of the function for a particular target! Since the numbers wont change our memoization can include only the target!
def can_sum_memo(target, numbers, memo={}):
    if target in memo:
        return memo[target]
    if target == 0:
        return True
    if target < 0:
        return False
    for num in numbers:
        remaining = target - num
        if can_sum_memo(remaining, numbers, memo) == True:
            memo[target] = True
            return True
    memo[target] = False
    return memo[target]


print(can_sum_memo(300, [7, 14]))  # fast!
