import sys
from timeit import default_timer as timer
from collections import defaultdict

# # Non-optimized recursion
# BOTH = "both"
# LEFT = "left"
# RIGHT = "right"
# # option = defaultdict(lambda: "Not Present") # --> wrong to put option[] out here
# def LPS(string, i, j):
#     option = defaultdict(lambda: "Not Present")
#     # print("Indices " + str(i) + " and " + str(j))
#     if i == j: return 1
#     if i > j: return 0
#     option[BOTH] = match(string[i], string[j]) + LPS(string, i+1, j-1)
#     option[LEFT] = 0 + LPS(string, i+1, j)
#     option[RIGHT] = 0 + LPS(string, i, j-1)
#     # print(str(option))
#     max_index = max(option, key=option.get)
#     return option.get(max_index)

def match(a, b):
    # print(a)
    # print(b)
    if a == b:
        return 2
    else:
        return 0 

# Top-down DP
dp = defaultdict(lambda: "Not Present")
def LPS(string, i, j):
    if (i,j) in dp: return dp[i,j]
    if i == j: return 1
    if i > j: return 0
    option_both = match(string[i], string[j]) + LPS(string, i+1, j-1)
    option_left = 0 + LPS(string, i+1, j)
    option_right = 0 + LPS(string, i, j-1)
    dp[i,j] = max(option_both, option_left, option_right)
    return dp[i,j]


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Problem needs 1 string input!")
        sys.exit(1)
    # print("Passed, sort of.")
    string = sys.argv[1]
    start = timer()
    res = LPS(string, 0, len(string)-1) # LPS means Longest Palindromic Subsequence
    end = timer()
    print(res)
    sys.stdout.flush()
    msg = "Time elapsed: {} seconds."
    formatted_msg = msg.format(end-start)
    print(formatted_msg)
    sys.stdout.flush()
