from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_dictionary_app")

@app.route("/")
def home():

    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_info)

@app.route("/scrape")
def scrape():

    mars_dictionary = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_dictionary, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)