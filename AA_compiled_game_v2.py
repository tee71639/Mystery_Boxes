from tkinter import *
from functools import partial # to prevent unwanted windows
import random
import re

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

        # how to play button
        self.howplay_button = Button(self.start_frame, text="How to Play", bg="#808080", fg="white", font=button_font, command=self.how_play)
        self.howplay_button.grid(row=5, pady=5)

    def how_play(self):
        HowPlay(self)

    def check_funds(self):
        starting_balance = self.start_amount_entry.get()
        
        # set error background colors (and assume that there are no errors 
        # at the start)
        error_back = "#ffafaf"
        has_errors = "no"

        # change background to white (for testing purposes)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # disable all stakes buttons in case user changes mind and decreases amount entered
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
        self.game_stats_list=[starting_balance, starting_balance]

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
        self.balance_label = Label(self.game_box, text="Game Cost: ${}\n \nHow much will you win?".format(5*stakes), font="Arial 12 bold", fg="#2e7d1b", justify=LEFT)
        self.balance_label.grid(row=4, padx=5, pady=5)

        # support buttons (row 5)
        self.support_frame = Frame(self.game_box)
        self.support_frame.grid(row=5)

        # help button
        self.help_button = Button(self.support_frame, text="Help / Rules", font="Arial 16 bold", fg="white", bg="grey", command=self.to_help)
        self.help_button.grid(row=0, column=0, padx=5, pady=5)

        # stats button
        self.stats_button = Button(self.support_frame, text="Game Stats...", font="Arial 16 bold", fg="white", bg="#2b4680", command=lambda: self.to_stats(self.round_stats_list, self.game_stats_list))
        self.stats_button.grid(row=0, column=1, padx=5, pady=10)

    def to_help(self):
        Help(self)

    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)

    def reveal_boxes(self):
        # retrieve the balance from the initial function
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winnings = 0
        prizes = []
        prize_stats_list = []
        backgrounds = []

        for item in range(0, 3):
            prize_num = random.randint(1, 100)

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
        # update game_stats_list with current balance (replace item in position 1 with  current balance)
        self.game_stats_list[1] = current_balance

        balance_statement = "Game Cost: ${} \nPayback: ${} \nCurrent Balance: ${}".format(5 * stakes_multiplier, round_winnings, current_balance)
        print(balance_statement)
        print("*=======================================================*")

        # add round results to statistics list
        round_summary = "{} | {} | {} - Cost: ${} | " \
                        "Payback: ${} | Current Balance: " \
                        "${}".format(prize_stats_list[0], prize_stats_list[1], prize_stats_list[2], 5 * stakes_multiplier, round_winnings, current_balance)
        self.round_stats_list.append(round_summary)
        print(self.round_stats_list)

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

class Help:
    def __init__(self, partner):

        # disable help button
        partner.help_button.config(state=DISABLED)

        # sets up child window (ie: help box)
        self.help_box = Toplevel()

        # if users press cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # set up gui frame
        self.help_frame = Frame(self.help_box, width=300)
        self.help_frame.grid()

        # set up help heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions", font="arial 14 bold")
        self.how_heading.grid(row=0)

        help_text="Choose an amount to play with and then choose the stakes. Higher stakes cost more per round but you can win more as well.\n\n When you enter the play area, you will see three mystery boxes. To reveal the contents of the boxes, click the 'Open Boxes' button or press <Enter>. If you don't have enough money to play, the button will turn red and you will need to quit the game.\n\n The contents of the boxes will be added to your balance. The boxes could contain...\n\n Low: Lead ($0) | Copper ($1) | Silver ($2) | Gold ($10)\n Medium: Lead ($0) | Copper ($2) | Silver ($4) | Gold ($25)\n High: Lead ($0) | Copper ($5) | Silver ($10) | Gold ($50)\n\n If each box contains gold, you earn $30 (low stakes). If they contained copper, silver and gold, you would receive $13 ($1 + $2 + $10) and so on."

        # help text (label, row 1)
        self.help_text = Label(self.help_frame, text=help_text, justify=LEFT, wrap=400, padx=10, pady=10)
        self.help_text.grid(row=1)

        # dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10, bg="#660000", fg="white", font="arial 15 bold", command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        self.help_box.destroy()
        partner.help_button.config(state=NORMAL)

class HowPlay:
    def __init__(self, partner):

        # disable help button
        partner.howplay_button.config(state=DISABLED)

        # sets up child window (ie: help box)
        self.howplay_box = Toplevel()

        # if users press cross at top, closes help and 'releases' help button
        self.howplay_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # set up gui frame
        self.howplay_frame = Frame(self.howplay_box, width=300)
        self.howplay_frame.grid()

        # set up help heading (row 0)
        self.howplay_heading = Label(self.howplay_frame, text="Help / Instructions", font="arial 14 bold")
        self.howplay_heading.grid(row=0)

        help_text="Choose an amount to play with and then choose the stakes. Higher stakes cost more per round but you can win more as well.\n\n When you enter the play area, you will see three mystery boxes. To reveal the contents of the boxes, click the 'Open Boxes' button or press <Enter>. If you don't have enough money to play, the button will turn red and you will need to quit the game.\n\n The contents of the boxes will be added to your balance. The boxes could contain...\n\n Low: Lead ($0) | Copper ($1) | Silver ($2) | Gold ($10)\n Medium: Lead ($0) | Copper ($2) | Silver ($4) | Gold ($25)\n High: Lead ($0) | Copper ($5) | Silver ($10) | Gold ($50)\n\n If each box contains gold, you earn $30 (low stakes). If they contained copper, silver and gold, you would receive $13 ($1 + $2 + $10) and so on."

        # help text (label, row 1)
        self.support_text = Label(self.howplay_frame, text=help_text, justify=LEFT, wrap=400, padx=10, pady=10)
        self.support_text.grid(row=1)

        # dismiss button (row 2)
        self.dismiss_instructions_btn = Button(self.howplay_frame, text="Dismiss", width=10, bg="#660000", fg="white", font="arial 15 bold", command=partial(self.close_help, partner))
        self.dismiss_instructions_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        self.howplay_box.destroy()
        partner.howplay_button.config(state=NORMAL)


class GameStats:
    def __init__(self, partner, game_history, game_stats):

        print(game_history)

        # disable help button
        partner.stats_button.config(state=DISABLED)

        heading = "Arial 12 bold"
        content = "Arial 12"

        # sets up child window (ie: help box)
        self.stats_box = Toplevel()

        # if users press cross at top, closes help and 'releases' help button

        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # set up gui frame
        self.stats_frame = Frame(self.stats_box)
        self.stats_frame.grid()

        # set up help heading (row 0)
        self.stats_heading_label = Label(self.stats_frame, text="Game Statistics", font="arial 19 bold")
        self.stats_heading_label.grid(row=0)

        # to export <instuctions> (row 1)
        self.export_instructions = Label(self.stats_frame, text="Here are your Game Statistics. Please use the Export button to access the results of each round that you played", wrap=250, font="arial 10 italic", justify=LEFT, fg="green", padx=10, pady=10)
        self.export_instructions.grid(row=1)

        # starting balance (row 2)
        self.details_frame = Frame(self.stats_frame)
        self.details_frame.grid(row=2)

        # starting balance (row 2.0)

        self.start_balance_label = Label(self.details_frame, text="Starting Balance:", font=heading, anchor="e")
        self.start_balance_label.grid(row=0, column=0, padx=0)

        self.start_balance_value_label = Label(self.details_frame, font=content, text="${}".format(game_stats[0]), anchor="w")
        self.start_balance_value_label.grid(row=0, column=1, padx=0)

        # current balance (row 2.2)
        self.current_balance_label = Label(self.details_frame, text="Current Balance:", font=heading, anchor="e")
        self.current_balance_label.grid(row=1, column=0, padx=0)
        
        self.current_balance_value_label = Label(self.details_frame, font=content, text="${}".format(game_stats[1], anchor="w"))
        self.current_balance_value_label.grid(row=1, column=1, padx=0)

        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "#660000"

        # amount won / lost (row 2.3)
        self.win_loss_label = Label(self.details_frame, text=win_loss, font=heading, anchor="e")
        self.win_loss_label.grid(row=2, column=0, padx=0)

        self.win_loss_value_label = Label(self.details_frame, font=content, text="${}".format(amount), fg=win_loss_fg, anchor="w")
        self.win_loss_value_label.grid(row=2, column=1, padx=0)

        # rounds played (row 2.4)
        self.games_played_label = Label(self.details_frame, text="Rounds Played:", font=heading, anchor="e")
        self.games_played_label.grid(row=4, column=0, padx=0)

        self.games_played_value_label = Label(self.details_frame, font=content, text=len(game_history), anchor="w")
        self.games_played_value_label.grid(row=4, column=1, padx=0)

        # export and dismiss buttons
        self.buttons_frame = Frame(self.stats_frame)
        self.buttons_frame.grid(row=3)

        self.export_button = Button(self.buttons_frame, text="Export...", font="arial 16 bold", fg="white", bg="#2b4680", command=partial(lambda: self.to_export(partner, game_history, game_stats)))
        self.export_button.grid(row=0, column=0, padx=5, pady=10)

        self.dismiss_button = Button(self.buttons_frame, text="Dismiss", font="arial 16 bold", fg="white", bg="#660000", command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=0, column=1, padx=5, pady=10)

    def close_stats(self, partner):
        self.stats_box.destroy()
        partner.stats_button.config(state=NORMAL)

    def to_export(self, partner, game_history, game_stats):
        Export(self, game_history, game_stats)

class Export:
    def __init__(self, partner, game_history, all_game_stats):

        print(game_history)

        # disable export button
        partner.export_button.config(state=DISABLED)

        # sets up child window (ie: export box)
        self.export_box = Toplevel()

        # if users press cross at top, closes export and 'releases' export button
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

        # set up gui frame
        self.export_frame = Frame(self.export_box, width=300)
        self.export_frame.grid()

        # set up export heading (row 0)
        self.how_heading = Label(self.export_frame, text="Export / Instructions", font="arial 14 bold")
        self.how_heading.grid(row=0)

        # export instructions (label, row 1)
        self.export_text = Label(self.export_frame, text="Enter a filename in the box below and press the Save button to save your calculation history to the text file.", justify=LEFT, width=40, wrap=250)
        self.export_text.grid(row=1)

        # warning text (label, row 2)
        self.export_text = Label(self.export_frame, text="If the filename you enter below already exists, its contents will be replaced with your calculation history.", justify=LEFT, bg="#ffafaf", fg="maroon", font="Arial 10 italic", wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)

        # filename entry box (row 3)
        self.filename_entry = Entry(self.export_frame, width=20, font="Arial 14 bold",justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        # error message labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon")
        self.save_error_label.grid(row=4)

        # save / cancel frame (row 5)
        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)

        # save and cancel buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_cancel_frame, text="Save", font="Arial 15 bold", bg="#003366", fg="white", command=partial(lambda: self.save_history(partner, game_history, all_game_stats)))
        self.save_button.grid(row=0, column=0)

        self.cancel_button = Button(self.save_cancel_frame, text="Cancel", font="Arial 15 bold", bg="#660000", fg="white", command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1)

    def close_export(self, partner):
        self.export_box.destroy()
        partner.export_button.config(state=NORMAL)

    def save_history(self, partner, game_history, game_stats):

        # regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"

        filename = self.filename_entry.get()
        print(filename)

        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "(no spaces allowed)"
            else:
                problem = ("(no {}'s allowed".format(letter))
            has_error = "yes"
            break

        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        if has_error == "yes":
            # display error message
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            # change entry box background to pink
            self.filename_entry.config(bg="#ffafaf")
            print()

        else:
            # if there are no errors, generate text file and then close dialogue
            # add .txt suffix!
            filename = filename + ".txt"

            # create file to hold data
            f = open(filename, "w+")

            # heading for stats
            f.write("Game Statistics\n\n")

            # game stats
            for round in game_stats:
                print(round)
                f.write(round + "\n")

            # heading for rounds
            f.write("\nRound Details\n\n")

            # add new line at end of each item
            for item in game_history:
                f.write(item + "\n")
            
            # close file
            f.close

                


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
