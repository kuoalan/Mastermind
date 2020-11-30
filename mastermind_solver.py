# Name: Alan Kuo
# Course: CS 325
# Assignment: Portfolio Project - Mastermind Solver

import random
import itertools


class SolutionChecker(object):
    """
    Represents an instance of checking a candidate solution against the list of guesses provided.
    """
    def __init__(self, candidate_sol, guesses):
        """
        Initializing object

        :param candidate_sol: The candidate solution to check against guesses.
        :param guesses: The list of guesses and scores provided.
        """
        self.candidate = candidate_sol
        self.guesses = guesses
        # Getting counts of colors in the candidate
        self.candidate_count = {}
        for num in self.candidate:
            self.candidate_count[num] = self.candidate.count(num)

    def get_candidate(self):
        """
        Getter function for candidate solution

        :return: Array representing the ordering of colors in the solution
        """
        return self.candidate

    def scoring(self, guess):
        """
        Class method to score a guess from the list of guesses against the candidate solution.

        :param guess
        :return: Returns the number of black and white pegs for the guess

        """
        # Initializing dictionary to hold guess information and variables
        guess_count = {}
        black_pegs = 0
        matches = 0
        # Getting counts of each color in the guess and comparing to the solution
        for num in guess[0]:
            guess_count[num] = guess[0].count(num)
        for key in guess_count:
            if key in self.candidate_count:
                if self.candidate_count[key] < guess_count[key]:
                    matches += self.candidate_count[key]
                else:
                    matches += guess_count[key]
        # Iterating through guess to get number of position matches
        for i in range(len(guess)+1):
            if self.candidate[i] == guess[0][i]:
                black_pegs += 1
        white_pegs = matches - black_pegs
        return black_pegs, white_pegs

    def verify_score(self, score, guess):
        """
        Helper function for verifying if score (against candidate solution) is consistent with score provided for a single guess.

        :param score: Score returned from scoring class method
        :param guess: Guess to be checked
        :return: Boolean, True if score is consistent, False if score does not match
        """
        black_pegs = score[0]
        white_pegs = score[1]
        if black_pegs != guess[1] or white_pegs != guess[2]:
            return False
        return True

    def score_guess_list(self):
        """
        Helper function for verifying the score of each guess in the list of guesses compared to the candidate solution.

        :return: Boolean, True if verification passes for all guesses in the list. False if verification fails for any guess in the list.
        """
        for guess in self.guesses:
            score = self.scoring(guess)
            if self.verify_score(score, guess) is False:
                return False
        return True

def candidate_scoring(candidate, source):
    # Initializing dictionary to hold guess information and variables
    candidate_count = {}
    source_count = {}
    black_pegs = 0
    matches = 0
    # Getting counts of each color in the guess and comparing to the solution
    for num in candidate:
        candidate_count[num] = candidate.count(num)
    for num in source:
        source_count[num] = source.count(num)
    for key in candidate_count:
        if key in source_count:
            if source_count[key] < candidate_count[key]:
                matches += source_count[key]
            else:
                matches += candidate_count[key]
    # Iterating through guess to get number of position matches
    for i in range(len(candidate)):
        if source[i] == candidate[i]:
            black_pegs += 1
    white_pegs = matches - black_pegs
    return black_pegs, white_pegs


def candidate_generator(guess):
    """
    Function for generating a list of candidate solutions based on information from a guess.

    :param guess: The guess to use as a starting point for generating a list of candidate solutions.
    """
    guess_count = {}
    black_pegs = guess[1]
    combo_list = []
    possible_candidate_list = []
    candidate_list_3 = []
    final_candidates = []
    # Getting counts of each color in the guess
    for num in guess[0]:
        guess_count[num] = guess.count(num)
    # Creating list of possible combinations of indices representing black pegs (where the color and index are correct).
    combinations_tuples = (list(itertools.combinations([0,1,2,3], black_pegs)))
    # for combo in combinations_tuples:
    #     combo_list.append(list(combo))
    # for combo in combo_list:

    # For each combination of black peg indices, create all possible candidates
    for combo in combinations_tuples:
        # Initializing candidate
        possible_candidate = [0,0,0,0]
        for i in range(4):
            # If index is a black peg, set color as the same as the color from the guess
            if i in combo:
                possible_candidate[i] = guess[0][i]
        # Add candidate to the list of candidates
        possible_candidate_list.append(possible_candidate)
    # While there are still possible candidates to process
    while possible_candidate_list:
        for possibility in possible_candidate_list:
            if 0 not in possibility:
                candidate_list_3.append(possibility)
                possible_candidate_list.remove(possibility)
            else:
                for i in range(4):
                    if possibility[i] == 0:
                        for j in range(1,7):
                            def func(k=j):
                                curr_possibility = possibility
                                def func_2():
                                    curr_possibility[i] = k
                                    curr_digits = int("".join(map(str, curr_possibility)))
                                    return curr_digits
                                return func_2
                            func3 = func()
                            new_possibility = [int(x) for x in str(func3())]
                            possible_candidate_list.append(new_possibility)
    [final_candidates.append(x) for x in candidate_list_3 if x not in final_candidates]
    final_candidates.remove(guess[0])
    for final_candidate in final_candidates:
        score = candidate_scoring(final_candidate, guess[0])
        if score[1] != guess[2]:
            final_candidates.remove(final_candidate)
    return final_candidates


def solver(guess_list_to_check, candidate_to_check):
    # Creating list of candidates
    candidate_list = candidate_generator(candidate_to_check)
    for entry in candidate_list:
        test = SolutionChecker(entry, guess_list_to_check)
        # If candidate is consistent with provided list of guesses and scores
        if test.score_guess_list() is True:
            return test.get_candidate()
    # No candidates are consistent with provided list of guesses and scores
    return "No solution"


def sort_guesses(list_to_sort):
    """
    Merge sort function for sorting list of guesses by the number of black pegs.
    Based on previous implementation in HW assignment 1.

    :param list_to_sort:
    :return: sorted list of guesses
    """
    if len(list_to_sort) < 2:
        return list_to_sort
    else:
        mid_index = len(list_to_sort) // 2
        left_array = sort_guesses(list_to_sort[:mid_index])
        right_array = sort_guesses(list_to_sort[mid_index:])
        return merge(left_array, right_array)


def merge(array1, array2):
    """
    Helper function for merge sort. Merges two arrays in descending order of black pegs.
    Based on previous implementation in HW assignment 1.

    :param array1: first array to merge
    :param array2: second array
    :return: merged array
    """
    new_array = []
    while array1 and array2:
        # Comparing black pegs for each guess in arrays, adding the one with more black pegs.
        if array1[0][1] > array2[0][1]:
            new_array.append(array1.pop(0))
        else:
            new_array.append(array2.pop(0))
    # Handling any remaining activities
    if array1:
        new_array += array1
    elif array2:
        new_array += array2
    return new_array



# guess_list = [[[1,1,3,2], 2, 1], [[1,3,2,1], 2, 1]]
# guess_list = [[[1,1,1,1],0,0],[[1,2,2,2],0,0],[[3,3,3,3],0,0],[[4,4,4,4],2,0],[[4,5,5,4],1,2],[[4,5,5,6],0,3],[[5,5,6,4],3,0]]
# candidate = [[5,5,6,4],3,0]
# guess_list = [[[1,1,1,1],2,0],[[1,1,2,2,],1,1],[[3,2,1,1],1,1],[[1,2,1,5],1,1]]
# candidate = [[2,1,1,6],3,0]
# guess_list = [[[1,1,1,1],1,0],[[2,2,2,2],0,0],[[3,3,3,3],0,0],[[4,4,4,4],1,0],[[5,5,5,5],1,0],[[1,5,5,6],0,3], [[1,4,5,6],1,3]]
# candidate = [[5,4,6,1],1,3]
# guess_list = [[[1,1,1,1],0,0], [[2,2,2,2],0,0],[[3,2,3,3],0,1],[[4,5,4,4],1,1], [[5,5,4,6],3,1]]
# candidate = [[5,4,3,6],2,2]
guess_list = [[[1,1,1,1],0,0], [[2,2,2,2],1,0], [[3,3,3,3],1,0], [[4,4,4,4],0,0],[[2,6,6,3],1,1],[[2,3,5,5],2,2]]
# candidate = [[6,4,5,4],2,0]
# guess_list = [[[1,1,1,1],0,0],[[2,2,2,2],1,0],[[3,4,4,3],0,1]]

# print(sort_guesses(guess_list))
# candidate = guess_list[0]

# Starts game if script is run directly.
if __name__ == '__main__':
    # Creating mapping of colors to integers from 1 to 6
    color_map = {"blue": 1, "red": 2, "green": 3, "yellow": 4, "purple": 5, "white": 6}
    rev_color_map = {1: "blue", 2: "red", 3: "green", 4: "yellow", 5: "purple", 6: "white"}
    guess_list = []
    with open("solve.txt","r") as input_file:
        data_remaining = True
        while data_remaining is True:
            input_array = []
            guess_colors = []
            guess_formatted = []
            guess_data = input_file.readline()
            if guess_data == "":
                data_remaining = False
            else:
                input_array.append([i.rstrip() for i in guess_data.split(" ")])
                for i in range(4):
                    guess_colors.append(color_map[input_array[0][i]])
                guess_formatted.append(guess_colors)
                for i in range(4,6):
                    guess_formatted.append(int(input_array[0][i]))
                guess_list.append(guess_formatted)
    sort_guesses(guess_list)
    print(guess_list)
    candidate = guess_list[0]
    solution = (solver(guess_list, candidate))
    solution_array = []
    for i in range(4):
        solution_array.append(rev_color_map[solution[i]])
    solution_string = ", ".join(map(str,solution_array))
    print(f"A possible solution is: {solution_string}")





