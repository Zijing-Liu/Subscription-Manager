# import framework and extensions
from flask import Flask, request, redirect
import tkinter as tk
from flask_restful import Api, Resource
# from flask_sqlalchemy import SQLAlchemy
import sqlite3, bcrypt, json
from datetime import date

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
                    'success': False,
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
                print("Successfully written to database.")
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


class ListView(Resource):
    # post method to get all the subscription data from the database and send the response to the GUI for display
    def post(self):
        # parse the post request data as json
        print("start posting")
        user = request.get_json()
        print(user)
        # get each value of the json data and write into new variables
        email = user.get('email')
        print("this is the user email: " + email)

        try:
            # use the email to get the user id from the User table
            conn = get_db_connection()
            print("connected to database")
            user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
            # convert the row object to tuple
            user_id = tuple(user_id_row)[0]
            print(type(user_id))
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
            # return response as JSON data
            response = {
                'all_subscriptions': subscriptions_list,
            }
            conn.commit()
            conn.close()
            return response
            
        except Exception as e:
            print("An error occurred:", str(e))
            response2 = {
                'success': False,
                'msg': str(e)
            }
            return response2

class ChartView(Resource):
    # post method to get all the subscription data from the database and send the response to the GUI for display
    def post(self):
        user = request.get_json()
        print(user)
        # get each value of the json data and write into new variables
        email = user.get('email')

        try:
            # use the email to get the user id from the User table
            conn = get_db_connection()
            print("connected to database")
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
            subscriptions = conn.execute('SELECT SUB.start_date, SUB.subscription_cycle, SUB.end_date, SUB.amount FROM SUBSCRIPTION AS SUB JOIN COMPANY AS CO ON CO.co_id = SUB.co_id WHERE SUB.user_id = ?', (user_id,)).fetchall()
            # Use list to store all the subscription tuple data
            subscriptions_list = []
            for row in subscriptions:
                subscriptions_list.append(row)
            subscriptions_list = [tuple(row) for row in subscriptions_list]
            response = {
                'success': True,
                'msg': "Fetch data success",
                'data': subscriptions_list      
            }
            conn.commit()
            conn.close()

            return response
            
        except Exception as e:
            print("An error occurred:", str(e))
            response2 = {
                'success': False,
                'msg': str(e),
                'data': []
            }
            return response2

class Cancel(Resource):
    def post(seld):
        # parse the post request data as json
        cancel = request.get_json()
        print(cancel)
        # get each value of the json data and write into new variables
        email = cancel.get('email')
        subscription_name = cancel.get('cancel_subscription_name')

        try:
            # use the email to get the user id from the User table
            conn = get_db_connection()
            print("connected to database")
            user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
            co_id_row = conn.execute('SELECT co_id FROM COMPANY WHERE name = ?', (subscription_name,)).fetchone()
            # convert the row object to tuple
            user_id = tuple(user_id_row)[0]
            co_id = tuple(co_id_row)[0]
            
            
            exist = conn.execute('SELECT * FROM Subscription WHERE user_id = ? and co_id = ?', (user_id, co_id, )).fetchone()
            if exist == None:
                respone1 = {
                'success': False,
                'msg': "Cannot find this subscription"   
                }
                return respone1 
            # if posted subscrition is valid, update the end_date value of this subscripotion tuple with the current date.
            end_date = date.today().strftime('%-m/%d%y')
            print(end_date)
            conn.execute('''
                UPDATE Subscription
                SET end_date = ？
                WHERE user_id = ? AND co_id = ?
            ''', (end_date, user_id, co_id))     

            response2 = {
                'success': True,
                'msg': "Cancel Success"
            }
            return response2
        

        except Exception as e:
            print("An error occurred:", str(e))
            response3 = {
                'success': False,
                'msg': str(e)
            }
            return response3

class Edit(Resource):
    def post(self):
        edit = request.get_json()
        email = edit.get('email')
        subscription_name = edit.get('edit_subscription_name')
        start_date = edit.get('start_date')
        amount = edit.get('amount')
        subscription_cycle = edit.get('subscription_cycle')
    
        try:
                # use the email to get the user id from the User table
                conn = get_db_connection()
                print("connected to database")
                user_id_row = conn.execute('SELECT user_id FROM USER WHERE email = ?', (email,)).fetchone()
                co_id_row = conn.execute('SELECT co_id FROM COMPANY WHERE name = ?', (subscription_name,)).fetchone()
                # convert the row object to tuple
                user_id = tuple(user_id_row)[0]
                co_id = tuple(co_id_row)[0]
                conn.execute('''
                        UPDATE Subscription
                        SET start_date = ?, amount = ?, subscription_cycle = ?
                        WHERE user_id = ? AND co_id = ?
                    ''', (start_date, amount, subscription_cycle, user_id, co_id))  

        except Exception as e:
            print("An error occurred:", str(e))
            response3 = {
                'success': False,
                'msg': str(e)
            }
            return response3    
                
            
        return
    
# Register the resource UserSignUp with the '/signup' URL endpoint
api.add_resource(UserSignUp, '/signup')
api.add_resource(UserLogIn, '/login')
api.add_resource(Homepage, '/homepage')
api.add_resource(ListView, '/listview')
api.add_resource(ChartView, '/chartview')
api.add_resource(Cancel, '/cancel')
api.add_resource(Edit, '/edit')
# start the server and the flask application
if __name__ == "__main__":
    app.run(port=8000, debug=True)
