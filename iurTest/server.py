from flask import *
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import numpy as numpy
import os 


app = Flask(__name__)
app.config.update(
	SESECRET_KEY="super_secret_key",
)

api = Api(app)

@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8888)