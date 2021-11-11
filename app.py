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
            if email == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("bingo"))
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
            return redirect(url_for("bingo"))
        else:
            return render_template("register.html",signup_fail = response)
    else:
        #if no input, refresh the page with no change
        return render_template("register.html")

@app.route('/bingo', methods=["POST","GET"])
def bingo():
    if request.method == "POST":
        print("owo")
        
        # rows, cols = (5, 5)
        userInput = [ [ None for i in range(5) ] for j in range(5) ]
        
        for row in range(0,5):
            for col in range(0,5):
                text = "bingo-field-"+str(row*5+col+1)
                if str(request.form.getlist(text)) == "['on']":
                    userInput[row][col]="X"
                else:
                    userInput[row][col]="O"

        print(userInput)

    if "username" in session:
        bingo = Methods.getUserBingo(session["email"])
        return render_template("bingo.html", user = session["username"], email = session["email"], bingos = Methods.getBingoPts(session["email"]),
        b1 = bingo[0],
        b2 = bingo[1],
        b3 = bingo[2],
        b4 = bingo[3],
        b5 = bingo[4],
        b6 = bingo[5],
        b7 = bingo[6],
        b8 = bingo[7],
        b9 = bingo[8],
        b10 = bingo[9],
        b11 = bingo[10],
        b12 = bingo[11],
        b13 = bingo[12],
        b14 = bingo[13],
        b15 = bingo[14],
        b16 = bingo[15],
        b17 = bingo[16],
        b18 = bingo[17],
        b19 = bingo[18],
        b20 = bingo[19],
        b21 = bingo[20],
        b22 = bingo[21],
        b23 = bingo[22],
        b24 = bingo[23],
        b25 = bingo[24],)
    else:
        return redirect(url_for(""))

@app.route('/admin')
def admin():
    if "username" in session and session["username"] == "admin":
        Methods.writeMasterJSON()
        master = [1,2]
        return render_template("admin.html")
    else:
        return redirect(url_for(""))


app.debug = True
#Runs the app
if __name__=="__main__'":
    app.run(debug=True)

