import sys
from timeit import default_timer as timer

""" Reading inputs """
with open(sys.argv[1], 'r') as my_file:
    input = my_file.readline().strip()
    n = int(input)
    input = my_file.readline().strip()
    segments_list = list(map(int, input.split()))
    
""" Start timing """
start = timer()

""" Prefix sum """
pf_sum_list = [0]*n
pf_sum_list[0] = segments_list[0]
for i in range(1, n):
    pf_sum_list[i] = pf_sum_list[i-1] + segments_list[i]

# print(n)
# print(segments_list)
# print(segments_list[0])
# print(n+segments_list[0])
# print(pf_sum_list)

""" Naive recursion """
def T(i,j):
    if i == 0:
        length = pf_sum_list[j]
    else:
        length = pf_sum_list[j] - pf_sum_list[i-1]
    if i == j: # base case
        return length
    return length - min(T(i+1,j), T(i,j-1))

""" Output """
print( T(0, n-1) )

""" End timing """
end = timer()
msg = "Time elapsed: {} ms."
formatted_msg = msg.format((end-start)*1000)
# print(formatted_msg)