# import the libraries to be used in this app
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


# start the server and the flask application
if __name__ == "__main__":
    app.run(debug = True)
