#!/usr/bin/env python

from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request

import traceback

app = Flask(__name__)
DB = DBHelper()

@app.route("/")
def home():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print(traceback.format_exc())
    return render_template("home.html",data=data)

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


if __name__ == "__main__":
    app.run(port=5000,debug=True)