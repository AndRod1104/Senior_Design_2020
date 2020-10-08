import tkinter as tk
from Design import *
from tkinter import ttk, Entry


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
        emailEntry = Entry(self)
        emailEntry.pack()

        passwordLabel = ttk.Label(self, text="Please enter your password", font=SMALL_FONT)
        passwordLabel.pack(pady=10, padx=10)
        passwordEntry = Entry(self)
        passwordEntry.pack()

        button2 = ttk.Button(self, text="Login",
                            command=lambda: controller.show_frame(HomePage))
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Data recording page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        nameLabel = ttk.Label(self, text="Patient Name", font=SMALL_FONT)
        nameLabel.pack()
        nameEntry = Entry(self)
        nameEntry.pack()

        ageLabel = ttk.Label(self, text="Age", font=SMALL_FONT)
        ageLabel.pack()
        ageEntry = Entry(self)
        ageEntry.pack()

        weightLabel = ttk.Label(self, text="Weight", font=SMALL_FONT)
        weightLabel.pack()
        weightEntry = Entry(self)
        weightEntry.pack()

        ethnicityLabel = ttk.Label(self, text="Ethnicity", font=SMALL_FONT)
        ethnicityLabel.pack()
        ethnicityEntry = Entry(self)
        ethnicityEntry.pack()

        raceLabel = ttk.Label(self, text="Race", font=SMALL_FONT)
        raceLabel.pack()
        raceEntry = Entry(self)
        raceEntry.pack()

        skinColorLabel = ttk.Label(self, text="Skin Color", font=SMALL_FONT)
        skinColorLabel.pack()
        skinColorEntry = Entry(self)
        skinColorEntry.pack()

        button1 = ttk.Button(self, text="Start recording")
        button1.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Pause recording")
        button2.pack()

        button3 = ttk.Button(self, text="Stop recording")
        button3.pack(pady=10, padx=10)

        button4 = ttk.Button(self, text="Store recording")
        button4.pack()

        button5 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        button5.pack(pady=10, padx=10)

        #endregion

        
app = Controller()
app.mainloop()