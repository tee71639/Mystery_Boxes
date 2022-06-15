# could not remember if i should use randint or randrange so checked that
# randint would randomly generate all four of the numbers 1, 2, 3, 4

import random

number_trials = 10
for item in range(0, number_trials):

    # randint finds numbers between given endpoints, including both endpoints
    prize_number = random.randint(1,4)
    print(prize_number)