# Access Tkinter modules
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import Calendar

# Access regular expressions
import re
import json
import requests
# TESTING!!!
# Access local
import os

################################################# HTTP requests communicating to the backend server
# Make a GET request to the /signup endpoint of the web app, and return the response data
def get_data():
    response = requests.get('http://localhost:8000/signup')
    if response.status_code == 200:
        return response  # a list of tuple
    else:
        print('Request failed with status code:', response.status_code)

# Make a post request to the backend api at the signup endpoint and pass the user input data as json data
def send_request():
    # Replace with the actual URL of your Flask endpoint
    url = 'http://localhost:8000/signup'
    data = {
        'name': name_text,
        'email': email_text,
        'password_hashed': password_text
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for any errors
        # print(response.json())  # Print the response data
    except requests.exceptions.RequestException as e:
        print('Error:', e)


# Create a landing screen named main_menu
def main_menu():
    global main_window
    main_window = Tk()
    # Set screen size, title, heading
    main_window.geometry("390x844")
    main_window.title("Subscription Manager")
    main_window.configure(bg="#323232")  # Set background color
    label1 = Label(main_window, text="Welcome \U0001F44B",
                   font="Helvetica 28 bold", fg="white")
    label1.configure(bg="#323232")  # Set background color of label
    label1.pack(fill=X, pady=40)
    # Create a log in button and a sign up button
    login_btn = Button(main_window, text="Log In",
                       width="26", height="2", command=log_in)
    login_btn.pack(pady=20)
    signup_btn = Button(main_window, text="Sign up",
                        width="26", height="2", command=sign_up)
    signup_btn.pack(pady=20)
    main_window.mainloop()


# Create a sign up screen
def sign_up():
    # Make variables global so that they are retrievable in other functions
    global name
    global email
    global password
    global name_entry
    global email_entry
    global password_entry
    global sign_up_window

    # Set screen position, size, title
    sign_up_window = Toplevel(main_window)
    sign_up_window.geometry("390x844")
    sign_up_window.title('Sign up')
    sign_up_window.configure(bg="#323232")  # Set background color

    # Create three variables named name, email, password
    name = StringVar()
    email = StringVar()
    password = StringVar()

    # Heading
    label2 = Label(sign_up_window, text="Sign up \U0001F511",
                   font='Helvetica 28 bold', fg='white')
    label2.pack(fill=X, pady=40)
    label2.configure(bg='#323232')

    # Name input
    user_info_panel = Frame(sign_up_window)
    user_info_panel.configure(bg="#323232")  # Set background color of label
    user_info_panel.pack(pady=30)
    name_label = Label(user_info_panel, text="Name: ",
                       bg="#323232", fg="white")
    name_label.grid(row=0, column=0)
    name_entry = Entry(user_info_panel, textvariable=name)
    name_entry.grid(row=0, column=1)

    # Spacing between input fields
    Label(user_info_panel, text="", bg="#323232", fg="white").grid(row=1)

    # Email input
    email_label = Label(user_info_panel, text="Email: ",
                        bg="#323232", fg="white")
    email_label.grid(row=2, column=0)
    email_entry = Entry(user_info_panel, textvariable=email)
    email_entry.grid(row=2, column=1)

    # Spacing between input fields
    Label(user_info_panel, text="", bg="#323232", fg="white").grid(row=3)

    # Password input
    password_label = Label(
        user_info_panel, text="Password: ", bg="#323232", fg="white")
    password_label.grid(row=4, column=0)
    password_entry = Entry(user_info_panel, textvariable=password, show='*')
    password_entry.grid(row=4, column=1)
    # Create a sign up button
    sign_up_btn = Button(sign_up_window, text="Sign up",
                         width="26", height="2", command=register)
    sign_up_btn.pack()



# Register and record the new account information into the database
def register():
    global name_text
    global email_text
    global password_text

    # TESTING!!!
    # Set registered as a boolean operator to False
    # Set "not registered" as default
    registered = False

    # Get the name, email, and password data from input field
    name_text = name.get()
    email_text = email.get()
    password_text = password.get()

    curr_users_data = get_data()
    existing_emails = []
    for row in curr_users_data:
        existing_emails.append(row[2])
    if (email_text in existing_emails):
        registered = True

    # Define a valid email pattern using regular expressions
    valid_email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # If some information is missing, alert users
    if name_text == "" or email_text == "" or password_text == "":
        # file.close()
        sign_up_missing_info_window = Toplevel(sign_up_window)
        sign_up_missing_info_window.geometry('300x300')
        sign_up_missing_info_window.title('Missing info')
        sign_up_missing_info_window.configure(
            bg="#323232")  # Set background color
        Label(sign_up_missing_info_window, text="Something is missing \U0001F494",
              font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_missing_info_window, text="Try again", width="26",
                               height="2", command=lambda: sign_up_missing_info_window.destroy())
        try_again_btn.pack(pady=20)
    # Check if email input is valid
    elif not re.match(valid_email_pattern, email_text):
        # file.close()
        sign_up_invalid_email_window = Toplevel(sign_up_window)
        sign_up_invalid_email_window.geometry('300x300')
        sign_up_invalid_email_window.title('Invalid Email')
        sign_up_invalid_email_window.configure(
            bg="#323232")  # Set background color
        Label(sign_up_invalid_email_window, text="Invalid email \U0001F92F",
              font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_invalid_email_window, text="Try again", width="26",
                               height="2", command=lambda: sign_up_invalid_email_window.destroy())
        try_again_btn.pack(pady=20)
    # If email has already registered, prompt an alert
    elif registered:
        # file.close()
        sign_up_fail_window = Toplevel(sign_up_window)
        sign_up_fail_window.geometry('300x300')
        sign_up_fail_window.title('Alert')
        sign_up_fail_window.configure(bg="#323232")  # Set background color
        Label(sign_up_fail_window, text="Email already exists \U0001F62C",
              font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_fail_window, text="Try again", width="26",
                               height="2", command=lambda: sign_up_fail_window.destroy())
        try_again_btn.pack(pady=20)
    # If not registered, write user info to the file
    else:
        # file.write('Name: ' + name_text + " Email: " +
        #            email_text + " Password: " + password_text + "\n")
        # Close the file
        # file.close()

        # send the post request to the backend server
        send_request()
        # Clear out the entry box
        name_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)
        # Prompt a pop up message window that indicates the account was successfully created
        sign_up_success_window = Toplevel(sign_up_window)
        sign_up_success_window.geometry('300x300')
        sign_up_success_window.title('Success')
        sign_up_success_window.configure(bg="#323232")  # Set background color
        Label(sign_up_success_window, text="You are all set \U0001F973",
              font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Confirm button to close the pop up message window
        confirm_btn = Button(sign_up_success_window, text="Confirm", width="26",
                             height="2", command=lambda: sign_up_success_window.destroy())
        confirm_btn.pack(pady=20)


# Create a log in screen
def log_in():
    # Make variables global
    global email_verify
    global email_verify_entry
    global password_verify
    global password_verify_entry
    global log_in_window

    # Set screen position, size, title, color
    log_in_window = Toplevel(main_window)
    log_in_window.geometry("390x844")
    log_in_window.title('Log in')
    log_in_window.configure(bg='#323232')

    # Heading
    label3 = Label(log_in_window, text="Log in \U0001F512",
                   font='Helvetica 28 bold', bg="#323232", fg="white")
    label3.pack(fill=X, pady=40)

    log_in_panel = Frame(log_in_window)
    log_in_panel.configure(bg='#323232')
    log_in_panel.pack(pady=30)

    email_verify = StringVar()
    password_verify = StringVar()

    # Email input
    email_label = Label(log_in_panel, text="Email: ", bg="#323232", fg="white")
    email_label.grid(row=0, column=0)
    email_verify_entry = Entry(log_in_panel, textvariable=email_verify)
    email_verify_entry.grid(row=0, column=1)

    # Spacing between input fields
    Label(log_in_panel, text="", bg="#323232", fg="white").grid(row=1)

    # Password input
    password_label = Label(
        log_in_panel, text="Password: ", bg="#323232", fg="white")
    password_label.grid(row=2, column=0)
    password_verify_entry = Entry(
        log_in_panel, textvariable=password_verify, show="*")
    password_verify_entry.grid(row=2, column=1)

    # Log in button
    login_btn = Button(log_in_window, text="Log in",
                       width="26", height="2", command=login_verify)
    login_btn.pack(pady=20)


# Verify email and password on login screen
def login_verify():

    # TESTING!!!
    global email_text1

    email_text1 = email_verify.get()
    password_text1 = password_verify.get()

    # TESTING!!!
    # Loop through each line in the file, and check if the email and password entered match the records in the database
    # Set login as False by default
    login = False
    for line in open('gui/credentials.txt', 'r').readlines():
        login_info = line.split()
        # If the email and password entered match the records in the database, set login to True
        if email_text1 == login_info[3] and password_text1 == login_info[5]:
            login = True
            break

    # When the email and password are correct
    if login:
        homepage()
    # When the email and/or password are incorrect
    # Prompt an error message
    else:
        log_in_fail_window = Toplevel(log_in_window)
        log_in_fail_window.geometry('300x300')
        log_in_fail_window.title('Oops')
        log_in_fail_window.configure(bg="#323232")  # Set background color
        Label(log_in_fail_window, text="Incorrect email or password \U0001F926",
              font='Helvetica 20 bold', bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(log_in_fail_window, text="Try again", width="26",
                               height="2", command=lambda: log_in_fail_window.destroy())
        try_again_btn.pack(pady=20)


# Create a homepage
def homepage():

<<<<<<< Updated upstream

main_menu()
=======
    selected_subscription_name = StringVar()
    cost_entry = StringVar()

    # Set screen position, size, title
    homepage_window = Toplevel(log_in_window)
    homepage_window.geometry("390x844")
    homepage_window.title('Homepage')
    homepage_window.configure(bg="#323232")  # Set background color

    # WARNING - TESTING / WORK IN PROGRESS
    # !!! NEED TO EXTRACT THE CORRESPONDING 'NAME' DATA FROM DB !!!
    # !!! ADD THE EXTRACTED 'NAME' DATA AFTER TEXT='HEY' TO CREATE A PERSONALIZED GREETING MESSAGE !!!
    file = open("gui/credentials.txt", "a")
    for line in open('gui/credentials.txt', 'r').readlines():
        login_info = line.split()
        if email_text1 == login_info[3]:
            name_text1= login_info[1]

    # Heading/Wecloming message
    label4 = Label(homepage_window, text="Hey " + name_text1 + " \U0001F44B", font='Helvetica 28 bold', fg='white')
    label4.pack(fill=X, pady=40)
    label4.configure(bg='#323232')

    # Instructional message
    label5 = Label(homepage_window, text="Complete the form to record a new subscription!", font="Helvetica 14", fg="white")
    label5.pack(fill=X, pady=20)
    label5.configure(bg='#323232')

    # Make a frame for input fields
    homepage_panel = Frame(homepage_window)
    homepage_panel.configure(bg='#323232')
    homepage_panel.pack(pady=30)
    
    # Subscription name dropdown
    # Create a list of options for the dropdown list
    subscription_name_options = ['Adobe Creative Cloud', 'AliExpress Premium', 'Amazon Prime', 'Apple Music', 'Apple TV+', 'Disney+', 'DoorDash', 'Google Workspace', 'Grubhub', 'HBO Max', 'Hulu', 'Microsoft 365', 'Netflix', 'Postmates', 'Spotify', 'Uber Eats', 'Walmart+', 'eBay Plus']
    # Create a combobox widget and a label
    subscription_name_label = Label(homepage_panel, text="Subscription name: ", bg="#323232", fg="white")
    subscription_name_label.grid(row=0, column=0)
    subscription_name_dropdown = Combobox(homepage_panel, values = subscription_name_options, state="readonly")
    # Set an initial value for the dropdown
    subscription_name_dropdown.set('Select a subscription')
    selected_subscription_name = subscription_name_dropdown.get()
    subscription_name_dropdown.grid(row=0, column=1)
    
    # Spacing between input fields
    Label(homepage_panel, text="", bg="#323232", fg="white").grid(row=1)

    # Cost input
    cost_label = Label(homepage_panel, text="Cost: $ ", bg="#323232", fg="white")
    cost_label.grid(row=2, column=0)
    cost_entry = Entry(homepage_panel,textvariable=cost_entry)
    cost_entry.grid(row=2, column=1)

    # Spacing between input fields
    Label(homepage_panel, text="", bg="#323232", fg="white").grid(row=3)

    # 
main_menu()
>>>>>>> Stashed changes
