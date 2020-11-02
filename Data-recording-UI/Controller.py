import seatease.spectrometers as s  # Emulator to test w/o spectrometer

import tkinter as tk
from datetime import datetime
from Design import *
from tkinter import ttk, Entry
import HelperMethods as hm
import numpy as np
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

spec = s.Spectrometer.from_first_available()
dev_list = s.list_devices()  # Part of emulator
spec = s.Spectrometer(dev_list[0])  # Part of emulator
integration_time = 20000  # 20 ms, set default integration time to a reasonable value
spectra_average = 1
spec.integration_time_micros(integration_time)
x = spec.wavelengths()
data = spec.intensities()  # correct_dark_counts=True, correct_nonlinearity=False PUT BACK IN ()
xmin = np.around(min(x), decimals=2)
xmax = np.around(max(x), decimals=2)
ymin = np.around(min(data), decimals=2)
ymax = np.around(max(data), decimals=2)
# minIntTime =spec.minimum_integration_time_micros          UNCOMMENT


class Controller(tk.Tk):
    def __init__(self, ax, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Data Recording")

        self.geometry("1000x700")

        # region Design
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # endregion

        # region Frames
        # Dictionary of class names, frames (Ex: HomePage, actual frame)
        self.frames = {}

        # Adds pages to the container
        for frame in (LoginPage, LogPatient, DataRecording, SignUp, ResetPW):
            if frame is DataRecording:
                print("I am DataRecording")
                tempFrame = frame(container, self, ax)
                self.frames[frame] = tempFrame

                tempFrame.grid(row=0, column=0, sticky="nsew")
            # Initialize frames and save them into frames
            else:
                print("I am the rest frames")
                tempFrame = frame(container, self)
                self.frames[frame] = tempFrame

                tempFrame.grid(row=0, column=0, sticky="nsew")

        # Starting page
        self.show_frame(LoginPage)
        # endregion

    def get_DataRecording(self):
        return self.all_frames[DataRecording]   # DataRecording frame

    # When called, passes the frame or page to be showed on windows
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


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
        sign_up_button = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(SignUp))
        sign_up_button.pack()

        # Forgot Password Button
        forgot_password_button = ttk.Button(self, text="Forgot Password",
                                            command=lambda: controller.show_frame(ResetPW))
        forgot_password_button.pack(pady=20, padx=10)

        # endregion

        def check_credentials():
            if hm.check_fields_inputs(
                    emailEntry=email_entry,
                    passwordEntry=password_entry,
                    checkEmailFormat=email_entry.get()):
                controller.show_frame(LogPatient)


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
                                          command=lambda: controller.show_frame(LoginPage))
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
        # endregion


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
        id_val = ttk.Label(self, text="001", font=SMALL_FONT)  # Interactive get subjID from DB
        id_val.grid(row=2, column=1)

        age_label = ttk.Label(self, text="Age:", font=SMALL_FONT)
        age_label.grid(row=4, column=0, padx=10, pady=10)
        age_entry = ttk.Entry(self)
        age_entry.insert(0, 30)  # 2TEST ERASE!!!
        age_entry.grid(row=4, column=1)

        gender_label = ttk.Label(self, text="Sex:", font=SMALL_FONT)
        gender_label.grid(row=6, column=0, padx=10, pady=10)
        self.gender_option_selected = tk.StringVar()
        self.gender_option_selected.set(hm.Gender[0])  # Initial value
        gender_options = ttk.OptionMenu(self, self.gender_option_selected, *hm.Gender)
        gender_options.grid(row=6, column=1)
        print(f'This is gender first value: {self.gender_option_selected}')

        weight_label = ttk.Label(self, text="Weight:", font=SMALL_FONT)
        weight_label.grid(row=8, column=0, padx=10, pady=10)
        weight_entry = ttk.Entry(self)
        weight_entry.insert(0, 130)  # 2TEST ERASE!!!
        weight_entry.grid(row=8, column=1)
        weight_label_unit = ttk.Label(self, text="Lb", font=SMALL_FONT)
        weight_label_unit.grid(row=8, column=2, padx=10, pady=10)

        height_label = ttk.Label(self, text="Height:", font=SMALL_FONT)
        height_label.grid(row=10, column=0, padx=10, pady=10)
        height_entry = ttk.Entry(self)
        height_entry.insert(0, 5.1)  # 2TEST ERASE!!!
        height_entry.grid(row=10, column=1)

        ethnicity_label = ttk.Label(self, text="Ethnicity:", font=SMALL_FONT)
        ethnicity_label.grid(row=12, column=0, padx=10, pady=10)
        self.ethnicity_option_selected = tk.StringVar()
        self.ethnicity_option_selected.set(hm.Ethnicity[0])  # Initial value
        ethnicity_options = ttk.OptionMenu(self, self.ethnicity_option_selected, *hm.Ethnicity)
        ethnicity_options.grid(row=12, column=1)

        skin_color_label = ttk.Label(self, text="Fitzpatrick Scale:", font=SMALL_FONT)
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
    current_ticking_value = 18000  # This depends on current timezone, may be different in other regions. Starts at 0
    ticking_value_max = 0  # initialization, actual value assigned on create_stopwatch() function
    timer_label = ""

    AbMode = 0  # start in raw intensity mode

    def __init__(self, parent, controller, ax=None):
        global data, x
        global integration_time, spectra_average
        global xmin, xmax, ymin, ymax
        global monitor_wave, monitor_index, monitor

        self.ax = ax
        self.x = x
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.data = data
        self.line = Line2D(self.x, self.data, color='red')
        self.ax.add_line(self.line)
        self.ax.set_ylim(ymin * 0.8, ymax * 1.1)
        self.ax.set_xlim(self.xmin, self.xmax)
        monitor_wave = np.median(x)

        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text=f"Session Recording", font=LARGE_FONT)
        label.pack(side='top', pady=20)

        # This frame1 packs all the labels on the first column on the UI
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side='left', anchor=tk.N)

        # This frame1 packs all the labels on the second column on the UI
        self.frame2 = tk.Frame(self)
        self.frame2.pack(side='left', anchor=tk.N)

        # This frame1 packs all the labels on the third column on the UI
        self.frame3 = tk.Frame(self)
        self.frame3.pack(side='left', anchor=tk.N)

        id_label = tk.Label(self.frame1, text="Patient ID:", font=SMALL_FONT)
        id_label.pack(side='top', pady=4)
        id_val = tk.Label(self.frame2, text="001", font=SMALL_FONT)                 # Interactive get subjID from DB
        id_val.pack(side='top', pady=4)
        filler_label = tk.Label(self.frame3, text="")
        filler_label.pack(side='top')

        # Integration time design
        duration_label = tk.Label(self.frame1, text="Integration Time", font=SMALL_FONT)
        duration_label.pack(side='top', pady=4)
        self.duration_entry = tk.Entry(self.frame2, width='7', justify='right')
        self.duration_entry.pack(side='top', pady=4, anchor=tk.N)
        seconds_label = tk.Label(self.frame3, text="Seconds", height='2', font=SMALL_FONT)
        seconds_label.pack(side='top', pady=4)
        self.duration_entry.bind('<Return>', self.validate_integration_time)

        # Amount of spectra to average design
        spec_avg_label = tk.Label(self.frame1, text='Amount of Spectra to Average', width='20', wraplength='150',
                                  font=SMALL_FONT)
        spec_avg_label.pack(side='top', pady=4)
        self.spec_avg_entry = tk.Entry(self.frame2, width='7', justify='right')
        self.spec_avg_entry.pack(side='top', pady=2)
        self.spec_avg_entry.bind('<Return>', self.validate_spec_avg)

        # Minimum wavelength label and entry field
        labelxmin = tk.Label(self.frame1, text='Minimum wavelength', font=SMALL_FONT)
        labelxmin.pack(side='top', pady=2)
        self.entryxmin = tk.Entry(self.frame2, width='7', justify='right')
        self.entryxmin.pack(side='top', pady=2)
        self.entryxmin.insert(0, xmin)                                           # AUTO INPUTS VALUE
        self.entryxmin.bind('<Return>', self.validate_xmin)

        # Maximum wavelength label and entry field
        labelxmax = tk.Label(self.frame1, text='Maximum wavelength', height='2', font=SMALL_FONT)
        labelxmax.pack(side='top', pady=2)
        self.entryxmax = tk.Entry(self.frame2, width='7', justify='right')
        self.entryxmax.pack(side='top', pady=2)
        self.entryxmax.insert(0, xmax)                                          # AUTO INPUTS VALUE
        self.entryxmax.bind('<Return>', self.validate_xmax)

        body_part_label = tk.Label(self.frame1, text="Body Location:", height='2', font=SMALL_FONT)
        body_part_label.pack(side='top', pady=4)
        self.body_part_option_selected = tk.StringVar()
        self.body_part_option_selected.set(hm.BodyParts[0])  # Initial Value
        body_part_options = ttk.OptionMenu(self.frame2, self.body_part_option_selected, *hm.BodyParts)
        body_part_options.pack(side='top', pady=4)

        btn_start_stop = ttk.Button(self.frame1, text="Start", command=lambda: start_stop_process())
        btn_start_stop.pack(side='top', pady=10)

        btn_save = ttk.Button(self.frame2, text="Save", command=lambda: save_recording())
        btn_save.pack(side='top', pady=10)

        btn_pause_resume = ttk.Button(self.frame1, text="Pause", command=lambda: pause_resume_process())
        btn_pause_resume.pack(side='top', pady=10)

        diff_patient_button = ttk.Button(self.frame2, text="Next Patient",
                                         command=lambda: controller.show_frame(LogPatient))
        diff_patient_button.pack(side='top', pady=10)

        log_out_button = tk.Button(self.frame1, text="Log out", command=lambda: controller.show_frame(LoginPage))
        log_out_button.pack(side='bottom', pady=10)

        checkbox_value = tk.IntVar()
        check_box_label = tk.Checkbutton(self.frame1, text="Interrupted session", variable=checkbox_value)
        check_box_label.pack(side='bottom', pady=10)
        # endregion

        # Disable pause while the clock is not started
        hm.disable_fields(btn_pause_resume)

        # Labels for the graph
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Counts')

        # Creates the design for the graph
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Blue line in on the graph
        monitor_index = np.searchsorted(x, monitor_wave, side='left')
        monitor = np.round(self.data[monitor_index], decimals=3)
        self.text = self.ax.text(0.9, 0.9, monitor, transform=ax.transAxes, fontsize=14)
        self.ax.axvline(x=monitor_wave, lw=2, color='blue', alpha=0.5)

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
            hm.disable_fields(body_part_options, self.duration_entry)

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
            hm.enable_fields(body_part_options, self.duration_entry)
            return

        def start_stop_process():

            if check_fields():    # no errors
                if hm.is_start_button(btn_start_stop):
                    start_process()
                else:
                    stop_process()

            return

        def start_process():

            hm.disable_fields(btn_save, log_out_button, diff_patient_button, body_part_options, self.duration_entry)
            hm.enable_fields(btn_pause_resume)
            btn_start_stop["text"] = "Stop"

            create_stopwatch()
            start_stopwatch(self.timer_label)
            return

        def stop_process():
            hm.disable_fields(btn_pause_resume)

            btn_pause_resume["text"] = "Pause"  # if stop the recording, we need to reset this button (bug)
            btn_start_stop["text"] = "Start"

            hm.enable_fields(btn_save, log_out_button, diff_patient_button, body_part_options, self.duration_entry)

            self.running = False
            self.timer_label.destroy()
            return

        # checks for any errors, prints them and returns False, otherwise no errors and returns True
        def check_fields():

            if hm.check_fields_inputs(durationEntry=self.duration_entry, bodyPartOption=self.body_part_option_selected.get()):

                self.duration_value = int(self.duration_entry.get())
                return True

            else:
                return False

        # region Stopwatch
        def create_stopwatch():
            self.timer_label = tk.Label(self.frame1, text="Welcome!", fg="black", font="Verdana 15 bold")
            self.timer_label.pack(pady=10)
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

    ############ NEW METHODS ##############
    def set_entry_config(self):
        """ This function handles new inputs on the text fields and it send values to spectrometer """

        global integration_time
        spec.integration_time_micros(integration_time)
        # write new configuration to dialog
        self.duration_entry.delete(0, "end")
        self.duration_entry.insert(0, integration_time / 1000)  # write ms, but integration_time is microseconds
        self.spec_avg_entry.delete(0, "end")
        self.spec_avg_entry.insert(0, spectra_average)  # set text in averages box

    def validate_integration_time(self, event):
        """ Update integration time and validates from 4ms to 65000 """

        global integration_time
        # typically OO spectrometers cant read faster than 4 ms
        int_time_temp = self.duration_entry.get()
        if int_time_temp.isdigit():
            if int(int_time_temp) > 65000:
                msg = "The integration time must be 65000 ms or smaller.  You set " + int_time_temp
                self.set_entry_config()
                #popupmsg(msg)
            elif int(int_time_temp) < 4:
                msg = "The integration time must be greater than 4 ms.  You set " + int_time_temp
                self.set_entry_config()
                #popupmsg(msg)
            else:
                integration_time = int(int_time_temp) * 1000  # convert ms to microseconds
                self.set_entry_config()
        else:
            msg = "Integration time must be an integer between 4 and 65000 ms.  You set " + str(int_time_temp)
            self.set_entry_config()
            #popupmsg(msg)

    def validate_spec_avg(self, event):
        ## averaging needs to be implemented here in code
        #  cseabreeze has average working, but python-seabreeze doesn't (2019)
        global spectra_average
        spectra_average = self.spec_avg_entry.get()
        if spectra_average.isdigit():
            spectra_average = int(float(spectra_average))
        else:
            msg = "spectra_average must be an integer.  You tried " + str(spectra_average) + ".  Setting value to 1."
            spectra_average = 1
            self.spec_avg_entry.delete(0, "end")
            self.spec_avg_entry.insert(0, spectra_average)  # set text in averages box
            #popupmsg(msg)

    def validate_xmax(self, event):
        """ Validates max wavelength to show in graph """

        global xmax
        xmax_temp = self.entryxmax.get()
        try:
            float(xmax_temp)
            xmax_temp = float(self.entryxmax.get())
            if xmax_temp > xmin:
                xmax = xmax_temp
                self.entryxmax.delete(0, 'end')
                self.entryxmax.insert(0, xmax)  # set text in box
                self.ax.set_xlim(xmin, xmax)
            else:
                msg = "Maximum wavelength must be larger than minimum wavelength.  You entered " + str(
                    xmax_temp) + " nm."
                self.entryxmax.delete(0, 'end')
                self.entryxmax.insert(0, xmax)  # set text in box
                #popupmsg(msg)
        except:
            self.entryxmax.delete(0, 'end')
            self.entryxmax.insert(0, xmax)  # set text in box to unchanged value

    def validate_xmin(self, event):
        """ Validates min wavelength to show in graph """

        global xmin
        xmin_temp = self.entryxmin.get()
        try:
            float(xmin_temp)
            xmin_temp = float(self.entryxmin.get())
            if xmin_temp < xmax:
                xmin = xmin_temp
                self.entryxmin.delete(0, 'end')
                self.entryxmin.insert(0, xmin)  # set text in box
                self.ax.set_xlim(xmin, xmax)
            else:
                msg = "Minimum wavelength must be smaller than maximum wavelength.  You entered " + str(
                    xmin_temp) + " nm."
                self.entryxmin.delete(0, 'end')
                self.entryxmin.insert(0, xmin)  # set text in box
                #popupmsg(msg)
        except:
            self.entryxmin.delete(0, 'end')
            self.entryxmin.insert(0, xmin)  # set text in box to unchanged value

    def update(self, data):
        """ This function manages the update of the
        spectral data in the graph. It issues a read request to the spectrometer,
        then conditionally processes the received data """

        self.data = spec.intensities()

        self.data = np.array(self.data, dtype=float)
        self.line.set_data(self.x, self.data)
        monitor = np.round(self.data[monitor_index], decimals=3)
        self.text.set_text(monitor)
        return self.line,


fig, ax = plt.subplots()
app = Controller(ax)
ani = animation.FuncAnimation(fig, app.frames[DataRecording].update, interval=10, blit=False)
app.mainloop()
