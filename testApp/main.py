#import framework and extensions
from flask import Flask, request, redirect, jsonify
import tkinter as tk
from flask_restful import Api, Resource
# from flask_sqlalchemy import SQLAlchemy
import sqlite3, json


#initialize this flask application, api 
app = Flask(__name__)
api = Api(app)


# connect to the sql database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn
# Example resource class for user login
class UserSignUp(Resource):
    def get(self):
        try:
            users_list = []
            conn = get_db_connection()
            # exists_ids = conn.execute('SELECT sub_id from Subscription').fetchall() 
            # while(sub_id in exists_ids):
            # sub_id += sub_id
            for row in conn.execute('SELECT name FROM User').fetchall():
                users_list.append(row['name'])

            conn.commit()
            conn.close()
            return json.dumps(users_list) 
            # return redirect('/sigup')
            
        except:
            return "Opps! 🫠"
        
    def post(self):
        usr_data = request.get_json()  
        name = usr_data.get('name')
        email = usr_data.get('email')
        password = usr_data.get('password_hashed')

        try:
            conn = get_db_connection()
            conn.execute('''INSERT OR REPLACE INTO User
                (name, email, password_hashed) VALUES (?, ?, ?)''',
                (name, email, password))

            new_users=[]
            for row in conn.execute('SELECT * FROM User').fetchall():
                new_users.append(row)
            new_users = [tuple(row) for row in new_users]
            conn.commit()
            conn.close()
            # for x in new_users:
            #     print(x)
            return redirect('/signup')
        
        except Exception as e:
            print("An error occurred:", str(e))
            return "Oops! There was an issue signing you up."
        
# Add the API resource to the app
api.add_resource(UserSignUp, '/signup')


# @app.route("/home", methods=["POST", "GET"])
# def process_request():
#     if request.method =="POST":

#             usr_data = request.get_json()  
#             name = usr_data.get('name')
#             email = usr_data.get('email')
#             password = usr_data.get('password')

#             response_data = {
#                 'name': 'Celine',
#                 'email': 'mangolzj@gmail.com',
#                 'password': "hfadksjfhapiufweb"
#             }
#             try:
#                 conn = get_db_connection()
#                 exists_ids = conn.execute('SELECT sub_id from Subscription').fetchall() 
#                 while(sub_id in exists_ids):
#                     sub_id += sub_id
#                 conn.execute('''INSERT OR REPLACE INTO Subscription
#                     (Sub_id, user_id, co_id, start_date, amount, subscription_cycle) VALUES (?, ?, ?, ?, ?, ?)''',
#                     (sub_id, user_id, service_id, start_date, amount, sub_cycle))
#                 conn.commit()
#                 conn.close()
#                 return redirect("/home")

#             except:
#                 return "There was an issue adding this subscription"
        
#     else:
#         conn = get_db_connection()
#         subscriptions = conn.execute('SELECT * FROM Subscription INNER JOIN Company on Subscription.co_id = Company.co_id WHERE user_id = 1' ).fetchall()
#         conn.close()
#         # return render_template('index.html', subscriptions = subscriptions)
#         return "hello"

# start the server and the flask application
if __name__ == "__main__":
    app.run(port=8000, debug = True)

