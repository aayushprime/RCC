# iterative implementation of grid traveler problem
# we can move only down or right
# so we form a grid where each cell represents the solution  to move from there to the end
# 00 01 02 # value at 01 represents the best way to move to 22 from 01(a subproblem)
# 10 11 12
# 20 21 22

# Classic recursive solution
# take the size of the grid and return number of ways
def grid_travel(x, y):
    if x == 0 or y == 0:
        return 0
    if x == 1 and y == 1:
        return 1
    return grid_travel(x - 1, y) + grid_travel(x, y - 1)


r = grid_travel(3, 3)
print(r)

from pprint import pprint

# now we try iterative
def grid_travel(x, y):
    res = [[0 for _ in range(y + 1)] for _ in range(x + 1)]
    # since we are counting starting with 0 is a good start
    # fill res[1][1] with 1 since there is only one way to go from
    res[1][1] = 1  # what we know
    for i in range(x + 1):
        for j in range(y + 1):
            if j + 1 <= y:  # check for bounds
                res[i][j + 1] += res[i][
                    j
                ]  # we can reach the right neighbour from here in res[i][j] ways
            if i + 1 <= x:
                res[i + 1][j] += res[i][j]
    return res[x][y]


r = grid_travel(2, 6)
print(r)

# visualize as a table
# table size is based on input
# choose initial values for tables
# choose the seed value(base case) like 1,1 here
# iterate over the table and find some logic to update based on a base case
