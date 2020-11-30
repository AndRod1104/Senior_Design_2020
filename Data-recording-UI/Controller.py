import seatease.spectrometers as s  # Emulator to test w/o spectrometer
# import seabreeze.spectrometers as s

from datetime import datetime
from tkinter.messagebox import showerror

import matplotlib
import numpy as np

from LogPatient import *
from LoginPage import *
from ResetPW import *
from SignUp import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

from azure.storage.blob import BlobClient
import csv

matplotlib.use("TkAgg")
style.use("ggplot")

dev_list = s.list_devices()
spec = s.Spectrometer(dev_list[0])  # Assign detected spectrometer to variable spec
integration_time = 20000  # 20 ms, set default integration time to a reasonable value
spec.integration_time_micros(integration_time)

x = spec.wavelengths()
data = spec.intensities()
xmin = np.around(min(x), decimals=2)
xmax = np.around(max(x), decimals=2)
ymin = np.around(min(data), decimals=2)
ymax = np.around(max(data), decimals=2)
# minIntTime = spec.minimum_integration_time_micros


class Controller(tk.Tk):
    def __init__(self, ax, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Data Recording")

        self.geometry("1000x700")

        # region Frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary of class names, frames (Ex: HomePage, actual frame)
        self.frames = {"LoginPage": LoginPage(container, self),
                       "LogPatient": LogPatient(container, self),
                       "DataRecording": DataRecording(container, self, ax),
                       "SignUp": SignUp(container, self),
                       "ResetPW": ResetPW(container, self)}

        for frame in self.frames:
            self.frames[frame].grid(row=0, column=0, sticky="nsew")

        # Starting page
        self.show_login_frame()
        # endregion

    # When called, passes the frame or page to be showed on windows
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
    # endregion


class DataRecording(tk.Frame):
    body_part_option_selected = ""
    duration_value = 0.0
    session_interrupt = -1

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

        # ID design
        id_label = tk.Label(self.frame1, text="Patient ID:", font=SMALL_FONT)
        id_label.pack(side='top', pady=4)
        id_val = tk.Label(self.frame2, text=LogPatient.patient_id, font=SMALL_FONT)
        id_val.pack(side='top', pady=4)
        filler_label = tk.Label(self.frame3, text="")
        filler_label.pack(side='top')

        # BMI design
        bmi_label = tk.Label(self.frame1, text="BMI:", font=SMALL_FONT)
        bmi_label.pack(side='top', pady=4)
        bmi_val = tk.Label(self.frame2, text="auto", font=SMALL_FONT)
        bmi_val.pack(side='top', pady=4)
        filler_label = tk.Label(self.frame3, text="")
        filler_label.pack(side='top', pady=6)

        # Integration time design
        duration_label = tk.Label(self.frame1, text="Integration Time", font=SMALL_FONT)
        duration_label.pack(side='top', pady=4)
        self.duration_entry = tk.Entry(self.frame2, width='7', justify='right')
        self.duration_entry.pack(side='top', pady=4, anchor=tk.N)
        seconds_label = tk.Label(self.frame3, text="Seconds", height='2', font=SMALL_FONT)
        seconds_label.pack(side='top', pady=4)
        self.duration_entry.bind('<Return>', self.validate_integration_time)

        # Number of spectra design
        num_spectra_label = tk.Label(self.frame1, text="Number of Spectra Returned", font=SMALL_FONT)
        num_spectra_label.pack(side='top', pady=4)
        num_spectra_entry = tk.Entry(self.frame2, width='7', justify='right')
        num_spectra_entry.pack(side='top', pady=10)

        # Amount of spectra to average design
        spec_avg_label = tk.Label(self.frame1, text='Amount of Spectra to Average ', width='20', wraplength='150',
                                  font=SMALL_FONT)
        spec_avg_label.pack(side='top', pady=4)
        self.spec_avg_entry = tk.Entry(self.frame2, width='7', justify='right')
        self.spec_avg_entry.pack(side='top', pady=20)
        self.spec_avg_entry.bind('<Return>', self.validate_spec_avg)

        # Minimum wavelength label and entry field
        xmin_label = tk.Label(self.frame1, text='Minimum wavelength', font=SMALL_FONT)
        xmin_label.pack(side='top', pady=2)
        self.xmin_entry = tk.Entry(self.frame2, width='7', justify='right')
        self.xmin_entry.pack(side='top', pady=15)
        self.xmin_entry.insert(0, xmin)  # AUTO INPUTS VALUE
        self.xmin_entry.bind('<Return>', self.validate_xmin)

        # Maximum wavelength label and entry field
        xmax_label = tk.Label(self.frame1, text='Maximum wavelength', height='2', font=SMALL_FONT)
        xmax_label.pack(side='top', pady=2)
        self.entryxmax = tk.Entry(self.frame2, width='7', justify='right')
        self.entryxmax.pack(side='top', pady=5)
        self.entryxmax.insert(0, xmax)  # AUTO INPUTS VALUE
        self.entryxmax.bind('<Return>', self.validate_xmax)

        body_part_label = tk.Label(self.frame1, text="Body Location:", height='2', font=SMALL_FONT)
        body_part_label.pack(side='top', pady=4)
        self.body_part_option_selected = tk.StringVar()
        self.body_part_option_selected.set(hm.BodyParts[0])  # Initial Value
        body_part_options = ttk.OptionMenu(self.frame2, self.body_part_option_selected, *hm.BodyParts)
        body_part_options.pack(side='top', pady=15)

        btn_start_stop = ttk.Button(self.frame1, text="Start", command=lambda: start_stop_process())
        btn_start_stop.pack(side='top', pady=10)

        btn_save = ttk.Button(self.frame2, text="Save", command=lambda: save_recording())
        btn_save.pack(side='top', pady=10)

        btn_pause_resume = ttk.Button(self.frame1, text="Pause", command=lambda: pause_resume_process())
        btn_pause_resume.pack(side='top', pady=10)

        diff_patient_button = ttk.Button(self.frame2, text="Next Patient",
                                         command=lambda: controller.show_patientLog_frame())
        diff_patient_button.pack(side='top', pady=10)

        quit_button = tk.Button(self.frame1, text="Quit")
        quit_button.pack(side='bottom', pady=10)
        quit_button.bind('<ButtonRelease-1>', self.quit_app)

        button_reset_y = tk.Button(self.frame1, text='Reset Y axis scale')
        button_reset_y.pack(side='bottom', pady=10)
        button_reset_y.bind('<ButtonRelease-1>', self.reset_y)

        log_out_button = tk.Button(self.frame1, text="Log out", command=lambda: controller.show_login_frame())
        log_out_button.pack(side='bottom', pady=10)

        check_box_label = tk.Checkbutton(self.frame1, text="Interrupted session", command=lambda: box_toggled())
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

        monitor_index = np.searchsorted(x, monitor_wave, side='left')
        monitor = np.round(self.data[monitor_index], decimals=3)
        self.text = self.ax.text(0.9, 0.9, monitor, transform=ax.transAxes, fontsize=14)
        #self.ax.axvline(x=monitor_wave, lw=2, color='blue', alpha=0.5)                 # Blue line in on the graph

        # This method changes a value when checkBox is checked meaning a session was interrupted
        def box_toggled():
            self.session_interrupt *= -1

        def save_csv_to_cloud(file_path):
            """ Upload csv file to Azure """
            blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=rawdatasp"
                                                              ";AccountKey"
                                                              "=ERlbwQPEtJizmGSbHVUZbC7DxB3hECChkICuiIRvCraOhfN9v"
                                                              "fna9aao3+anNZG3VfhpifZhSV71euAVwwURvQ==;"
                                                              "EndpointSuffix=core.windows.net",
                                                     container_name="blobcont",
                                                     blob_name=file_path)
            with open(file_path, "rb") as up:
                blob.upload_blob(up)

        def save_recording():
            if self.session_interrupt == -1:
                print("Normal session")
                file_name = str(LogPatient.patient_id) + "_" + str(self.body_part_option_selected.get()) + ".csv"
                print(file_name)
                save_csv_to_cloud(file_name)
            else:
                # TODO: Message box will probably have to be a customized pop-up. You can't add an entry text field here
                result = tk.messagebox.askyesno("Interrupted session", "You have marked this session as interrupted.\n"
                                                                       "Data will be saved in different database")
                if result:  # If user confirmed session was interrupted and he/she agrees with message
                    # TODO: Data in different database
                    print("Result:")
                    print(result)

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

            # TODO
            # Connect to save again values with different body part in DB
            print(self.duration_value)
            print(self.body_part_option_selected.get())

            return

        def pause_process():
            # TODO
            # Do we want to change the duration and body part once user pauses? *** BUG ***
            btn_pause_resume["text"] = "Resume"
            self.running = False
            hm.enable_fields(body_part_options, self.duration_entry)
            return

        def start_stop_process():

            if check_fields():  # no errors
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

                self.duration_value = float(self.duration_entry.get())
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
                if self.running and self.current_ticking_value <= self.ticking_value_max:  # if from 0 to limit
                    # To manage the initial delay.
                    if self.current_ticking_value == 18000:
                        display = "Starting..."
                    else:
                        tt = datetime.fromtimestamp(self.current_ticking_value)
                        string = tt.strftime("%H:%M:%S")
                        display = string

                    timer_label['text'] = display  # Or label.config(text=display)

                    timer_label.after(1000, count)
                    self.current_ticking_value += 1

                elif not self.running and self.current_ticking_value <= self.ticking_value_max:  # if paused
                    timer_label['text'] = "Paused..."

                else:
                    timer_label['text'] = "Finished!"
                    hm.disable_fields(btn_pause_resume)
                    btn_pause_resume["text"] = "Pause"

            # Triggering the start of the counter.
            count()
        # endregion

    def quit_app(root, event):
        """ Quits the program """
        root.destroy()
        exit()

    def reset_y(self, event):
        data = spec.intensities(correct_dark_counts=True, correct_nonlinearity=False)
        ymin = min(data)
        ymax = max(data)
        ax.set_ylim(ymin * 0.0, ymax * 2.1)

    # region Graph and connection to Pi
    def set_entry_config(self):
        """ This function handles new inputs on the text fields and it send values to spectrometer """
        global integration_time  # , spectra_average
        spec.integration_time_micros(integration_time)
        # spec.scans_to_average(spectra_average)
        # write new configuration to dialog
        self.duration_entry.delete(0, "end")
        self.duration_entry.insert(0, integration_time / 1000)  # write ms, but integration_time is microseconds

    def validate_integration_time(self, event):
        """ Update integration time and validates from 4ms to 65000 """
        global integration_time
        # typically OO spectrometers cant read faster than 4 ms
        int_time_temp = self.duration_entry.get()

        if int_time_temp.isdigit():
            if int(int_time_temp) > 65000:
                msg = "The integration time must be 65000 ms or smaller.  You set " + int_time_temp
                self.set_entry_config()
                # popupmsg(msg)
            elif int(int_time_temp) < 4:
                msg = "The integration time must be greater than 4 ms.  You set " + int_time_temp
                self.set_entry_config()
                # popupmsg(msg)
            else:
                integration_time = int(int_time_temp) * 1000  # convert ms to microseconds
                self.set_entry_config()
        else:
            msg = "Integration time must be an integer between 4 and 65000 ms.  You set " + str(int_time_temp)
            self.set_entry_config()
            # popupmsg(msg)

    def validate_spec_avg(self, event):
        ## averaging needs to be implemented here in code
        #  cseabreeze has average working, but python-seabreeze doesn't (2019)
        global spectra_average
        spectra_average = self.spec_avg_entry.get()
        if spectra_average.isdigit():

            # spectra_average = int(spectra_average)
            spec.scans_to_average(int(spectra_average))

        else:
            msg = "spectra_average must be an integer.  You tried " + str(spectra_average) + ".  Setting value to 1."
            spectra_average = 1
            self.spec_avg_entry.delete(0, "end")
            self.spec_avg_entry.insert(0, spectra_average)

            # self.spec_avg_entry.delete(0, "end")
            # self.insert(0, spectra_average)
            # popupmsg(msg)

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
                # popupmsg(msg)
        except:
            self.entryxmax.delete(0, 'end')
            self.entryxmax.insert(0, xmax)  # set text in box to unchanged value

    def validate_xmin(self, event):
        """ Validates min wavelength to show in graph """
        global xmin
        xmin_temp = self.xmin_entry.get()

        try:
            float(xmin_temp)
            xmin_temp = float(self.xmin_entry.get())
            if xmin_temp < xmax:
                xmin = xmin_temp
                self.xmin_entry.delete(0, 'end')
                self.xmin_entry.insert(0, xmin)  # set text in box
                self.ax.set_xlim(xmin, xmax)
            else:
                msg = "Minimum wavelength must be smaller than maximum wavelength.  You entered " + str(
                    xmin_temp) + " nm."
                self.xmin_entry.delete(0, 'end')
                self.xmin_entry.insert(0, xmin)  # set text in box
                # popupmsg(msg)
        except:
            self.xmin_entry.delete(0, 'end')
            self.xmin_entry.insert(0, xmin)  # set text in box to unchanged value

    def update(self, data):
        """ This function manages the update of the
        spectral data in the graph. It issues a read request to the spectrometer,
        then conditionally processes the received data """
        file_name = str(LogPatient.patient_id) + "_" + str(self.body_part_option_selected.get()) + ".csv"
        with open(file_name, "w", newline='') as towrite:
            lineWriter = csv.writer(towrite, quotechar='|', delimiter='\n', quoting=csv.QUOTE_NONE)
            lineWriter.writerow(self.data)

        self.data = spec.intensities()
        self.data = np.array(self.data, dtype=float)
        self.line.set_data(self.x, self.data)
        monitor = np.round(self.data[monitor_index], decimals=3)
        self.text.set_text(monitor)
        return self.line,
    # endregion


fig, ax = plt.subplots()
app = Controller(ax)
ani = animation.FuncAnimation(fig, app.frames["DataRecording"].update, interval=10, blit=False)
app.mainloop()
