#!/usr/bin/env python

from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import traceback
import dbconfig
import json
if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():
    crimes = []
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print(traceback.format_exc())
    return render_template("home.html", crimes=crimes)


@app.route("/add",methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(traceback.format_exc())
    return home()

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(traceback.format_exc())
    return home()

@app.route("/submitcrime",methods=["POST"])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_crime(category,date,latitude,longitude,description)
    return home()


@app.route("/cookies")
def cookies():
    cookies_str = ";".join([str(x)+"="+str(y) for x,y in request.cookies.items()])
    return cookies_str


@app.route("/ip")
def ip():
    return jsonify({"ip": request.remote_addr}),200

if __name__ == "__main__":
    app.run(port=5000,debug=True)
