"""
Name: Jasmin Maizel
Final Project subject: Cryptography - Enigma
this is the enigma  file - it encrypts text using the enigma.
the enigma is adjustable as used to be in WWII.
Python Version: 3.7.4
Date: 10.02.2021
"""

import random
from rotors import Rotors
from reflector import Reflector
from plugboard import Plugboard


class Enigma:
    """
    this class is the main class of the enigma machine simulator.
    it will encrypt and decrypt messages.
    """

    def __init__(self):
        """
        sets the initial machine with reflector, default rotors and default plugboard.
        """
        self.__reflector = Reflector()
        self.plugboard = Plugboard()
        self.rotors = Rotors()

    def decrypt_encrypt_text(self, text):
        """
        encrypts or decrypts a whole text
        :param text:
        :return:
        """
        text_after_enigma = ""
        for i in text:
            letter_after_enigma, encryption_str = self.encrypt_letter(i)
            text_after_enigma += letter_after_enigma
        return text_after_enigma

    def encrypt_letter(self, letter):
        """
        encrypts a given letter
        :param letter:
        :return: encrypted letter and encryption string which explains the stages
        of the encryption. used in the simulator when showing the encryption stages.
        """
        encryption_str = "the letter to encrypt: " + letter + "\n"
        letter = letter.upper()
        encryption_str += "letters on rotors: " + str(self.rotors.letter_on_rotors()) + "\n"
        encryption_str += "letter before plugboard = " + letter + "\n"
        letter_after_plugboard = self.plugboard.return_encrypted_letter(letter)
        encryption_str += "letter after plugboard = " + letter_after_plugboard + "\n"
        letter_before_reflector, cipher_txt = self.rotors.\
            cipher_letter_plugboard_to_reflector(letter_after_plugboard)
        encryption_str += cipher_txt
        encryption_str += "letter before reflector = " + letter_before_reflector + "\n"
        letter_after_reflector = self.__reflector.get_encrypted_letter(letter_before_reflector)
        encryption_str += "letter after reflector = " + letter_after_reflector + "\n"
        letter_before_plugboard, decipher_txt = self.rotors.cipher_letter_reflector_to_plugboard(
            letter_after_reflector)
        encryption_str += decipher_txt
        encryption_str += "letter before plugboard = " + letter_before_plugboard + "\n"
        letter_encrypted = self.plugboard.return_encrypted_letter(letter_before_plugboard)
        encryption_str += "letter encrypted = " + letter_encrypted
        self.rotors.move_rotors_after_cipher()
        return letter_encrypted, encryption_str

    def set_random_settings(self):
        """
        this function sets the enigma to a random settings.
        :return:
        """
        # setting random rotors
        rotors_numbers = random.sample([1, 2, 3, 4, 5], 3)
        rotors_letters = random.sample([chr(i) for i in range(65, 91)], 3)
        self.rotors.set_rotors(rotors_numbers[0], rotors_numbers[1], rotors_numbers[2],
                                 rotors_letters[0], rotors_letters[1], rotors_letters[2])

        # setting random plugboard
        num_pairs = random.randint(0, 10)
        plugboard_letters = random.sample([chr(i) for i in range(65, 91)], num_pairs * 2)
        for i in plugboard_letters:
            self.plugboard.add_letter(i)
