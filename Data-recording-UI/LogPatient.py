import tkinter as tk
from tkinter import ttk

import Connection as conn
import HelperMethods as hm


class LogPatient(tk.Frame):
    # values for all entries
    bmi = 0.0
    age_value = 0
    weight_value = 0
    height_value = 0
    skin_color_type = ""
    ethnicity_option_selected = ""
    gender_option_selected = ""
    duration_value = 0
    patient_id = 1
    id_list = conn.multi_select('subject_id', conn.subject)     # Initialize list with all subjects' ids

    # Check for empty subject table and if not empty get the patient's id to display
    if id_list != []:
        patient_id = id_list[-1][0] + 1

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # region Design
        label = ttk.Label(self, text="Patient's Info", font=hm.LARGE_FONT)
        label.grid(row=0, column=1, padx=0, pady=10)

        id_label = ttk.Label(self, text="Patient ID:", font=hm.SMALL_FONT)
        id_label.grid(row=2, column=0, padx=0, pady=10)
        id_val = ttk.Label(self, text=self.patient_id, font=hm.SMALL_FONT)
        id_val.grid(row=2, column=1)

        age_label = ttk.Label(self, text="Age:", font=hm.SMALL_FONT)
        age_label.grid(row=4, column=0, padx=10, pady=10)
        age_entry = ttk.Entry(self)
        age_entry.insert(0, 30)  # 2TEST ERASE!!!
        age_entry.grid(row=4, column=1)

        gender_label = ttk.Label(self, text="Sex:", font=hm.SMALL_FONT)
        gender_label.grid(row=6, column=0, padx=10, pady=10)
        self.gender_option_selected = tk.StringVar()
        self.gender_option_selected.set(hm.Gender[0])
        gender_options = ttk.OptionMenu(self, self.gender_option_selected, *hm.Gender)
        gender_options.grid(row=6, column=1)

        weight_label = ttk.Label(self, text="Weight:", font=hm.SMALL_FONT)
        weight_label.grid(row=8, column=0, padx=10, pady=10)
        weight_entry = ttk.Entry(self)
        weight_entry.insert(0, 130)  # 2TEST ERASE!!!
        weight_entry.grid(row=8, column=1)
        weight_label_unit = ttk.Label(self, text="Lb", font=hm.SMALL_FONT)
        weight_label_unit.grid(row=8, column=2, padx=10, pady=10)

        height_label = ttk.Label(self, text="Height:", font=hm.SMALL_FONT)
        height_label.grid(row=10, column=0, padx=10, pady=10)
        height_entry = ttk.Entry(self)
        height_entry.insert(0, 5.1)  # 2TEST ERASE!!!
        height_entry.grid(row=10, column=1)

        ethnicity_label = ttk.Label(self, text="Ethnicity:", font=hm.SMALL_FONT)
        ethnicity_label.grid(row=12, column=0, padx=10, pady=10)
        self.ethnicity_option_selected = tk.StringVar()
        self.ethnicity_option_selected.set(hm.Ethnicity[0])
        ethnicity_options = ttk.OptionMenu(self, self.ethnicity_option_selected, *hm.Ethnicity)
        ethnicity_options.grid(row=12, column=1)

        skin_color_label = ttk.Label(self, text="Fitzpatrick Scale:", font=hm.SMALL_FONT)
        skin_color_label.grid(row=14, column=0, padx=10, pady=10)
        self.skin_color_type = tk.StringVar()
        self.skin_color_type.set(hm.SkinColor[0])
        skin_color_entry = ttk.OptionMenu(self, self.skin_color_type, *hm.SkinColor)
        skin_color_entry.grid(row=14, column=1)

        save_button = ttk.Button(self, text="Save and Continue", command=lambda: save_and_go_to_recording_page())
        save_button.grid(row=26, column=1, padx=10, pady=30)
        # endregion

        def update_bmi(height, weight, CONSTANT = 703.0):
            """ Method to calculate BMI """
            height = height * 12.0
            if weight > 0.0 and height > 0.0:
                bmi = (weight / (height ** 2)) * CONSTANT
                return round(bmi, 1)
            else:
                return 0.0

        def save_and_go_to_recording_page():
            """ Gets data input in the fields and saves it to subject table in database. This happens only
            if all fields pass validation in get_value() method """
            if get_values():
                self.bmi = update_bmi(self.height_value, float(self.weight_value))
                # Save patient to database in azure
                conn.insert(conn.subject, hm.current_researcher, self.age_value, self.weight_value,
                            self.height_value, self.bmi, self.ethnicity_option_selected.get(),
                            self.skin_color_type.get(), self.gender_option_selected.get())
                # move to recording page
                controller.show_dataRecording_frame()

            return

        # get_values stores all values from fields into variables and returns any errors found when trying to
        # convert each field into its respective type
        def get_values():
            """ Validates all fields in LogPatient frame for correct input """
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
