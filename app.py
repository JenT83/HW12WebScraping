from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_marsnews
# import scrape_marsfeaturedimage
# import scrape_marstwitter
# import scrape_marsfacts
# import scrape_marshemi

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#ex but will need to customize for HW
@app.route("/")
def index():
    mars_data = mongo.db.mars_news.find_one()
    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scraper():
    #scrape ex but will need 5
    # mars_news = mongo.db.mars_news
    mars_data = scrape_marsnews.scrape()
    mongo.db.mars_news.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
