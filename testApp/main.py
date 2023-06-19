# import framework and extensions
from flask import Flask, request, redirect
import tkinter as tk
from flask_restful import Api, Resource
# from flask_sqlalchemy import SQLAlchemy
import sqlite3, bcrypt, json

# initialize this flask application, api
app = Flask(__name__)
api = Api(app)

#### helper funciton ####

# define a function to connect to the sql database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    # Enable the retrieval of rows as sqlite3.Row objects to achieve minimal memory overhead (pass-by-reference)
    conn.row_factory = sqlite3.Row
    return conn

    # encryptPassword using bcrypt and return a hash value and a salt 
def encryptPassword(password_text):
    # converting password to array of bytes
    bytes = password_text.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    password_text_hashed = bcrypt.hashpw(bytes, salt)
    # convert the passwrod from byte to string
    hashed_password_str = password_text_hashed.decode('utf-8')
    salt_str = salt.decode('utf-8')

    encryption = {
    'salt': salt_str,
    'password_hashed': hashed_password_str
    }

    return encryption

#### end of helper funciton ###
# Define a resource class for the user Signup endpoint
class UserSignUp(Resource):
    # define the get method that fetch all the user data from the data.db database and return the data as a list of tuple named users_list
    def get(self):
        try:
            users_list = []
            conn = get_db_connection()
            for row in conn.execute('SELECT email FROM User').fetchall():
                users_list.append(row)
            users_list = [tuple(row) for row in users_list]
            print(users_list)
            conn.commit()
            conn.close()
            return users_list
        except:
            return "Opps! There was an issue getting the data from the database 🫠"

    # define the post method that get the data user posted and write into the data.db database, redirect to the signup page
    def post(self):
        usr_data = request.get_json()
        name = usr_data.get('name')
        email = usr_data.get('email')
        password = usr_data.get('password_plain')
        salt = encryptPassword(password)['salt']
        password_hashed = encryptPassword(password)['password_hashed']
        try:
            conn = get_db_connection()
            conn.execute('''INSERT OR REPLACE INTO User
                (name, email, password_hashed, salt) VALUES (?, ?, ?, ?)''',
                         (name, email, password_hashed, salt))
            
            conn.commit()
            conn.close()
            return redirect('/signup')

        except Exception as e:
            print("An error occurred:", str(e))
            return "Oops! There was an issue signing you up."

# Define a UserLogin resource for the 'login' endpoint
class UserLogIn(Resource):
    def post(self):
        login_data = request.get_json()
        user_email = login_data.get("email")
        user_password = login_data.get("password")
        conn = get_db_connection()

        try:
            hash = conn.execute('SELECT name, password_hashed FROM USER WHERE email = ?', (user_email,)).fetchone()
            if hash is None:
                return "Email not found" 
            tuple(hash) 
            user_name = hash[0]
            password_hashed = hash[1]

            # conver the str back to byte
            hashed_password_bytes = password_hashed.encode('utf-8')
            # encode the password that user input]
            user_password_bytes= user_password.encode('utf-8')
            login_status = bcrypt.checkpw(user_password_bytes, hashed_password_bytes)

            response = {
                'login_status': login_status,
                'user_name': user_name, 
                'user_password': user_password_bytes.decode('utf-8'),
                'hash_password': hashed_password_bytes.decode('utf-8')
                }
            return response
        
        except Exception as e:
            print("An error occurred:", str(e))
            return "Oops! An error occurred when logging you in, please double-check your email."


# Register the resource UserSignUp with the '/signup' URL endpoint
api.add_resource(UserSignUp, '/signup')
api.add_resource(UserLogIn, '/login')
# start the server and the flask application
if __name__ == "__main__":
    app.run(port=8000, debug=True)
