"""
Name: Jasmin Maizel
Final Project subject: Cryptography - Enigma
this is the Morse file - it encrypts text with morse combined with ASCII code
Python Version: 3.7.4
Date: 10.02.2021
"""


class Morse:
    """
    this class will encrypt and decrypt texts using code morse.
    """

    def __init__(self):
        """
        sets the morse dictionary
        """
        self.__dict = {"0": "-----", "1": ".----", "2": "..---",
                       "3": "...--", "4": "....-", "5": ".....",
                       "6": "-....", "7": "--...", "8": "---..", "9": "----."}

    def encrypt(self, plain_text):
        """
        encrypts plain text
        :param plain_text:
        :return: the encrypted text. the text is encrypted with morse combined with ASCII
        """
        message = ""
        plain_text = plain_text.replace(" ", "").upper()
        for i in plain_text:
            message += self.__dict[str(ord(i) // 10)] + self.__dict[str(ord(i) % 10)] + "/"

        return message[:-1]

    def decrypt(self, encrypted_text):
        """
        decrypts text
        :param encrypted_text:
        :return: the decrypted text
        """
        decrypted = ""
        lst_values = list(self.__dict.values())
        decrypt_to_numbers = ""

        skips = 0
        while skips < len(encrypted_text):
            if encrypted_text[skips] == "/":
                skips += 1
            decrypt_to_numbers += str(lst_values.index(encrypted_text[skips:skips + 5]))
            skips += 5

        for i in range(0, len(decrypt_to_numbers), 2):
            decrypted += chr(int(decrypt_to_numbers[i:i + 2])).upper()

        return decrypted
