#import framework and extensions
from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import sqlite3

#initialize this flask application, api 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///test.db"
#initialize the database
# db = SQLAlchemy()

#create a class model
# class SubscriptionsModel(db.Model):
#     sub_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     user_id = db.Column(db.Integer, primary_key=False, nullable=False)
#     co_id = db.Column(db.Integer, primary_key=False, nullable=False)
#     start_date = db.Column(db.DateTime, default = datetime.utcnow, nullable=True)
#     subscription_cycle = db.Column(db.String(200), primary_key=False, nullable=True)

#     def __repr__(self):
#         return '<Subscription %r>' % self.sub_id
# db.init_app(app)
# connect to the sql database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["POST", "GET"])
def index():
    
    if request.method =="POST":
        sub_id = random.randint(0, 1000)
        service_id = request.form["service_id"]
        user_id = request.form["user_id"]
        start_date = request.form["start_date"]
        amount = request.form["amount"]
        sub_cycle = request.form["cycle"]

        try:
            conn = get_db_connection()
            exists_ids = conn.execute('SELECT sub_id from Subscription').fetchall() 
            while(sub_id in exists_ids):
                sub_id += sub_id
            conn.execute('''INSERT OR REPLACE INTO Subscription
                (Sub_id, user_id, co_id, start_date, amount, subscription_cycle) VALUES (?, ?, ?, ?, ?, ?)''',
                (sub_id, user_id, service_id, start_date, amount, sub_cycle))
            conn.commit()
            conn.close()
            return redirect("/")

        except:
            return "There was an issue adding this subscription"
    
    else:
        conn = get_db_connection()
        subscriptions = conn.execute('SELECT * FROM Subscription INNER JOIN Company on Subscription.co_id = Company.co_id WHERE user_id = 1' ).fetchall()
        conn.close()
        return render_template('index.html', subscriptions = subscriptions)


# start the server and the flask application
if __name__ == "__main__":
    app.run(port=3000, debug = True)

