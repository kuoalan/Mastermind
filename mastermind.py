# Importing modules
import tkinter as tk
import random
from tkinter import messagebox as mb

# Setting up initial window.
window = tk.Tk()
window.geometry("275x350")
window.resizable(0,0)
window.configure(bg="#cdcfd1")
window.title("MASTERMIND")
game_frame = tk.Frame(window, width=275, height=400)
color_map = {1:"blue", 2:"red", 3:"green", 4:"yellow", 5:"purple", 6:"white"}


class Square(object):
    """
    Represents a square used by player to input a guess in the interface.
    """
    def __init__(self, canvas, coords):
        """

        :param canvas: The canvas the square is drawn on
        :param coords: Coordinates used to draw the square
        """
        # Initializing color to blue.
        self.curr_color = 1
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(coords, fill="blue")
        # Binds color changing function to left mouse click
        self.canvas.tag_bind(self.id, "<Button-1>", self.next_color)

    def next_color(self, event=None):
        """Function for changing color of Square to next color in order"""
        if self.curr_color <= 5:
            self.curr_color += 1
        else:
            self.curr_color = 1
        self.canvas.itemconfigure(self.id, fill=color_map[self.curr_color])

    def change_color(self, color):
        """Function for changing color of Square to a specific color passed in as parameter."""
        self.canvas.itemconfigure(self.id, fill=color_map[color])

    def disable(self):
        """Function for disabling color changing on click"""
        self.canvas.tag_unbind(self.id, "<Button-1>")

class Solution(object):
    """
    Represents the solution code for an instance of the game
    """
    def __init__(self):
        """
        Initializes value of solution
        """
        self.solution = [random.randint(1, 6) for _ in range(4)]
        self.sol_count = {}
        for num in self.solution:
            self.sol_count[num] = self.solution.count(num)


    def check_guess(self, guess):
        """
        Function for checking a user-provided guess against solution. Returns feedback on accuracy.
        Black pegs represent correct color in correct place. White pegs represent correct color in incorrect place.

        :param guess: Passing in guess input by user as an array
        :return: Returns number of black and white pegs as a tuple.
        """
        # Initializing dictionary to hold guess information and variables
        guess_count = {}
        black_pegs = 0
        matches = 0
        # Getting counts of each color in the guess and comparing to the solution
        for num in guess:
            guess_count[num] = guess.count(num)
        for key in guess_count:
            if key in self.sol_count:
                if self.sol_count[key] < guess_count[key]:
                    matches += self.sol_count[key]
                else:
                    matches += guess_count[key]
        # Iterating through guess to get number of position matches
        for i in range(len(guess)):
            if self.solution[i] == guess[i]:
                black_pegs += 1
        white_pegs = matches - black_pegs
        return black_pegs, white_pegs


class GUI(object):

    def __init__(self):
        """
        Initializes GUI and game instance by calling function for resetting game.
        """
        self.reset_game()

    def reset_game(self):
        """
        Resets GUI and game parameters

        :return: None
        """
        # Sets current guess to first guess
        self.guess_num = 1
        # Creates new canvas for drawing current guess on
        self.active_guess = tk.Canvas(window, width=150, height=45, highlightthickness=0, background="#d9dadb", borderwidth=1, relief="groove")
        self.active_guess.place(x=10, y = 50)
        # Creates squares for player to input guess
        self.square_1 = Square(self.active_guess, (10, 10, 35, 35))
        self.square_2 = Square(self.active_guess, (45, 10, 70, 35))
        self.square_3 = Square(self.active_guess, (80, 10, 105, 35))
        self.square_4 = Square(self.active_guess, (115, 10, 140, 35))
        # Creating and placing button for submitting guess
        self.submit_button = tk.Button(window, text="Submit Guess!", highlightbackground="#cdcfd1", highlightcolor="#cdcfd1", command=self.add_guess)
        self.submit_button.place(x=167, y=62)
        # Creating and placing label for game name
        self.game_name = tk.Label(window, text="MASTERMIND", background="#cdcfd1", font="Arial 30 bold")
        self.game_name.place(x=50, y=5)
        # Creating and placing brain icon. Brain icon from pixabay.com (no attribution required)
        self.brain_icon = tk.PhotoImage(file="brain_icon_small.gif")
        self.game_icon = tk.Label(image=self.brain_icon, background="#cdcfd1")
        self.game_icon.place(x=15,y=5)
        # Creating canvas for drawing guesses on
        self.guess_list = tk.Canvas(window, width=250, height = 200, highlightthickness=0, background="#d9dadb", borderwidth=1, relief="groove")
        self.guess_list.place(x = 10, y = 110)
        # Adding list of guess numbers
        for i in range(8):
            self.guess_list.create_text(10, 40+(i*20), font="Arial 12 bold", text = f"{i+1}.")
        # Creating headers for guess list
        self.guess_list.create_text(55,15, font="Arial 14 bold", text="Guesses")
        self.guess_list.create_text(175,15, font="Arial 14 bold", text="Score")
        # Creating and placing game reset button
        self.reset_button = tk.Button(window, text="New Game", highlightbackground="#cdcfd1", highlightcolor="#cdcfd1", command=self.clear_board)
        self.reset_button.place(x=8, y=320)
        # Creating and placing game instruction button
        self.info_button = tk.Button(window, text="Instructions", highlightbackground="#cdcfd1", highlightcolor="#cdcfd1", command=self.show_instructions)
        self.info_button.place(x=185, y = 320)
        # Creates instance of solution code
        self.solution = Solution()

    def clear_board(self):
        """
        Function for clearing board of UI elements
        :return:
        """
        ui_elements=[self.active_guess,self.submit_button,self.game_icon, self.game_name, self.guess_list, self.reset_button, self.info_button]
        for element in ui_elements:
            element.destroy()
        self.reset_game()

    def victory_message(self):
        """
        Creates pop-up when player wins

        :return: None
        """
        mb.showinfo("You won!", "Congratulations, you figured out the code! Please press New Game to play again.")

    def lose_message(self):
        """
        Creates pop-up when player loses

        :return: None
        """
        mb.showinfo("You lost!", "Too bad, you didn't figure out the code! Please click New Game to try again.")

    def show_instructions(self):
        """
        Creates pop-up with instructions on how to play the game

        :return: None
        """
        mb.showinfo("Instructions", "The evil computer has created a code of 4 colors (duplicate colors allowed!), and your job is to figure it out before it's too late!\n\nYou will have 8 tries, and you will receive feedback for each incorrect guess.\n\nA black circle means that you have entered a correct color in the correct position.\n\nA white circle means that you have entered a correct color in the incorrect position\n\nGood luck!")

    def disable_inputs(self):
        """
        Disables player input for submitting a guess. Called after the game is over.

        :return: None
        """
        self.submit_button["state"] = "disabled"
        self.submit_button.config(text="Correct answer")
        self.submit_button.place(x=167, y=62)
        self.square_1.disable()
        self.square_2.disable()
        self.square_3.disable()
        self.square_4.disable()

    def create_circle(self, x, y, radius, canvas, **kwargs):
        """
        Function for creating a circle with specified center and radius.

        :param x: X-coordinate for center of circle
        :param y: Y coordinate for center of circle
        :param radius: Radius of circle
        :param canvas: Canvas to draw the circle on
        :param kwargs: Keyword arguments to pass into tkinter oval creation
        :return: Object ID of created circle
        """
        x_1 = x - radius
        y_1 = y - radius
        x_2 = x + radius
        y_2 = y + radius
        return canvas.create_oval(x_1, y_1, x_2, y_2, **kwargs)

    def add_guess(self):
        """
        Evaluates and adds current guess to the list of guesses

        :return: None
        """
        # Initializes variables/arrays for evaluating current guess
        guess_num = self.guess_num
        curr_guess = [self.square_1.curr_color, self.square_2.curr_color, self.square_3.curr_color, self.square_4.curr_color]
        pos = 0
        # Gets evaluation of scores from solution class method
        scores = self.solution.check_guess(curr_guess)
        # Creating circles representing black pegs
        for _ in range(scores[0]):
            self.create_circle(160+(20*pos), 17+(20*guess_num-1), 5, self.guess_list, fill="black")
            pos += 1
        # Creating circles representing white pegs
        for _ in range(scores[1]):
            self.create_circle(160+(20*pos), 17+(20*guess_num-1), 5, self.guess_list, fill="white")
            pos += 1
        # Adding guess to list of previous guesses
        for i in range(4):
            self.guess_list.create_rectangle(25+(20*i), 30+(20*(guess_num-1)), (20*i)+40, 45+(20*(guess_num-1)), fill = color_map[curr_guess[i]])
        # If player has made a correct guess, run victory procedure
        if scores[0] == 4:
            # Show victory pop up
            self.victory_message()
            # Disable user input for making more guesses
            self.disable_inputs()
            return
        # Incrementing current guess number
        self.guess_num += 1
        # If user has made 8 incorrect guesses, run procedure for game loss
        if self.guess_num == 9:
            # Show losing pop up
            self.lose_message()
            # Disable user input for making more guesses
            self.disable_inputs()
            # Switch active guess to show correct solution
            correct_sol = self.solution.solution
            self.square_1.change_color(correct_sol[0])
            self.square_2.change_color(correct_sol[1])
            self.square_3.change_color(correct_sol[2])
            self.square_4.change_color(correct_sol[3])
            return


# Starts game if script is run directly.
if __name__ == '__main__':
    game = GUI()
    window.mainloop()
