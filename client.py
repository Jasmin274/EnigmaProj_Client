"""
Name: Jasmin Maizel
Final Project subject: Cryptography - Enigma
this is the client class file - it connects to the server and handles all the GUI.
Python Version: 3.7.4
Date: 10.02.2021
"""


import socket
import sys
from datetime import datetime
from pickle import dumps, loads
from threading import Thread
from tkinter import Tk, Label, Button, Frame, Entry, END, Scrollbar, Text, OptionMenu, \
    BOTTOM, LEFT, RIGHT, DISABLED, NORMAL, Y, RIDGE, StringVar, font

import speech_recognition

from morse import Morse
from rsa_class import RSA_encryption
from canvas_enigma_encryption import ShowEncryption
from enigma import Enigma


class Client:
    """
    this class represents the client: its gui and socket.
    """

    def __init__(self, host_ip="127.0.0.1", dst_port=2000):
        """
        creates the Tk object, the socket and starts running the entire code.
        """
        self.my_socket = socket.socket()

        try:
            self.my_socket.connect((host_ip, dst_port))
            print("Connected to server successfully")
        except socket.error:
            print("no server is waiting...")
            sys.exit()

        # creating RSA object and exchanging keys with server
        self.rsa_object = RSA_encryption()
        self.server_key = self.my_socket.recv(8000)
        self.my_socket.send(self.rsa_object.get_public_key())

        # variables connected to enigma
        self.simulator_enigma = Enigma()
        self.simulator_encryption = []
        self.simulator_encryption_text = ""

        self.log_in_tries = 0
        self.sign_in_tries = 0
        self.username = ""

        # variable the will contain all the messages and a message receiver thread
        self.receive_thread = Thread(target=self.receive, daemon=True)
        self.msg_list = []

        # these variables are used in more than one function, and not always exist.
        # therefore we need to make them None when they are not in use.
        self.messages_window = None
        self.refresh_button = None

        # speech thread variable that will determine whether or not the thread can be started
        self.thread_speech_is_running = False

        # the GUI object and its properties
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.close_root)
        self.root.resizable(False, False)
        self.root.title("my enigma project")
        self.bg_color = "khaki1"
        self.root.configure(background=self.bg_color)

        # fonts for the GUI
        self.title_font = font.Font(family="Helvetica", size=20, weight=font.BOLD,
                                    slant=font.ITALIC)
        self.text_font = font.Font(family="Helvetica", size=14, weight=font.BOLD)

        # starting the object
        self.log_in()
        self.root.mainloop()

    def close_root(self):
        """
        this is the closing protocol. this function closes all Tk
        objects that might exist in order to close the program entirely.
        :return:
        """
        if self.messages_window is not None:
            self.messages_window.destroy()
        self.root.destroy()

    def after_3_wrong_attempts(self, str_from_where):
        """
        after 3 wrong attempts, this function will block the user
        from signing/logging in for 60 seconds.
        :param str_from_where:
        :return:
        """
        self.clear_screen()

        def timer_tick(seconds):
            """
            this is an inner-function that is responsible for the
            timer after3 failed attempts at logging/signing in.
            :param seconds:
            :return:
            """
            if seconds > 0:
                timer_label['text'] = "You had 3 wrong attempts.\nTry again in " + \
                                      str(seconds) + " seconds."
                self.root.after(1000, lambda: timer_tick(seconds - 1))
            else:
                if str_from_where == "log in":
                    self.log_in()
                else:
                    self.sign_in()

        timer_label = Label(self.root, font=self.title_font, bg=self.bg_color)
        timer_label.pack(padx=50, pady=150)
        timer_tick(60)

    def log_in(self):
        """
        this function shows the log in window
        :return:
        """
        self.clear_screen()
        lbl_log_in = Label(self.root, text="Welcome. Please log in to the system.",
                           font=self.title_font,
                           bg=self.bg_color)
        lbl_log_in.pack(pady=5, padx=10)

        user_name = Label(self.root, text="enter user name", font=self.text_font, bg=self.bg_color)
        user_name.pack(pady=5, padx=10)
        user_name_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25)
        user_name_entry.pack(pady=5, padx=10)

        password = Label(self.root, text="enter password", font=self.text_font, bg=self.bg_color)
        password.pack(pady=5, padx=10)
        password_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25, show="*")
        password_entry.pack(pady=5, padx=10)

        passcode = Label(self.root, text="enter passcode", font=self.text_font, bg=self.bg_color)
        passcode.pack(pady=5, padx=10)
        passcode_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25, show="*")
        passcode_entry.pack(pady=5, padx=10)

        button_enter_log = Button(self.root, text="log in", command=lambda: self.submit_log_in(
            user_name_entry, password_entry, passcode_entry))
        button_enter_log.pack(pady=10)

        button_sign_in = Button(self.root, text="Don't have a user? Sign in", command=self.sign_in)
        button_sign_in.pack(pady=10)

    def submit_log_in(self, user_name, password, passcode):
        """
        this function sends to the server the data and returns
        whether the client logged in successfully or not.
        :param user_name:
        :param password:
        :param passcode:
        :return:
        """
        username_txt = user_name.get()
        password_txt = password.get()
        passcode_txt = passcode.get()
        self.my_socket.send(dumps("log in"))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S").split(":")
        time = current_time[0] + current_time[1]
        str_log_in = username_txt + ";" + password_txt + ";" + passcode_txt + ";" + time
        self.my_socket.send(self.rsa_object.encrypt(str_log_in.encode(), self.server_key))

        response = self.rsa_object.decrypt(self.my_socket.recv(1024)).decode()
        if response == "access granted":
            self.username = username_txt
            self.choose_path()
        else:
            if self.log_in_tries == 2:
                self.log_in_tries = 0
                self.after_3_wrong_attempts("log in")
            else:
                self.log_in_tries += 1
                lbl_response = Label(self.root, text=response, font=self.title_font,
                                     bg=self.bg_color)
                lbl_response.pack(pady=5, padx=10)
                lbl_response.after(1000, lbl_response.destroy)
                user_name.delete(0, END)
                password.delete(0, END)
                passcode.delete(0, END)

    def sign_in(self):
        """
        this function shows the sign in window
        :return:
        """
        self.clear_screen()
        lbl_sign_in = Label(self.root, text="Welcome. Please sign in to the system.",
                            font=self.title_font, bg=self.bg_color)
        lbl_sign_in.pack(pady=5, padx=10)

        user_name = Label(self.root, text="enter user name", font=self.text_font, bg=self.bg_color)
        user_name.pack(pady=5, padx=10)
        user_name_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25)
        user_name_entry.pack(pady=5, padx=10)

        id_label = Label(self.root, text="enter id", font=self.text_font, bg=self.bg_color)
        id_label.pack(pady=5, padx=10)
        id_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25)
        id_entry.pack(pady=5, padx=10)

        password1 = Label(self.root, text="create password", font=self.text_font, bg=self.bg_color)
        password1.pack(pady=5, padx=10)
        password_explanation = Label(self.root, text="please note that the password must "
                                                     "contain at\nleast 8 characters, and at least "
                                                     "one of each:\ncapital and a small "
                                                     "letter, a symbol and a digit", font="none 11",
                                     bg=self.bg_color, fg="navy")
        password_explanation.pack(pady=5, padx=10)
        password1_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25, show="*")
        password1_entry.pack(pady=5, padx=10)

        password2 = Label(self.root, text="repeat password", font=self.text_font, bg=self.bg_color)
        password2.pack(pady=5, padx=10)
        password2_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25, show="*")
        password2_entry.pack(pady=5, padx=10)

        passcode = Label(self.root, text="enter passcode", font=self.text_font, bg=self.bg_color)
        passcode.pack(pady=5, padx=10)
        passcode_entry = Entry(self.root, font='Helvetica 14', fg='blue', width=25, show="*")
        passcode_entry.pack(pady=5, padx=10)

        button_enter = Button(self.root, text="sign in",
                              command=lambda: self.submit_sign_in(user_name_entry,
                                                                  id_entry, password1_entry,
                                                                  password2_entry,
                                                                  passcode_entry))
        button_enter.pack(pady=5, padx=10)
        button_enter = Button(self.root, text="go to log in", command=self.log_in)
        button_enter.pack(pady=5, padx=10)

    def submit_sign_in(self, user_name, id_widget, password1, password2, passcode):
        """
        this function sends to the server the data and returns
        whether the user was created successfully or not.
        :param user_name:
        :param id_widget:
        :param password1:
        :param password2:
        :param passcode:
        :return:
        """
        username_txt = user_name.get()
        id_txt = id_widget.get()
        password1_txt = password1.get()
        password2_txt = password2.get()
        passcode_txt = passcode.get()

        self.my_socket.send(dumps("sign in"))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S").split(":")
        time = current_time[0] + current_time[1]
        sign_in_str = username_txt + ";" + id_txt + ";" + password1_txt + ";" + \
                      password2_txt + ";" + passcode_txt + ";" + time
        self.my_socket.send(self.rsa_object.encrypt(sign_in_str.encode(), self.server_key))

        response = self.rsa_object.decrypt(self.my_socket.recv(1024)).decode()
        if self.sign_in_tries == 2:
            self.sign_in_tries = 0
            self.after_3_wrong_attempts("sign in")
        else:
            if response != "user successfully signed in. to complete the process, log in.":
                self.sign_in_tries += 1
            lbl_response = Label(self.root, text=response, font=self.title_font,
                                 bg=self.bg_color)
            lbl_response.pack(pady=5, padx=10)
            lbl_response.after(1000, lbl_response.destroy)
            user_name.delete(0, END)
            id_widget.delete(0, END)
            password1.delete(0, END)
            password2.delete(0, END)
            passcode.delete(0, END)

    def choose_path(self):
        """
        this function shows the paths window. the client may choose what to do.
        :return:
        """
        if not self.receive_thread.is_alive():
            self.receive_thread.start()
        self.clear_screen()
        self.refresh_button = None
        user_label = Label(self.root, text="Hello " + self.username, font=self.title_font,
                           bg=self.bg_color, height=2)
        user_label.pack(pady=10, padx=50)
        button_read_msg = Button(self.root, text="read messages", font=self.text_font,
                                 height=2, width=20, command=lambda: self.read_messages(1))
        button_read_msg.pack(pady=20, padx=50)

        button_send_msg = Button(self.root, text="send message", font=self.text_font,
                                 height=2, width=20, command=self.send_messages)
        button_send_msg.pack(pady=20, padx=50)

        button_simulator = Button(self.root, text="simulator", font=self.text_font,
                                  height=2, width=20, command=self.simulator)
        button_simulator.pack(pady=20, padx=50)

        button_read = Button(self.root, text="About", font=self.text_font,
                             height=2, width=20, command=self.about_screen)
        button_read.pack(pady=20, padx=50)

    def read_messages(self, msg_num):
        """
        this function shows the read window.
        it allows the client to read all the messages. both received and sent.
        :param msg_num:
        :return:
        """
        self.clear_screen()
        user_label = Label(self.root, text="Hello " + self.username, font=self.title_font,
                           bg=self.bg_color, height=2)
        user_label.pack(pady=5, padx=50)
        lbl_msg = Label(self.root, text="Message " + str(msg_num), font=self.title_font,
                        bg=self.bg_color)
        lbl_msg.pack(pady=5, padx=10)
        self.refresh_button = Button(self.root, text="Refresh page", font=self.text_font,
                                     bg=self.bg_color, command=lambda: self.refresh(msg_num))
        self.refresh_button.pack(padx=10, pady=10)
        messages_frame = Frame(self.root)
        messages_frame.pack(padx=30, pady=15)
        scrollbar_msg = Scrollbar(messages_frame)
        scrollbar_msg.pack(side=RIGHT, fill=Y)
        text_widget = Text(messages_frame, width=50, height=15, font=self.text_font,
                           yscrollcommand=scrollbar_msg.set)
        text_widget.pack()
        scrollbar_msg.config(command=text_widget.yview)
        button_send = Button(self.root, text="go back", font=self.text_font,
                             height=2, width=20, command=self.go_back_read)
        button_send.pack(pady=5, side=BOTTOM)
        button_send = Button(self.root, text="see/close message\ncontrol panel",
                             font=self.text_font,
                             height=2, width=20,
                             command=lambda: self.new_window_messages(button_send))
        button_send.pack(pady=5, side=BOTTOM)
        if self.msg_list:
            if msg_num < len(self.msg_list):
                next_msg = Button(self.root, text="next message", font=self.text_font,
                                  height=2, width=20,
                                  command=lambda: self.read_messages(msg_num + 1))
                next_msg.pack(pady=5, padx=5, side=RIGHT)
            if msg_num > 1:
                previous_msg = Button(self.root, text="previous message", font=self.text_font,
                                      height=2, width=20,
                                      command=lambda: self.read_messages(msg_num - 1))
                previous_msg.pack(pady=5, padx=5, side=LEFT)
            text_widget.insert(END, "from: " + self.msg_list[msg_num - 1][2] + "\n")
            text_widget.tag_add('sender', '1.0', '1.end')
            text_widget.tag_config('sender', font='none 14')

            text_widget.insert(END, self.msg_list[msg_num - 1][0])
            text_widget.tag_add('msg', '2.0', END)
            text_widget.tag_config('msg', font='none 12')

        text_widget.config(state=DISABLED)

    def refresh(self, msg_num):
        """
        this function refreshes the read messages page.
        :param msg_num:
        :return:
        """
        if self.messages_window is not None:
            self.messages_window.destroy()
            self.messages_window = None
        self.read_messages(msg_num)

    def go_back_read(self):
        """
        this function makes sure that when going back
        from the read  window, all windows work properly.
        :return:
        """
        if self.messages_window is not None:
            self.messages_window.destroy()
            self.messages_window = None
        self.choose_path()

    def new_window_messages(self, button_see_all_msgs):
        """
        opens a new window that contains all the messages.
        :param button_see_all_msgs:
        :return:
        """
        # changing the button command to closing the window
        button_see_all_msgs.config(command=lambda: self.close_window(button_see_all_msgs))

        # creating the chat Tk object
        self.messages_window = Tk()
        self.messages_window.resizable(False, False)
        self.messages_window.config(bg=self.bg_color)
        self.messages_window.protocol("WM_DELETE_WINDOW",
                                      lambda: self.close_window(button_see_all_msgs))

        chat_label = Label(self.messages_window, text="Hello " + self.username +
                                                      "\nHere are your messages",
                           bg=self.bg_color, font=self.title_font)
        chat_label.pack(padx=20, pady=10)
        chat_frame = Frame(self.messages_window)
        chat_frame.pack(padx=15, pady=15)
        scrollbar_chat = Scrollbar(chat_frame)
        scrollbar_chat.pack(side=RIGHT, fill=Y)
        text_chat = Text(chat_frame, width=30, height=15, font=self.text_font,
                         yscrollcommand=scrollbar_chat.set)
        text_chat.pack()
        scrollbar_chat.config(command=text_chat.yview)
        for msg, encryption_data, sender_user in self.msg_list:
            text_chat.insert(END, "from: " + sender_user + "\n")
            text_chat.insert(END, msg + "\n\n")
        text_chat.config(state=DISABLED)

    def close_window(self, button_msgs):
        """
        closing the second Tk object
        :param button_msgs:
        :return:
        """
        if self.messages_window is not None:
            self.messages_window.destroy()
            self.messages_window = None
            button_msgs.config(command=lambda: self.new_window_messages(button_msgs))

    def send_messages(self):
        """
        this function is the send window.
        it allows the client to send a message.
        :return:
        """
        self.clear_screen()
        user_label = Label(self.root, text="Hello " + self.username,
                           font=self.title_font, bg=self.bg_color, height=2)
        user_label.pack(pady=10, padx=50)
        messages_frame = Frame(self.root)
        messages_frame.pack(padx=30, pady=10)
        scrollbar_msg = Scrollbar(messages_frame)
        scrollbar_msg.pack(side=RIGHT, fill=Y)
        write_message = Text(messages_frame, width=50, height=15, font=self.text_font,
                             yscrollcommand=scrollbar_msg.set)
        write_message.pack()
        scrollbar_msg.config(command=write_message.yview)
        button_speech_rec = Button(self.root, text="listen\nto speech", font=self.text_font,
                                   height=2, width=20,
                                   command=lambda: self.create_speech_thread(write_message))
        button_speech_rec.pack(pady=10)
        button_send = Button(self.root, text="send", font=self.text_font,
                             height=2, width=20, command=lambda: self.send(write_message))
        button_send.pack(pady=10)
        button_send = Button(self.root, text="go back", font=self.text_font,
                             height=2, width=20, command=self.choose_path)
        button_send.pack(pady=10)

    def create_speech_thread(self, text_widget):
        """
        this function creates a thread that will listen to users input in microphone
        :param text_widget:
        :return:
        """
        if not self.thread_speech_is_running:
            thread_speech = Thread(target=self.speech_recognizer_function,
                                   args=(text_widget,), daemon=True)
            thread_speech.start()
            self.thread_speech_is_running = True

    def speech_recognizer_function(self, text_widget):
        """
        this function recognizes the input of the microphone and turns it into text.
        the text is inserted to the text widget and then the user
        will be able to send it as a message
        :param text_widget:
        :return:
        """
        label_listening = Label(self.root, text="listening to input...",
                                font=self.text_font, bg=self.bg_color)
        label_listening.pack(pady=10)
        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            text += " "
        except:
            text = ""
        text_widget.insert(END, text)
        label_listening.destroy()
        self.thread_speech_is_running = False

    def color_letter(self, letter, lst_labels, plain_text_widget, encrypted_text_widget):
        """
        this function colors the encrypted letter label in the simulator for 300 milliseconds
        :param letter:
        :param lst_labels:
        :param plain_text_widget:
        :param encrypted_text_widget:
        :return:
        """
        new_letter, txt_encryption = self.simulator_enigma.encrypt_letter(letter)
        lst_encryption_letter_stages = [i[-1] for i in txt_encryption.split("\n")]
        lst_encryption_letter_stages.remove(')')
        self.simulator_encryption.append((txt_encryption, lst_encryption_letter_stages))
        lst_labels[ord(new_letter) - 65].config(bg="yellow")
        lst_labels[ord(new_letter) - 65].after(300, lambda: lst_labels[ord(new_letter) -
                                                                       65].config(bg="khaki"))

        plain_text_widget.config(state=NORMAL)
        plain_text_widget.insert(END, letter)
        plain_text_widget.config(state=DISABLED)
        encrypted_text_widget.config(state=NORMAL)
        encrypted_text_widget.insert(END, new_letter)
        encrypted_text_widget.config(state=DISABLED)

    def simulator(self, rotors_settings=(1, 2, 3, 'A', 'A', 'A'),
                  plugboard_settings=None, plain_text=""):
        """
        displays the enigma simulator
        :return:
        """
        self.clear_screen()
        user_label = Label(self.root, text="Hello " + self.username,
                           font=self.title_font, bg=self.bg_color, height=2)
        user_label.grid(pady=10, padx=50, row=0, column=11, columnspan=5)
        if plain_text == "":
            self.simulator_encryption = []
        if plugboard_settings is None:
            self.simulator_enigma.plugboard.reset_plugboard()

        self.simulator_enigma.rotors.set_rotors(rotors_settings[0], rotors_settings[1],
                                                rotors_settings[2], rotors_settings[3],
                                                rotors_settings[4], rotors_settings[5])
        simulator_title = Label(self.root, text="Enigma Simulator",
                                font=self.title_font, bg=self.bg_color)
        simulator_title.grid(row=0, column=2, columnspan=8, rowspan=2, pady=15, padx=5)
        lst_labels = []
        plain_text_frame = Frame(self.root, width=300, height=200)
        plain_text_frame.grid(row=2, column=11, columnspan=5, rowspan=3, padx=10)
        plain_text_label = Label(plain_text_frame, text="Plain Text",
                                 width=12, font=self.title_font)
        plain_text_label.pack(padx=5, pady=3)
        text_widget_frame1 = Frame(plain_text_frame)
        text_widget_frame1.pack()
        scrollbar1 = Scrollbar(text_widget_frame1)
        scrollbar1.pack(side=RIGHT, fill=Y)
        plain_text_text = Text(text_widget_frame1, width=30, height=8, font=self.text_font,
                               yscrollcommand=scrollbar1.set)
        plain_text_text.pack(padx=5, pady=3)
        scrollbar1.config(command=plain_text_text.yview)
        plain_text_text.insert(END, plain_text)
        plain_text_text.config(state=DISABLED)

        encrypted_text_frame = Frame(self.root, width=300, height=200)
        encrypted_text_frame.grid(row=6, column=11, columnspan=5, rowspan=3, padx=10)
        encrypted_text_label = Label(encrypted_text_frame, text="Encrypted Text",
                                     width=12, font=self.title_font)
        encrypted_text_label.pack(padx=5, pady=3)
        text_widget_frame2 = Frame(encrypted_text_frame)
        text_widget_frame2.pack()
        scrollbar2 = Scrollbar(text_widget_frame2)
        scrollbar2.pack(side=RIGHT, fill=Y)
        encrypted_text_text = Text(text_widget_frame2, width=30, height=8, font=self.text_font,
                                   yscrollcommand=scrollbar2.set)
        encrypted_text_text.pack(padx=5, pady=3)
        scrollbar2.config(command=encrypted_text_text.yview)
        encrypted_text_text.insert(END, self.simulator_enigma.decrypt_encrypt_text(plain_text))
        encrypted_text_text.config(state=DISABLED)

        for i in range(65, 75):
            letter_label = Label(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                 bg="khaki", relief=RIDGE, height=2, width=3)
            letter_label.grid(row=2, column=i - 64, pady=5, padx=5)
            lst_labels.append(letter_label)

        for i in range(75, 85):
            letter_label = Label(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                 bg="khaki", relief=RIDGE, height=2, width=3)
            letter_label.grid(row=3, column=i - 74, pady=5, padx=5)
            lst_labels.append(letter_label)

        for i in range(85, 91):
            letter_label = Label(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                 bg="khaki", relief=RIDGE, height=2, width=3)
            letter_label.grid(row=4, column=i - 82, pady=5, padx=5)
            lst_labels.append(letter_label)
        label_line = Label(self.root, text=" ", font=self.text_font, bg=self.bg_color)
        label_line.grid(row=5, column=0)
        for i in range(65, 75):
            letter_button = Button(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                   height=2, width=3, bg="sienna2",
                                   command=lambda letter_ord=i:
                                   self.color_letter(chr(letter_ord),
                                                     lst_labels,
                                                     plain_text_text,
                                                     encrypted_text_text))
            letter_button.grid(row=6, column=i - 64, pady=5, padx=5)

        for i in range(75, 85):
            letter_button = Button(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                   height=2, width=3, bg="sienna2",
                                   command=lambda letter_ord=i:
                                   self.color_letter(chr(letter_ord),
                                                     lst_labels,
                                                     plain_text_text,
                                                     encrypted_text_text))
            letter_button.grid(row=7, column=i - 74, pady=5, padx=5)

        for i in range(85, 91):
            letter_button = Button(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                   height=2, width=3, bg="sienna2",
                                   command=lambda letter_ord=i:
                                   self.color_letter(chr(letter_ord),
                                                     lst_labels,
                                                     plain_text_text,
                                                     encrypted_text_text))
            letter_button.grid(row=8, column=i - 82, pady=5, padx=5)

        button_go_back = Button(self.root, text="go back to\nchoose path", font=self.text_font,
                                height=2, width=15, command=self.choose_path)
        button_go_back.grid(row=10, column=1, columnspan=4, rowspan=2, pady=20, padx=5)

        button_change_settings = Button(self.root, text="change settings", font=self.text_font,
                                        height=2, width=15, command=self.change_settings)
        button_change_settings.grid(row=10, column=5, columnspan=4, rowspan=2, pady=20, padx=5)

        button_explain = Button(self.root, text="See Encryption", font=self.text_font,
                                height=2, width=15,
                                command=lambda: self.show_simulator_encryption(rotors_settings,
                                                                               plugboard_settings,
                                                                               plain_text_text.get(
                                                                                   "1.0", END).
                                                                               replace("\n", "")))
        button_explain.grid(row=10, column=9, columnspan=4, rowspan=2, pady=20, padx=5)
        plugboard_settings_to_send = [self.simulator_enigma.plugboard.plugboard1,
                                      self.simulator_enigma.plugboard.plugboard2]
        button_change_settings = Button(self.root, text="send encrypted\nmessage",
                                        height=2, width=15, font=self.text_font,
                                        command=lambda: self.send(plain_text_text, rotors_settings,
                                                                  plugboard_settings_to_send))
        button_change_settings.grid(row=10, column=13, columnspan=4, rowspan=2, pady=20, padx=5)

    def change_settings(self):
        """
        this function lets the user change the settings of the simulator
        :return:
        """
        self.clear_screen()
        # making sure the screen grid will be organized
        label_line = Label(self.root, text="    ", font=self.text_font, bg=self.bg_color)
        label_line.grid(row=0, column=0)
        label_line = Label(self.root, text="    ", font=self.text_font, bg=self.bg_color)
        label_line.grid(row=0, column=10)

        user_label = Label(self.root, text="Hello " + self.username,
                           font=self.title_font, bg=self.bg_color, height=2)
        user_label.grid(pady=10, padx=50, row=0, column=6, columnspan=4)
        settings_title = Label(self.root, text="Enigma Settings",
                               font=self.title_font, bg=self.bg_color)
        settings_title.grid(row=0, column=2, columnspan=4, pady=15)
        rotor1_num, rotor2_num, rotor3_num, rotor1_letter, rotor2_letter, rotor3_letter = \
            self.simulator_enigma.rotors.get_initial_setting()
        lst_roman_rotor_num = ["I", "II", "III", "IV", "V"]

        rotors_number = Label(self.root, text="the rotors in the enigma",
                              font=self.title_font, bg=self.bg_color)
        rotors_number.grid(row=1, column=3, columnspan=5, pady=5)

        numbers_lst = ["I", "II", "III", "IV", "V"]
        first_rotor_label_num = Label(self.root, text="First Rotor",
                                      font=self.text_font, bg=self.bg_color)
        first_rotor_label_num.grid(row=2, column=1, columnspan=3)
        options_rotor1 = StringVar()
        options_rotor1.set(lst_roman_rotor_num[int(rotor1_num) - 1])
        rotor_num1_options = OptionMenu(self.root, options_rotor1, *numbers_lst)
        rotor_num1_options.grid(row=3, column=1, columnspan=3, padx=15)

        second_rotor_label_num = Label(self.root, text="Second Rotor",
                                       font=self.text_font, bg=self.bg_color)
        second_rotor_label_num.grid(row=2, column=4, columnspan=3)
        options_rotor2 = StringVar()
        options_rotor2.set(lst_roman_rotor_num[int(rotor2_num) - 1])
        rotor_num2_options = OptionMenu(self.root, options_rotor2, *numbers_lst)
        rotor_num2_options.grid(row=3, column=4, columnspan=3, padx=15)

        third_rotor_label_num = Label(self.root, text="Third Rotor",
                                      font=self.text_font, bg=self.bg_color)
        third_rotor_label_num.grid(row=2, column=7, columnspan=3)
        options_rotor3 = StringVar()
        options_rotor3.set(lst_roman_rotor_num[int(rotor3_num) - 1])
        rotor_num3_options = OptionMenu(self.root, options_rotor3, *numbers_lst)
        rotor_num3_options.grid(row=3, column=7, columnspan=3, padx=15)

        rotors_letters = Label(self.root, text="the letters on the rotors",
                               font=self.title_font, bg=self.bg_color)
        rotors_letters.grid(row=4, column=3, columnspan=5, pady=5)

        abc_lst = [chr(i) for i in range(65, 91)]

        first_rotor_label_letter = Label(self.root, text="first Rotor",
                                         font=self.text_font, bg=self.bg_color)
        first_rotor_label_letter.grid(row=5, column=1, columnspan=3)
        options_rotor_l1 = StringVar()
        options_rotor_l1.set(rotor1_letter)
        rotor_l1_options = OptionMenu(self.root, options_rotor_l1, *abc_lst)
        rotor_l1_options.grid(row=6, column=1, columnspan=3, padx=15)

        second_rotor_label_letter = Label(self.root, text="second Rotor",
                                          font=self.text_font, bg=self.bg_color)
        second_rotor_label_letter.grid(row=5, column=4, columnspan=3)
        options_rotor_l2 = StringVar()
        options_rotor_l2.set(rotor2_letter)
        rotor_l2_options = OptionMenu(self.root, options_rotor_l2, *abc_lst)
        rotor_l2_options.grid(row=6, column=4, columnspan=3, padx=15)

        third_rotor_label_letter = Label(self.root, text="Third Rotor",
                                         font=self.text_font, bg=self.bg_color)
        third_rotor_label_letter.grid(row=5, column=7, columnspan=3)
        rotors_letters = Label(self.root, text="the letters on the rotors",
                               font=self.title_font, bg=self.bg_color)
        rotors_letters.grid(row=4, column=3, columnspan=5, pady=5)
        options_rotor_l3 = StringVar()
        options_rotor_l3.set(rotor3_letter)
        rotor_l3_options = OptionMenu(self.root, options_rotor_l3, *abc_lst)
        rotor_l3_options.grid(row=6, column=7, columnspan=3, padx=15)

        plugboard_title = Label(self.root, text="Plugboard settings",
                                font=self.title_font, bg=self.bg_color)
        plugboard_title.grid(row=7, column=3, columnspan=5, pady=5)
        plugboard_note = Label(self.root, text="Plugboard can contain 10 pairs max",
                               bg=self.bg_color, font=self.text_font)
        plugboard_note.grid(row=8, column=3, columnspan=5, pady=5)
        lst_buttons = []
        for i in range(65, 74):
            plugboard_letter = Button(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                      bg="khaki", relief=RIDGE, height=2, width=3,
                                      command=lambda letter=chr(i):
                                      self.add_letter_in_plugboard(letter, lst_buttons))
            plugboard_letter.grid(row=9, column=i - 64, pady=5, padx=5)
            lst_buttons.append(plugboard_letter)

        for i in range(74, 83):
            plugboard_letter = Button(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                      bg="khaki", relief=RIDGE, height=2, width=3,
                                      command=lambda letter=chr(i):
                                      self.add_letter_in_plugboard(letter, lst_buttons))
            plugboard_letter.grid(row=10, column=i - 73, pady=5, padx=5)
            lst_buttons.append(plugboard_letter)

        for i in range(83, 91):
            plugboard_letter = Button(self.root, text=" " + chr(i) + " ", font=self.text_font,
                                      bg="khaki", relief=RIDGE, height=2, width=3,
                                      command=lambda letter=chr(i):
                                      self.add_letter_in_plugboard(letter, lst_buttons))
            plugboard_letter.grid(row=11, column=i - 82, pady=5, padx=5)
            lst_buttons.append(plugboard_letter)

        self.set_plugboard(lst_buttons)

        button_save_settings = Button(self.root, text="save settings and go to simulator",
                                      height=2, width=35, font=self.text_font,
                                      command=lambda: self.save_settings(options_rotor1.get(),
                                                                         options_rotor2.get(),
                                                                         options_rotor3.get(),
                                                                         options_rotor_l1.get(),
                                                                         options_rotor_l2.get(),
                                                                         options_rotor_l3.get()))
        button_save_settings.grid(row=12, column=0, columnspan=10, rowspan=2, pady=20, padx=5)

    def save_settings(self, rotor_num1, rotor_num2, rotor_num3, rotor_l1, rotor_l2, rotor_l3):
        """
        this function saves the changes in the simulator settings made by the user.
        :param rotor_num1:
        :param rotor_num2:
        :param rotor_num3:
        :param rotor_l1:
        :param rotor_l2:
        :param rotor_l3:
        :return:
        """
        dict_rotor_num = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}
        label_txt = ""
        rotor_num1 = dict_rotor_num[rotor_num1]
        rotor_num2 = dict_rotor_num[rotor_num2]
        rotor_num3 = dict_rotor_num[rotor_num3]
        if rotor_num1 == rotor_num2 or rotor_num1 == rotor_num3 or rotor_num2 == rotor_num3:
            label_txt = "rotor can not be used more than once at a time"
        if label_txt == "":
            self.simulator((rotor_num1, rotor_num2, rotor_num3, rotor_l1, rotor_l2, rotor_l3), 1)
        else:
            error_label = Label(self.root, text=label_txt, font=self.text_font, bg=self.bg_color)
            error_label.grid(row=14, column=0, columnspan=10, pady=10)

    def add_letter_in_plugboard(self, letter, lst_buttons):
        """
        this function adds a letter to the plugboard
        :param letter:
        :param lst_buttons:
        :return:
        """
        self.simulator_enigma.plugboard.add_letter(letter)
        self.set_plugboard(lst_buttons)

    def set_plugboard(self, lst_buttons):
        """
        this function sets the plugboard in the simulator
        settings and lets the user edit it.
        :param lst_buttons:
        :return:
        """
        colors = ['purple', 'yellow', 'blue', 'orange', 'coral4', 'pink', 'cyan',
                  'SpringGreen2', 'red', 'green']
        used_colors = list(filter(lambda button_bg: button_bg != "khaki",
                                  [i['bg'] for i in lst_buttons]))
        for i in range(len(lst_buttons)):
            if chr(i + 65) not in self.simulator_enigma.plugboard.plugboard1 and \
                    chr(i + 65) not in self.simulator_enigma.plugboard.plugboard2:
                lst_buttons[i].config(bg="khaki")

        for i in range(len(self.simulator_enigma.plugboard.plugboard1)):
            if lst_buttons[ord(self.simulator_enigma.plugboard.plugboard1[i]) - 65]['bg'] \
                    == "khaki" or \
                    lst_buttons[ord(self.simulator_enigma.plugboard.plugboard2[i]) - 65]['bg'] \
                    == "khaki":
                color_index = 0
                while used_colors.count(colors[color_index]) == 2:
                    color_index += 1
                lst_buttons[ord(self.simulator_enigma.plugboard.plugboard1[i]) - 65]. \
                    config(bg=colors[color_index])
                used_colors.append(colors[color_index])
                if self.simulator_enigma.plugboard.plugboard2[i] is not None:
                    lst_buttons[ord(self.simulator_enigma.plugboard.plugboard2[i]) - 65]. \
                        config(bg=colors[color_index])
                    used_colors.append(colors[color_index])

    def show_simulator_encryption(self, rotors_settings, plugboard_settings, plain_text,
                                  letter_number=1):
        """
        this function shows the encryption process in the enigma.
        :param rotors_settings:
        :param plugboard_settings:
        :param plain_text:
        :param letter_number:
        :return:
        """
        self.clear_screen()

        if len(self.simulator_encryption) > 0:
            user_label = Label(self.root, text="Hello " + self.username,
                               font=self.text_font, bg=self.bg_color)
            user_label.grid(pady=5, row=0, column=0, columnspan=5)
            lbl_encryption = Label(self.root,
                                   text="Encrypting The Letter: " +
                                        self.simulator_encryption[letter_number - 1][1][0],
                                   font=self.text_font, bg=self.bg_color)
            lbl_encryption.grid(row=1, column=0, columnspan=5, pady=5, padx=10)

            # text widget to display the stages of the encryption written
            encryption_text_widget = Text(self.root, width=30, height=19,
                                          bg="khaki", font=self.text_font)
            encryption_text_widget.grid(row=2, rowspan=7, column=0,
                                        columnspan=5, padx=10, pady=5)
            encryption_text_widget.insert(END, self.simulator_encryption[letter_number - 1][0])
            encryption_text_widget.config(state=DISABLED)

            # setting canvas to display the encryption visually
            encryption_stages_list = self.simulator_encryption[letter_number - 1][1]
            show_canvas = ShowEncryption(self.root, encryption_stages_list)
            show_canvas.set_canvas()

            # setting a next/previous button if necessary
            if len(self.simulator_encryption) > letter_number:
                next_button = Button(self.root, width=20, height=2,
                                     text="Next Letter", font=self.text_font,
                                     command=lambda:
                                     self.show_simulator_encryption(rotors_settings,
                                                                    plugboard_settings,
                                                                    plain_text,
                                                                    letter_number + 1))
                next_button.grid(row=11, column=0, columnspan=5, padx=10, pady=5)
            if letter_number > 1:
                previous_button = Button(self.root, width=20, height=2,
                                         text="Previous Letter", font=self.text_font,
                                         command=lambda:
                                         self.show_simulator_encryption(rotors_settings,
                                                                        plugboard_settings,
                                                                        plain_text,
                                                                        letter_number - 1))
                previous_button.grid(row=9, column=0, columnspan=5, padx=10, pady=5)
        else:
            # no letters were encrypted
            lbl_encryption = Label(self.root, text="No Letters Have Been Encrypted",
                                   font=self.text_font, bg=self.bg_color)
            lbl_encryption.grid(row=0, column=0, columnspan=5, pady=10, padx=10)

        button_go_back = Button(self.root, text="go back to simulator", font=self.text_font,
                                height=2, width=20,
                                command=lambda: self.simulator(rotors_settings,
                                                               plugboard_settings, plain_text))
        button_go_back.grid(row=10, column=0, columnspan=5, padx=10, pady=5)

    def about_screen(self):
        """
        this function shows the About the Project window.
        it shows information regarding the project.
        :return:
        """
        self.clear_screen()
        user_label = Label(self.root, text="Hello " + self.username,
                           font=self.title_font, bg=self.bg_color, height=2)
        user_label.pack(pady=10, padx=50)
        about_text = """My name is Jasmin, I am 17 years old and this is my final project
for 12th grade in the Cyber Bagrut.
The project contains a multi client-server connection.
The project includes Enigma simulator and explanations about the encryption.
It allows chatting between all the connected users.
Logging in and signing in is through the server. 
the client sends the user data to the server with RSA encryption,
and the server responds appropriately.
Encryption key of messaging is changed every 10 minutes according to the
database enigma settings. the user can also send a message through the 
simulator, using whichever settings he wants. the setting key
(time/settings from the simulator) are sent with RSA encryption. 
the encryption of a message is done with the Enigma machine and
Morse code combined with ASCII afterwards."""
        lbl_about = Label(self.root, text="About The Project",
                          font=self.title_font, bg=self.bg_color)
        lbl_about.pack(pady=5, padx=10)
        about_frame = Frame(self.root, width=100, height=300, bg='white')
        about_frame.pack(padx=30, pady=20)
        text_widget = Text(about_frame)
        text_widget.pack()
        text_widget.insert(END, about_text)
        text_widget.config(state=DISABLED)
        button_send = Button(self.root, text="go back to choose path", font=self.text_font,
                             height=2, width=20, command=self.choose_path)
        button_send.pack(pady=20)

    def clear_screen(self):
        """
        clears the screen from widgets.
        :return:
        """
        lst_grid = self.root.grid_slaves()
        for widget in lst_grid:
            widget.destroy()
        lst_pack = self.root.pack_slaves()
        for widget in lst_pack:
            widget.destroy()

    def receive(self):
        """
        this is a thread method.
        it receives messages from sever and then decrypts them.
        :return:
        """
        print("waiting for messages")
        finish = False
        morse_object = Morse()
        while not finish:
            enigma_sim = Enigma()
            try:
                chunks = []
                bytes_recd = 0
                msg_length = loads(self.my_socket.recv(8000))
                while bytes_recd < msg_length:
                    chunk = self.my_socket.recv(min(msg_length - bytes_recd, 2048))
                    if chunk == b'':
                        raise RuntimeError("socket connection broken")
                    chunks.append(chunk)
                    bytes_recd = bytes_recd + len(chunk)

                encryption_data = loads(self.my_socket.recv(500))
                encryption_data = self.rsa_object.decrypt(encryption_data).decode()

                enigma_sim.rotors.set_rotors(int(encryption_data[0]), int(encryption_data[1]),
                                             int(encryption_data[2]), encryption_data[3],
                                             encryption_data[4], encryption_data[5])
                plugboard1_str = encryption_data[6:(len(encryption_data) - 6) // 2 + 6]
                plugboard2_str = encryption_data[(len(encryption_data) - 6) // 2 + 6:]
                for i in range(len(plugboard1_str)):
                    enigma_sim.plugboard.add_letter(plugboard1_str[i])
                    enigma_sim.plugboard.add_letter(plugboard2_str[i])
                msg = b''.join(chunks).decode()
                msg, username = msg.split(";")
                msg_dec = enigma_sim.decrypt_encrypt_text(morse_object.
                                                          decrypt(msg))
                self.msg_list.append([msg_dec, encryption_data, username])
                if self.refresh_button is not None:
                    self.refresh_button.configure(fg="red")
            except ConnectionResetError:
                finish = True

    def send(self, text_box, rotors_settings=None, plugboard_settings=None):
        """
        send a message to the rest of the clients. if from the
        send box - encrypts according to the time.
        otherwise, from the simulator - encrypts according to its settings.
        :param text_box:
        :param rotors_settings:
        :param plugboard_settings:
        :return:
        """
        morse_instance = Morse()
        enigma_sim = Enigma()
        if plugboard_settings is None and rotors_settings is None:
            enigma_sim.set_random_settings()
        else:
            enigma_sim.rotors.set_rotors(rotors_settings[0], rotors_settings[1], rotors_settings[2],
                                         rotors_settings[3], rotors_settings[4], rotors_settings[5])
            for i in range(len(plugboard_settings[0])):
                enigma_sim.plugboard.add_letter(plugboard_settings[0][i])
                enigma_sim.plugboard.add_letter(plugboard_settings[1][i])
        encryption_data_rotors = ""
        for i in enigma_sim.rotors.get_initial_setting():
            encryption_data_rotors += str(i)
        encryption_data_p1 = ""
        for i in enigma_sim.plugboard.plugboard1:
            encryption_data_p1 += i
        encryption_data_p2 = ""
        for i in enigma_sim.plugboard.plugboard2:
            encryption_data_p2 += i
        encryption_data = encryption_data_rotors + encryption_data_p1 + encryption_data_p2
        my_msg = text_box.get("1.0", END)
        text_box.delete('1.0', END)

        msg = self.manage_text(my_msg)
        if msg != "":
            msg_to_send = morse_instance.encrypt(enigma_sim.decrypt_encrypt_text(msg))
            total_sent = 0
            msg_length = len(msg_to_send)
            self.my_socket.send(dumps(msg_length))
            while total_sent < msg_length:
                sent = self.my_socket.send(msg_to_send[total_sent:].encode())
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                total_sent = total_sent + sent
            self.my_socket.send("encryption data;".encode())
            self.my_socket.send(self.rsa_object.encrypt(encryption_data.encode(), self.server_key))

    @staticmethod
    def manage_text(msg):
        """
        this function customizes the text so it can be encrypted.
        :param msg:
        :return:
        """
        msg = msg.upper()
        msg_final = ""
        for i in msg:
            if i.isalpha():
                msg_final += i
        return msg_final


if __name__ == '__main__':
    client = Client()
