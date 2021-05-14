"""
Name: Jasmin Maizel
Final Project subject: Cryptography - Enigma
this is the plugboard file - it sets the plugboard of the enigma.
Python Version: 3.7.4
Date: 10.02.2021
"""


class Plugboard:
    """
    this is the plugboard class. it can have up to 10
    """
    def __init__(self):
        """
        the function sets initial setting of plugboard
        """
        self.plugboard1 = []
        self.plugboard2 = []

    def get_plugboard(self):
        """
        this function returns the plugboard.
        :return:
        """
        return self.plugboard1, self.plugboard2

    def add_letter(self, letter):
        """
        function adds a letter to the plugboard unless there are 10 pairs.
        :param letter:
        :return: None if the letter was added to the plugboard, string if otherwise.
        """
        if (len(self.plugboard1) < 10 or
            (len(self.plugboard1) == 10 and self.plugboard2[-1] is None)) and \
                letter not in self.plugboard1 and letter not in self.plugboard2:
            if len(self.plugboard1) == 0 or (len(self.plugboard1) < 10 and
                                             self.plugboard2[-1] is not None):
                self.plugboard1.append(letter)
                self.plugboard2.append(None)
            elif self.plugboard2[-1] is None:
                self.plugboard2[-1] = letter
        else:
            if letter in self.plugboard1:
                position = self.plugboard1.index(letter)
                self.plugboard1.remove(letter)
                if self.plugboard2[position] is not None:
                    self.plugboard2.remove(self.plugboard2[position])
            elif letter in self.plugboard2:
                position = self.plugboard2.index(letter)
                self.plugboard2.remove(letter)
                self.plugboard1.remove(self.plugboard1[position])
            else:
                return "plugboard is full"
        return None

    def reset_plugboard(self):
        """
        this function resets the plugboard
        :return:
        """
        self.plugboard1 = []
        self.plugboard2 = []

    def return_encrypted_letter(self, letter):
        """
        the function returns the value of the letter after encryption by plugboard
        :param letter:
        :return:
        """
        if letter in self.plugboard1:
            position = self.plugboard1.index(letter)
            if self.plugboard2[position] is None:
                return letter
            return self.plugboard2[position]
        if letter in self.plugboard2:
            position = self.plugboard2.index(letter)
            return self.plugboard1[position]
        return letter
