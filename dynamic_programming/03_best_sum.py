# this time return the shortest sequence of numbers that make up the number

# best_sum(7, [5, 3, 4, 7]) = [7]
# best_sum(8, [2, 3, 5]) = [5, 3]

# NOTE: Taking the largest numbers first doesn't yield the best result!
# this problem when encountered alone might encourage us to go that route, but its wrong!
# exhaustive search is the way to go!


def best_sum(target, numbers, memo={}):
    # memo base case
    if target in memo:
        return memo[target]
    # if we are already at 0 then we have gotten where we want, kickstart the accumulation with []
    if target == 0:
        return []
    # if target is less than 0 then we have overshoot(the sought out case is not possible)
    if target < 0:
        return None
    # a place to keep all children solutions
    possible = []
    for num in numbers:
        # compute the children solutions
        remainder = target - num
        res = best_sum(remainder, numbers, memo)
        # if the children solution is valid add it to possible solutions
        if res is None:
            continue
        # we can compare the length right here and keep only the shortest array only for better space complexity
        possible.append(
            [*res, num]
        )  # remember to add the number to the children's solution
    # find the best (min length array in the possible solutions)
    result = sorted(possible, key=lambda x: len(x))
    # if there are no solution possibles(the children have all failed, you fail as well)
    if len(result) == 0:
        # Returning? memoize first!
        memo[target] = None
        return memo[target]
    # return the best, but memoize first
    memo[target] = result[0]
    return memo[target]


print(best_sum(8, [2, 3, 5]))
print(best_sum(100, [1, 2, 5, 25]))  # instant
