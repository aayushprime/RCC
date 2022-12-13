# basically the same as calc_sum but the function must also return how the numbers were added up to get the target


def how_sum(target, numbers, way=[]):
    if target == 0:
        print(way)
        return
    if target < 0:
        return

    for num in numbers:
        remainder = target - num
        way.append(num)
        how_sum(remainder, numbers, way)
        way.pop()


how_sum(7, [5, 3, 4, 7])
print("----")


def how_sum(target, numbers):
    if target == 0:
        return []
    if target < 0:
        return None

    for num in numbers:
        remainder = target - num
        remainder_result = how_sum(remainder, numbers)
        if remainder_result is not None:
            # return as soon as we find the fisrt matching element
            # if remainder_result is not None then it means we found one that is valid
            # as a parent we extend the child's solution and return the result
            return [*remainder_result, num]
    return None


print(how_sum(7, [2, 3]))
print("Slow")
# print(how_sum(300, [7, 14]))

# lets memoize this
def how_sum_memo(target, numbers, memo={}):
    if target in memo:
        return memo[target]
    if target == 0:
        return []
    if target < 0:
        return None

    for num in numbers:
        remainder = target - num
        remainder_result = how_sum_memo(remainder, numbers, memo)

        if remainder_result is not None:
            # return as soon as we find the fisrt matching element
            # if remainder_result is not None then it means we found one that is valid
            # as a parent we extend the child's solution and return the result
            memo[target] = [*remainder_result, num]
            return [*remainder_result, num]
    # notice the following two lines! in the non memoized case return None can be skipped, because reutrn None is implicit
    # but for memoization we need to add it to memo!
    memo[target] = None
    return None


# fast
print(how_sum_memo(300, [7, 14]))
