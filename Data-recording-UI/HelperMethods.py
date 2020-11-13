import re
from tkinter.messagebox import showerror

# region Min-Max values
MIN_AGE = 17
MAX_AGE = 100

MIN_WEIGHT = 0
MAX_WEIGHT = 500

# For now the concept of height is 5'10" = 5.10. Another example 6'01" = 6.01
# ************************** CAUTION WITH 5.1 AND 5.01 may have to think of a different way ****************************
MIN_HEIGHT = 1.00
MAX_HEIGHT = 8.00

# Duration is in seconds
MIN_DURATION = 1
MAX_DURATION = 120  # 2 min

# Keeps track of the researcher logged in
current_researcher = 0

DEFAULT_SCROLLDOWNMENU_OPTION = "Select an option"

Ethnicity = ["Select an option",
             "American Indian",
             "Alaska Native",
             "Native Hawaiian or Other Pacific Islander",
             "Asian",
             "African American",
             "White",
             "Hispanic",
             "Latino",
             "Caribbean"]

Gender = ["Select an option",
          "Female",
          "Male",
          "Neutral"]

BodyParts = ["Select an option",
             "Head",
             "Arm",
             "Leg",
             "Chest"]

SkinColor = ["Select an option",
             "Type I",
             "Type II",
             "Type III",
             "Type IV",
             "Type V",
             "Type VI"]
# endregion


def isAgeValid(age):
    return MIN_AGE < age < MAX_AGE


def isWeightValid(weight):
    return MIN_WEIGHT < weight < MAX_WEIGHT


def isScrollDownMenuWrong(option):
    return option == DEFAULT_SCROLLDOWNMENU_OPTION


def isEmpty(field):
    return len(field) == 0


def isHeightValid(height):
    return MIN_HEIGHT < height < MAX_HEIGHT


def disable_fields(*fields):
    for field in fields:
        field["state"] = "disabled"


def enable_fields(*fields):
    for field in fields:
        field["state"] = "normal"


def isDurationValid(duration):
    return MIN_DURATION < duration < MAX_DURATION


def correct_email_format(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    return False


def is_start_button(button):
    return button["text"] == "Start"


def is_pause_button(button):
    return button["text"] == "Pause"


# checks if any errors were built, printing them and returning false. If no errors, then returns true
def check_fields_inputs(ageEntry=None, heightEntry=None, weightEntry=None, durationEntry=None, ethnicityOption=None,
                        genderOption=None, skinColorOption=None, bodyPartOption=None, emailEntry=None,
                        passwordEntry=None, reEnterPasswordEntry=None, checkEmailFormat=None, fNameEntry=None,
                        middleInitialEntry=None, lNameEntry=None, instEntry=None):

    error_message = ""

    if ageEntry is not None:
        try:
            ageValue = int(ageEntry.get())
            if not isAgeValid(ageValue):
                error_message += "\u2022    " + "Number entered for age is invalid.\n"

        except ValueError:
            error_message += "\u2022    " + "Value entered for age is not a number.\n"

    if heightEntry is not None:
        try:
            heightValue = float(heightEntry.get())

            if not isHeightValid(heightValue):
                error_message += "\u2022    " + "Number entered for height is invalid.\n"

        except ValueError:
            error_message += "\u2022    " + "Value entered for height is not a number.\n"

    if weightEntry is not None:
        try:
            weightValue = int(weightEntry.get())

            if not isWeightValid(weightValue):
                error_message += "\u2022    " + "Number entered for weight is invalid.\n"

        except ValueError:
            error_message += "\u2022    " + "Value entered for weight is not a number.\n"

    if durationEntry is not None:
        try:
            durationValue = float(durationEntry.get())

            # This was moved here, because there is no need to print this error if above already failed
            if not isDurationValid(durationValue):
                error_message += "\u2022    " + "Value entered for duration is invalid.\n"

        except ValueError:
            error_message += "\u2022    " + "Value entered for duration is not a number.\n"

    if ethnicityOption is not None:
        if isScrollDownMenuWrong(ethnicityOption):
            error_message += "\u2022    " + "Please select an option for ethnicity.\n"

    if genderOption is not None:
        if isScrollDownMenuWrong(genderOption):
            error_message += "\u2022    " + "Please select an option for gender.\n"

    if skinColorOption is not None:
        if isScrollDownMenuWrong(skinColorOption):
            error_message += "\u2022    " + "Please select an option for skin color.\n"

    if bodyPartOption is not None:
        if isScrollDownMenuWrong(bodyPartOption):
            error_message += "\u2022    " + "Please select an option for body part.\n"

    if emailEntry is not None:
        if isEmpty(emailEntry.get()):
            error_message += "\u2022    " + "Please enter an email.\n"
        else:
            if checkEmailFormat is not None:
                if not correct_email_format(checkEmailFormat):
                    error_message += "\u2022    Incorrect format for email.\n"

    if passwordEntry is not None:
        if isEmpty(passwordEntry.get()):
            error_message += "\u2022    " + "Please enter a password.\n"

    # this is from signUp page in specific!
    if reEnterPasswordEntry is not None:
        if isEmpty(reEnterPasswordEntry.get()):
            error_message += "\u2022    " + "Please re-enter a password.\n"

    if passwordEntry is not None and reEnterPasswordEntry is not None:
        if not passwords_match(passwordEntry.get(), reEnterPasswordEntry.get()):
            error_message += "\u2022    " + "Passwords do not match.\n"

    if fNameEntry is not None:
        if isEmpty(fNameEntry.get()):
            error_message += "\u2022    " + "Please fill out the First Name Field\n"
    if middleInitialEntry is not None:
        if isEmpty(middleInitialEntry.get()):
            error_message += "\u2022    " + "Please fill out the Middle Initial Field\n"
    if lNameEntry is not None:
        if isEmpty(lNameEntry.get()):
            error_message += "\u2022    " + "Please fill out the Last Name Field\n"
    if emailEntry is not None:
        if isEmpty(emailEntry.get()):
            error_message += "\u2022    " + "Please fill out the Email Field\n"
    if instEntry is not None:
        if isEmpty(instEntry.get()):
            error_message += "\u2022    " + "Please fill out the Institution Field\n"

    # final check for errors
    if isEmpty(error_message):
        return True
    else:
        showerror("Error", "Please fix the following errors:\n" + error_message)
        return False


def passwords_match(password, re_password):
    if password == re_password:
        return True
    return False