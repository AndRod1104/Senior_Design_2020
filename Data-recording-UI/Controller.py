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

        password_bullets = "\u2022" # Bullet points for password security

        # region Design
        welcome_label = ttk.Label(self, text="Welcome to the BMI reading Platform", font=LARGE_FONT)
        welcome_label.pack(pady=10, padx=10)

        # Picture for paws up
        paws_up_image = ImageTk.PhotoImage(Image.open("./images/pawsUpImage.gif"))
        paws_up_image_label = tk.Label(self, image=paws_up_image)
        paws_up_image_label.image = paws_up_image
        paws_up_image_label.pack()
        
        # Email Label and entry box
        email_label = ttk.Label(self, text="Email *", font=SMALL_FONT)
        email_label.pack(pady=10, padx=10)
        email_entry = ttk.Entry(self)
        email_entry.pack()

        # Password label and entry box
        password_label = ttk.Label(self, text="Password *", font=SMALL_FONT)
        password_label.pack(pady=10, padx=10)
        password_entry = ttk.Entry(self, show=password_bullets)
        password_entry.pack()

        #region Buttons

        # Login
        log_in_button = ttk.Button(self, text="Log In", command=lambda: check_credentials())
        log_in_button.pack(pady=10)

        # Signup
        sign_up_button = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(SignUp))
        sign_up_button.pack()

        # Forgot Password 
        forgot_password_button = ttk.Button(self, text="Forgot Password", command=lambda: controller.show_frame(ResetPW))
        forgot_password_button.pack(pady=20, padx=10)
        # endregion

        # endregion

        # region Methods
        def check_credentials():

            if hm.check_fields_inputs(
                    emailEntry=email_entry,
                    passwordEntry=password_entry,
                    checkEmailFormat=email_entry.get()):

                controller.show_frame(LogPatient)

        # endregion


class SignUp(tk.Frame):
    first_name = ""
    middle_Initial = ""
    last_name = ""
    email = ""
    institution = ""


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        welcome_label = ttk.Label(self, text="New Researcher", font=LARGE_FONT)
        welcome_label.grid(row=0, column=1, pady=10)

        f_name_label = ttk.Label(self, text="First Name *", font=SMALL_FONT)
        f_name_label.grid(row=2, column=0, padx=0, pady=10)
        f_name_entry = ttk.Entry(self)
        f_name_entry.grid(row=2, column=1)

        m_initial_label = ttk.Label(self, text="Middle Initial *", font=SMALL_FONT)
        m_initial_label.grid(row=4, column=0, padx=10, pady=10)
        middle_initial_entry = ttk.Entry(self)
        middle_initial_entry.grid(row=4, column=1)

        l_name_label = ttk.Label(self, text="Last Name *", font=SMALL_FONT)
        l_name_label.grid(row=8, column=0, padx=10, pady=10)
        l_name_entry = ttk.Entry(self)
        l_name_entry.grid(row=8, column=1)

        email_label = ttk.Label(self, text="Email *", font=SMALL_FONT)
        email_label.grid(row=10, column=0, padx=10, pady=10)
        email_entry = ttk.Entry(self)
        email_entry.grid(row=10, column=1)

        inst_label = ttk.Label(self, text="Institution *", font=SMALL_FONT)
        inst_label.grid(row=12, column=0, padx=10, pady=10)
        inst_entry = ttk.Entry(self)
        inst_entry.grid(row=12, column=1)

        password_label = ttk.Label(self, text="Password *", font=SMALL_FONT)
        password_label.grid(row=14, column=0, pady=10)
        password_entry = ttk.Entry(self, show="*")
        password_entry.grid(row=14, column=1, pady=10)

        retype_password_label = ttk.Label(self, text="Retype password *", font=SMALL_FONT)
        retype_password_label.grid(row=16, column=0, pady=10)
        retype_password_entry = ttk.Entry(self, show="*")
        retype_password_entry.grid(row=16, column=1, pady=10)

        sign_up_button = ttk.Button(self, text="Sign Up", command=lambda: signUp())
        sign_up_button.grid(row=18, column=1, pady=10)

        alreadyHaveAnAccount = ttk.Button(self, text="Already have an Account? Login", command=lambda: controller.show_frame(LoginPage))
        alreadyHaveAnAccount.grid(row=20, column=1)
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
                    checkEmailFormat=email_entry.get(),
                    ):
                get_values()
                print(self.first_name)
                print(self.middle_Initial)
                print(self.last_name)
                print(self.institution)

        def get_values():
            self.first_name = f_name_entry.get()
            self.middle_Initial = middle_initial_entry.get()
            self.last_name = l_name_entry.get()
            self.email = email_entry.get()
            self.institution = inst_entry.get()

        # endregion


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

        send_button = ttk.Button(self, text="Send password reset", command=lambda: controller.show_frame(LoginPage))
        send_button.pack(pady=30, padx=10)


class LogPatient(tk.Frame):
    # values for all entries
    age_value = 0
    weight_value = 0
    height_value = 0
    skin_color_type = ""
    ethnicity_option_selected = ""
    gender_option_selected = ""
    duration_value = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Patient's Info", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=0, pady=10)

        id_label = ttk.Label(self, text="Patient ID:", font=SMALL_FONT)
        id_label.grid(row=2, column=0, padx=0, pady=10)
        id_val = ttk.Label(self, text="001", font=SMALL_FONT)      # Interactive get subjID from DB
        id_val.grid(row=2, column=1)

        age_label = ttk.Label(self, text="Age:", font=SMALL_FONT)
        age_label.grid(row=4, column=0, padx=10, pady=10)
        age_entry = ttk.Entry(self)
        age_entry.grid(row=4, column=1)

        gender_label = ttk.Label(self, text="Sex:", font=SMALL_FONT)
        gender_label.grid(row=6, column=0, padx=10, pady=10)
        self.gender_option_selected = tk.StringVar()
        self.gender_option_selected.set(hm.Gender[0])  # Initial value
        gender_options = ttk.OptionMenu(self, self.gender_option_selected, *hm.Gender)
        gender_options.grid(row=6, column=1)

        weight_label = ttk.Label(self, text="Weight:", font=SMALL_FONT)
        weight_label.grid(row=8, column=0, padx=10, pady=10)
        weight_entry = ttk.Entry(self)
        weight_entry.grid(row=8, column=1)

        height_label = ttk.Label(self, text="Height:", font=SMALL_FONT)
        height_label.grid(row=10, column=0, padx=10, pady=10)
        height_entry = ttk.Entry(self)
        height_entry.grid(row=10, column=1)

        ethnicity_label = ttk.Label(self, text="Ethnicity:", font=SMALL_FONT)
        ethnicity_label.grid(row=12, column=0, padx=10, pady=10)
        self.ethnicity_option_selected = tk.StringVar()
        self.ethnicity_option_selected.set(hm.Ethnicity[0])  # Initial value
        ethnicity_options = ttk.OptionMenu(self, self.ethnicity_option_selected, *hm.Ethnicity)
        ethnicity_options.grid(row=12, column=1)


        skin_color_label = ttk.Label(self, text="Skin Color:", font=SMALL_FONT)
        skin_color_label.grid(row=16, column=0, padx=10, pady=10)
        self.skin_color_type = tk.StringVar()
        self.skin_color_type.set(hm.SkinColor[0])  # Initial value
        skin_color_entry = ttk.OptionMenu(self, self.skin_color_type, *hm.SkinColor)
        skin_color_entry.grid(row=16, column=1)

        save_button = ttk.Button(self, text="Save and Continue", command=lambda: save_and_go_to_recording_page())
        save_button.grid(row=26, column=1, padx=10, pady=30)
        # endregion
        
        # region methods
        def save_and_go_to_recording_page():

            if get_values():
                print(self.age_value)
                print(self.height_value)
                print(self.weight_value)
                print(self.ethnicity_option_selected.get())
                print(self.gender_option_selected.get())
                print(self.skin_color_type.get())
                # move to recording page
                controller.show_frame(DataRecording)

            return

        # get_values stores all values from fields into variables and returns any errors found when trying to
        # convert each field into its respective type
        def get_values():

            if hm.check_fields_inputs(
                    ageEntry=age_entry,
                    heightEntry=height_entry,
                    weightEntry=weight_entry,
                    ethnicityOption=self.ethnicity_option_selected.get(),
                    genderOption=self.gender_option_selected.get(),
                    skinColorOption=self.skin_color_type.get()):

                self.age_value = int(age_entry.get())
                self.height_value = float(height_entry.get())
                self.weight_value = int(weight_entry.get())
                return True
            else:
                return False
        # endregion


class DataRecording(tk.Frame):
    body_part_option_selected = ""
    duration_value = 0

    # stopwatch
    running = False
    current_ticking_value = 18000   # This depends on current timezone, may be different in other regions. Starts at 0
    ticking_value_max = 0   # initialization, actual value assigned on create_stopwatch() function
    timer_label = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Session Recording", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=0, pady=10)

        id_label = ttk.Label(self, text="Patient ID:", font=SMALL_FONT)
        id_label.grid(row=2, column=0, padx=0, pady=10)
        id_val = ttk.Label(self, text="001", font=SMALL_FONT)      # Interactive get subjID from DB
        id_val.grid(row=2, column=1)

        duration_label = ttk.Label(self, text="Duration:", font=SMALL_FONT)
        duration_label.grid(row=5, column=0, padx=0, pady=10)
        duration_entry = ttk.Entry(self)
        duration_entry.grid(row=5, column=1)

        body_part_label = ttk.Label(self, text="Body Location:", font=SMALL_FONT)
        body_part_label.grid(row=4, column=0, padx=0, pady=10)
        self.body_part_option_selected = tk.StringVar()
        self.body_part_option_selected.set(hm.BodyParts[0])  # Initial Value
        body_part_options = ttk.OptionMenu(self, self.body_part_option_selected, *hm.BodyParts)
        body_part_options.grid(row=4, column=1, padx=0, pady=10)

        btn_start_stop = ttk.Button(self, text="Start", command=lambda: start_stop_process())
        btn_start_stop.grid(row=8, column=0, padx=0, pady=10)

        btn_save = ttk.Button(self, text="Save", command=lambda: save_recording())
        btn_save.grid(row=14, column=0, padx=0, pady=10)

        btn_pause_resume = ttk.Button(self, text="Pause", command=lambda: pause_resume_process())
        btn_pause_resume.grid(row=8, column=1, padx=0, pady=10)


        diff_patient_button = ttk.Button(self, text="Next Patient", command=lambda: controller.show_frame(LogPatient))
        diff_patient_button.grid(row=14, column=1, padx=0, pady=10)

        log_out_button = ttk.Button(self, text="Log out", command=lambda: controller.show_frame(LoginPage))
        log_out_button.grid(row=14, column=2, padx=0, pady=10)

        checkbox_value = tk.IntVar()
        check_box_label = tk.Checkbutton(self, text="Interrupted session", variable=checkbox_value)

        check_box_label.grid(row=15, padx=0, pady=10)
        # endregion

        hm.disable_fields(btn_pause_resume)

        def save_recording():
            if checkbox_value.get() == 1:    # If interrupted session

                # TODO: Message box will probably have to be a customized pop-up. You can't add an entry text field here
                result = tk.messagebox.askyesno("Interrupted session", "You have marked this session as interrupted.\n"
                                                                       "Data will be saved in different database")
                if result:     # If user confirmed session was interrupted and he/she agrees with message
                    # TODO: Data in different database
                    print("Result:")
                    print(result)

            else:   # normal session
                print(self.duration_value)

            return

        def pause_resume_process():

            if hm.is_pause_button(btn_pause_resume):
                pause_process()
            else:
                # check if no errors when re-entering fields
                if check_fields():
                    resume_process()

            return

        def resume_process():

            btn_pause_resume["text"] = "Pause"
            start_stopwatch(self.timer_label)
            hm.disable_fields(body_part_options, duration_entry)

            #TODO
            # Connect to save again values with different body part in DB
            print(self.duration_value)
            print(self.body_part_option_selected.get())

            return

        def pause_process():
            #TODO
            # Do we want to change the duration and body part once user pauses? *** BUG ***
            btn_pause_resume["text"] = "Resume"
            self.running = False
            hm.enable_fields(body_part_options, duration_entry)
            return

        def start_stop_process():

            if check_fields():    # no errors
                if hm.is_start_button(btn_start_stop):
                    start_process()
                else:
                    stop_process()

            return


        def start_process():

            hm.disable_fields(btn_save, log_out_button, diff_patient_button, body_part_options, duration_entry)
            hm.enable_fields(btn_pause_resume)
            btn_start_stop["text"] = "Stop"

            create_stopwatch()
            start_stopwatch(self.timer_label)
            return

        def stop_process():
            hm.disable_fields(btn_pause_resume)

            btn_pause_resume["text"] = "Pause"  # if stop the recording, we need to reset this button (bug)
            btn_start_stop["text"] = "Start"

            hm.enable_fields(btn_save, log_out_button, diff_patient_button, body_part_options, duration_entry)

            self.running = False
            self.timer_label.destroy()
            return

        # checks for any errors, prints them and returns False, otherwise no errors and returns True
        def check_fields():

            if hm.check_fields_inputs(durationEntry=duration_entry, bodyPartOption=self.body_part_option_selected.get()):

                self.duration_value = int(duration_entry.get())
                return True

            else:
                return False

        # region Stopwatch
        def create_stopwatch():
            self.timer_label = tk.Label(self, text="Welcome!", fg="black", font="Verdana 15 bold")
            self.timer_label.grid(row=10, column=1, padx=10, pady=10)
            self.current_ticking_value = 18000  # we need to reset the timer after 1st recording

            # Cannot assign ticking_value_max until we know the duration_value and after being checked
            self.ticking_value_max = self.current_ticking_value + self.duration_value
            return

        def start_stopwatch(timer_label):
            self.running = True
            counter_label(timer_label)
            return

        def counter_label(timer_label):
            def count():
                if self.running and self.current_ticking_value <= self.ticking_value_max:     # if from 0 to limit
                    # To manage the intial delay.
                    if self.current_ticking_value == 18000:
                        display = "Starting..."
                    else:
                        tt = datetime.fromtimestamp(self.current_ticking_value)
                        string = tt.strftime("%H:%M:%S")
                        display = string

                    timer_label['text'] = display  # Or label.config(text=display)

                    timer_label.after(1000, count)
                    self.current_ticking_value += 1

                elif not self.running and self.current_ticking_value <= self.ticking_value_max:   # if paused
                    timer_label['text'] = "Paused..."

                else:
                    timer_label['text'] = "Finished!"
                    hm.disable_fields(btn_pause_resume)
                    btn_pause_resume["text"] = "Pause"
            # Triggering the start of the counter.
            count()
        # endregion


app = Controller()
app.mainloop()
