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
        for frame in (HomePage, LoginPage, RecordingPage):

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

        headerLabel = ttk.Label(self, text="Please Sign in with your credentials", font=MEDIUM_FONT)
        headerLabel.pack(pady=10, padx=10)
        
        emailLabel = ttk.Label(self, text="Enter your email", font=SMALL_FONT)
        emailLabel.pack(pady=10, padx=10)
        emailEntry = ttk.Entry(self)
        emailEntry.pack()

        passwordLabel = ttk.Label(self, text="Please enter your password", font=SMALL_FONT)
        passwordLabel.pack(pady=10, padx=10)
        passwordEntry = ttk.Entry(self)
        passwordEntry.pack()

        button2 = ttk.Button(self, text="Login", command=lambda: controller.show_frame(HomePage))
        button2.pack(pady=10, padx=10)
        # endregion


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

    # stopwatch
    running = False
    counter = 0
    timer = ""

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

                self.timer = tk.Label(self, text="Welcome!", fg="black", font="Verdana 20 bold")
                self.timer.grid(row=28, column=0, padx=10, pady=10)

                Start(self.timer)

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

            self.running = False
            self.timer.destroy()

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

            ErrorMessage += checkScrollDownLables(self.bodyPartOptionSelected.get(), "body part",
                                                  self.ethnicityOptionSelected.get(), "ethnicity",
                                                  self.genderOptionSelected.get(), "gender",
                                                  self.raceOptionSelected.get(), "race")

            ErrorMessage += check_strings_not_empty()

            return ErrorMessage

        def check_strings_not_empty():
            ErrorMessage = ""

            if not hm.isAgeValid(self.ageValue):
                ErrorMessage += "Value of age is invalid.\n"

            if not hm.isWeightValid(self.weightValue):
                ErrorMessage += "Value of weight is invalid.\n"

            if not hm.isHeightValid(self.heightValue):
                ErrorMessage += "Value of height is invalid.\n"

            if not hm.isDurationValid(self.durationValue):
                ErrorMessage += "Value of duration is invalid.\n"

            return ErrorMessage

        def checkScrollDownLables(*arguments):
            errorMsg = ""

            count = 0
            for argument in arguments:
                if count % 2 == 0:
                    if(hm.isScrollDownMenuWrong(argument)):
                        errorMsg += "Please select an option for " + arguments[count + 1] + ".\n"
                count += 1

            return errorMsg

        def Start(current_lable2):
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
