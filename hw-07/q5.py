import sys
from timeit import default_timer as timer
from collections import defaultdict 

# # Non-optimized recursion
# def rod(n):
#     # if n <= 0: return -999999 # no negative or zero input
#     if n == 1: return 1
#     elif n == 2: return 2
#     elif n == 3: return 4
#     else: return rod(n-1) + rod(n-2) + rod(n-3) # general case

# Bottom-up DP
def rod(n): # n>0
    dp = defaultdict(lambda: "Not Present")
    dp[1] = 1 # can have some IF conditions to return early
    dp[2] = 2
    dp[3] = 4
    for i in range (4,n+1): dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
    return dp[n]
   
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Problem needs 1 integer input!")
        sys.exit(1)
    # print("Passed, sort of.")
    n = int(sys.argv[1])
    start = timer()
    res = rod(n)
    end = timer()
    print(res)
    sys.stdout.flush()
    msg = "Time elapsed: {} seconds."
    formatted_msg = msg.format(end-start)
    print(formatted_msg)
    sys.stdout.flush()
