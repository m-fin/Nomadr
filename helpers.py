from flask import redirect, render_template, request, session

def apology(message, code):
    return render_template("error.html", code=code, message=message)