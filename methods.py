from pymongo import MongoClient
import re
import json
import random


from dotenv import load_dotenv
from os import getenv


load_dotenv() 
MONGO_KEY = getenv("MONGO")

#MONGO STUFF --> DO NOT LEAK THIS KEY PLEASE
cluster=MongoClient(MONGO_KEY)
database = cluster["LiquidBingo"]
userCollection = database["Users"]
masterCollection = database["Admin_Valorant"]

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def loginMethod(email,password):
    
    if (userCollection.count_documents({"_id":email}) == 0):
        return "Account does not exist, consider signing up!"
    else:
        userPost = userCollection.find_one({"_id":email})
        if password == userPost["Password"]:
            return "Success"
        else:
            return "Incorrect email or password!"



def signUpMethod(email,username,password):
    if (userCollection.count_documents({"_id":email}) == 0):
        if checkEmail(email) == False:
            return "Please enter a valid email"
        elif len(username) < 3 or len(username) > 20:
            return "Please enter a username between 3-20 characters."
        elif len(password) < 3 or len(password) > 20:
            return "Please enter a password between 3-20 characters."

        userInitPost = {
            "_id":email,
            "Username":username,
            "Password":password,
            "Liquid+ Points":10000,
            "Bingo Wins":0,
            "Bingo":{}
        }
        userCollection.insert_one(userInitPost)
        resetBingo(email)
        return "Success"
    else:
        return "Account already exists"

def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def resetBingo(email):
    masterPost = masterCollection.find_one({"_id":"Valorant"})
    master = []
    for key in masterPost["items"]:
        master.append(key)
    print(master)

    userCollection.find_one_and_update({"_id":email},{"$set":{"Bingo":random.sample(master,25)}})

def getUsername(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Username"]

def getPassword(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Password"]

def getBingoPts(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Bingo Wins"]

def getUserBingo(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Bingo"]

def getLPts(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Liquid+ Points"]

def writeMasterJSON():
    masterPost = masterCollection.find_one({"_id":"Valorant"})
    with open ("static/js/master.json", 'w') as f:
        json.dump(masterPost["items"], f, indent=4)

def updateMaster(key,value):
    if value == "false":
        bool = True
    if value == "true":
        bool = False
    itemPath = "items."+key
    masterCollection.find_one_and_update({"_id":"Valorant"},{"$set":{itemPath:bool}})

def checkBingo(userInput,email):
    userPost = userCollection.find_one({"_id":email})
    userBoard = userPost["Bingo"]
    # print(userBoard)

    #only allow one bingo win
    if userPost["Bingo Wins"] == 1:
        return "You have already won the Bingo for this event! Check in again to play Free SpACE for future Team Liquid Valorant events!"
    else:

        masterPost = masterCollection.find_one({"_id":"Valorant"})
        masterPost["items"]

        #declare board that will contain spots where the user pressed a box AND the corresponding event is true in the database
        userPressedaAndValidBoard = [ [ None for i in range(5) ] for j in range(5) ]
        for row in range(0,5):
            for col in range(0,5):
                currentCellEvent = userBoard[row*5+col]

                if userInput[row][col] == "X" and masterPost["items"][currentCellEvent] == True:
                    userPressedaAndValidBoard[row][col] = "X"
                else:
                    userPressedaAndValidBoard[row][col] = ""
        
        if userInput[2][2] == "X":
            userPressedaAndValidBoard[2][2] = "X"

        print(userPressedaAndValidBoard)
        
        bingoBool = False
        # col check
        for col in range(5):
            colCheck = ""
            for (x) in range(5):
                colCheck += userPressedaAndValidBoard[x][col]
            if len(colCheck) == 5:
                print("bingo")
                bingoBool = True
            else:
                print("no bingo")

        # row check
        for row in range(5):
            rowCheck = ""
            for (x) in range(5):
                rowCheck += userPressedaAndValidBoard[row][x]
            if len(rowCheck) == 5:
                bingoBool = True

        # diagonal check
        diagCheck1 = ""
        for x in range(5):
            diagCheck1 += userPressedaAndValidBoard[x][x]
        diagCheck2 = ""
        for x in range(5):
            diagCheck2 += userPressedaAndValidBoard[x][4- x]

        if len(diagCheck1) == 5 or len(diagCheck2) == 5:
            bingoBool = True
            
        if bingoBool == True:
            userCollection.find_one_and_update({"_id":email},{"$inc":{"Bingo Wins":1}})
            userCollection.find_one_and_update({"_id":email},{"$inc":{"Liquid+ Points":50000}})
            return "Bingo! Congratulations, you have been award 50,000 Liquid+ Points!"
        else:
            return "Uh Oh! Not a Bingo! You need to select events that have happened!" 


        

  


# userInput = [['X', 'X', 'X', 'X', 'X'], ['O', 'O', 'O', 'O', 'O'], ['O', 'O', 'X', 'O', 'O'], ['O', 'O', 'O', 'O', 'O'], ['X', 'X', 'X', 'X', 'X']]
# print(signUpMethod("ivanyu@gmail.com","weewoo","123"))

# checkBingo(userInput,"ivanyu@gmail.com")