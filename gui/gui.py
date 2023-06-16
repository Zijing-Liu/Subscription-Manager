# Access Tkinter modules
from tkinter import *
# Access regular expressions
import re
import requests
# TESTING!!!
# Access local
import os


# Create a landing screen named main_menu
def main_menu():
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
    login_btn = Button(main_window, text="Log In", width="26", height="2", command=log_in)
    login_btn.pack(pady=20)
    signup_btn = Button(main_window, text="Sign up", width="26", height="2", command=sign_up)
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
    sign_up_window=Toplevel(main_window)
    sign_up_window.geometry("390x844")
    sign_up_window.title('Sign up')
    sign_up_window.configure(bg="#323232")  # Set background color
    
    # Create three variables named name, email, password
    name=StringVar()
    email=StringVar()
    password=StringVar()

    # Heading
    label2 = Label(sign_up_window, text="Sign up \U0001F511", font='Helvetica 28 bold', fg='white')
    label2.pack(fill=X, pady=40)
    label2.configure(bg='#323232')

    # Name input
    user_info_panel=Frame(sign_up_window)
    user_info_panel.configure(bg="#323232")  # Set background color of label
    user_info_panel.pack(pady=30)
    name_label=Label(user_info_panel, text="Name: ", bg="#323232", fg="white")
    name_label.grid(row=0, column=0)
    name_entry=Entry(user_info_panel, textvariable=name)
    name_entry.grid(row=0, column=1)

    # Spacing between input fields
    Label(user_info_panel, text="",bg="#323232", fg="white").grid(row=1)

    # Email input
    email_label=Label(user_info_panel, text="Email: ", bg="#323232", fg="white")
    email_label.grid(row=2, column=0)
    email_entry=Entry(user_info_panel, textvariable=email)
    email_entry.grid(row=2, column=1)

    # Spacing between input fields
    Label(user_info_panel, text="", bg="#323232", fg="white").grid(row=3)

    # Password input
    password_label=Label(user_info_panel, text="Password: ", bg="#323232", fg="white")
    password_label.grid(row=4, column=0)
    password_entry=Entry(user_info_panel, textvariable=password, show='*')
    password_entry.grid(row=4, column=1)

    # Create a sign up button
    sign_up_btn = Button(sign_up_window, text="Sign up", width="26", height="2", command=send_request)
    sign_up_btn.pack()


def send_request():
    url = 'http://localhost:5000/home'  # Replace with the actual URL of your Flask endpoint
    
    name_text = name.get()
    email_text = email.get()
    password_text=password.get()

    data = {
        'name': name_text,
        'email': email_text,
        'password': password_text
    }  # Replace with the data you want to send in the request

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for any errors
        print(response.json())  # Print the response data
    except requests.exceptions.RequestException as e:
        print('Error:', e)


# Register and record the new account information into the database
def register():
    # TESTING!!!
    # Set registered as a boolean operator to False
    # Set "not registered" as default
    registered = False

    # Get the name, email, and password data from input field
    name_text = name.get()
    email_text = email.get()
    password_text=password.get()

    # TESTING!!!
    # Access local, create a file named credentials.txt if it doesn't exist
    # If already existed, write to the file
    file = open("gui/credentials.txt", "a")
    # Return all the lines in the file as a list where each line is an item
    # Loop through each line in the file and split the line
    for line in open('gui/credentials.txt', 'r').readlines():
        userinfo = line.split()
        # Set registered from False to True when the email input has already existed in the database
        # If the email has already existed, then registered = True
        # Otherwise, registered = False
        if email_text == userinfo[3]:
            registered = True
    
    # Define a valid email pattern using regular expressions
    valid_email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # If some information is missing, alert users
    if name_text == "" or email_text == "" or password_text == "":
        file.close()
        sign_up_missing_info_window = Toplevel(sign_up_window)
        sign_up_missing_info_window.geometry('300x300')
        sign_up_missing_info_window.title('Missing info')
        sign_up_missing_info_window.configure(bg="#323232")  # Set background color
        Label(sign_up_missing_info_window, text="Something is missing \U0001F494",font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_missing_info_window, text="Try again", width="26", height="2", command=lambda : sign_up_missing_info_window.destroy())
        try_again_btn.pack(pady=20)
    # Check if email input is valid
    elif not re.match(valid_email_pattern, email_text):
        file.close()
        sign_up_invalid_email_window = Toplevel(sign_up_window)
        sign_up_invalid_email_window.geometry('300x300')
        sign_up_invalid_email_window.title('Invalid Email')
        sign_up_invalid_email_window.configure(bg="#323232")  # Set background color
        Label(sign_up_invalid_email_window, text="Invalid email \U0001F92F", font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_invalid_email_window, text="Try again", width="26", height="2", command=lambda : sign_up_invalid_email_window.destroy())
        try_again_btn.pack(pady=20)
    # If email has already registered, prompt an alert
    elif registered:
        file.close()
        sign_up_fail_window = Toplevel(sign_up_window)
        sign_up_fail_window.geometry('300x300')
        sign_up_fail_window.title('Alert')
        sign_up_fail_window.configure(bg="#323232")  # Set background color
        Label(sign_up_fail_window, text="Email already exists \U0001F62C",font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Try again button
        try_again_btn = Button(sign_up_fail_window, text="Try again", width="26", height="2", command=lambda : sign_up_fail_window.destroy())
        try_again_btn.pack(pady=20)
    # If not registered, write user info to the file
    else:
        file.write('Name: ' + name_text + " Email: " + email_text + " Password: " + password_text + "\n")
        # Close the file
        file.close()
        # Clear out the entry box
        name_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)
        # Prompt a pop up message window that indicates the account was successfully created
        sign_up_success_window = Toplevel(sign_up_window)
        sign_up_success_window.geometry('300x300')
        sign_up_success_window.title('Success')
        sign_up_success_window.configure(bg="#323232")  # Set background color
        Label(sign_up_success_window, text="You are all set \U0001F973",font="Helvetica 20 bold", bg="#323232", fg="white").pack(fill=X, pady=40)
        # Confirm button to close the pop up message window
        confirm_btn = Button(sign_up_success_window, text="Confirm", width="26", height="2", command= lambda : sign_up_success_window.destroy())
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
    log_in_window=Toplevel(main_window)
    log_in_window.geometry("390x844")
    log_in_window.title('Log in')
    log_in_window.configure(bg='#323232')
   
    # Heading
    label3 = Label(log_in_window, text="Log in \U0001F512", font='Helvetica 28 bold', bg="#323232", fg="white")
    label3.pack(fill=X, pady=40)

    log_in_panel = Frame(log_in_window)
    log_in_panel.configure(bg='#323232')
    log_in_panel.pack(pady=30)

    email_verify = StringVar()
    password_verify = StringVar()

    # Email input
    email_label=Label(log_in_panel, text="Email: ", bg="#323232", fg="white")
    email_label.grid(row=0, column=0)
    email_verify_entry=Entry(log_in_panel, textvariable=email_verify)
    email_verify_entry.grid(row=0, column=1)

    # Spacing between input fields
    Label(log_in_panel, text="", bg="#323232", fg="white").grid(row=1)

    # Password input
    password_label=Label(log_in_panel, text="Password: ", bg="#323232", fg="white")
    password_label.grid(row=2, column=0)
    password_verify_entry=Entry(log_in_panel, textvariable=password_verify, show="*")
    password_verify_entry.grid(row=2, column=1)

    # Log in button
    login_btn = Button(log_in_window, text="Log in", width="26", height="2", command = login_verify)
    login_btn.pack(pady=20)


# Verify email and password on login screen
def login_verify():
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
        Label(log_in_fail_window, text="Incorrect email or password \U0001F926", font='Helvetica 20 bold', bg="#323232", fg="white").pack(fill=X, pady= 40)
        # Try again button
        try_again_btn = Button(log_in_fail_window, text="Try again", width="26", height="2", command=lambda : log_in_fail_window.destroy())
        try_again_btn.pack(pady=20)


def homepage():
    print('1')

main_menu()