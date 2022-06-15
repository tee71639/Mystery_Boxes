from tkinter import *
from functools import partial # to prevent unwanted windows
import random


class Start:
    def __init__(self, parent):

        # gui to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.push_me_button = Button(text="Push Me", command=self.to_game)
        self.push_me_button.grid(row=0, pady=10)

    def to_game(self):

        # retrieve starting balance
        starting_balance = 50
        stakes = 1

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

        # play gui setup
        self.game_box = Toplevel()
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
        self.box_one = Label(self.mystery_frame, text="?", justify=CENTER, bg=box_color, height=3, width=10, font="Arial 12 bold")
        self.box_one.grid(row=0, column=0, padx=10, pady=10)

        # box two
        self.box_two = Label(self.mystery_frame, text="?", justify=CENTER, bg=box_color, height=3, width=10, font="Arial 12 bold")
        self.box_two.grid(row=0, column=1, padx=5, pady=10)

        # box three
        self.box_three = Label(self.mystery_frame, text="?", justify=CENTER, bg=box_color, height=3, width=10, font="Arial 12 bold")
        self.box_three.grid(row=0, column=2, padx=10, pady=10)

        # open boxes button (row 3)
        self.box_button = Button(self.game_box, text="Open Boxes", font="Arial 16 bold", bg="#FFFF33", height=2, width=25)
        self.box_button.grid(row=3, pady=10)

        # text that shows the player's balance (row 4)
        self.balance_text = Label(self.game_box, text="Welcome, your starting balance is ${}".format(starting_balance), font="Arial 12 bold", fg="#2e7d1b")
        self.balance_text.grid(row=4, padx=5, pady=5)

        # support buttons (row 5)
        self.support_frame = Frame(self.game_box)
        self.support_frame.grid(row=5)

        # help button
        self.help_button = Button(self.support_frame, text="Help / Rules", font="Arial 16 bold", fg="white", bg="grey")
        self.help_button.grid(row=0, column=0, padx=5, pady=5)

        # stats button
        self.stats_button = Button(self.support_frame, text="Game Stats...", font="Arial 16 bold", fg="white", bg="#2b4680")
        self.stats_button.grid(row=0, column=1, padx=5, pady=10)




# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
