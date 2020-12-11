import tkinter as tk
from tkinter import ttk
from HelperMethods import LARGE_FONT, SMALL_FONT


class ResetPW(tk.Frame):
    """ This class needs the functionalities of sending an email with a link to reset the pw """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        welcome_label = ttk.Label(self, text="Forgot Your Password?", font=LARGE_FONT)
        welcome_label.pack(pady=20, padx=10)

        f_name_label = ttk.Label(self, text="Enter registered email", font=SMALL_FONT)
        f_name_label.pack(pady=10, padx=10)
        f_name_entry = ttk.Entry(self)
        f_name_entry.pack()

        send_button = ttk.Button(self, text="Send password reset", command=lambda: controller.show_login_frame())
        send_button.pack(pady=30, padx=10)