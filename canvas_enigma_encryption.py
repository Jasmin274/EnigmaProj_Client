"""
Name: Jasmin Maizel
Final Project subject: Cryptography - Enigma
this is the enigma canvas file - it displays a comfortable encryption of the enigma visually
Python Version: 3.7.4
Date: 10.02.2021
"""

from tkinter import Canvas, font, FIRST, LAST


class ShowEncryption:
    """
    this is the enigma canvas class
    it displays a comfortable encryption of the enigma visually
    """
    def __init__(self, root, encryption_stages_list):
        """
        the init method - uses an existing Tk object, and a stages list
        of the encryption to display the canvas
        :param root:
        :param encryption_stages_list:
        """
        self.root = root
        self.encryption_stages_list = encryption_stages_list
        self.title_font = font.Font(family="Helvetica", size=20,
                                    weight=font.BOLD, slant=font.ITALIC)
        self.text_font = font.Font(family="Helvetica", size=14, weight=font.BOLD)

    def set_canvas(self):
        """
        this function sets the canvas
        :return:
        """
        canvas = Canvas(self.root, height=730, width=1000)
        canvas.grid(row=0, rowspan=15, column=5, columnspan=10, padx=20, pady=15)

        canvas.create_text(900, (ord(self.encryption_stages_list[-1]) - 65) * 25 + 75,
                           text="the encrypted\nletter is " + self.encryption_stages_list[-1],
                           font=self.title_font)

        # sets the abc of the rotors, plugboard and reflector.
        for x_values in [75, 190, 260, 365, 435, 540, 610, 715, 785]:
            for y_values in range(75, 725, 25):
                canvas.create_text(x_values, y_values, text=chr((y_values - 75) // 25 + 65),
                                   font=self.text_font)

        # titles and rectangles for the rotors, plugboard and reflector.
        canvas.create_text(750, 30, text="plugboard", font=self.title_font)
        canvas.create_rectangle(705, 55, 795, 710)
        canvas.create_text(575, 30, text="first rotor", font=self.title_font)
        canvas.create_rectangle(530, 55, 620, 710)
        canvas.create_text(400, 30, text="second rotor", font=self.title_font)
        canvas.create_rectangle(355, 55, 445, 710)
        canvas.create_text(225, 30, text="third rotor", font=self.title_font)
        canvas.create_rectangle(180, 55, 270, 710)
        canvas.create_text(75, 30, text="reflector", font=self.title_font)
        canvas.create_rectangle(55, 55, 95, 710)

        # lines inside rotors and plugboard

        # lines inside the plugboard
        # when the plugboard is before the first rotor
        canvas.create_rectangle(775, (ord(self.encryption_stages_list[1]) - 65) * 25 + 65, 795,
                                (ord(self.encryption_stages_list[1]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_rectangle(705, (ord(self.encryption_stages_list[2]) - 65) * 25 + 65, 725,
                                (ord(self.encryption_stages_list[2]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_line(775, (ord(self.encryption_stages_list[1]) - 65) * 25 + 75, 725,
                           (ord(self.encryption_stages_list[2]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))

        # when the plugboard is after the first rotor
        canvas.create_rectangle(775, (ord(self.encryption_stages_list[12]) - 65) * 25 + 65, 795,
                                (ord(self.encryption_stages_list[12]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_rectangle(705, (ord(self.encryption_stages_list[11]) - 65) * 25 + 65, 725,
                                (ord(self.encryption_stages_list[11]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_line(775, (ord(self.encryption_stages_list[12]) - 65) * 25 + 75, 725,
                           (ord(self.encryption_stages_list[11]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=FIRST, arrowshape=(16, 20, 6))

        # lines inside the first rotor
        # when the first rotor is after the plugboard
        canvas.create_rectangle(530, (ord(self.encryption_stages_list[3]) - 65) * 25 + 65, 550,
                                (ord(self.encryption_stages_list[3]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_rectangle(600, (ord(self.encryption_stages_list[2]) - 65) * 25 + 65, 620,
                                (ord(self.encryption_stages_list[2]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_line(600, (ord(self.encryption_stages_list[2]) - 65) * 25 + 75, 550,
                           (ord(self.encryption_stages_list[3]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))

        # when the first rotor is before the plugboard
        canvas.create_rectangle(530, (ord(self.encryption_stages_list[9]) - 65) * 25 + 65, 550,
                                (ord(self.encryption_stages_list[9]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_rectangle(600, (ord(self.encryption_stages_list[10]) - 65) * 25 + 65, 620,
                                (ord(self.encryption_stages_list[10]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_line(600, (ord(self.encryption_stages_list[10]) - 65) * 25 + 75, 550,
                           (ord(self.encryption_stages_list[9]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=FIRST, arrowshape=(16, 20, 6))

        # lines inside the second rotor
        # when second is after the first rotor
        canvas.create_rectangle(355, (ord(self.encryption_stages_list[4]) - 65) * 25 + 65, 375,
                                (ord(self.encryption_stages_list[4]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_rectangle(425, (ord(self.encryption_stages_list[3]) - 65) * 25 + 65, 445,
                                (ord(self.encryption_stages_list[3]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_line(425, (ord(self.encryption_stages_list[3]) - 65) * 25 + 75, 375,
                           (ord(self.encryption_stages_list[4]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))
        # when second is after the third rotor
        canvas.create_rectangle(355, (ord(self.encryption_stages_list[8]) - 65) * 25 + 65, 375,
                                (ord(self.encryption_stages_list[8]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_rectangle(425, (ord(self.encryption_stages_list[9]) - 65) * 25 + 65, 445,
                                (ord(self.encryption_stages_list[9]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_line(425, (ord(self.encryption_stages_list[9]) - 65) * 25 + 75, 375,
                           (ord(self.encryption_stages_list[8]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=FIRST, arrowshape=(16, 20, 6))

        # lines inside the third rotor
        # when third rotor is after the reflector
        canvas.create_rectangle(180, (ord(self.encryption_stages_list[7]) - 65) * 25 + 65, 200,
                                (ord(self.encryption_stages_list[7]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_rectangle(250, (ord(self.encryption_stages_list[8]) - 65) * 25 + 65, 270,
                                (ord(self.encryption_stages_list[8]) - 65) * 25 + 85,
                                outline="green", width=2)
        canvas.create_line(250, (ord(self.encryption_stages_list[8]) - 65) * 25 + 75, 200,
                           (ord(self.encryption_stages_list[7]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=FIRST, arrowshape=(16, 20, 6))
        # when third rotor is after second rotor
        canvas.create_rectangle(180, (ord(self.encryption_stages_list[5]) - 65) * 25 + 65, 200,
                                (ord(self.encryption_stages_list[5]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_rectangle(250, (ord(self.encryption_stages_list[4]) - 65) * 25 + 65, 270,
                                (ord(self.encryption_stages_list[4]) - 65) * 25 + 85,
                                outline="red", width=2)
        canvas.create_line(250, (ord(self.encryption_stages_list[4]) - 65) * 25 + 75, 200,
                           (ord(self.encryption_stages_list[5]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))

        # the line in the reflector
        canvas.create_rectangle(65, (ord(self.encryption_stages_list[6]) - 65) * 25 + 65, 85,
                                (ord(self.encryption_stages_list[6]) - 65) * 25 + 85,
                                outline="blue", width=2)
        canvas.create_rectangle(65, (ord(self.encryption_stages_list[7]) - 65) * 25 + 65, 85,
                                (ord(self.encryption_stages_list[7]) - 65) * 25 + 85,
                                outline="blue", width=2)
        canvas.create_line([(65, (ord(self.encryption_stages_list[6]) - 65) * 25 + 75),
                            (40, (ord(self.encryption_stages_list[6]) - 65) * 25 + 75),
                            (40, (ord(self.encryption_stages_list[7]) - 65) * 25 + 75),
                            (65, (ord(self.encryption_stages_list[7]) - 65) * 25 + 75)],
                           fill="blue", width=2, arrow=LAST)

        # lines between the first rotor and the plugboard
        # from the first rotor
        canvas.create_line(620, (ord(self.encryption_stages_list[10]) - 65) * 25 + 75, 705,
                           (ord(self.encryption_stages_list[11]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=LAST, arrowshape=(16, 20, 6))
        # from the plugboard
        canvas.create_line(705, (ord(self.encryption_stages_list[2]) - 65) * 25 + 75, 620,
                           (ord(self.encryption_stages_list[2]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))

        # lines between first and second rotors
        # from the first rotor
        canvas.create_line(530, (ord(self.encryption_stages_list[3]) - 65) * 25 + 75, 445,
                           (ord(self.encryption_stages_list[3]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))
        # from the second rotor
        canvas.create_line(445, (ord(self.encryption_stages_list[9]) - 65) * 25 + 75, 530,
                           (ord(self.encryption_stages_list[9]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=LAST, arrowshape=(16, 20, 6))

        # lines between the second rotor and the third rotor
        # from the second rotor
        canvas.create_line(355, (ord(self.encryption_stages_list[4]) - 65) * 25 + 75, 270,
                           (ord(self.encryption_stages_list[4]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))
        # from the third rotor
        canvas.create_line(270, (ord(self.encryption_stages_list[8]) - 65) * 25 + 75, 355,
                           (ord(self.encryption_stages_list[8]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=LAST, arrowshape=(16, 20, 6))

        # lines between the reflector and the third rotor
        # from the reflector
        canvas.create_line(85, (ord(self.encryption_stages_list[7]) - 65) * 25 + 75, 180,
                           (ord(self.encryption_stages_list[7]) - 65) * 25 + 75,
                           fill="green", width=2, arrow=LAST, arrowshape=(16, 20, 6))
        # from the third rotor
        canvas.create_line(180, (ord(self.encryption_stages_list[5]) - 65) * 25 + 75, 85,
                           (ord(self.encryption_stages_list[6]) - 65) * 25 + 75,
                           fill="red", width=2, arrow=LAST, arrowshape=(16, 20, 6))
