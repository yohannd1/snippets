import sys, random

LENGTH = (int(sys.argv[1]) if len(sys.argv) > 1 else 4)

arr = list("abcdefghklmnopqrstuvwxyz0123456789")
random = [arr[x] for x in [random.randint(0, len(arr) - 1) for rand in range(LENGTH)]]

print("".join(random))
