import pandas as pd 
from flask import Flask, render_template, redirect
import scrape_mars
# Module used to connect Python with MongoDb
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsDB")


#Routes
@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data = mars_data)

# #/scrape
@app.route("/scrape")
def scrape_data():
    scraped_data = scrape_mars.scrape()
    mongo.db.collection.update({}, scraped_data, upsert=True)
    # return scraped_data
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
