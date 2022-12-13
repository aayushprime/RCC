# find the fib(n)

from functools import cache


@cache
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# fast because of cache
print(fib(50))


# Tabulation
# Iterative method of thinking
# 1 and 2 are used to form 3
# So instead of using recursion we use iteration, we use arrays, each element in array represents a subproblem's solution


def fib(n):
    arr = [0 for _ in range(max(n + 1, 2))]
    arr[0] = 0
    arr[1] = 1
    for i in range(2, n + 1):
        arr[i] = arr[i - 1] + arr[i - 2]
    print(arr[n])


fib(50)

# instead of looking back and updating self, we can also look forward and update others
def fib(n):
    arr = [
        0 for _ in range(max(n + 2, 2))
    ]  # make the array 2 larger for correct value at the end
    arr[0] = 0
    arr[1] = 1
    for i in range(n):
        arr[i + 1] += arr[i]
        arr[i + 2] += arr[i]
    print(arr[n])


fib(50)

# contrast the same implementation but one is recursive and another is iterative
