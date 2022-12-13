from pprint import pprint

# same deal return all the constructions possible

# this is different
# we need to return a 2d array of all possible ways
# eg: abc : [[a,b,c], [ab,c], [abc], ...]


def all_construct(target, wordlist):
    if target == "":
        return [[]]  # use base cases to guide what should be here
    out = []
    for word in wordlist:
        if target.startswith(word):
            res = all_construct(target[len(word) :], wordlist)
            # if the children can construct the word, we add the current word and create a bigger list
            # think how we can combine the children's solution to pass along to the parent node
            out.extend([[word, *k] for k in res])

    return out


# read base cases carefully
r = all_construct("hello", ["cat", "dog", "mouse"])  # []
pprint(r)

r = all_construct("", ["cat", "dog", "mouse"])  # [[]]
pprint(r)

r = all_construct("abcdef", ["ab", "abc", "cd", "def", "abcd", "ef", "c"])  # 4 ways
pprint(r)

# now we memoize
def all_construct(target, wordlist, memo={}):
    if target in memo:
        return memo[target]
    if target == "":
        return [[]]  # use base cases to guide what should be here
    out = []
    for word in wordlist:
        if target.startswith(word):
            res = all_construct(target[len(word) :], wordlist, memo)
            # if the children can construct the word, we add the current word and create a bigger list
            # think how we can combine the children's solution to pass along to the parent node
            out.extend([[word, *k] for k in res])

    memo[target] = out
    return out


# read base cases carefully
r = all_construct("hello", ["cat", "dog", "mouse"])  # []
pprint(r)

r = all_construct("", ["cat", "dog", "mouse"])  # [[]]
pprint(r)
# fast
r = all_construct("abcdef", ["ab", "abc", "cd", "def", "abcd", "ef", "c"])  # 4 ways
pprint(r)
