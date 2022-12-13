# same problem but iterative


def count_construct(target, wordbank):
    arr = [0 for _ in range(len(target) + 1)]
    arr[0] = 1  # base case we can construct the ''
    for i, val in enumerate(arr):
        if val == 0:
            continue
        for word in wordbank:
            if target[i:].startswith(word):  # if our condition is satisfied
                if len(word) + i <= len(target):  # if we are in bounds
                    arr[len(word) + i] += val  # update that position

    return arr[len(target)]


# examples (fast)
r = count_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"])
print(r)

r = count_construct("purple", ["purp", "p", "ur", "le", "purpl"])
print(r)
