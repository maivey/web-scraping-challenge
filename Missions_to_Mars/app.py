import pandas as pd 
from flask import Flask, render_template, redirect
import scrape_mars
# Module used to connect Python with MongoDb
# import pymongo
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsDB")


#Routes
@app.route("/")
def index():
    # client = pymongo.MongoClient("localhost", 27017)
    # db = client.marsDB
    # mongo = PyMongo(app, uri="mongodb://localhost:27017/marsDB")
    # mars_data = mongo.db.marsData.find_one()
    mars_data = mongo.db.collection.find_one()

    return render_template("index.html", mars_data = mars_data)

# #/scrape
@app.route("/scrape")
def scrape_data():
    # mars_data = mongo.db.marsData
    scraped_data = scrape_mars.scrape()
    ## client = pymongo.MongoClient("localhost", 27017)
    ## db = client.marsDB
    ## marsData = db.marsData
    ## mars_data.update({}, scraped_data, upsert=True)

    mongo.db.collection.update({}, scraped_data, upsert=True)
    # return scraped_data
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
