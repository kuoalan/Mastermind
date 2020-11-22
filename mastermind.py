import tkinter as tk
import random
from tkinter import messagebox as mb

window = tk.Tk()
window.geometry("275x350")
window.resizable(0,0)
window.configure(bg="#cdcfd1")
window.title("MASTERMIND")
game_frame = tk.Frame(window, width=275, height=400)
color_map = {1:"blue", 2:"red", 3:"green", 4:"yellow", 5:"purple", 6:"white"}


class Square(object):

    def __init__(self, canvas, coords):
        self.curr_color = 1
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(coords, fill="blue")
        self.canvas.tag_bind(self.id, "<Button-1>", self.next_color)

    def next_color(self, event=None):
        if self.curr_color <= 5:
            self.curr_color += 1
        else:
            self.curr_color = 1
        self.canvas.itemconfigure(self.id, fill=color_map[self.curr_color])

    def change_color(self, color):
        self.canvas.itemconfigure(self.id, fill=color_map[color])

    def disable(self):
        self.canvas.tag_unbind(self.id, "<Button-1>")

class Solution(object):
    def __init__(self):
        self._solution = [random.randint(1,6) for _ in range(4)]

    def check_guess(self, guess):
        sol_count = {}
        guess_count = {}
        black_pegs = 0
        matches = 0
        for num in self._solution:
            sol_count[num] = self._solution.count(num)
        print(sol_count)
        for num in guess:
            guess_count[num] = guess.count(num)
        print(guess_count)
        for key in guess_count:
            if key in sol_count:
                if sol_count[key] < guess_count[key]:
                    matches += sol_count[key]
                else:
                    matches += guess_count[key]
        for i in range(4):
            if self._solution[i] == guess[i]:
                black_pegs += 1
        white_pegs = matches - black_pegs
        return black_pegs, white_pegs

    def get_sol(self):
        return self._solution





class GUI(object):

    def __init__(self):
        self.reset_game()

    def victory_message(self):
        mb.showinfo("You won!", "Congratulations, you figured out the code! Please press New Game to play again.")
    def lose_message(self):
        mb.showinfo("You lost!", "Too bad, you didn't figure out the code! Please click New Game to try again.")
    def show_instructions(self):
        mb.showinfo("Instructions", "The evil computer has created a code of 4 colors (duplicate colors allowed!), and your job is to figure it out before it's too late!\n\nYou will have 8 tries, and you will receive feedback for each incorrect guess.\n\nA black circle means that you have entered a correct color in the correct position.\n\nA white circle means that you entered have a correct color in the incorrect position\n\nGood luck!")
    def disable_inputs(self):
        self.submit_button["state"] = "disabled"
        self.submit_button.config(text="Correct answer")
        self.submit_button.place(x=167, y=62)
        self.square_1.disable()
        self.square_2.disable()
        self.square_3.disable()
        self.square_4.disable()
    def create_circle(self, x, y, radius, canvas, **kwargs):
        x_1 = x - radius
        y_1 = y - radius
        x_2 = x + radius
        y_2 = y + radius
        return canvas.create_oval(x_1, y_1, x_2, y_2, **kwargs)

    def add_guess(self):
        guess_num = self.guess_num
        curr_guess = [self.square_1.curr_color, self.square_2.curr_color, self.square_3.curr_color, self.square_4.curr_color]
        scores = self.solution.check_guess(curr_guess)
        pos = 0
        for _ in range(scores[0]):
            self.create_circle(160+(20*pos), 17+(20*guess_num-1), 5, self.guess_list, fill="black")
            pos += 1
        for _ in range(scores[1]):
            self.create_circle(160+(20*pos), 17+(20*guess_num-1), 5, self.guess_list, fill="white")
            pos += 1
        for i in range(4):
            self.guess_list.create_rectangle(25+(20*i), 30+(20*(guess_num-1)), (20*i)+40, 45+(20*(guess_num-1)), fill = color_map[curr_guess[i]])
        if scores[0] == 4:
            self.victory_message()
            self.disable_inputs()
            return
        self.guess_num += 1
        if self.guess_num == 9:
            self.lose_message()
            self.disable_inputs()
            correct_sol = self.solution.get_sol()
            print(correct_sol)
            self.square_1.change_color(correct_sol[0])
            print(correct_sol[0])
            print(correct_sol[1])
            self.square_2.change_color(correct_sol[1])
            self.square_3.change_color(correct_sol[2])
            self.square_4.change_color(correct_sol[3])
            return
    def clear_board(self):
        ui_elements=[self.active_guess,self.submit_button,self.game_icon, self.game_name, self.guess_list, self.reset_button, self.info_button]
        for element in ui_elements:
            element.destroy()
        self.reset_game()
    def reset_game(self):
        self.guess_num = 1
        self.active_guess = tk.Canvas(window, width=150, height=45, highlightthickness=0, background="#d9dadb", borderwidth=1, relief="groove")
        self.active_guess.place(x=10, y = 50)
        self.square_1 = Square(self.active_guess, (10, 10, 35, 35))
        self.square_2 = Square(self.active_guess, (45, 10, 70, 35))
        self.square_3 = Square(self.active_guess, (80, 10, 105, 35))
        self.square_4 = Square(self.active_guess, (115, 10, 140, 35))
        self.submit_button = tk.Button(window, text="Submit Guess!", highlightbackground="#cdcfd1", highlightcolor="#cdcfd1", command=self.add_guess)
        self.submit_button.place(x=167, y=62)
        self.game_name = tk.Label(window, text="MASTERMIND", background="#cdcfd1", font="Arial 30 bold")
        self.game_name.place(x=50, y=5)
        self.brain_icon = tk.PhotoImage(file="brain_icon_small.gif")
        self.game_icon = tk.Label(image=self.brain_icon, background="#cdcfd1")
        self.game_icon.place(x=15,y=5)
        self.guess_list = tk.Canvas(window, width=250, height = 200, highlightthickness=0, background="#d9dadb", borderwidth=1, relief="groove")
        self.guess_list.place(x = 10, y = 110)
        for i in range(8):
            self.guess_list.create_text(10, 40+(i*20), font="Arial 12 bold", text = f"{i+1}.")
        self.guess_list.create_text(55,15, font="Arial 14 bold", text="Guesses")
        self.guess_list.create_text(175,15, font="Arial 14 bold", text="Score")
        self.reset_button = tk.Button(window, text="New Game", highlightbackground="#cdcfd1", highlightcolor="#cdcfd1", command=self.clear_board)
        self.reset_button.place(x=8, y=320)
        self.info_button = tk.Button(window, text="Instructions", highlightbackground="#cdcfd1", highlightcolor="#cdcfd1", command=self.show_instructions)
        self.info_button.place(x=185, y = 320)
        self.solution = Solution()


game = GUI()
window.mainloop()