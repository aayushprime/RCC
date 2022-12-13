from pprint import pprint

# same problem but now we are using iterative method
def all_construct(target, wordlist):
    # assume there are no ways to create a random string
    arr = [None for _ in range(len(target) + 1)]
    arr[0] = [[]]  # base case: one way to create the '' which is to take none
    for i, val in enumerate(arr):
        if val is None:
            continue
        for word in wordlist:
            if target[i:].startswith(word):
                if len(word) + i <= len(target):  # we are in bounds
                    if arr[len(word) + i] is None:
                        # if the destination is not already reachable
                        # add the word to the already existing path in self and update destination
                        arr[len(word) + i] = [[*k, word] for k in val]
                    else:
                        # add an extra path to the destination
                        arr[len(word) + i].extend([[*k, word] for k in val])
    return arr[len(target)]


# read base cases carefully
r = all_construct("hello", ["cat", "dog", "mouse"])  # []
pprint(r)
r = all_construct("", ["cat", "dog", "mouse"])  # [[]]
pprint(r)
r = all_construct("abcdef", ["ab", "abc", "cd", "def", "abcd", "ef", "c"])  # 4 ways
pprint(r)
