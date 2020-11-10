import binascii
import hashlib
import os
import tkinter as tk
from tkinter import ttk

import Connection as conn
import HelperMethods as hm
from Design import *


class SignUp(tk.Frame):
    first_name = ""
    middle_Initial = ""
    last_name = ""
    email = ""
    institution = ""
    pw = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        welcome_label = ttk.Label(self, text="New Researcher", font=LARGE_FONT)
        welcome_label.pack(pady=10)

        f_name_label = ttk.Label(self, text="First Name *", font=SMALL_FONT)
        f_name_label.pack(pady=10)
        f_name_entry = ttk.Entry(self)
        f_name_entry.pack()

        m_initial_label = ttk.Label(self, text="Middle Initial *", font=SMALL_FONT)
        m_initial_label.pack(pady=10)
        middle_initial_entry = ttk.Entry(self)
        middle_initial_entry.pack()

        l_name_label = ttk.Label(self, text="Last Name *", font=SMALL_FONT)
        l_name_label.pack(pady=10)
        l_name_entry = ttk.Entry(self)
        l_name_entry.pack()

        email_label = ttk.Label(self, text="Email *", font=SMALL_FONT)
        email_label.pack(pady=10)
        email_entry = ttk.Entry(self)
        email_entry.pack()

        inst_label = ttk.Label(self, text="Institution *", font=SMALL_FONT)
        inst_label.pack(pady=10)
        inst_entry = ttk.Entry(self)
        inst_entry.pack()

        password_label = ttk.Label(self, text="Password *", font=SMALL_FONT)
        password_label.pack(pady=10)
        password_entry = ttk.Entry(self, show="*")
        password_entry.pack()

        retype_password_label = ttk.Label(self, text="Retype password *", font=SMALL_FONT)
        retype_password_label.pack(pady=10)
        retype_password_entry = ttk.Entry(self, show="*")
        retype_password_entry.pack()

        sign_up_button = ttk.Button(self, text="Sign Up", command=lambda: signUp())
        sign_up_button.pack(pady=10)

        alreadyHaveAnAccount = ttk.Button(self, text="Already have an Account? Login",
                                          command=lambda: controller.show_login_frame())
        alreadyHaveAnAccount.pack()

        # endregion

        # region Methods
        def signUp():
            # check if fields are empty, if password match and if email is in correct format
            if hm.check_fields_inputs(
                    fNameEntry=f_name_entry,
                    middleInitialEntry=middle_initial_entry,
                    lNameEntry=l_name_entry,
                    instEntry=inst_entry,
                    passwordEntry=password_entry,
                    reEnterPasswordEntry=retype_password_entry,
                    emailEntry=email_entry,
                    checkEmailFormat=email_entry.get()):
                get_values()
                print(self.first_name)
                print(self.middle_Initial)
                print(self.last_name)
                print(self.institution)

                # Call the function to hash pw and save it to variable
                hashed_pw = hash_password(self.pw)
                # Save new researcher into Azure database
                conn.insert(conn.researcher, self.email, hashed_pw, self.first_name, self.middle_Initial,
                            self.last_name, self.institution)
                controller.show_login_frame()

        def get_values():
            self.first_name = f_name_entry.get()
            self.middle_Initial = middle_initial_entry.get()
            self.last_name = l_name_entry.get()
            self.email = email_entry.get()
            self.institution = inst_entry.get()
            self.pw = password_entry.get()

        def hash_password(pw):
            """Hash a password for storing."""
            salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
            pwhash = hashlib.pbkdf2_hmac('sha512', pw.encode('utf-8'), salt, 100000)
            pwhash = binascii.hexlify(pwhash)
            return (salt + pwhash).decode('ascii')
        # endregion
