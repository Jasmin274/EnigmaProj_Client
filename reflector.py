"""
Name: Jasmin Maizel
Final Project subject: Cryptography - Enigma
this is the reflector file - it sets the reflector of the enigma.
Python Version: 3.7.4
Date: 10.02.2021
"""


class Reflector:
    """
    this class is the class of the reflector.
    it will navigate the letter between rotors encryption.
    like that:

    rotor1 encryption -> rotor2 encryption -> rotor3 encryption -> reflector ->
    -> rotor3 decryption -> rotor2 decryption -> rotor1 decryption
    """

    def __init__(self):
        """
        sets the reflector.
        """
        self.__first_list = ['E', 'I', 'F', 'D', 'L', 'K', 'J', 'G', 'C', 'M', 'H', 'A', 'B']
        self.__second_list = ['W', 'Z', 'S', 'V', 'O', 'N', 'U', 'P', 'Y', 'T', 'R', 'Q', 'X']

    def get_encrypted_letter(self, letter):
        """
        this function returns
        :param letter:
        :return:
        """
        if letter in self.__first_list:
            position = self.__first_list.index(letter)
            return self.__second_list[position]
        position = self.__second_list.index(letter)
        return self.__first_list[position]
