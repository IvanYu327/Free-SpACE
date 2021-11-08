from flask import Flask, render_template, url_for, request

import login as Login

app = Flask(__name__)



#route and url for the home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=["POST","GET"])
def login():
    
    if request.method == "POST":
        
        username = str(request.form["username-field"])
        password = str(request.form["pw-field"])
        
        if (Login.loginMethod(username,password)):
            return render_template("bingo.html")
        else:
            return render_template("login.html",login_fail = "Username or Password is incorrect!")
    else:
        #if no input, refresh the page with no change
        return render_template("login.html")

@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == "POST":
        
        username = str(request.form["username-field"])
        password = str(request.form["pw-field"])
        
        if (Login.signUpMethod(username,password)):
            return render_template("bingo.html")
        else:
            return render_template("login.html",login_fail = "Username exists!")
    else:
        #if no input, refresh the page with no change
        return render_template("register.html")


#Runs the app
if __name__=="__main__'":
    app.run(debug=True, use_debugger=False, use_reloader=False)

