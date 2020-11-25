import binascii
import hashlib
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

import Connection as conn
import HelperMethods as hm


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        password_bullets = "\u2022"  # Bullet points for password security

        # region Design
        welcome_label = ttk.Label(self, text="Welcome to the BMI reading Platform", font=hm.LARGE_FONT)
        welcome_label.pack(pady=10, padx=10)

        # Picture for paths up
        paws_up_image = ImageTk.PhotoImage(Image.open("./images/PathsUp.gif"), master=self)
        paws_up_image_label = tk.Label(self, image=paws_up_image)
        paws_up_image_label.image = paws_up_image
        paws_up_image_label.pack()

        # Email Label and entry box
        email_label = ttk.Label(self, text="Email *", font=hm.SMALL_FONT)
        email_label.pack(pady=10, padx=10)
        email_entry = ttk.Entry(self)
        email_entry.insert(0, "user@yahoo.com")  # 2TEST ERASE!!!
        email_entry.pack()

        # Password label and entry box
        password_label = ttk.Label(self, text="Password *", font=hm.SMALL_FONT)
        password_label.pack(pady=10, padx=10)
        password_entry = ttk.Entry(self, show=password_bullets)
        password_entry.insert(0, "user")   # 2TEST ERASE!!!
        password_entry.pack()

        # Login Button
        log_in_button = ttk.Button(self, text="Log In", command=lambda: check_credentials())
        log_in_button.pack(pady=10)

        # Signup Button
        sign_up_button = ttk.Button(self, text="Sign Up", command=lambda: controller.show_signUp_frame())
        sign_up_button.pack()

        # Forgot Password Button
        forgot_password_button = ttk.Button(self, text="Forgot Password",
                                            command=lambda: controller.show_resetPW_frame())
        forgot_password_button.pack(pady=20, padx=10)
        # endregion

        def check_credentials():
            """ Validates email and password when logging into the database """
            if hm.check_fields_inputs(emailEntry=email_entry,
                                      passwordEntry=password_entry,
                                      checkEmailFormat=email_entry.get()):
                # Get list of emails from db and check if input email is in that list
                if conn.email_exist(email_entry.get()):
                    stored_pw = conn.select('passwrd', conn.researcher, 'email', email_entry.get())
                    # If email is in the list verify the password and allow access, else prompt error
                    if verify_password(stored_pw, password_entry.get()):
                        hm.current_researcher = conn.select('researcher_id', conn.researcher,
                                                            'email', email_entry.get())
                        controller.show_patientLog_frame()
                    else:
                        hm.showerror("Authentication Error", "\u2022    Wrong Password. Try again")
                else:
                    hm.showerror("Error", "\u2022    This email is not registered")

        def verify_password(stored_pw, provided_pw):
            """Verify a stored password against one provided by user"""
            salt = stored_pw[:64]
            stored_pw = stored_pw[64:]
            pwhash = hashlib.pbkdf2_hmac('sha512', provided_pw.encode('utf-8'), salt.encode('ascii'), 100000)
            pwhash = binascii.hexlify(pwhash).decode('ascii')
            return pwhash == stored_pw