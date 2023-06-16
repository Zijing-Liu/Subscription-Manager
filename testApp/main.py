# import framework and extensions
from flask import Flask, request, redirect
import tkinter as tk
from flask_restful import Api, Resource
# from flask_sqlalchemy import SQLAlchemy
import sqlite3

# initialize this flask application, api
app = Flask(__name__)
api = Api(app)

# define a function to connect to the sql database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Define a resource class for the user Signup endpoint
class UserSignUp(Resource):
    # define the get method that fetch all the user data from the data.db database and return the data as a list of tuple named users_list
    def get(self):
        try:
            users_list = []
            conn = get_db_connection()
            for row in conn.execute('SELECT * FROM User').fetchall():
                users_list.append(row)
            users_list = [tuple(row) for row in users_list]
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
        password = usr_data.get('password_hashed')
        try:
            conn = get_db_connection()
            conn.execute('''INSERT OR REPLACE INTO User
                (name, email, password_hashed) VALUES (?, ?, ?)''',
                         (name, email, password))
            conn.commit()
            conn.close()
            return redirect('/signup')

        except Exception as e:
            print("An error occurred:", str(e))
            return "Oops! There was an issue signing you up."

# Register the resource UserSignUp with the '/signup' URL endpoint
api.add_resource(UserSignUp, '/signup')

# start the server and the flask application
if __name__ == "__main__":
    app.run(port=8000, debug=True)
