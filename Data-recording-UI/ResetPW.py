import tkinter as tk
from Design import *
from tkinter import ttk, Entry
import HelperMethods as hm


class ResetPW(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        welcome_label = ttk.Label(self, text="Forgot Your Password?", font=LARGE_FONT)
        welcome_label.pack(pady=20, padx=10)

        f_name_label = ttk.Label(self, text="Enter registered email", font=SMALL_FONT)
        f_name_label.pack(pady=10, padx=10)
        f_name_entry = ttk.Entry(self)
        f_name_entry.pack()

        send_button = ttk.Button(self, text="Send password reset", command=lambda: controller.show_frame(controller.frames["LoginPage"]))
        send_button.pack(pady=30, padx=10)
        # endregion