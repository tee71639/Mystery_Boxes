import random

number_trials = 10
winnings = 0

cost = number_trials * 5

for item in range(0, number_trials):
    prize = ""
    round_winnings = 0

    for thing in range(0, 3):

        # randint finds numbers between given endpoints, including both endpoints
        prize_number = random.randint(1,4)
        prize += " "
        if prize_number == 1:
            prize += "gold"
            round_winnings += 5
        elif prize_number == 2:
            prize += "silver"
            round_winnings += 2
        elif prize_number == 3:
            prize += "copper"
            round_winnings += 1
        else:
            prize += "lead"

    print("You won {} which is worth {}!".format(prize, round_winnings))
    winnings += round_winnings

print("=========================================================")
print("Paid In: ${}".format(cost))
print("Pay Out: ${}".format(winnings))
print("=========================================================")

if winnings > cost:
    print("You came out ${} ahead!".format(winnings-cost))
else:
    print("You lost ${}!".format(cost-winnings))
print("=========================================================")