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
            #TODO: change this into an error response so that the gui can display the detailed instructions
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
            #TODO: change this into an error response so that the gui can display the detailed instructions
            return "Oops! There was an issue signing you up."

# Define a UserLogin resource for the 'login' endpoint
class UserLogIn(Resource):
    def post(self):
        login_data = request.get_json()
        user_email = login_data.get("email")
        user_password = login_data.get("password")
        conn = get_db_connection()

        try:
            hash = conn.execute('SELECT name, password_hashed, email FROM USER WHERE email = ?', (user_email,)).fetchone()
            if hash is None:
                return "Email not found" 
            tuple(hash) 
            user_name = hash[0]
            password_hashed = hash[1]
            user_email = hash[2]
            conn.close()
            # conver the str back to byte
            hashed_password_bytes = password_hashed.encode('utf-8')
            # encode the password that user input]
            user_password_bytes= user_password.encode('utf-8')
            login_status = bcrypt.checkpw(user_password_bytes, hashed_password_bytes)

            response = {
                'login_status': login_status,
                'user_name': user_name, 
                'user_email': user_email,
                'user_password': user_password_bytes.decode('utf-8'),
                'hash_password': hashed_password_bytes.decode('utf-8')
                }
            return response
        
        except Exception as e:
            print("An error occurred:", str(e))
            #TODO: change this into an error response so that the gui can display the detailed instructions
            return "Oops! An error occurred when logging you in, please double-check your email."

# Define a Homepgae resource for the 'homepage' endpoint
class Homepage(Resource):
    def post(self):
        # parse the post request data as json
        new_subcription = request.get_json()
        # get each value of the json data and write into new variables
        email = new_subcription.get('user_email')
        sub_name = new_subcription.get('sub_name')
        amount = new_subcription.get('amount')
        date = new_subcription.get('date')
        subscription_cycle = new_subcription.get('subscription_cycle')
        print(sub_name + " " + email)

        # use the email to get the user id from the User table
        conn = get_db_connection()
        print("connected to database")
        user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
        # convert the row object to tuple
        user_id = tuple(user_id_row)[0]

        # if the user is not found in the database (not loged in), return false and the error message
        if user_id_row[0] == None:
            return {
                'success': False,
                'msg': "Email not found"
            }
        

        ## check if the sub_name is valid
        # use the sub_name to get the sub_id from the Company table
        co_id_row = conn.execute('SELECT co_id FROM Company WHERE name = ?', (sub_name,)).fetchone()
        # convert the row object to tuple
        co_id = tuple(co_id_row)[0] 
        print(co_id) 
        # if service name input is not found in the Company table (invalid input of company), return false and error message
        if co_id is None:
            print("Subscription service provider not found") 
            return {
                'success': False,
                'msg': "Service not found."
            }
        print("Found the subscription service provider: " + str(co_id))

        ## check if the current user already subscribed to this company
        co_id_tuple = []
        for row in conn.execute('SELECT co_id FROM Subscription  WHERE user_id = ?', (user_id,)).fetchall():
            co_id_tuple.append(row)
        # convert a list of row objects into a list of tuple
        co_id_tuple = [tuple(row) for row in co_id_tuple]
        # convert a list of tuple into a list of number
        # if user has already subscribed to the same service, return false and error message
        for id in co_id_tuple:
            if (id[0] == co_id):
                print("You already subscribed to this service, do you want to update your current subscription list?")
                response1 = {
                    'success': True,
                    'msg': "Duplicated Service.",
                }
                print(response1)
                return response1

        else:
            print("Starting to write to the database")
            # write the new subscription data into the database, if success, return json data passing true
            try:
                conn.execute('''INSERT OR REPLACE INTO Subscription
                    (user_id, co_id, start_date, amount, subscription_cycle) VALUES (?, ?, ?, ?, ?)''',
                                (user_id, co_id, date, amount, subscription_cycle))
                conn.commit()
                conn.close()
                print("success written to database.")
                response2  = {
                    'success': True,
                    'msg': "New subscription added."
                }
                print(response2)
                return response2
            # return false and err message if any other error happened during writing data into the database
            except Exception as e:
                print("An error occurred:", str(e))
                response3 = {
                    'success': False,
                    'msg': str(e)
                }
                print(response3)
                return response3

# define a Dashboard resource to '/dashboard' endpoint
class Dashboard(Resource):
    # get method to get all the subscription data from the database and send the response to the GUI for display
    def get(self):
        return 
    # post a deletion request to delete the subscription data in the database
    def post(self):
        return





# Register the resource UserSignUp with the '/signup' URL endpoint
api.add_resource(UserSignUp, '/signup')
api.add_resource(UserLogIn, '/login')
api.add_resource(Homepage, '/homepage')
api.add_resource(Dashboard, '/dashboard')
# start the server and the flask application
if __name__ == "__main__":
    app.run(port=8000, debug=True)
