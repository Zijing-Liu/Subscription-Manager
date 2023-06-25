# Access modules
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import Calendar
from tkinter import ttk
import tkinter as tk
import datetime as dt
from datetime import datetime, timedelta
import re
import json
import requests
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

def getAllSubscriptions():
    url = 'http://localhost:8000/listview'
    user = {'email': user_email}  
    try:
        response = requests.post(url, json = user)
        response.raise_for_status() 
        print(response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        print('Error:', e)

def cancelASubscription():
    url = 'http://localhost:8000/cancel'
    subscription = {'email': user_email,
                    'cancel_subscription_name': 'cancel_subscription_name'}  
    try:
        response = requests.post(url, json = subscription)
        response.raise_for_status() 
        print(response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        print('Error:', e)

def editASubscription():
    url = 'http://localhost:8000/edit'
    subscription = {'email': user_email,
                    'edit_subscription_name': 'edit_subscription_name',
                    'edit_start_date': 'edit_start_date',
                    'amount': 'edit_amount',
                    'subscription_cycle': 'edit_billing_cycle'
                    }  
    try:
        response = requests.post(url, json = subscription)
        response.raise_for_status() 
        print(response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        print('Error:', e)

 ################################################# HTTP requests end here

# Create a landing screen named main_menu
def mainMenu():
    global main_window
    main_window = Tk()
    # Set screen size, title, heading
    main_window.geometry("390x844")
    main_window.title("Subscription Manager")
    main_window.configure(bg="#323232")  # Set background color
    label1 = Label(main_window, text="Welcome \U0001F44B", font="Helvetica 28 bold", fg="white")
    label1.configure(bg="#323232")  # Set background color of label
    label1.pack(fill=X, pady=40)
    # Create a log in button and a sign up button
    login_btn = Button(main_window, text="Log In", width="26", height="2", command=logIn)
    login_btn.pack(pady=20)
    signup_btn = Button(main_window, text="Sign up", width="26", height="2", command=signUp)
    signup_btn.pack(pady=20)
    main_window.mainloop()


# Create a sign up screen
def signUp():
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
    label2 = Label(sign_up_window, text="Sign up \U0001F511", font='Helvetica 28 bold', fg='white')
    label2.pack(fill=X, pady=40)
    label2.configure(bg='#323232')

    # Name input
    user_info_panel = Frame(sign_up_window)
    user_info_panel.configure(bg="#323232")  # Set background color of label
    user_info_panel.pack(pady=30)
    name_label = Label(user_info_panel, text="Name: ", bg="#323232", fg="white")
    name_label.grid(row=0, column=0)
    name_entry = Entry(user_info_panel, textvariable=name)
    name_entry.grid(row=0, column=1)

    # Spacing between input fields
    Label(user_info_panel, text="", bg="#323232", fg="white").grid(row=1)

    # Email input
    email_label = Label(user_info_panel, text="Email: ", bg="#323232", fg="white")
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
    sign_up_btn = Button(sign_up_window, text="Sign up", width="26", height="2", command=register)
    sign_up_btn.pack()
    

# Register and record the new account information into the database
def register():
    global name_text
    global email_text
    global password_text


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
    validEmailPattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # If some information is missing, alert users
    if name_text == "" or email_text == "" or password_text == "":
        sign_up_missing_info_window = Toplevel(sign_up_window)
        sign_up_missing_info_window.geometry('300x300')
        sign_up_missing_info_window.title('Missing info')
        sign_up_missing_info_window.configure(bg="#323232")  # Set background color
        Label(sign_up_missing_info_window, text="Something is missing \U0001F494", font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_missing_info_window, text="Try again", width="26", height="2", command=lambda: sign_up_missing_info_window.destroy())
        try_again_btn.pack(pady=20)
    # Check if email input is valid
    elif not re.match(validEmailPattern, email_text):
        sign_up_invalid_email_window = Toplevel(sign_up_window)
        sign_up_invalid_email_window.geometry('300x300')
        sign_up_invalid_email_window.title('Invalid Email')
        sign_up_invalid_email_window.configure(
            bg="#323232")  # Set background color
        Label(sign_up_invalid_email_window, text="Invalid email \U0001F92F",
              font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_invalid_email_window, text="Try again", width="26", height="2", command=lambda: sign_up_invalid_email_window.destroy())
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
        try_again_btn = Button(sign_up_fail_window, text="Try again", width="26", height="2", command=lambda: sign_up_fail_window.destroy())
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
def logIn():
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
    password_label = Label(log_in_panel, text="Password: ", bg="#323232", fg="white")
    password_label.grid(row=2, column=0)
    password_verify_entry = Entry(log_in_panel, textvariable=password_verify, show="*")
    password_verify_entry.grid(row=2, column=1)

    # Log in button
    login_btn = Button(log_in_window, text="Log in", width="26", height="2", command=loginVerify)
    login_btn.pack(pady=20)



# Verify email and password on login screen
def loginVerify():
    global email_text1
    global password_text1
    email_text1 = email_verify.get()
    password_text1 = password_verify.get()

    # If inputs are blank
    if email_text1 == "" or password_text1 == "": 
        log_in_missing_info_window = Toplevel(log_in_window)
        log_in_missing_info_window.geometry('300x300')
        log_in_missing_info_window.title('Missing info')
        log_in_missing_info_window.configure(bg="#323232")  # Set background color
        Label(log_in_missing_info_window, text="Something is missing \U0001F494", font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(log_in_missing_info_window, text="Try again", width="26", height="2", command=lambda: log_in_missing_info_window.destroy())
        try_again_btn.pack(pady=20)
    else: 
        # If password verification is successful , recieve response result (true) from the backend and assign it to the login variable
        login_response = logInReq()
        login_json = login_response.json()
        login = login_json['login_status']
        login_user_name = login_json['user_name']
        login_user_email = login_json['user_email']

        # If login is set to true
        if login:
            # Clear out the entry box
            email_verify_entry.delete(0, END)
            password_verify_entry.delete(0, END)
            log_in_window.destroy()
            homepage(login_user_name, login_user_email)
        # When the password is incorrect
        # Prompt an error message
        else:
            log_in_fail_window = Toplevel(log_in_window)
            log_in_fail_window.geometry('300x300')
            log_in_fail_window.title('Oops')
            log_in_fail_window.configure(bg="#323232")  # Set background color
            Label(log_in_fail_window, text="Password incorrect \U0001F926",
                font='Helvetica 20 bold', bg="#323232", fg="white").pack(fill=X, pady=40)
            # Try again button
            try_again_btn = Button(log_in_fail_window, text="Try again", width="26",
                                height="2", command=lambda: log_in_fail_window.destroy())
            try_again_btn.pack(pady=20)


# Create a homepage
def homepage(login_user_name, user_email):
    global homeAction, tableViewAction, chartViewAction
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
    today = dt.date.today()
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
    def submitValidationPost():
        global selected_subscription_name, cost_value,selected_starting_date,selected_billing_cycle
        ## Validation
        # Define a valid cost pattern
        validCostPattern = r'^\d+(\.\d{1,2})?$'
        # Get the variables
        selected_subscription_name = subscription_name_dropdown.get()
        cost_value = cost.get()
        selected_starting_date = starting_date_cal.get_date()
        selected_billing_cycle = billing_cycle_dropdown.get()

        # If inputs are empty, prompt an alert message
        if selected_subscription_name == " Select a subscription" or cost_value == "" or selected_billing_cycle == " Select a billing cycle":
            submit_missing_window = Toplevel(homepage_window)
            submit_missing_window.geometry('300x300')
            submit_missing_window.title('Oops')
            submit_missing_window.configure(bg="#323232")  # Set background color
            Label(submit_missing_window, text="Something is missing \U0001F494", font='Helvetica 20 bold', bg="#323232", fg="white").pack(fill=X, pady=40)
            # Try again button
            try_again_btn = Button(submit_missing_window, text="Try again", width="26", height="2", command=lambda: submit_missing_window.destroy())
            try_again_btn.pack(pady=20)

        # If the cost input is invalid, prompt an error message
        elif not re.match(validCostPattern, cost_value):
            submit_invalid_window = Toplevel(homepage_window)
            submit_invalid_window.geometry('300x300')
            submit_invalid_window.title('Error')
            submit_invalid_window.configure(bg="#323232")  # Set background color
            Label(submit_invalid_window, text="Invalid cost input \U0001F92F", font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
            # Try again button
            try_again_btn = Button(submit_invalid_window, text="Try again", width="26", height="2", command=lambda: submit_invalid_window.destroy())
            try_again_btn.pack(pady=20)
        
        else: 
            ## post request
            # get the response after post the submission data to the backend, read as json data, and get the success and msg variables
            submission_response = postNewSubscription()
            submission_json = submission_response.json()
            # getting the repsonse of the submission action from the backend
            submission_success = submission_json['success']
            submission_msg = submission_json['msg']
    
            # If the service name has already existed
            if (submission_success == False and submission_msg == 'Duplicated Service.'):
                submit_invalid_window = Toplevel(homepage_window)
                submit_invalid_window.geometry('300x300')
                submit_invalid_window.title('Error')
                submit_invalid_window.configure(bg="#323232")  # Set background color
                Label(submit_invalid_window, text="Subscription already existed \U0001F92F", font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
                # Try again button
                try_again_btn = Button(submit_invalid_window, text="Try again", width="26", height="2", command=lambda: submit_invalid_window.destroy())
                try_again_btn.pack(pady=20)

            # If success
            elif (submission_success == True and submission_msg == 'New subscription added.'):
                # Clear out the entry box, reset dropdown and calendar picker
                subscription_name_dropdown.set(' Select a subscription')
                cost_entry.delete(0, END)
                starting_date_cal.selection_set(today)
                billing_cycle_dropdown.set(' Select a billing cycle')
                # Pop up window
                submit_success_window = Toplevel(homepage_window)
                submit_success_window.geometry('300x300')
                submit_success_window.title('Success')
                submit_success_window.configure(bg="#323232")  # Set background color
                Label(submit_success_window, text="Success \U0001F973", font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
                # Confirm button to close the pop up message window
                confirm_btn = Button(submit_success_window, text="Confirm", width="26",
                                height="2", command=lambda: submit_success_window.destroy())
                confirm_btn.pack(pady=20)


    # Submit subscription and call the "submitValidationPost" function
    submit_subscription_btn = Button(homepage_window, text="Submit", width="26", height="2", command=submitValidationPost)
    submit_subscription_btn.pack(pady=20)

    # Bottom nav bar
    # Action
    def homeAction():
        homepage(login_user_name, user_email)
    def tableViewAction():
        table_view()
    def chartViewAction():
        
        chart_view()
    # Frame
    bottom_nav_frame = tk.Frame(homepage_window)
    bottom_nav_frame.pack(side='bottom', fill='x')
    # Nav tabs
    home_button = tk.Button(bottom_nav_frame, text='Home')
    home_button.pack(side='left', fill='both', expand=True)
    list_view_button = tk.Button(bottom_nav_frame, text='Table View', command=tableViewAction)
    list_view_button.pack(side='left', fill='both', expand=True)
    chart_view_button = tk.Button(bottom_nav_frame, text='Chart View', command=chartViewAction)
    chart_view_button.pack(side='left', fill='both', expand=True)


# Table View Screen
def table_view():
    global table_view_window
    global user_email
    # Set screen position, size, title
    table_view_window = Toplevel(main_window)
    table_view_window.geometry("390x844")
    table_view_window.title('Table View')
    table_view_window.configure(bg="#323232")  # Set background color

    # Heading
    label4 = Label(table_view_window, text="Table View \U0001F4CB", font='Helvetica 28 bold', fg='white')
    label4.pack(fill=X, pady=40)
    label4.configure(bg='#323232')

    # Make a frame for treeview
    table_view_panel = Frame(table_view_window)
    table_view_panel.configure(bg='#323232')
    table_view_panel.pack()

    # Create a treeview table
    table = ttk.Treeview(table_view_panel, columns=("Subscription", "Cost", "Starting date", "Billing cycle", "Next charge on"))
    # Name column headings
    table.heading("Subscription", text="Subscription")
    table.heading("Cost", text="Cost ($)")
    table.heading("Starting date", text="Starting date")
    table.heading("Billing cycle", text="Billing cycle")
    table.heading("Next charge on", text="Next charge on")

    # Get a list of all subscription data under the current user 
    user_email = login_user_email
    subscriptions = getAllSubscriptions()
    subscription_json =subscriptions.json()
    # print("I want to print out the response")
    dic = (subscription_json['all_subscriptions'])

    for row in dic:
        # Extract starting date and billing cycle
        row_start_date = row[2]
        row_billing_cycle = row[3]
        # Convert the start date string into a "datetime" object
        row_start_datetime = datetime.strptime(row_start_date, "%m/%d/%y")
        # Determine how many days are there in one billing cycle
        if row_billing_cycle == 'weekly':
            billing_days = 7
        elif row_billing_cycle == 'monthly':
            billing_days = 30
        elif row_billing_cycle == '3-months':
            billing_days = 90
        elif row_billing_cycle == '6-months':
            billing_days = 180
        elif row_billing_cycle == 'annually':
            billing_days = 365
        # Convert the billing_days into a timedelta object for later calculation
        billing_days_duration = timedelta(days = billing_days)
        # Get the current date
        today_date = datetime.now().date()
        # Calculate the number of completed cycles
        # Use // to return the largest integer that is less than or equal to the result
        completed_cycles = (today_date - row_start_datetime.date()).days // (billing_days_duration).days
        # Calculate the next billing date
        # (Completed cycle + 1) => determine the next billing cycle after the completed cycle
        # (Completed cycle + 1) * (days in one billing cycle) => # of days after the next billing cycle
        # Start date + (Completed cycle + 1) * (days in one billing cycle) => adds up the days to calculate the next billing date from the starting date
        next_billing_date = row_start_datetime + timedelta(days = (completed_cycles + 1) * billing_days_duration.days)
        next_billing_date = next_billing_date.strftime('%-m/%d/%y')

        # Insert into table
        table.insert("", "end", values=(row[0], row[1], row[2], row[3], next_billing_date))

    # Configure column properties
    table.column("#0", width=0, stretch=tk.NO)  # Hide the first indexing column (default)
    table.column("Subscription", width=80, anchor=tk.CENTER)
    table.column("Cost", width=60, anchor=tk.CENTER)
    table.column("Starting date", width=80, anchor=tk.CENTER)
    table.column("Billing cycle", width=80, anchor=tk.CENTER)
    table.column("Next charge on", width=100, anchor=tk.CENTER)
    # Font
    style = ttk.Style()
    style.configure("Treeview", font=('Helvetica', 9))
    # Pack the treeview widget
    table.pack(fill="both", expand=True)

    # Remove subscription button
    remove_subscription_btn = Button(table_view_window, text="Remove subscription", width="26", height="2")
    remove_subscription_btn.pack(pady=50)

    # Bottom nav bar
    # Frame
    bottom_nav_frame = tk.Frame(table_view_window)
    bottom_nav_frame.pack(side='bottom', fill='x')
    # Nav buttons
    home_button = tk.Button(bottom_nav_frame, text='Home', command=homeAction)
    home_button.pack(side='left', fill='both', expand=True)
    list_view_button = tk.Button(bottom_nav_frame, text='Table View')
    list_view_button.pack(side='left', fill='both', expand=True)
    chart_view_button = tk.Button(bottom_nav_frame, text='Chart View', command=chartViewAction)
    chart_view_button.pack(side='left', fill='both', expand=True)


# Remove subscription screen
def remove_sub():
    # Set screen position, size, title
    remove_sub_window = Toplevel(table_view_window)
    remove_sub_window.geometry("390x844")
    remove_sub_window.title('Remove subscription')
    remove_sub_window.configure(bg="#323232")  # Set background color

    # Heading
    label4 = Label(remove_sub_window, text="Remove Subscription", font='Helvetica 28 bold', fg='white')
    label4.pack(fill=X, pady=40)
    label4.configure(bg='#323232')


# Chart View Screen
def chart_view():
    # Set screen position, size, title
    chart_view_window = Toplevel(main_window)
    chart_view_window.geometry("390x844")
    chart_view_window.title('Chart View')
    chart_view_window.configure(bg="#323232")  # Set background color

    # Heading
    label4 = Label(chart_view_window, text="Chart View \U0001F4C8", font='Helvetica 28 bold', fg='white')
    label4.pack(fill=X, pady=40)
    label4.configure(bg='#323232')

    # Bottom nav bar
    bottom_nav_frame = tk.Frame(chart_view_window)
    bottom_nav_frame.pack(side='bottom', fill='x')

    home_button = tk.Button(bottom_nav_frame, text='Home', command=homeAction)
    home_button.pack(side='left', fill='both', expand=True)
    list_view_button = tk.Button(bottom_nav_frame, text='Table View', command=tableViewAction)
    list_view_button.pack(side='left', fill='both', expand=True)
    chart_view_button = tk.Button(bottom_nav_frame, text='Chart View')
    chart_view_button.pack(side='left', fill='both', expand=True)





mainMenu()