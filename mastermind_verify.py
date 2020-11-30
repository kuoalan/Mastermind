# Name: Alan Kuo
# Course: CS 325
# Assignment: Portfolio Project - Certificate solution verification


class solution_checker(object):
    """
    Represents an instance of checking a certificate solution against the list of guesses and scores provided.
    """
    def __init__(self, certificate, guess_list):
        """
        Initializing object

        :param candidate: The certificate solution to check against guesses.
        :param guess_list: The list of guesses and scores provided.
        """
        self.certificate = certificate
        self.guess_list = guess_list
        # Getting counts of colors in the candidate
        self.certificate_count = {}
        for num in self.certificate:
            self.certificate_count[num] = self.certificate.count(num)

    def get_certificate(self):
        """
        Getter function for certificate solution

        :return: Array representing the ordering of colors in the solution
        """
        return self.certificate

    def scoring(self, guess):
        """
        Class method to score a guess from the list of guesses against the certificate solution.

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
            if key in self.certificate_count:
                if self.certificate_count[key] < guess_count[key]:
                    matches += self.certificate_count[key]
                else:
                    matches += guess_count[key]
        # Iterating through guess to get number of position matches
        for i in range(len(guess)+1):
            if self.certificate[i] == guess[0][i]:
                black_pegs += 1
        white_pegs = matches - black_pegs
        return black_pegs, white_pegs

    def verify_score(self, score, guess):
        """
        Helper function for verifying if score (against certificate solution) is consistent with score provided for a single guess.

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
        Helper function for verifying the score of each guess in the list of guesses compared to the certificate solution.

        :return: Boolean, True if verification passes for all guesses in the list. False if verification fails for any guess in the list.
        """
        for guess in self.guess_list:
            score = self.scoring(guess)
            if self.verify_score(score, guess) is False:
                return False
        return True

if __name__ == '__main__':
    # Creating mapping of colors to integers from 1 to 6
    color_map = {"blue": 1, "red": 2, "green": 3, "yellow": 4, "purple": 5, "white": 6}
    rev_color_map = {1: "blue", 2: "red", 3: "green", 4: "yellow", 5: "purple", 6: "white"}
    guess_list = []
    with open("verify.txt","r") as input_file:
        solution_to_verify = []
        solution_data = input_file.readline()
        solution_to_verify.append([i.rstrip() for i in solution_data.split(" ")])
        for i in range(4):
            solution_to_verify.append(color_map[solution_to_verify[0][i]])
        del solution_to_verify[0]
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
    print(solution_to_verify)
    print(guess_list)
    if solution_to_verify and guess_list:
        verification = solution_checker(solution_to_verify,guess_list)
        if verification.score_guess_list() is True:
            print("This solution is valid.")
        else:
            print("This solution is not valid.")
    else:
        print("No information entered.")