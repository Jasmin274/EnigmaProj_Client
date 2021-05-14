"""
Name: Jasmin Maizel
Final Project subject: Cryptography - Enigma
this is the rotors file - it sets the rotors of the enigma.
Python Version: 3.7.4
Date: 10.02.2021
"""


class Rotors:
    """
    this is the class of the rotors. it sets the rotors'
    setting and encrypts letters through them.
    """
    the_abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    rotor1 = ['E', 'Z', 'A', 'T', 'Q', 'Y', 'S', 'F', 'U', 'R', 'M', 'W', 'C',
              'I', 'N', 'L', 'K', 'B', 'V', 'J', 'H', 'P', 'O', 'X', 'D', 'G']
    rotor2 = ['V', 'Z', 'A', 'N', 'I', 'F', 'J', 'E', 'W', 'Y', 'S', 'O', 'U',
              'M', 'H', 'G', 'K', 'B', 'C', 'R', 'P', 'L', 'Q', 'D', 'T', 'X']
    rotor3 = ['X', 'K', 'N', 'C', 'B', 'W', 'U', 'D', 'I', 'Z', 'R', 'F', 'H',
              'J', 'L', 'A', 'E', 'M', 'Y', 'G', 'V', 'S', 'O', 'T', 'Q', 'P']
    rotor4 = ['Q', 'T', 'F', 'W', 'E', 'Y', 'J', 'R', 'C', 'U', 'D', 'K', 'B',
              'I', 'N', 'P', 'S', 'G', 'M', 'O', 'V', 'L', 'X', 'H', 'A', 'Z']
    rotor5 = ['W', 'L', 'O', 'R', 'S', 'H', 'M', 'D', 'P', 'T', 'C', 'G', 'B',
              'N', 'Z', 'Q', 'I', 'U', 'Y', 'J', 'E', 'K', 'V', 'X', 'A', 'F']
    all_rotors = [rotor1, rotor2, rotor3, rotor4, rotor5]

    def __init__(self, first_rotor_number=1, second_rotor_number=2, third_rotor_number=3,
                 first_rotor_letter='A', second_rotor_letter='A', third_rotor_letter='A'):
        """
        sets initial values for the rotors.
        :param first_rotor_number:
        :param second_rotor_number:
        :param third_rotor_number:
        """
        self.__chosen_rotor1 = self.all_rotors[first_rotor_number - 1][:]
        self.__chosen_rotor2 = self.all_rotors[second_rotor_number - 1][:]
        self.__chosen_rotor3 = self.all_rotors[third_rotor_number - 1][:]
        self.__rotor1_steps = ord(first_rotor_letter) - 65
        self.__rotor2_steps = ord(second_rotor_letter) - 65
        self.__rotor3_steps = ord(third_rotor_letter) - 65
        self.initial_settings = (first_rotor_number, second_rotor_number, third_rotor_number,
                                 first_rotor_letter, second_rotor_letter, third_rotor_letter)

    def cipher_letter_plugboard_to_reflector(self, letter):
        """
        :param letter:
        :return: the letter after passing it through the rotors,
        from the plugboard to the reflector.
        """
        first_cipher, rotor_letter1 = self.cipher_rotor(letter, self.__chosen_rotor1,
                                                        self.__rotor1_steps)
        second_cipher, rotor_letter2 = self.cipher_rotor(first_cipher, self.__chosen_rotor2,
                                                         self.__rotor2_steps)
        third_cipher, rotor_letter3 = self.cipher_rotor(second_cipher, self.__chosen_rotor3,
                                                        self.__rotor3_steps)
        cipher_txt = "First Rotor: " + rotor_letter1 + "Second Rotor: " + \
                     rotor_letter2 + "Third Rotor: " + rotor_letter3
        return third_cipher, cipher_txt

    def cipher_letter_reflector_to_plugboard(self, letter):
        """
        :param letter:
        :return: the letter after passing it through the rotors,
        from the reflector to the plugboard.
        """
        first_cipher, rotor_letter1 = self.decipher_rotor(letter, self.__chosen_rotor3,
                                                          self.__rotor3_steps)
        second_cipher, rotor_letter2 = self.decipher_rotor(first_cipher, self.__chosen_rotor2,
                                                           self.__rotor2_steps)
        third_cipher, rotor_letter3 = self.decipher_rotor(second_cipher, self.__chosen_rotor1,
                                                          self.__rotor1_steps)
        decipher_txt = "Third Rotor: " + rotor_letter1 + "Second Rotor: " + \
                       rotor_letter2 + "First Rotor: " + rotor_letter3
        return third_cipher, decipher_txt

    def cipher_rotor(self, letter_to_encrypt, rotor, steps_num):
        """
        :param letter_to_encrypt:
        :param rotor:
        :param steps_num:
        :return: the letter after encryption in the rotor
        """
        abc_stepped = self.the_abc[steps_num:] + self.the_abc[:steps_num]
        index_in_abc = abc_stepped.index(letter_to_encrypt)
        rotor_enc_str = letter_to_encrypt + " --> " + rotor[index_in_abc] + "\n"
        return rotor[index_in_abc], rotor_enc_str

    def decipher_rotor(self, letter_to_decrypt, rotor, steps_num):
        """
        :param letter_to_decrypt:
        :param rotor:
        :param steps_num:
        :return: the letter after decryption in the rotor
        """
        abc_stepped = self.the_abc[steps_num:] + self.the_abc[:steps_num]
        index_in_rotor = rotor.index(letter_to_decrypt)
        rotor_dec_str = letter_to_decrypt + " --> " + abc_stepped[index_in_rotor] + "\n"
        return abc_stepped[index_in_rotor], rotor_dec_str

    def move_rotors_after_cipher(self):
        """
        moves the first rotor in one step, and the others accordingly.
        takes into consideration the notches.
        """
        if self.all_rotors[0] in [self.__chosen_rotor1, self.__chosen_rotor2, self.__chosen_rotor3]:
            if self.all_rotors[0] == self.__chosen_rotor1 and \
                    self.the_abc[self.__rotor1_steps] == "Q":
                self.move_step_rotor2()
            elif self.all_rotors[0] == self.__chosen_rotor2 and \
                    self.the_abc[self.__rotor2_steps] == "Q":
                self.move_step_rotor3()
            elif self.the_abc[self.__rotor3_steps] == "Q":
                self.move_step_rotor1()

        if self.all_rotors[1] in [self.__chosen_rotor1, self.__chosen_rotor2,
                                  self.__chosen_rotor3]:
            if self.all_rotors[1] == self.__chosen_rotor1 and \
                    self.the_abc[self.__rotor1_steps] == "E":
                self.move_step_rotor2()
            elif self.all_rotors[1] == self.__chosen_rotor2 and \
                    self.the_abc[self.__rotor2_steps] == "E":
                self.move_step_rotor3()
            elif self.the_abc[self.__rotor3_steps] == "E":
                self.move_step_rotor1()

        if self.all_rotors[2] in [self.__chosen_rotor1, self.__chosen_rotor2,
                                  self.__chosen_rotor3]:
            if self.all_rotors[2] == self.__chosen_rotor1 and \
                    self.the_abc[self.__rotor1_steps] == "V":
                self.move_step_rotor2()
            elif self.all_rotors[2] == self.__chosen_rotor2 and \
                    self.the_abc[self.__rotor2_steps] == "V":
                self.move_step_rotor3()
            elif self.the_abc[self.__rotor3_steps] == "V":
                self.move_step_rotor1()

        if self.all_rotors[3] in [self.__chosen_rotor1, self.__chosen_rotor2,
                                  self.__chosen_rotor3]:
            if self.all_rotors[3] == self.__chosen_rotor1 and \
                    self.the_abc[self.__rotor1_steps] == "J":
                self.move_step_rotor2()
            elif self.all_rotors[3] == self.__chosen_rotor2 and \
                    self.the_abc[self.__rotor2_steps] == "J":
                self.move_step_rotor3()
            elif self.the_abc[self.__rotor3_steps] == "J":
                self.move_step_rotor1()

        if self.all_rotors[4] in [self.__chosen_rotor1, self.__chosen_rotor2,
                                  self.__chosen_rotor3]:
            if self.all_rotors[4] == self.__chosen_rotor1 and \
                    self.the_abc[self.__rotor1_steps] == "Z":
                self.move_step_rotor2()
            elif self.all_rotors[4] == self.__chosen_rotor2 and \
                    self.the_abc[self.__rotor2_steps] == "Z":
                self.move_step_rotor3()
            elif self.the_abc[self.__rotor3_steps] == "Z":
                self.move_step_rotor1()

        self.__rotor1_steps += 1
        self.__rotor2_steps += self.__rotor1_steps // 26
        self.__rotor3_steps += self.__rotor2_steps // 26
        self.__rotor1_steps %= 26
        self.__rotor2_steps %= 26
        self.__rotor3_steps %= 26

    def letter_on_rotors(self):
        """
        :return: the letter shown on each rotor
        """
        letter_on_rotor1 = self.the_abc[self.__rotor1_steps]
        letter_on_rotor2 = self.the_abc[self.__rotor2_steps]
        letter_on_rotor3 = self.the_abc[self.__rotor3_steps]
        return letter_on_rotor3, letter_on_rotor2, letter_on_rotor1

    def move_step_rotor1(self):
        """
        moves the first rotor in one step
        """
        self.__rotor1_steps += 1
        self.__rotor1_steps %= 26

    def move_step_rotor2(self):
        """
        moves the second rotor in one step
        """
        self.__rotor2_steps += 1
        self.__rotor2_steps %= 26

    def move_step_rotor3(self):
        """
        moves the third rotor in one step
        """
        self.__rotor3_steps += 1
        self.__rotor3_steps %= 26

    def set_rotors(self, first_rotor_number, second_rotor_number, third_rotor_number,
                   first_rotor_letter, second_rotor_letter, third_rotor_letter):
        """
        sets the rotors
        :param first_rotor_number:
        :param second_rotor_number:
        :param third_rotor_number:
        :param first_rotor_letter:
        :param second_rotor_letter:
        :param third_rotor_letter:
        :return:
        """
        self.__chosen_rotor1 = self.all_rotors[first_rotor_number - 1]
        self.__chosen_rotor2 = self.all_rotors[second_rotor_number - 1]
        self.__chosen_rotor3 = self.all_rotors[third_rotor_number - 1]
        self.__rotor1_steps = ord(first_rotor_letter) - 65
        self.__rotor2_steps = ord(second_rotor_letter) - 65
        self.__rotor3_steps = ord(third_rotor_letter) - 65
        self.initial_settings = (first_rotor_number, second_rotor_number, third_rotor_number,
                                 first_rotor_letter, second_rotor_letter, third_rotor_letter)

    def get_initial_setting(self):
        """
        the function returns the initial settings of the rotors
        :return:
        """
        return self.initial_settings
