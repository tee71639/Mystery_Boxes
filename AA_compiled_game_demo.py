from tkinter import *
from functools import partial # to prevent unwanted windows
import random


class Start:
    def __init__(self, parent):

        # gui to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # set initial balance to zero
        self.starting_funds = IntVar()
        self.starting_funds.set(0)

        # mystery heading (row 0)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game", font="Arial 19 bold")
        self.mystery_box_label.grid(row=0)

        # initial instructions (row 1)
        self.mystery_instructions = Label(self.start_frame, font="Arial 10 italic", text="Please enter a dollar amount " "(between $5 and $50) in the box " "below. Then choose the " "stakes. The higher the stakes, " "the more you can win!", wrap=275, justify=LEFT, padx=10, pady=10)
        self.mystery_instructions.grid(row=1)

        # entry box, button & error label (row 2)
        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame, font="Arial 19 bold", width=10)
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame, font="Arial 14 bold", text="Add Funds", command=self.check_funds)
        self.add_funds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, font="Arial 10 bold", wrap=275, justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # button frame (row 3)
        self.stakes_frame = Frame(self.start_frame)
        self.stakes_frame.grid(row=3)

        # buttons go here
        button_font = "Arial 12 bold"
        # orange low stakes button
        self.low_stakes_button = Button(self.stakes_frame, text="Low ($5)", command=lambda: self.to_game(1), font=button_font, bg="#FF9933")
        self.low_stakes_button.grid(row=0, column=0, pady=10)

        # yellow medium stakes button
        self.medium_stakes_button = Button(self.stakes_frame, text="Medium ($10)", command=lambda: self.to_game(2), font=button_font, bg="#FFFF33")
        self.medium_stakes_button.grid(row=0, column=1, padx=5, pady=10)

        # green high stakes button
        self.high_stakes_button = Button(self.stakes_frame, text="High ($15)", command=lambda: self.to_game(3), font=button_font, bg="#99FF33")
        self.high_stakes_button.grid(row=0, column=2, pady=10)

        # disable all stakes buttons at start
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        # help button
        self.help_button = Button(self.start_frame, text="How to Play", bg="#808080", fg="white", font=button_font)
        self.help_button.grid(row=5, pady=10)

    def check_funds(self):
        starting_balance = self.start_amount_entry.get()
        
        # set error background colors (and assume that there are no errors 
        # at the start)
        error_back = "#ffafaf"
        has_errors = "no"

        # change background to white (for testing purposes)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # disable all stakes buttons in case user changes mind and decreases       # amount entered
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry, the least you " \
                                 "can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too high! The most you can risk in " \
                                 "this game is $50"
            
            elif starting_balance >= 15:
                # enable all buttons
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
                self.high_stakes_button.config(state=NORMAL)
            elif starting_balance >= 10:
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
            else:
                self.low_stakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (no text / decimals)"
        
        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback, fg="red")

        else:
            # set starting balance to amount entered by user
            self.starting_funds.set(starting_balance)

    def to_game(self, stakes):

        # retrieve starting balance
        starting_balance = self.starting_funds.get()

        Game(self, stakes, starting_balance)

        # hide start up window
        root.withdraw()

class Game:

    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        # initialise variables
        self.balance = IntVar()

        # set starting balance to amount entered by user at start of game
        self.balance.set(starting_balance)

        # get value of stakes (use it as multiplier when calculating winnings)
        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        # list for holding statistics
        self.round_stats_list = []

        # play gui setup
        self.game_box = Toplevel()

        # if users press cross at top right, game quits
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)

        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # play heading (row 0)
        self.play_heading = Label(self.game_box, text="Play...", font="Arial 20 bold")
        self.play_heading.grid(row=0, pady=10)

        # play instructions (row 1)
        self.play_instructions = Label(self.game_box, text="Press <enter> or click the 'Open Boxes' button to reveal the contents of the mystery boxes.", font="Arial 10", wrap=275, justify=LEFT, padx=10, pady=20)
        self.play_instructions.grid(row=1)

        # mystery boxes (row 2)
        self.mystery_frame =  Frame(self.game_box)
        self.mystery_frame.grid(row=2)

        # boxes go here
        box_color = "#a5d192"

        # box one
        self.prize1_label = Label(self.mystery_frame, text="?", justify=CENTER, bg=box_color, height=3, width=10, font="Arial 12 bold")
        self.prize1_label.grid(row=0, column=0, padx=10, pady=10)

        # box two
        self.prize2_label = Label(self.mystery_frame, text="?", justify=CENTER, bg=box_color, height=3, width=10, font="Arial 12 bold")
        self.prize2_label.grid(row=0, column=1, padx=5, pady=10)

        # box three
        self.prize3_label = Label(self.mystery_frame, text="?", justify=CENTER, bg=box_color, height=3, width=10, font="Arial 12 bold")
        self.prize3_label.grid(row=0, column=2, padx=10, pady=10)

        # play button goes here (row 3)
        self.play_button = Button(self.game_box, text="Open Boxes", bg ="#FFFF33", font="Arial 15 bold", width=20, padx=10, pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

        # bind button to <enter> (users can push enter to reveal the boxes)

        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
        self.play_button.grid(row=3)

        # text that shows the game cost (row 4)
        self.balance_label = Label(self.game_box, text="Game Cost: ${} \n \n How much will you win?".format(5*stakes), font="Arial 12 bold", fg="#2e7d1b", justify=LEFT)
        self.balance_label.grid(row=4, padx=5, pady=5)

        # support buttons (row 5)
        self.support_frame = Frame(self.game_box)
        self.support_frame.grid(row=5)

        # help button
        self.help_button = Button(self.support_frame, text="Help / Rules", font="Arial 16 bold", fg="white", bg="grey")
        self.help_button.grid(row=0, column=0, padx=5, pady=5)

        # stats button
        self.stats_button = Button(self.support_frame, text="Game Stats...", font="Arial 16 bold", fg="white", bg="#2b4680")
        self.stats_button.grid(row=0, column=1, padx=5, pady=10)

    def reveal_boxes(self):
        # retrieve the balance from the initial function
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winnings = 0
        prizes = []
        prize_stats_list = []
        backgrounds = []

        for item in range(0, 3):
            prize_num = random.randint(1,100)

            if 0 < prize_num <= 5:
                prize = "gold\n(${})".format(5* stakes_multiplier)
                prize_stats = "gold"
                round_winnings += 5 * stakes_multiplier
                back_color = "#CEA935"  # gold color
            elif 5 < prize_num <= 25:
                prize = "silver\n(${})".format(2* stakes_multiplier)
                prize_stats = "silver"
                round_winnings += 2 * stakes_multiplier
                back_color = "#B7B7B5"   # silver color
            elif 25 < prize_num <= 65:
                prize = "copper\n(${})".format(1* stakes_multiplier)
                prize_stats = "copper"
                round_winnings += 1 * stakes_multiplier
                back_color = "#BC7F61"   # copper color
            else:
                prize = "lead\n($0)"
                prize_stats = "lead"
                back_color = "#595E71"  # lead color

            print("You won {} which is worth ${}!".format(prize_stats, round_winnings))
            print("=========================================================")
            
            prizes.append(prize)
            prize_stats_list.append(prize_stats)
            backgrounds.append(back_color)

        # display prizes and edit background
        self.prize1_label.config(text=prizes[0], bg=backgrounds[0])

        self.prize2_label.config(text=prizes[1], bg=backgrounds[1])

        self.prize3_label.config(text=prizes[2], bg=backgrounds[2])

        # deduct cost of game
        current_balance -= 5 * stakes_multiplier

        # add winnings
        current_balance += round_winnings
        
        # set balance to new balance
        self.balance.set(current_balance)

        balance_statement = "Game Cost: ${}\nPayback: ${} \nCurrent Balance: ${}".format(5 * stakes_multiplier, round_winnings, current_balance)
        print(balance_statement)
        print("*=======================================================*")

        # edit label so user can see their balance
        self.balance_label.configure(text=balance_statement)

        # stop user from playing if their balance is too low
        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")

            balance_statement = "Current Balance: ${}\n Your balance is too low. You can only quit or view your stats. Sorry about that.".format(current_balance)
            self.balance_label.config(fg="#660000", font="Arial 10 bold", wrap=300, text=balance_statement)

    def to_quit(self):
        root.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
