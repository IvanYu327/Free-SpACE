from pymongo import MongoClient
import re


from dotenv import load_dotenv
from os import getenv
load_dotenv() 
MONGO_KEY = getenv("MONGO")

#MONGO STUFF --> DO NOT LEAK THIS KEY PLEASE
cluster=MongoClient(MONGO_KEY)
database = cluster["LiquidBingo"]
userCollection = database["Users"]

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def loginMethod(email,password):
    
    if (userCollection.count_documents({"_id":email}) == 0):
        return "Account does not exist, consider signing up!"
    else:
        userPost = userCollection.find_one({"_id":email})
        if password == userPost["Password"]:
            return "Success"
        else:
            return "Incorrect username or password!"



def signUpMethod(email,username,password):
    if (userCollection.count_documents({"_id":email}) == 0):
        if checkEmail(email) == False:
            return "Please enter a valid email"
        elif len(username) < 4 or len(username) > 20:
            return "Please enter a username between 4-20 characters."
        elif len(password) < 4 or len(password) > 20:
            return "Please enter a password between 4-20 characters."

        userInitPost = {
            "_id":email,
            "Username":username,
            "Password":password,
            "Points":0
        }
        userCollection.insert_one(userInitPost)
        return "Success"
    else:
        return "Account already exists"

def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


def getUsername(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Username"]

def getPassword(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Password"]
