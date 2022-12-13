# same deal but count the possible combinations this time
# wordbank is infinite

# quite easy if you follow the progression
def count_construct(target, wordbank):
    if target == "":
        return 1
    s = 0
    for word in wordbank:
        if target.startswith(word):
            s += count_construct(target[len(word) :], wordbank)
    return s


# examples
r = count_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"])
print(r)

r = count_construct("purple", ["purp", "p", "ur", "le", "purpl"])
print(r)

# lets memoize
def count_construct(target, wordbank, memo={}):
    if target in memo:
        return memo[target]
    if target == "":
        return 1
    s = 0
    for word in wordbank:
        if target.startswith(word):
            s += count_construct(target[len(word) :], wordbank)
    memo[target] = s
    return memo[target]


# examples (fast)
r = count_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"])
print(r)

r = count_construct("purple", ["purp", "p", "ur", "le", "purpl"])
print(r)
