import random
number_trials = 100
winnings = 0

cost = number_trials * 5

for item in range(0, number_trials):
    # prize = ""
    round_winnings = 0

    for thing in range(0, 3):

        # randint finds numbers between given endpoints, including  both endpoints
        prize_number = random.randint(1, 100)
        # prize += " "
        if 0 < prize_number <= 5:
            round_winnings += 5
        elif 5 < prize_number <= 25:
            round_winnings += 2
        elif 25 < prize_number <= 65:
            round_winnings += 1
        '''else:
            prize += "lead"'''

    # print("You won {} which is worth {}".format(prize, round_winnings))
    winnings += round_winnings

print("=========================================================")
print("Paid in: ${}".format(cost))
print("Paid out: ${}".format(winnings))
print("=========================================================")

if winnings > cost:
    print("You came out ${} ahead!".format(winnings-cost))
else:
    print("You lost ${}!".format(cost-winnings))
print("=========================================================")

