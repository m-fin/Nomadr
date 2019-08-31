from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file


import mysql.connector
import sqlite3

import folium
import pandas

import os
import logging

from helpers import apology

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

    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        result = db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))

        if not result:
            return 400

        connector.commit()

        session["user_id"] = ("SELECT id FROM users WHERE username = ?", (username,))

        return redirect("/")
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
        return redirect("/")

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

@app.route('/maps/mapEmbed.html')
def show_map():
    return send_file("mapEmbed.html")

@app.route('/add')
def add():
    return render_template("add.html")