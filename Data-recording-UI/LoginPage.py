import tkinter as tk
from Design import *
from tkinter import ttk, Entry
import HelperMethods as hm
from PIL import Image, ImageTk


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        password_bullets = "\u2022"  # Bullet points for password security

        # region Design
        welcome_label = ttk.Label(self, text="Welcome to the BMI reading Platform", font=LARGE_FONT)
        welcome_label.pack(pady=10, padx=10)

        # Picture for paths up
        paws_up_image = ImageTk.PhotoImage(Image.open("./images/PathsUp.gif"), master=self)
        paws_up_image_label = tk.Label(self, image=paws_up_image)
        paws_up_image_label.image = paws_up_image
        paws_up_image_label.pack()

        # Email Label and entry box
        email_label = ttk.Label(self, text="Email *", font=SMALL_FONT)
        email_label.pack(pady=10, padx=10)
        email_entry = ttk.Entry(self)
        email_entry.insert(0, "test@yahoo.com")  # 2TEST ERASE!!!
        email_entry.pack()

        # Password label and entry box
        password_label = ttk.Label(self, text="Password *", font=SMALL_FONT)
        password_label.pack(pady=10, padx=10)
        password_entry = ttk.Entry(self, show=password_bullets)
        password_entry.insert(0, "badbunny")  # 2TEST ERASE!!!
        password_entry.pack()

        # Login Button
        log_in_button = ttk.Button(self, text="Log In", command=lambda: check_credentials())
        log_in_button.pack(pady=10)

        # Signup Button
        sign_up_button = ttk.Button(self, text="Sign Up", command=lambda: controller.show_signUp_frame())
        sign_up_button.pack()

        # Forgot Password Button
        forgot_password_button = ttk.Button(self, text="Forgot Password", command=lambda: controller.show_resetPW_frame())
        forgot_password_button.pack(pady=20, padx=10)

        # endregion

        def check_credentials():
            if hm.check_fields_inputs(
                    emailEntry=email_entry,
                    passwordEntry=password_entry,
                    checkEmailFormat=email_entry.get()):
                controller.show_patientLog_frame()

