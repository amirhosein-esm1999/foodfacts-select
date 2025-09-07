from flask import Flask, render_template,request , jsonify
from database import search_products
from database import get_all_brands , get_all_countries
import threading
import webbrowser


app = Flask(__name__)

@app.route("/", methods = ["GET"])
def homepage():
    return render_template("index.html")


@app.route("/datafilter.html" , methods = ["GET"])
def datafilter():
    return render_template("datafilter.html")

@app.route("/index.html" , methods = ["GET"])
def about():
    return render_template("index.html")

@app.route("/search", methods = ["POST"])
def search():
    data = request.json
    brand = data.get("brand" , "")
    country = data.get("country" , "")
    products = search_products(brand=brand , country=country)
    return jsonify(products)


@app.route("/brands", methods=["GET"])
def get_brands():
    brands = get_all_brands()  # Should return a list like
    return jsonify(brands)


@app.route("/countries" , methods = ["GET"])
def get_countries():
    countries = get_all_countries()
    return jsonify(countries)




def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.25, open_browser).start()
    app.run()
