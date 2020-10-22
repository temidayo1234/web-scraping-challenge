from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import missions_to_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/missions_to_mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    all_results = mongo.db.all_results.find_one()
    return render_template("index.html", all_results=all_results)

@app.route("/scrape")
def scraper():
    all_results = mongo.db.all_results
    results_data = missions_to_mars.scrape()
    all_results.update({}, results_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
