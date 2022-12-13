# write a funetion that takes a target string and an array of stings
# return a boolean indicating whether the target can be constructed from the cobination of the array of strings

"""
def can_construct(target:str, wordlist:List[str]):
    pass
"""
from typing import List

# own attempt
def can_construct(target: str, wordlist: List[str]):
    # base cases
    if target in wordlist:
        return True

    for word in wordlist:
        if target.startswith(word):
            if can_construct(target[len(word) :], wordlist):
                return True
    return False


# things to learn
# the empty base case can_construct('', any_list) => True (I'll just take nothing)
def can_construct(target, wordlist):
    if target == "":  # this base case is better way of thinking
        return True
    for word in wordlist:
        if target.startswith(word):
            if can_construct(target[len(word) :], wordlist):
                return True
    return False


# examples
print(can_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))  # abc+def, True
print(
    can_construct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"])
)  # not possible, False
# slow
# res = can_construct(
#     "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeeee"]
# )
# print(res)


# now we memoize
def can_construct(target, wordlist, memo={}):
    if target in memo:
        return memo[target]
    # no need to add result to memo if we are in the base case(whats the point right?)
    if target == "":
        return True
    for word in wordlist:
        if target.startswith(word):
            if can_construct(target[len(word) :], wordlist, memo):
                memo[target] = True
                return True
    memo[target] = False
    return False


# examples
print(can_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))  # abc+def, True
print(
    can_construct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"])
)  # not possible, False
res = can_construct(
    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeeee"]
)
print(res)
