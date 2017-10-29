from flask import Flask
from flask_pymongo import PyMongo
import pprint

app = Flask(__name__)
mongo = PyMongo(app)


if __name__ == '__main__':
    print(__name__)
    pprint.pprint(dir(app))