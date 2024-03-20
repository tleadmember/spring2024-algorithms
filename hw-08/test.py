from collections import defaultdict 

# print(max(1,4))

# for i in range(3,2): print("iteration" + i)

# option = defaultdict(lambda: "Not Present")
# option[0] = 900
# option[1] = 1
# option[2] = 911
# max_index = max(option, key=option.get)
# print(option.get(max_index))

def match(a, b):
    if a == b:
        return 2
    else:
        return 0 
    
print(match("as", "a"))
