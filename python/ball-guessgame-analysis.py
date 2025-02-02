## A small program to calculate possibilities in a game that I learned with my
## sister.
##
## Each person gets an amount of paper balls (same amount for everyone) - they
## pick a set amount and hide it in their hand. Everyone puts their hands on
## the table, closed, and the person that guesses the right sum wins.
##
## I was trying to see the best "lazy" guesses and it seems that the best bet
## is usually the max sum divided by two.

from queue import Queue

def permutations(num_balls: int, num_players: int) -> list[list[int]]:
    ret = []

    q = Queue()
    q.put([])

    while not q.empty():
        x = q.get()
        if len(x) < num_players:
            for i in range(num_balls + 1):
                q.put(x + [i])
        else:
            ret.append(x)

    return ret

def analyze_possibilities(num_balls: int, num_players: int) -> None:
    sums = {}

    for choices in permutations(num_balls, num_players):
        s = sum(choices)
        sums[s] = sums.get(s, 0) + 1

    print(f"With {num_balls=}, {num_players=}:")
    for k, v in sums.items():
        print(f"sum={k}: {v} times")
    print()

# the game we tried: 3 balls for each person, 4 people playing
# max sum is 12, half is 6 and it's the main amount of sums
analyze_possibilities(3, 4)

# in this case the max sum is 9
# 9/2 = 4.5, and the sums 4 and 5 are both winners here.
# so I guess it doesn't matter if you round it up or down.
analyze_possibilities(3, 3)
