import scrape_mars
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_coll_app")

@app.route("/")
def home():
    mars_rec_find = mongo.db.mars_collection.find_one()
    return render_template("index.html", mars_dictionary=mars_rec_find)

@app.route("/scrape")
def scrape():
    mars_dictionary = scrape_mars.scrape_all()
    mongo.db.mars_collection.update({}, mars_dictionary, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)