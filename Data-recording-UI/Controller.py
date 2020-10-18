import tkinter as tk
import time
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

        saveButton = ttk.Button(self, text="Save and Continue", command=lambda: controller.show_frame(DataRecording))
        saveButton.grid(row=26, column=1, padx=10, pady=30)


class DataRecording(tk.Frame):
    bodyPartOptionSelected = ""

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

        btnStart = ttk.Button(self, text="Start/Stop")      # START AND STOP NEED TO BE MERGED BY IF STATEMENTS
        btnStart.grid(row=8, column=1, padx=10, pady=10)

        timerLabel = ttk.Label(self, text="09:58s", font=MEDIUM_FONT)
        timerLabel.grid(row=10, column=1, padx=0, pady=10)

        save = ttk.Button(self, text="Save")
        save.grid(row=14, column=0, padx=10, pady=10)

        diffPatientButton = ttk.Button(self, text="Next Patient", command=lambda: controller.show_frame(LogPatient))
        diffPatientButton.grid(row=14, column=1, padx=10, pady=10)

        logOutButton = ttk.Button(self, text="Log out", command=lambda: controller.show_frame(LoginPage))
        logOutButton.grid(row=14, column=2, padx=10, pady=10)


"""
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Log in", command=lambda: controller.show_frame(LoginPage))
        button1.pack()

        button2 = ttk.Button(self, text="Start a patient Recording", command=lambda: controller.show_frame(RecordingPage))
        button2.pack()
        # endregion


class RecordingPage(tk.Frame):
    # values for all labels
    ageValue = 0
    weightValue = 0
    heightValue = 0
    idValue = ""
    skinColorValue = ""
    raceOptionSelected = ""
    ethnicityOptionSelected = ""
    genderOptionSelected = ""
    bodyPartOptionSelected = ""
    durationValue = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Data recording", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=0, pady=10)

        idLabel = ttk.Label(self, text="Patient ID:", font=SMALL_FONT)
        idLabel.grid(row=2, column=0, padx=0, pady=10)
        idEntry = ttk.Entry(self)
        idEntry.grid(row=2, column=1)

        ageLabel = ttk.Label(self, text="Age:", font=SMALL_FONT)
        ageLabel.grid(row=4, column=0, padx=10, pady=10)
        ageEntry = ttk.Entry(self)
        ageEntry.grid(row=4, column=1)

        genderLabel = ttk.Label(self, text="Biological Gender:", font=SMALL_FONT)
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
        self.ethnicityOptionSelected.set(hm.Ethnicity[0])   # Initial value
        ethnicityOptions = ttk.OptionMenu(self, self.ethnicityOptionSelected, *hm.Ethnicity)
        ethnicityOptions.grid(row=12, column=1)


        raceLabel = ttk.Label(self, text="Race:", font=SMALL_FONT)
        raceLabel.grid(row=14, column=0, padx=10, pady=10)
        self.raceOptionSelected = tk.StringVar()
        self.raceOptionSelected.set(hm.Race[0])             # Initial value
        raceOptions = ttk.OptionMenu(self, self.raceOptionSelected, *hm.Race)
        raceOptions.grid(row=14, column=1)

        skinColorLabel = ttk.Label(self, text="Skin Color:", font=SMALL_FONT)
        skinColorLabel.grid(row=16, column=0, padx=10, pady=10)
        skinColorEntry = ttk.Entry(self)
        skinColorEntry.grid(row=16, column=1)

        bodyPartLabel = ttk.Label(self, text="Body part:", font=SMALL_FONT)
        bodyPartLabel.grid(row=18, column=0, padx=10, pady=10)
        self.bodyPartOptionSelected = tk.StringVar()
        self.bodyPartOptionSelected.set(hm.BodyParts[0])    # Initial Value
        bodyPartOptions = ttk.OptionMenu(self, self.bodyPartOptionSelected, *hm.BodyParts)
        bodyPartOptions.grid(row=18, column=1, padx=10, pady=10)

        durationLabel = ttk.Label(self, text="Duration:", font=SMALL_FONT)
        durationLabel.grid(row=20, column=0, padx=10, pady=10)
        durationEntry = ttk.Entry(self)
        durationEntry.grid(row=20, column=1)

        btnStart = ttk.Button(self, text="Start recording", command=lambda: start_process())
        btnStart.grid(row=22, column=0, padx=10, pady=10)

        btnStop = ttk.Button(self, text="Stop recording", command=lambda: stop_process())
        btnStop.grid(row=22, column=1, padx=10, pady=10)

        btnPause = ttk.Button(self, text="Pause recording", command=lambda: pause_process())
        btnPause.grid(row=24, column=0, padx=10, pady=10)

        btnResume = ttk.Button(self, text="Resume recording", command=lambda: resume_process())
        btnResume.grid(row=24, column=1, padx=10, pady=10)

        btnStore = ttk.Button(self, text="Store recording")
        btnStore.grid(row=26, column=0, padx=10, pady=10)

        btnBackHome = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        btnBackHome.grid(row=26, column=1, padx=10, pady=10)

        progressBar = ttk.Progressbar(self, orient="horizontal", length=150, mode="determinate")
        # endregion

        # At first only btnStart and back to home, will be enable
        hm.disable_fields(btnStore, btnResume, btnPause, btnStop)

        # verify all fields first, then connect to db and send all info
        def start_process():
            # getValues stores all values from fields into variables and returns any errors found when trying to
            # convert each field into its respective type
            error = getValues()

            if len(error) == 0:     # no errors
                # set up connection and send values
                print(self.ageValue)
                print(self.heightValue)
                print(self.weightValue)
                print(self.ethnicityOptionSelected.get())
                print(self.genderOptionSelected.get())
                print(self.raceOptionSelected.get())
                print(self.skinColorValue)

                hm.enable_fields(btnPause, btnStop)

                hm.disable_fields(btnStart, btnBackHome, btnStore, idEntry, genderOptions, ageEntry, weightEntry,
                                  heightEntry, ethnicityOptions, raceOptions, skinColorEntry, bodyPartOptions,
                                  btnResume, durationEntry)

                progressBar.grid(row=28, padx=10, pady=10)
                threading.Thread(target=startProgressBar()).start()

                return
            else:
                # display pop-up dialog box with error message
                showerror("Errors", "Please fix the following errors:\n" + error)
                return

        # stops the recording session, enables back all buttons and saves the data. Disconnect from db
        def stop_process():
            hm.enable_fields(btnStart, btnBackHome, btnStore, idEntry, genderOptions, ageEntry, weightEntry,
                             heightEntry, ethnicityOptions, raceOptions, skinColorEntry, bodyPartOptions, durationEntry)

            hm.disable_fields(btnResume, btnPause, btnStop)

            return

        # Used to pause session, enabling the option to switch the sensor to another body part. Keeps the connection
        # open and saves data as a different record since patient ID and body location are both primary key
        def pause_process():

            hm.disable_fields(btnPause)
            hm.enable_fields(bodyPartOptions, btnResume, durationEntry)

            return

        # Resumes process. Lets you re-input body part. Sends new body part + ID to database
        def resume_process():

            # check if everything is correct and if you changed body part it gets the new value and checks it as well
            error = getValues()

            if len(error) == 0:
                hm.enable_fields(btnPause)
                hm.disable_fields(btnResume, bodyPartOptions, durationEntry)
            else:
                showerror("Errors", "Please fix the following errors:\n" + error)

            return

        def getValues():

            ErrorMessage = ""

            try:
                self.ageValue = int(ageEntry.get())
            except ValueError:
                ErrorMessage += "Value entered for age is not a number.\n"

            try:
                self.heightValue = float(heightEntry.get())
            except ValueError:
                ErrorMessage += "Value entered for height is not a number.\n"

            try:
                self.weightValue = int(weightEntry.get())
            except ValueError:
                ErrorMessage += "Value entered for weight is not a number.\n"

            try:
                self.durationValue = int(durationEntry.get())
            except ValueError:
                ErrorMessage += "Value entered for duration is not a number.\n"

            self.skinColorValue = skinColorEntry.get()
            if hm.isEmpty(self.skinColorValue):
                ErrorMessage += "No entry for skin color.\n"

            self.idValue = idEntry.get()
            if hm.isEmpty(self.idValue):
                ErrorMessage += "No entry for ID.\n"

            if hm.isScrollDownMenuWrong(self.bodyPartOptionSelected.get()):
                ErrorMessage += "Please select an option for body part.\n"

            if hm.isScrollDownMenuWrong(self.ethnicityOptionSelected.get()):
                ErrorMessage += "Please select an option for ethnicity.\n"

            if hm.isScrollDownMenuWrong(self.genderOptionSelected.get()):
                ErrorMessage += "Please select an option for ethnicity.\n"

            if hm.isScrollDownMenuWrong(self.raceOptionSelected.get()):
                ErrorMessage += "Please select an option for race.\n"

            if not hm.isAgeValid(self.ageValue):
                ErrorMessage += "Value of age is invalid.\n"

            if not hm.isWeightValid(self.weightValue):
                ErrorMessage += "Value of weight is invalid.\n"

            if not hm.isHeightValid(self.heightValue):
                ErrorMessage += "Value of height is invalid.\n"

            if not hm.isDurationValid(self.durationValue):
                ErrorMessage += "Value of duration is invalid.\n"

            return ErrorMessage

        def startProgressBar():
            for x in range(self.durationValue):
                progressBar["value"] += 20
                self.update_idletasks()
                time.sleep(1)

            return
"""

app = Controller()
app.mainloop()
