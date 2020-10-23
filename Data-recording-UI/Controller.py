import tkinter as tk
from datetime import datetime
from Design import *
from tkinter import ttk, Entry
import HelperMethods as hm
from tkinter.messagebox import showerror
import threading
from PIL import Image, ImageTk



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

        passwordBullets = "\u2022" # Bullet points for password security

        # region Design
        welcomeLabel = ttk.Label(self, text="Welcome to the BMI reading Platform", font=LARGE_FONT)
        welcomeLabel.pack(pady=10, padx=10)

        # Picture for paws up
        pawsUpImage = ImageTk.PhotoImage(Image.open("./images/pawsUpImage.gif"))
        pawsUpImageLabel = tk.Label(self, image=pawsUpImage)
        pawsUpImageLabel.image = pawsUpImage
        pawsUpImageLabel.pack()
        
        # Email Label and entry box
        emailLabel = ttk.Label(self, text="Email *", font=SMALL_FONT)
        emailLabel.pack(pady=10, padx=10)
        emailEntry = ttk.Entry(self)
        emailEntry.pack()

        # Password label and entry box
        passwordLabel = ttk.Label(self, text="Password *", font=SMALL_FONT)
        passwordLabel.pack(pady=10, padx=10)
        passwordEntry = ttk.Entry(self, show=passwordBullets)
        passwordEntry.pack()

        #region Buttons

        # Login
        logInButton = ttk.Button(self, text="Log In", command=lambda: check_credentials())
        logInButton.pack(pady=10)

        # Signup
        signUpButton = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(SignUp))
        signUpButton.pack()

        # Forgot Password 
        forgotPasswordPWButton = ttk.Button(self, text="Forgot Password", command=lambda: controller.show_frame(ResetPW))
        forgotPasswordPWButton.pack(pady=20, padx=10)
        # endregion

        # endregion

        # region Methods
        def check_credentials():

            if hm.check_fields_inputs(
                    emailEntry=emailEntry,
                    passwordEntry=passwordEntry,
                    checkEmailFormat=emailEntry.get()):

                controller.show_frame(LogPatient)

        # endregion


class SignUp(tk.Frame):
    firstName = ""
    middleInitial = ""
    lastName = ""
    email = ""
    institution = ""


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        welcomeLabel = ttk.Label(self, text="New Researcher", font=LARGE_FONT)
        welcomeLabel.grid(row=0, column=1, pady=10)

        fNameLabel = ttk.Label(self, text="First Name *", font=SMALL_FONT)
        fNameLabel.grid(row=2, column=0, padx=0, pady=10)
        fNameEntry = ttk.Entry(self)
        fNameEntry.grid(row=2, column=1)

        mInitialLabel = ttk.Label(self, text="Middle Initial *", font=SMALL_FONT)
        mInitialLabel.grid(row=4, column=0, padx=10, pady=10)
        middleInitialEntry = ttk.Entry(self)
        middleInitialEntry.grid(row=4, column=1)

        lNameLabel = ttk.Label(self, text="Last Name *", font=SMALL_FONT)
        lNameLabel.grid(row=8, column=0, padx=10, pady=10)
        lNameEntry = ttk.Entry(self)
        lNameEntry.grid(row=8, column=1)

        emailLabel = ttk.Label(self, text="Email *", font=SMALL_FONT)
        emailLabel.grid(row=10, column=0, padx=10, pady=10)
        emailEntry = ttk.Entry(self)
        emailEntry.grid(row=10, column=1)

        instLabel = ttk.Label(self, text="Institution *", font=SMALL_FONT)
        instLabel.grid(row=12, column=0, padx=10, pady=10)
        instEntry = ttk.Entry(self)
        instEntry.grid(row=12, column=1)

        passwordLabel = ttk.Label(self, text="Password *", font=SMALL_FONT)
        passwordLabel.grid(row=14, column=0, pady=10)
        passwordEntry = ttk.Entry(self, show="*")
        passwordEntry.grid(row=14, column=1, pady=10)

        retypePasswordLabel = ttk.Label(self, text="Retype password *", font=SMALL_FONT)
        retypePasswordLabel.grid(row=16, column=0, pady=10)
        retypePasswordEntry = ttk.Entry(self, show="*")
        retypePasswordEntry.grid(row=16, column=1, pady=10)

        signUpButton = ttk.Button(self, text="Sign Up", command=lambda: signUp())
        signUpButton.grid(row=18, column=1, pady=10)

        alreadyHaveAnAccount = ttk.Button(self, text="Already have an Account? Login", command=lambda: controller.show_frame(LoginPage))
        alreadyHaveAnAccount.grid(row=20, column=1)
        # endregion

        # region Methods
        def signUp():
            # check if fields are empty, if password match and if email is in correct format
            if hm.check_fields_inputs(
                    fNameEntry=fNameEntry,
                    middleInitialEntry=middleInitialEntry,
                    lNameEntry=lNameEntry,
                    instEntry=instEntry,
                    passwordEntry=passwordEntry,
                    reEnterPasswordEntry=retypePasswordEntry,
                    emailEntry=emailEntry,
                    checkEmailFormat=emailEntry.get(),
                    ):
                get_values()
                print(self.firstName)
                print(self.middleInitial)
                print(self.lastName)
                print(self.institution)

        def get_values():
            self.firstName = fNameEntry.get()
            self.middleInitial = middleInitialEntry.get()
            self.lastName = lNameEntry.get()
            self.email = emailEntry.get()
            self.institution = instEntry.get()

        # endregion


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
    # values for all entries
    ageValue = 0
    weightValue = 0
    heightValue = 0
    skinColorType = ""
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


        skinColorLabel = ttk.Label(self, text="Skin Color:", font=SMALL_FONT)
        skinColorLabel.grid(row=16, column=0, padx=10, pady=10)
        self.skinColorType = tk.StringVar()
        self.skinColorType.set(hm.SkinColor[0])  # Initial value
        skinColorEntry = ttk.OptionMenu(self, self.skinColorType, *hm.SkinColor)
        skinColorEntry.grid(row=16, column=1)

        saveButton = ttk.Button(self, text="Save and Continue", command=lambda: save_and_goToRecordingPage())
        saveButton.grid(row=26, column=1, padx=10, pady=30)
        # endregion
        
        # region methods
        def save_and_goToRecordingPage():

            if get_values():
                print(self.ageValue)
                print(self.heightValue)
                print(self.weightValue)
                print(self.ethnicityOptionSelected.get())
                print(self.genderOptionSelected.get())
                print(self.skinColorType.get())
                # move to recording page
                controller.show_frame(DataRecording)

            return

        # get_values stores all values from fields into variables and returns any errors found when trying to
        # convert each field into its respective type
        def get_values():

            if hm.check_fields_inputs(
                    ageEntry=ageEntry,
                    heightEntry=heightEntry,
                    weightEntry=weightEntry,
                    ethnicityOption=self.ethnicityOptionSelected.get(),
                    genderOption=self.genderOptionSelected.get(),
                    skinColorOption=self.skinColorType.get()):

                self.ageValue = int(ageEntry.get())
                self.heightValue = float(heightEntry.get())
                self.weightValue = int(weightEntry.get())
                return True
            else:
                return False
        # endregion


class DataRecording(tk.Frame):
    bodyPartOptionSelected = ""
    durationValue = 0

    # stopwatch
    running = False
    counter = 18000
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

        durationLabel = ttk.Label(self, text="Duration:", font=SMALL_FONT)
        durationLabel.grid(row=5, column=0, padx=0, pady=10)
        durationEntry = ttk.Entry(self)
        durationEntry.grid(row=5, column=1)

        bodyPartLabel = ttk.Label(self, text="Body Location:", font=SMALL_FONT)
        bodyPartLabel.grid(row=4, column=0, padx=0, pady=10)
        self.bodyPartOptionSelected = tk.StringVar()
        self.bodyPartOptionSelected.set(hm.BodyParts[0])  # Initial Value
        bodyPartOptions = ttk.OptionMenu(self, self.bodyPartOptionSelected, *hm.BodyParts)
        bodyPartOptions.grid(row=4, column=1, padx=10, pady=10)

        btn_Start_Stop = ttk.Button(self, text="Start", command=lambda: start_stop_process())
        btn_Start_Stop.grid(row=8, column=0, padx=10, pady=10)

        btnSave = ttk.Button(self, text="Save")
        btnSave.grid(row=14, column=0, padx=10, pady=10)

        btn_Pause_Resume = ttk.Button(self, text="Pause", command=lambda: pause_resume_process())
        btn_Pause_Resume.grid(row=8, column=1, padx=10, pady=10)


        diffPatientButton = ttk.Button(self, text="Next Patient", command=lambda: controller.show_frame(LogPatient))
        diffPatientButton.grid(row=14, column=1, padx=10, pady=10)

        logOutButton = ttk.Button(self, text="Log out", command=lambda: controller.show_frame(LoginPage))
        logOutButton.grid(row=14, column=2, padx=10, pady=10)
        # endregion

        hm.disable_fields(btn_Pause_Resume)

        def pause_resume_process():

            if hm.is_pause_button(btn_Pause_Resume):
                pause_process()
            else:
                # check if no errors when re-entering fields
                if check_fields():
                    resume_process()

            return

        def resume_process():

            btn_Pause_Resume["text"] = "Pause"
            start_stopwatch(self.timer)
            hm.disable_fields(bodyPartOptions, durationEntry)

            #TODO
            # Connect to save again values with different body part in DB
            print(self.durationValue)
            print(self.bodyPartOptionSelected.get())

            return

        def pause_process():

            btn_Pause_Resume["text"] = "Resume"
            self.running = False
            hm.enable_fields(bodyPartOptions, durationEntry)
            return

        def start_stop_process():

            if check_fields():    # no errors
                if hm.is_start_button(btn_Start_Stop):
                    start_process()
                else:
                    stop_process()

            return


        def start_process():

            hm.disable_fields(btnSave, logOutButton, diffPatientButton, bodyPartOptions, durationEntry)
            hm.enable_fields(btn_Pause_Resume)
            btn_Start_Stop["text"] = "Stop"

            self.timer = tk.Label(self, text="Welcome!", fg="black", font="Verdana 15 bold")
            self.timer.grid(row=10, column=1, padx=10, pady=10)
            self.counter = 18000  # we need to reset the timer after 1st recording

            start_stopwatch(self.timer)
            return

        def stop_process():
            hm.disable_fields(btn_Pause_Resume)

            btn_Pause_Resume["text"] = "Pause"  # if stop the recording, we need to reset this button (bug)
            btn_Start_Stop["text"] = "Start"

            hm.enable_fields(btnSave, logOutButton, diffPatientButton, bodyPartOptions, durationEntry)

            self.running = False
            self.timer.destroy()
            return

        # checks for any errors, prints them and returns False, otherwise no errors and returns True
        def check_fields():

            if hm.check_fields_inputs(durationEntry=durationEntry, bodyPartOption=self.bodyPartOptionSelected.get()):

                self.durationValue = int(durationEntry.get())
                return True

            else:
                return False

        # region Stopwatch
        def start_stopwatch(current_lable2):
            self.running = True
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
        # endregion


app = Controller()
app.mainloop()
