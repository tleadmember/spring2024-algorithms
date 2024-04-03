import sys
from timeit import default_timer as timer
from collections import defaultdict 

""" Reading inputs """
with open(sys.argv[1], 'r') as my_file:
    input = my_file.readline().strip()
    n = int(input)
    input = my_file.readline().strip()
    segments_list = list(map(int, input.split()))
    
""" Start timing """
start = timer()

""" Prefix sum """
pf_sum_list = [0]*(n+1)
pf_sum_list[1] = segments_list[0] # pf_sum_list index starts from 1
for i in range(2, n+1):
    pf_sum_list[i] = pf_sum_list[i-1] + segments_list[i-1]

# print(n)
# print(segments_list)
# print(segments_list[0])
# print(n+segments_list[0])
# print(pf_sum_list)

# """ Naive recursion """
# def T(i,j):
#     length = pf_sum_list[j] - pf_sum_list[i-1]
#     if i == j: # base case
#         return length
#     return length - min(T(i+1,j), T(i,j-1))
    
""" Bottom up DP """
def T(i,j):
    dp = defaultdict(lambda: "Not Present")

    for k in range(1, n+1): # base case
        dp[k,k] = pf_sum_list[k] - pf_sum_list[k-1]

    for a in range(1, n):
        for b in range(1, n-a+1):
            dp[b,b+a] = pf_sum_list[b+a] - pf_sum_list[b-1] - min(dp[b+1,b+a], dp[b,b+a-1])
    
    return dp[i,j]


""" Output """
print( T(1, n) )

""" End timing """
end = timer()
msg = "Time elapsed: {} ms."
formatted_msg = msg.format((end-start)*1000)
print(formatted_msg)