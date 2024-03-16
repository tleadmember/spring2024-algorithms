import sys
from timeit import default_timer as timer
from collections import defaultdict 

# # Non-optimized recursion
# def stirling_2nd(n,k):
#     if n < 0 or k < 0: return -999999 # no negative input
#     elif n > 0 and k == 0: return 0
#     elif n == k and k >= 0: return 1
#     elif n > 1 and k == 1: return 1
#     elif n < k: return 0
#     else: return k*stirling_2nd(n-1,k) + stirling_2nd(n-1,k-1) # general case

# # Top-down DP
# dp = defaultdict(lambda: "Not Present") 
# def stirling_2nd(n,k):    
#     if (n,k) in dp: return dp[n,k]
#     if n < 0 or k < 0: return -999999 # no negative input
#     elif n > 0 and k == 0: dp[n,k] = 0
#     elif n == k and k >= 0: dp[n,k] = 1
#     elif n > 1 and k == 1: dp[n,k] = 1
#     elif n < k: return 0
#     else: dp[n,k] = k*stirling_2nd(n-1,k) + stirling_2nd(n-1,k-1)
#     return dp[n,k]

# Bottom-up DP
def stirling_2nd(n,k):    
    dp = defaultdict(lambda: "Not Present")
    if n < 0 or k < 0: return -999999 # no negative input
    for i in range(1,n+1): dp[i,0] = 0
    for i in range(0,min(n,k)+1): dp[i,i] = 1
    for i in range(2,n+1): dp[i,1] = 1
    for i in range(0,n+1):
        for j in range(1,k+1):
            if i < j: dp[i,j] = 0
    for i in range(3,n+1):
        for j in range(2,k+1):
            if i == j: break
            dp[i,j] = j*dp[i-1,j] + dp[i-1,j-1]
    return dp[n,k]
   
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("Sterling number second kind program needs 2 integer inputs!")
        sys.exit(1)
    # print("Passed, sort of.")
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    start = timer()
    res = stirling_2nd(n,k)
    end = timer()
    print(res)
    sys.stdout.flush()
    msg = "Time elapsed: {} seconds."
    formatted_msg = msg.format(end-start)
    print(formatted_msg)
    sys.stdout.flush()
