from flask import Flask, render_template, url_for, request, session
from werkzeug.utils import redirect

import methods as Methods

app = Flask(__name__)

from dotenv import load_dotenv
from os import getenv
load_dotenv() 
FLASK_APP_KEY = getenv("APP_KEY")

app.secret_key = FLASK_APP_KEY


#route and url for the home page
@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = str(request.form["email-field"])
        password = str(request.form["pw-field"])
        
        response = Methods.loginMethod(email,password) 
    
        if (response == "Success"):
            session["email"] = email
            session["username"] = Methods.getUsername(email)
            return redirect(url_for("profile", user = session["username"], email = session["email"]))
        else:
            return render_template("login.html",login_fail = response)
    else:
        #if no input, refresh the page with no change
        return render_template("login.html")

@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == "POST":
        email = str(request.form["email-field"])
        username = str(request.form["username-field"])   
        password = str(request.form["pw-field"])
        
        response = Methods.signUpMethod(email,username,password)
        
        if response == "Success":
            session["email"] = email
            session["username"] = Methods.getUsername(email)
            return redirect(url_for("profile"), user = session["username"], email = session["email"])
        else:
            return render_template("register.html",signup_fail = response)
    else:
        #if no input, refresh the page with no change
        return render_template("register.html")

@app.route('/bingo')
def bingo():
    if "username" in session:
        return render_template("bingo.html",user = session["username"])
    else:
        return redirect(url_for(""))

@app.route('/profile')
def profile():
    if "username" in session:
        return render_template("profile.html",user = session["username"],email = session["email"])
    else:
        return render_template("profile.html")

app.debug = True
#Runs the app
if __name__=="__main__'":
    app.run(debug=True)

