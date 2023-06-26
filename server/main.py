# Import framework and extensions
from flask import Flask, request, redirect
import tkinter as tk
from flask_restful import Api, Resource
# From flask_sqlalchemy import SQLAlchemy
import sqlite3, bcrypt, json
from datetime import date

# Initialize this flask application, api
app = Flask(__name__)
api = Api(app)

#### constant definitions ####
# define the response for failed reqests
request_fail = {
                'success': False,
                'msg': 'Database connection failed'
            }
#### End of constant definitions ####

#### Helper funciton ####

# Function to connect to the sql database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    # Enable the retrieval of rows as sqlite3.Row objects to achieve minimal memory overhead (pass-by-reference)
    conn.row_factory = sqlite3.Row
    return conn

# Function to encrypt Password using bcrypt library and return a hash value and a salt 
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
    # return the encryption as josn
    encryption = {
    'salt': salt_str,
    'password_hashed': hashed_password_str
    }
    return encryption

#### End of helper funciton ####

# Define a resource class for the user signup endpoint
class UserSignUp(Resource):
    # Define the get method that fetch all the user data from the data.db database and return the data as a list of tuple named users_list
    def get(self):
        try:
            # Initialize an empty list to store the user email data
            users_list = []
            # Connect to db, and fetch all the email row from the User table and write to the users_list
            conn = get_db_connection()
            for row in conn.execute('SELECT email FROM User').fetchall():
                users_list.append(row)
            # Conver each sqlite3.Row object into tuple
            users_list = [tuple(row) for row in users_list]
            # close the data connection 
            conn.close()
            # return user_list as response object to the front end
            return users_list
        # return a request_fail response if failed to get user data
        except Exception as e:
            print("An error occurred:", str(e))
            return request_fail

    # Define the post method that get the data from the request and write into the data.db database, redirect to the signup page
    def post(self):
        # Parse request data as json, get the values for usr_data, name, password from usr_data 
        usr_data = request.get_json()
        name = usr_data.get('name')
        email = usr_data.get('email')
        password = usr_data.get('password_plain')
        # Call the encryptPassword helper function to hash the password, get the hashed value and salt
        salt = encryptPassword(password)['salt']
        password_hashed = encryptPassword(password)['password_hashed']

        
        try:
            # Connect to db and insert a new data tuple, wrting name, email, password_hashed, salt into the User table
            conn = get_db_connection()
            conn.execute('''INSERT OR REPLACE INTO User
                (name, email, password_hashed, salt) VALUES (?, ?, ?, ?)''',
                         (name, email, password_hashed, salt))
            # commit the pending transaction to the db
            conn.commit()
            #  close the existing db connection
            conn.close()
            # rediect back to the signup page
            return redirect('/signup')
        # return a request_fail response if failed to insert new data into User table
        except Exception as e:
            print("An error occurred:", str(e))
            return request_fail

# Define a UserLogin Resource for the 'login' endpoint

class UserLogIn(Resource):
    # Define the post method to verify user login
    def post(self):
        # parse the login data 
        login_data = request.get_json()
        user_email = login_data.get("email")
        user_password = login_data.get("password")
    
        try:
            # connect to db, fetch the row in User associated with user_email 
            conn = get_db_connection()
            user_data = conn.execute('SELECT name, password_hashed, email FROM USER WHERE email = ?', (user_email,)).fetchone()
            # check if email exists in db
            if user_data is None:
                return "Email not found" 
            # convert the sqliteRow object into tuple and get the user_name, password_hashed, user_email
            tuple(user_data) 
            user_name = user_data[0]
            password_hashed = user_data[1]
            user_email = user_data[2]
            # end the current connection
            conn.close()
            # conver the password from str back to byte for verification
            hashed_password_bytes = password_hashed.encode('utf-8')
            # encode the password sent from the front end 
            user_password_bytes= user_password.encode('utf-8')
            # password verification 
            login_status = bcrypt.checkpw(user_password_bytes, hashed_password_bytes)
            # use a dictionary to collect response data and return 
            response = {
                'login_status': login_status,
                'user_name': user_name, 
                'user_email': user_email,
                }
            return response
        # return request_fail response object if login verification failed
        except Exception as e:
            print("An error occurred:", str(e))
            return request_fail

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

        # use the email to get the user id from the User table
        conn = get_db_connection()
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
        # if service name input is not found in the Company table (invalid input of company), return false and error message
        if co_id is None:
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
                response1 = {
                    'success': False,
                    'msg': "Duplicated Service.",
                }
                return response1

        else:
            # write the new subscription data into the database, if success, return json data passing true
            try:
                
                conn.execute('''INSERT OR REPLACE INTO Subscription
                    (user_id, co_id, start_date, amount, subscription_cycle) VALUES (?, ?, ?, ?, ?)''',
                                (user_id, co_id, date, amount, subscription_cycle))
                conn.commit()
                conn.close()
                response2  = {
                    'success': True,
                    'msg': "New subscription added."
                }
                return response2
            # return request_fail response object if login verification failed
            except Exception as e:
                print("An error occurred:", str(e))
                return request_fail

# define a Dashboard resource to '/dashboard' endpoint
class ListView(Resource):
    # post method to get all the subscription data from the database and send the response to the GUI for display
    def post(self):
        # parse the post request data as json
        user = request.get_json()
        # get each value of the json data and write into new variables
        email = user.get('email')
        try:
            # use the email to get the user id from the User table
            conn = get_db_connection()
            user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
            # convert the row object to tuple
            user_id = tuple(user_id_row)[0]
  
            # if the user is not found in the database (not loged in), return false and the error message
            if user_id == None:
                return {
                    'success': False,
                    'msg': "Email not found"
                }

            # Fetch the subscription data under the current user name
            subscriptions = conn.execute('SELECT CO.name, SUB.amount, SUB.start_date, SUB.subscription_cycle FROM SUBSCRIPTION AS SUB JOIN COMPANY AS CO ON CO.co_id = SUB.co_id WHERE SUB.end_date IS NULL AND SUB.user_id = ?', (user_id,)).fetchall()
            # Use list to store all the subscription tuple data
            subscriptions_list = []
            for row in subscriptions:
                subscriptions_list.append(row)
            subscriptions_list = [tuple(row) for row in subscriptions_list]
            # sotre the subscriptions_list in a dictionary and return 
            response = {
                'all_subscriptions': subscriptions_list,
            }
            conn.commit()
            conn.close()
            return response
        
        # return request_fail response object if login verification failed
        except Exception as e:
            print("An error occurred:", str(e))
            return request_fail

class ChartView(Resource):
    # define the post HTTP method in ChartView resource to get all the subscription data from the db 
    # and send the response to the GUI for display
    def post(self):
        user = request.get_json()
        # get each value of the json data and write into new variables
        email = user.get('email')

        try:
            # use the email to get the user id from the User table
            conn = get_db_connection()
            user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
            # convert the row object to tuple
            user_id = tuple(user_id_row)[0]
            # if the user is not found in the database (not loged in), return false and the error message
            if user_id == None:
                return {
                    'success': False,
                    'msg': "Email not found",
                    'data': []

                }

            # Fetch all the subscription data under the current user name
            subscriptions = conn.execute('SELECT SUB.start_date, SUB.subscription_cycle, SUB.end_date, SUB.amount FROM SUBSCRIPTION AS SUB JOIN COMPANY AS CO ON CO.co_id = SUB.co_id WHERE SUB.user_id = ? ', (user_id,)).fetchall()
            # Use list to store all the subscription tuple data
            subscriptions_list = []
            for row in subscriptions:
                subscriptions_list.append(row)
            subscriptions_list = [tuple(row) for row in subscriptions_list]
            # sotre values in dictionary and send data in response object
            response = {
                'success': True,
                'msg': "Fetch data success",
                'data': subscriptions_list      
            }
            conn.commit()
            conn.close()

            return response
        
        # return request_fail response object if login verification failed
        except Exception as e:
            print("An error occurred:", str(e))
            return request_fail
        
# Define a Remove resource adding to the '/remove' endpoint 
class Remove(Resource):
    # Define the post HTTP method in Remove Resource to update a tuple in Subscription table in db
    def post(self):
        # parse the post request data as json
        remove = request.get_json()
        # Get email, remove_subscription_name of the json data and assign them into new variables
        email = remove.get('email')
        remove_subscription_name = remove.get('remove_subscription_name')
        try:
            # Connect to db, use the email to get the user_id from the User table
            conn = get_db_connection()
            user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
            # User remove_subscription_name to get the co_id from the Company table
            co_id_row = conn.execute('SELECT co_id FROM COMPANY WHERE name = ?', (remove_subscription_name,)).fetchone()
            # Convert the row object to tuple
            user_id = tuple(user_id_row)[0]
            co_id = tuple(co_id_row)[0]
            
            # Update the end_date value of this subscripotion tuple with the current date.
            # Get the date of today (date when a HTTP post request is made), convert the format to match with the end_date filed in db
            end_date = date.today().strftime('%-m/%-d/%y')
            # Select the row in the subscription where user_id and co_id is equal to the posted user_id and co_id
            # Update the end_date value for the this selected row
            conn.execute('''
                UPDATE Subscription
                SET end_date = ?
                WHERE user_id = ? AND co_id = ?
            ''', (end_date, user_id, co_id)) 
            # Commit the pending transcation to db
            conn.commit()
            # Close the current connection
            conn.close()
            # Return response object to the front end 
            response= {
                'success': True,
                'msg': "Cancel Success"
            }
            return response
        
        # return request_fail response object if login verification failed
        except Exception as e:
            print("An error occurred:", str(e))
            return request_fail

# Define Edit Resource adding to the 'edit' endpoint
class Edit(Resource):
    def post(self):
        # parse post data as json 
        edit = request.get_json()
        email = edit.get('email')
        subscription_name = edit.get('edit_subscription_name')
        start_date = edit.get('edit_start_date')
        amount = edit.get('amount')
        subscription_cycle = edit.get('subscription_cycle')

        try:
            # use the email to get the user id from the User table
            # user the subscription_name to get co_id fro the Company table
            conn = get_db_connection()
            user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
            co_id_row = conn.execute('SELECT co_id FROM COMPANY WHERE name = ?', (subscription_name,)).fetchone()
            # convert the row object to tuple
            user_id = tuple(user_id_row)[0]
            co_id = tuple(co_id_row)[0]

            # update the attributes in the row of the Subscription table associated with the user_id and co_id sent from the client
            conn.execute('''
                    UPDATE Subscription
                    SET start_date = ?, amount = ?, subscription_cycle = ?
                    WHERE user_id = ? AND co_id = ?
                ''', (start_date, amount, subscription_cycle, user_id, co_id))  
            
            # return the success response 
            response = {
                'success': True,
                'msg': "Edit success"
            }
            conn.commit()
            conn.close()
            return response
        
        # return request_fail response object if login verification failed
        except Exception as e:
            print("An error occurred:", str(e))
            return request_fail
# Resourceful Routing¶ to access to multiple HTTP methods by defining methods 
# Register the resource UserSignUp with the '/signup' URL endpoint
api.add_resource(UserSignUp, '/signup')
api.add_resource(UserLogIn, '/login')
api.add_resource(Homepage, '/homepage')
api.add_resource(ListView, '/listview')
api.add_resource(ChartView, '/chartview')
api.add_resource(Remove, '/remove')
api.add_resource(Edit, '/edit')
# start the server and the flask application
if __name__ == "__main__":
    app.run(port=8000, debug=True)
