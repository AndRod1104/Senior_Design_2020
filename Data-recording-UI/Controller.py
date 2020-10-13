import tkinter as tk
from Design import *
from tkinter import ttk, Entry
import HelperMethods as hm
from tkinter.messagebox import showerror

class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Data Recording")

        self.geometry("400x600")

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Data recording page", font=LARGE_FONT)
        label.grid(row=0, column=1)

        nameLabel = ttk.Label(self, text="Patient ID", font=SMALL_FONT)
        nameLabel.grid(row=2, column=0, padx=0, pady=10)
        nameEntry = ttk.Entry(self)
        nameEntry.grid(row=2, column=1)

        ageLabel = ttk.Label(self, text="Age", font=SMALL_FONT)
        ageLabel.grid(row=4, column=0, padx=10, pady=10)
        ageEntry = ttk.Entry(self)
        ageEntry.grid(row=4, column=1)

        genderLabel = ttk.Label(self, text="Biological Gender", font=SMALL_FONT)
        genderLabel.grid(row=6, column=0, padx=10, pady=10)
        self.genderOptionSelected = tk.StringVar()
        self.genderOptionSelected.set(hm.Gender[0])  # Initial value
        genderOptions = ttk.OptionMenu(self, self.genderOptionSelected, *hm.Gender)
        genderOptions.grid(row=6, column=1)

        weightLabel = ttk.Label(self, text="Weight", font=SMALL_FONT)
        weightLabel.grid(row=8, column=0, padx=10, pady=10)
        weightEntry = ttk.Entry(self)
        weightEntry.grid(row=8, column=1)

        heightLabel = ttk.Label(self, text="Height", font=SMALL_FONT)
        heightLabel.grid(row=10, column=0, padx=10, pady=10)
        heightEntry = ttk.Entry(self)
        heightEntry.grid(row=10, column=1)

        ethnicityLabel = ttk.Label(self, text="Ethnicity", font=SMALL_FONT)
        ethnicityLabel.grid(row=12, column=0, padx=10, pady=10)
        self.ethnicityOptionSelected = tk.StringVar()
        self.ethnicityOptionSelected.set(hm.Ethnicity[0])   # Initial value
        ethnicityOptions = ttk.OptionMenu(self, self.ethnicityOptionSelected, *hm.Ethnicity)
        ethnicityOptions.grid(row=12, column=1)


        raceLabel = ttk.Label(self, text="Race", font=SMALL_FONT)
        raceLabel.grid(row=14, column=0, padx=10, pady=10)
        self.raceOptionSelected = tk.StringVar()
        self.raceOptionSelected.set(hm.Race[0])             # Initial value
        raceOptions = ttk.OptionMenu(self, self.raceOptionSelected, *hm.Race)
        raceOptions.grid(row=14, column=1)

        skinColorLabel = ttk.Label(self, text="Skin Color", font=SMALL_FONT)
        skinColorLabel.grid(row=16, column=0, padx=10, pady=10)
        skinColorEntry = ttk.Entry(self)
        skinColorEntry.grid(row=16, column=1)

        button1 = ttk.Button(self, text="Start recording", command=lambda: start_process())
        button1.grid(row=18, column=0, padx=10, pady=10)

        button2 = ttk.Button(self, text="Pause recording")
        button2.grid(row=18, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Stop recording")
        button3.grid(row=20, column=0, padx=10, pady=10)

        button4 = ttk.Button(self, text="Store recording")
        button4.grid(row=20, column=1, padx=10, pady=10)

        button5 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        button5.grid(row=22, column=1, padx=10, pady=10)
        # endregion

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

                return
            else:
                # display pop-up dialog box with error message
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

            self.skinColorValue = skinColorEntry.get()
            if hm.isEmpty(self.skinColorValue):
                ErrorMessage += "No entry for skin color.\n"

            self.idValue = nameEntry.get()
            if hm.isEmpty(self.idValue):
                ErrorMessage += "No entry for name.\n"

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

            return ErrorMessage


app = Controller()
app.mainloop()
