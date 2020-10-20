import tkinter as tk
from datetime import datetime
from Design import *
from tkinter import ttk, Entry
import HelperMethods as hm
from tkinter.messagebox import showerror
import threading


class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Data Recording")

        self.geometry("400x650")

        # region Design
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #endregion

        #region Frames
        # Dictionary of class names, frames (Ex: HomePage, actual frame)
        self.frames = {}

        # Adds pages to the container
        for frame in (LoginPage, LogPatient, DataRecording, SignUp, ResetPW):

            # Initialize frames and save them into frames
            tempFrame = frame(container, self)
            self.frames[frame] = tempFrame

            tempFrame.grid(row=0, column=0, sticky="nsew")

        # Starting page
        self.show_frame(LoginPage)
        #endregion

    # When called, passes the frame or page to be showed on windows
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        welcomeLabel = ttk.Label(self, text="Welcome to the BMI reading Platform", font=LARGE_FONT)
        welcomeLabel.pack(pady=10, padx=10)

        emailLabel = ttk.Label(self, text="Email", font=SMALL_FONT)
        emailLabel.pack(pady=10, padx=10)
        emailEntry = ttk.Entry(self)
        emailEntry.pack()

        passwordLabel = ttk.Label(self, text="Password", font=SMALL_FONT)
        passwordLabel.pack(pady=10, padx=10)
        passwordEntry = ttk.Entry(self)
        passwordEntry.pack()

        logInButton = ttk.Button(self, text="Log In", command=lambda: controller.show_frame(LogPatient))
        logInButton.pack(pady=10, padx=10)

        signUpButton = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(SignUp))
        signUpButton.pack(pady=10, padx=10)

        fgtPWButton = ttk.Button(self, text="Forgot Password", command=lambda: controller.show_frame(ResetPW))
        fgtPWButton.pack(pady=10, padx=10)
        # endregion


class SignUp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        welcomeLabel = ttk.Label(self, text="New Researcher", font=LARGE_FONT)
        welcomeLabel.pack(pady=10, padx=10)

        fNameLabel = ttk.Label(self, text="First Name", font=SMALL_FONT)
        fNameLabel.pack(pady=10, padx=10)
        fNameEntry = ttk.Entry(self)
        fNameEntry.pack()

        mInitialLabel = ttk.Label(self, text="Middle Initial", font=SMALL_FONT)
        mInitialLabel.pack(pady=10, padx=10)
        mInEntry = ttk.Entry(self)
        mInEntry.pack()

        lNameLabel = ttk.Label(self, text="Last Name", font=SMALL_FONT)
        lNameLabel.pack(pady=10, padx=10)
        lNameEntry = ttk.Entry(self)
        lNameEntry.pack()

        emailLabel = ttk.Label(self, text="Email", font=SMALL_FONT)
        emailLabel.pack(pady=10, padx=10)
        emailEntry = ttk.Entry(self)
        emailEntry.pack()

        instLabel = ttk.Label(self, text="Institution", font=SMALL_FONT)
        instLabel.pack(pady=10, padx=10)
        instEntry = ttk.Entry(self)
        instEntry.pack()

        signUpButton = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(LoginPage))
        signUpButton.pack(pady=30, padx=10)


class ResetPW(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        welcomeLabel = ttk.Label(self, text="Forgot Your Password?", font=LARGE_FONT)
        welcomeLabel.pack(pady=20, padx=10)

        fNameLabel = ttk.Label(self, text="Enter registered email", font=SMALL_FONT)
        fNameLabel.pack(pady=10, padx=10)
        fNameEntry = ttk.Entry(self)
        fNameEntry.pack()

        sendButton = ttk.Button(self, text="Send password reset", command=lambda: controller.show_frame(LoginPage))
        sendButton.pack(pady=30, padx=10)


class LogPatient(tk.Frame):
    # values for all labels
    ageValue = 0
    weightValue = 0
    heightValue = 0
    skinColorType = ""
    raceOptionSelected = ""
    ethnicityOptionSelected = ""
    genderOptionSelected = ""
    durationValue = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Patient's Info", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=0, pady=10)

        idLabel = ttk.Label(self, text="Patient ID:", font=SMALL_FONT)
        idLabel.grid(row=2, column=0, padx=0, pady=10)
        idVal = ttk.Label(self, text="001", font=SMALL_FONT)      # Interactive get subjID from DB
        idVal.grid(row=2, column=1)

        ageLabel = ttk.Label(self, text="Age:", font=SMALL_FONT)
        ageLabel.grid(row=4, column=0, padx=10, pady=10)
        ageEntry = ttk.Entry(self)
        ageEntry.grid(row=4, column=1)

        genderLabel = ttk.Label(self, text="Sex:", font=SMALL_FONT)
        genderLabel.grid(row=6, column=0, padx=10, pady=10)
        self.genderOptionSelected = tk.StringVar()
        self.genderOptionSelected.set(hm.Gender[0])  # Initial value
        genderOptions = ttk.OptionMenu(self, self.genderOptionSelected, *hm.Gender)
        genderOptions.grid(row=6, column=1)

        weightLabel = ttk.Label(self, text="Weight:", font=SMALL_FONT)
        weightLabel.grid(row=8, column=0, padx=10, pady=10)
        weightEntry = ttk.Entry(self)
        weightEntry.grid(row=8, column=1)

        heightLabel = ttk.Label(self, text="Height:", font=SMALL_FONT)
        heightLabel.grid(row=10, column=0, padx=10, pady=10)
        heightEntry = ttk.Entry(self)
        heightEntry.grid(row=10, column=1)

        ethnicityLabel = ttk.Label(self, text="Ethnicity:", font=SMALL_FONT)
        ethnicityLabel.grid(row=12, column=0, padx=10, pady=10)
        self.ethnicityOptionSelected = tk.StringVar()
        self.ethnicityOptionSelected.set(hm.Ethnicity[0])  # Initial value
        ethnicityOptions = ttk.OptionMenu(self, self.ethnicityOptionSelected, *hm.Ethnicity)
        ethnicityOptions.grid(row=12, column=1)

        raceLabel = ttk.Label(self, text="Race:", font=SMALL_FONT)
        raceLabel.grid(row=14, column=0, padx=10, pady=10)
        self.raceOptionSelected = tk.StringVar()
        self.raceOptionSelected.set(hm.Race[0])  # Initial value
        raceOptions = ttk.OptionMenu(self, self.raceOptionSelected, *hm.Race)
        raceOptions.grid(row=14, column=1)

        skinColorLabel = ttk.Label(self, text="Skin Color:", font=SMALL_FONT)
        skinColorLabel.grid(row=16, column=0, padx=10, pady=10)
        self.skinColorType = tk.StringVar()
        self.skinColorType.set(hm.SkinColor[0])  # Initial value
        skinColorEntry = ttk.OptionMenu(self, self.skinColorType, *hm.SkinColor)
        skinColorEntry.grid(row=16, column=1)

        saveButton = ttk.Button(self, text="Save and Continue", command=lambda: save_and_goToRecordingPage())
        saveButton.grid(row=26, column=1, padx=10, pady=30)
        # endregion

        def save_and_goToRecordingPage():
            # get_values stores all values from fields into variables and returns any errors found when trying to
            # convert each field into its respective type
            error = get_values()

            if len(error) == 0:  # no errors
                # set up connection and send values
                print(self.ageValue)
                print(self.heightValue)
                print(self.weightValue)
                print(self.ethnicityOptionSelected.get())
                print(self.genderOptionSelected.get())
                print(self.raceOptionSelected.get())
                print(self.skinColorType.get())

                # move to recording page
                controller.show_frame(DataRecording)
            else:
                # display pop-up dialog box with error message
                showerror("Errors", "Please fix the following errors:\n" + error)
                return

        def get_values():

            error_message = ""

            try:
                self.ageValue = int(ageEntry.get())
            except ValueError:
                error_message += "Value entered for age is not a number.\n"

            try:
                self.heightValue = float(heightEntry.get())
            except ValueError:
                error_message += "Value entered for height is not a number.\n"

            try:
                self.weightValue = int(weightEntry.get())
            except ValueError:
                error_message += "Value entered for weight is not a number.\n"

            error_message += check_scroll_down_labels(self.ethnicityOptionSelected.get(), "ethnicity",
                                                   self.genderOptionSelected.get(), "gender",
                                                   self.raceOptionSelected.get(), "race",
                                                   self.skinColorType.get(), "skin color")

            error_message += check_fields_not_empty()

            return error_message

        def check_fields_not_empty():
            error_message = ""

            if not hm.isAgeValid(self.ageValue):
                error_message += "Value of age is invalid.\n"

            if not hm.isWeightValid(self.weightValue):
                error_message += "Value of weight is invalid.\n"

            if not hm.isHeightValid(self.heightValue):
                error_message += "Value of height is invalid.\n"

            return error_message

        def check_scroll_down_labels(*arguments):
            error_msg = ""

            count = 0
            for argument in arguments:
                if count % 2 == 0:
                    if (hm.isScrollDownMenuWrong(argument)):
                        error_msg += "Please select an option for " + arguments[count + 1] + ".\n"
                count += 1

            return error_msg


class DataRecording(tk.Frame):
    bodyPartOptionSelected = ""

    # stopwatch
    running = False
    counter = 0
    timer = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Session Recording", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=0, pady=10)

        idLabel = ttk.Label(self, text="Patient ID:", font=SMALL_FONT)
        idLabel.grid(row=2, column=0, padx=0, pady=10)
        idVal = ttk.Label(self, text="001", font=SMALL_FONT)      # Interactive get subjID from DB
        idVal.grid(row=2, column=1)

        bodyPartLabel = ttk.Label(self, text="Body Location:", font=SMALL_FONT)
        bodyPartLabel.grid(row=4, column=0, padx=0, pady=10)
        self.bodyPartOptionSelected = tk.StringVar()
        self.bodyPartOptionSelected.set(hm.BodyParts[0])  # Initial Value
        bodyPartOptions = ttk.OptionMenu(self, self.bodyPartOptionSelected, *hm.BodyParts)
        bodyPartOptions.grid(row=4, column=1, padx=10, pady=10)

        btnStart_Stop = ttk.Button(self, text="Start", command=lambda: start_process())
        btnStart_Stop.grid(row=8, column=1, padx=10, pady=10)

        save = ttk.Button(self, text="Save")
        save.grid(row=14, column=0, padx=10, pady=10)

        diffPatientButton = ttk.Button(self, text="Next Patient", command=lambda: controller.show_frame(LogPatient))
        diffPatientButton.grid(row=14, column=1, padx=10, pady=10)

        logOutButton = ttk.Button(self, text="Log out", command=lambda: controller.show_frame(LoginPage))
        logOutButton.grid(row=14, column=2, padx=10, pady=10)
        # endregion

        def start_process():

            errors = check_fields()

            if len(errors) == 0:    # no errors

                if is_start_button(btnStart_Stop):
                    start_event_handler()
                else:
                    stop_event_handler()

            else:
                showerror("Errors", "Please fix the following errors:\n" + errors)

            return

        def is_start_button(button):
            return button["text"] == "Start"

        def start_event_handler():
            btnStart_Stop["text"] = "Stop"

            self.timer = tk.Label(self, text="Welcome!", fg="black", font="Verdana 15 bold")
            self.timer.grid(row=10, column=1, padx=10, pady=10)

            start_stopwatch(self.timer)
            return

        def stop_event_handler():
            btnStart_Stop["text"] = "Start"

            self.running = False
            self.timer.destroy()
            return

        def check_fields():

            error_message = ""

            if hm.isScrollDownMenuWrong(self.bodyPartOptionSelected.get()):
                error_message += "Please select an option for body part"

            return error_message

        def start_stopwatch(current_lable2):
            self.running = True
            self.counter = 18000
            counter_label(current_lable2)

        def counter_label(current_label):
            def count():
                if self.running:

                    # To manage the intial delay.
                    if self.counter == 18000:
                        display = "Starting..."
                    else:
                        tt = datetime.fromtimestamp(self.counter)
                        string = tt.strftime("%H:%M:%S")
                        display = string

                    current_label['text'] = display  # Or label.config(text=display)

                    current_label.after(1000, count)
                    self.counter += 1
            # Triggering the start of the counter.
            count()


app = Controller()
app.mainloop()
