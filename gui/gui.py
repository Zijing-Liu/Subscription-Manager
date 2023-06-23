# Access modules
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import Calendar
import tkinter as tk
import datetime
import re
import json
import requests
# TESTING!!!
# Access local
import os



################################################# HTTP requests start here, communicating to the backend server
# Make a GET request to the /signup endpoint of the web app, and return the response data
def getUserData():
    response = requests.get('http://localhost:8000/signup')
    if response.status_code == 200:
        return response  # a list of tuple
    else:
        print('Request failed with status code:', response.status_code)

# Make a post request to the backend signup endpoint to pass the user input data to the backend database
def signUpReq():
    url = 'http://localhost:8000/signup'
    data = {
        'name': name_text,
        'email': email_text,
        'password_plain': password_text,
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for any errors
    except requests.exceptions.RequestException as e:
        print('Error:', e)

    
# Make a get request method to the login endpoint
def logInReq():
    url = 'http://localhost:8000/login' 
    data = {'email': email_text1,
            'password': password_text1
            }  

    response = requests.post(url)
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for any errors
        return response
    except requests.exceptions.RequestException as e:
        print('Error:', e)

# Make a post request method to the Homepage endpoint
def postNewSubscription():
    url = 'http://localhost:8000/homepage'
    new_subcription = {
        'user_email': login_user_email,
        'sub_name': selected_subscription_name,
        'amount': cost_value,
        'date': selected_starting_date,
        'subscription_cycle': selected_billing_cycle,
    }
    try:
        response = requests.post(url, json = new_subcription)
        response.raise_for_status() # Check for any errors
        # print(response.status_code)
        return response 
    except requests.exceptions.RequestException as e:
        print('Error:', e)

################################################# HTTP requests end here





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

    # # Create spacing between sign up button and "Already have an account?" label
    # Label(sign_up_window, text="", bg="#323232", fg="white").pack(pady=140)

    # # Already have an account?
    # login_label = Label(sign_up_window, text="Already have an account?", bg="#323232", fg="white")
    # login_label.pack()
    # # Create "Log in" button
    # login_btn = Button(sign_up_window, text="Log in", width="12", height="2", command=log_in)
    # login_btn.pack(pady=10)
    

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

    # check if the current input email already exisit in the user table, if so set registered to true
    curr_users_data = getUserData()
    existing_emails = []
    for row in curr_users_data:
        existing_emails.append(row[0])
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
        # send the post request to the backend server
        signUpReq()
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
    global email_text1
    global password_text1
    email_text1 = email_verify.get()
    password_text1 = password_verify.get()

    # Set login as False by default
    # login = False

    # if the password verification is successcual , recieve response result (true) from the backend and assign it to the login variable
    login_response = logInReq()
    login_json = login_response.json()
    login = login_json['login_status']
    login_user_name = login_json['user_name']
    login_user_email = login_json['user_email']



    # if login is set to ture, open the homepage
    if login:
        # Clear out the entry box
        email_verify_entry.delete(0, END)
        password_verify_entry.delete(0, END)
        log_in_window.destroy()
        homepage(login_user_name, login_user_email)
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
def homepage(login_user_name, user_email):
    global login_user_email
    login_user_email = user_email
    cost = StringVar()
    selected_subscription_name = StringVar()
    selected_billing_cycle = StringVar()
    selected_starting_date = StringVar()
    cost_value = StringVar()

    # Set screen position, size, title
    homepage_window = Toplevel(main_window)
    homepage_window.geometry("390x844")
    homepage_window.title('Homepage')
    homepage_window.configure(bg="#323232")  # Set background color

    # WARNING - TESTING / WORK IN PROGRESS
    # !!! NEED TO EXTRACT THE CORRESPONDING 'NAME' DATA FROM DB !!!
    # !!! ADD THE EXTRACTED 'NAME' DATA AFTER TEXT='HEY' TO CREATE A PERSONALIZED GREETING MESSAGE !!!
    # file = open("gui/credentials.txt", "a")
    # for line in open('gui/credentials.txt', 'r').readlines():
    #     login_info = line.split()
    #     if email_text1 == login_info[3]:
    #         name_text1= login_info[1]

    name_text1 = login_user_name
    login_user_email = login_user_email
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
    subscription_name_dropdown.set(' Select a subscription')
    subscription_name_dropdown.grid(row=0, column=1)
    
    # subscription_name_dropdown.bind("<<ComboboxSelected>>", get_selected_subscription)
    
    # Spacing between input fields
    Label(homepage_panel, text="", bg="#323232", fg="white").grid(row=1)

    # Cost input
    cost_label = Label(homepage_panel, text="Cost: $ ", bg="#323232", fg="white")
    cost_label.grid(row=2, column=0)
    cost_entry = Entry(homepage_panel,textvariable= cost)
    cost_entry.grid(row=2, column=1)

    # Spacing between input fields
    Label(homepage_panel, text="", bg="#323232", fg="white").grid(row=3)

    # Starting date datepicker
    # Create a label
    starting_date_label = Label(homepage_panel, text="Starting date: ", bg="#323232", fg="white")
    starting_date_label.grid(row=4, column=0)
    # Get today's date
    today = datetime.date.today()
    # Create a calendar
    starting_date_cal = Calendar(homepage_panel, selectmode='day', year=today.year, month=today.month, day=today.day, width=10, height=30, background='white', foreground='black', selectforeground='red')
    starting_date_cal.grid(row=4, column=1)


    # Spacing between input fields
    Label(homepage_panel, text="", bg="#323232", fg="white").grid(row=5)

    # Billing cycle dropdown
    # Create a list of options for the dropdown list
    billing_cycle_options = ['weekly', 'monthly', '3-months', '6-months', 'annually']
    # Create a combobox widget and a label
    billing_cycle_options_label = Label(homepage_panel, text="Billing cycle: ", bg="#323232", fg="white")
    billing_cycle_options_label.grid(row=6, column=0)
    billing_cycle_dropdown = Combobox(homepage_panel, values = billing_cycle_options, state="readonly")
    # Set an initial value for the dropdown
    billing_cycle_dropdown.set(' Select a billing cycle')
    billing_cycle_dropdown.grid(row=6, column=1)

    # Get the variables
    def postSubscriptionData():
        global selected_subscription_name, cost_value,selected_starting_date,selected_billing_cycle
        selected_subscription_name = subscription_name_dropdown.get()
        cost_value = cost.get()
        selected_starting_date = starting_date_cal.get_date()
        selected_billing_cycle = billing_cycle_dropdown.get()

        # get the response after post the submision data to the backend, read as json data, and get the success and msg variables
        submission_response = postNewSubscription()
        submission_json = submission_response.json()
        # getting the repsonse of the submission action from the backend
        submission_success = submission_json['success']
        submission_msg = submission_json['msg']
    ###### Implement the prompt window to ask if user want to add more subscription data or view the dashboard
        

    # Submit subscription and call the "get_create_subscription_date()" function
    submit_subscription_btn = Button(homepage_window, text="Submit", width="26", height="2", command=postSubscriptionData)
    submit_subscription_btn.pack(pady=20)

    # # Create a bottom nav bar
    # # Create a frame
    # bottom_nav_frame = tk.Frame(homepage_window, width=390, height=100)
    # bottom_nav_frame.configure(width=390, height=100)
    # bottom_nav_frame.pack(side="bottom", fill="x")
    # # Nav tabs
    # home_button = tk.Button(bottom_nav_frame, text="Home", bg="blue", fg="white", width=80)
    # home_button.pack(side="left")
    # dashboard_button = tk.Button(bottom_nav_frame, text="Dashboard", bg="white", fg="black", width=80)
    # dashboard_button.pack(side="right")

main_menu()