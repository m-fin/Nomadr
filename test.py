from flask import Flask, flash, jsonify, redirect, render_template, request, session
import folium
import pandas
import mysql.connector
import sqlite3

import logging

# Configure CS50 Library to use SQLite database
connector = sqlite3.connect('database.db')
db = connector.cursor()

def index():
    db.execute('INSERT INTO users (id, username, password) VALUES (?, ?, ?)', (6, "test69", "test69"))
    connector.commit
    test = db.execute('SELECT username FROM users WHERE id = 6')
    print(test.fetchone()[0])


index()