import random

reels = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]


def spin():
    spinResult = ''
    for reel in reels:
        spinResult += str(random.choice(reel))
    return spinResult


counter = 0

for i in range(10000):
    currSpin = spin()
    if currSpin == '777':
        counter += 1

print(f"There were a total of {counter} jackpots hit!")
