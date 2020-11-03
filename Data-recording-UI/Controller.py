import seatease.spectrometers as s  # Emulator to test w/o spectrometer

from LoginPage import *
from SignUp import *
from ResetPW import *
from LogPatient import *

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


        #region Frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary of class names, frames (Ex: HomePage, actual frame)
        self.frames = {}
        self.frames["LoginPage"] = LoginPage(container, self)
        self.frames["LogPatient"] = LogPatient(container, self)
        self.frames["DataRecording"] = DataRecording(container, self, ax)
        self.frames["SignUp"] = SignUp(container, self)
        self.frames["ResetPW"] = ResetPW(container, self)

        for frame in self.frames:
            self.frames[frame].grid(row=0, column=0, sticky="nsew")

        # Starting page
        self.show_login_frame()
        # endregion

    #region Show frames functions
    def show_login_frame(self):
        frame = self.frames["LoginPage"]
        frame.tkraise()


    def show_patientLog_frame(self):
        frame = self.frames["LogPatient"]
        frame.tkraise()

    def show_dataRecording_frame(self):
        frame = self.frames["DataRecording"]
        frame.tkraise()

    def show_signUp_frame(self):
        frame = self.frames["SignUp"]
        frame.tkraise()

    def show_resetPW_frame(self):
        frame = self.frames["ResetPW"]
        frame.tkraise()
    #endregion

class DataRecording(tk.Frame):
    body_part_option_selected = ""
    duration_value = 0

    # stopwatch
    running = False
    current_ticking_value = 18000  # This depends on current timezone, may be different in other regions. Starts at 0
    ticking_value_max = 0  # initialization, actual value assigned on create_stopwatch() function
    timer_label = ""

    AbMode = 0  # start in raw intensity mode

    def __init__(self, parent, controller, ax):
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
                                         command=lambda: controller.show_frame("LogPatient"))
        diff_patient_button.pack(side='top', pady=10)

        log_out_button = tk.Button(self.frame1, text="Log out", command=lambda: controller.show_login_frame())
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
                print("Normal session")

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

            if hm.check_fields_inputs(durationEntry=self.duration_entry,
                                      bodyPartOption=self.body_part_option_selected.get()):

                self.duration_value = int(self.duration_entry.get())
                return True

            else:
                return False

        # region Stopwatch
        def create_stopwatch():
            self.timer_label = tk.Label(self.frame1, text="Stopwatch!", fg="black", font="Verdana 15 bold")
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

    #region Graph and connection to Pi
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
    #endregion

fig, ax = plt.subplots()
app = Controller(ax)
ani = animation.FuncAnimation(fig, app.frames["DataRecording"].update, interval=10, blit=False)
app.mainloop()
