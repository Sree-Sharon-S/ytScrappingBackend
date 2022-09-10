from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymongo
import certifi

ca = certifi.where()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

'''
clientmongo = pymongo.MongoClient("mongodb+srv://user0:1a2b3c4d@cluster0.dvd6clz.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
dbmo = clientmongo.test

database = clientmongo['projects']
collection = database['YTScrapping']
'''

from finalscrapper import routes

