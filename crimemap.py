#!/usr/bin/env python

from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import flash, redirect, url_for
import traceback
import dbconfig
import json
import dateparser
import datetime
import string

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

categories = ["mugging", "break-in"]

@app.route("/")
def home(error_message=None):
    crimes = []
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print(traceback.format_exc())
    return render_template("home.html", crimes=crimes, categories=categories
                           , error_message=error_message)


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
    if category not in categories:
        flash("%s not in categories:%s" %(category, categories))
        return redirect(url_for("home"))
    date = request.form.get("date")
    if not date:
        return home("Invaild date. please use yyyy-mm-dd format")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        flash(traceback.format_exc())
        return redirect(url_for("home"))
    description = request.form.get("description")
    description = sanitize_string(description)
    DB.add_crime(category,date,latitude,longitude,description)
    return home()


@app.route("/cookies")
def cookies():
    cookies_str = ";".join([str(x)+"="+str(y) for x,y in request.cookies.items()])
    return cookies_str


@app.route("/ip")
def ip():
    return jsonify({"ip": request.remote_addr}),200


def format_date(userdata):
    date = dateparser.parse(userdata)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;-'&"""
    return filter(lambda x: x in whitelist, userinput)

if __name__ == "__main__":
    app.run(port=5000,debug=True)
