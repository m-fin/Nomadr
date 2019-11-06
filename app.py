from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file

import mysql.connector
import sqlite3

import folium
import pandas

import os
import logging

import pygeoip

from helpers import apology, makeMap

# To set to debug mode:
# export FLASK_DEBUG=1

# Configure app
app = Flask(__name__)

# secret key
app.secret_key = "93182467741328904107"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Connect database
connector = sqlite3.connect('database.db')
db = connector.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # result = db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))
        result = db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))

        if not result:
            return 400

        connector.commit()

        session["user_id"] = ("SELECT id FROM users WHERE username = ?", (username,))

        return redirect("/map")
    else:
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username.", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password.", 400)

        username = request.form.get("username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        # Ensure username exists and password is correct
        if not rows.fetchone():
            return apology("Invalid username and/or password.", 400)

        # Remember which user has logged in
        session["user_id"] = rows.fetchone()

        # Redirect user to home page
        return redirect("/map")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/mapEmbed')
def show_map():
    makeMap()
    return send_file('maps/mapEmbed.html')

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        app.logger.info("999999900614783416801947839147213490789147314807823478923147894708941370814237809124387912347890140798431")
        # connector.commit()

        # dummy data
        # lat = [(49.060329), (50.060329)]
        # lon = [(-122.462227), (-123.462227)]
        # title = [("title0"), ("title1")]
        # description = [("desc0"), ("desc1")]

        latitude = request.form.get("inputLatitude")
        longitude = request.form.get("inputLongitude")
        title = request.form.get("inputTitle")
        description = request.form.get("inputDescription")
        locType = request.form.get("inputType")

        db.execute('INSERT INTO locations (latitude, longitude, title, description, locType) VALUES (?, ?, ?, ?, ?)', (latitude, longitude, title, description, locType))
        connector.commit()
        
        # for lt,ln,nm,ds in zip(latitude,longitude,title,description):
        #     db.execute('INSERT INTO locations (latitude, longitude, title, description) VALUES (?, ?, ?, ?)', (lt, ln, nm, ds))
        #     # db.execute('INSERT INTO locations (lat, long) VALUES (?, ?)', (lat, lon))

        return redirect("/map")
    else:
        return render_template("add.html")
