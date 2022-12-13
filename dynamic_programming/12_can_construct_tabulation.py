# same problem like before using iteration this time


def can_construct(target, wordlist):
    arr = [False for _ in range(len(target) + 1)]
    # False because this is a boolean function
    # arr represents if we can construct string upto that position
    arr[0] = True  # base case
    for i, val in enumerate(arr):
        if val is False:  # if we cannot reach here no point going forward
            continue
        for word in wordlist:
            if target[i:].startswith(word):  # if the string matches as needed
                if i + len(word) <= len(target):  # if we are in bounds
                    arr[i + len(word)] = True  # update the value
    return arr[len(target)]


print(can_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))  # abc+def, True
print(
    can_construct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"])
)  # not possible, False
res = can_construct(
    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef", ["e", "ee", "eee", "eeee", "eeeeee"]
)
print(res)
