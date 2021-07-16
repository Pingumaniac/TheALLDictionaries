from flask import Flask, Blueprint, g, render_template, request, redirect, url_for, session, jsonify, flash, escape
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from python.dictionaries import *
from python.thealldictionariesAPI import DB
import time
import datetime
import requests
import re
from chat_pages import chat_pages
from error_pages import error_pages
from game_pages import game_pages
from my_pages import my_pages

# Codes for initialising the flask application
app = Flask(__name__)
app.register_blueprint(error_pages)
app.register_blueprint(my_pages)
app.register_blueprint(chat_pages)
app.register_blueprint(game_pages)
app.secret_key = "pingu moon".encode('utf8')
app.config['USE_SESSION_FOR_NEXT'] = True

# Code for using flask-bootstrap
bootstrap = Bootstrap(app) 

"""
function before_request is executed before the first request is made.
There is a separate function called teardown_request which is executed once every request has been completed.
Since teardown_request is not needed for this application, I have not created.
e.g. if teardown_request is used to disconnect the database, every time the client has finished its request,
the database will be disconnected and therefore have to reconnect the database whenever he or she makes a new request.

g is a global variable for flask. Hence I have used the variable 
1. g.dbObject to maintain the connection til the client closes the web applicaiton,
2. g.userID to store the userID and thereby not use try except method to check the userID for each page
"""
@app.before_request
def before_request():
    if 'dbObject' not in g:
        g.dbObject = DB()
    else:
        g.dbObject.connectDB()

    if 'userID' in session:
        g.userID = str(escape(session['userID']))
        checkAdmin = g.dbObject.checkAdmin(g.userID)
        
         # Case: the user has not deleted its account
        if checkAdmin != None:
            g.adminStatus = checkAdmin[0]
        # Case: the user has deleted its account
        else: 
            g.adminStatus = None
    else:
        g.userID = None
        g.adminStatus = None

"""
HTTP status code 400 is given when there is a bug while running the app locally.
To check the cause of the bug, 
1. Make bad_request + page400 functions have been commented(?)
2. Make sure you are running the app in debug mode (it is currently executed in debug mode though)
"""
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html', userID = g.userID, adminStatus = g.adminStatus), 400

#HTTP status code 404 is given when there is no such page for the given URL.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', userID = g.userID, adminStatus = g.adminStatus), 404
    
@app.errorhandler(408)
def request_timeout(e):
    return render_template('408.html', userID = g.userID, adminStatus = g.adminStatus), 408

"""
HTTP status code 410 is given when the page for the corresponding URL has been deleted from the server(?),
but the data for this page is stored in the cache of the client's computer.
"""
@app.errorhandler(410)
def gone(e):
    return render_template('410.html', userID = g.userID, adminStatus = g.adminStatus), 410

@app.errorhandler(429)
def too_many_requests(e):
    return render_template('429.html', userID = g.userID, adminStatus = g.adminStatus), 429

@app.errorhandler(431)
def request_header_fields_too_large(e):
    return render_template('431.html', userID = g.userID, adminStatus = g.adminStatus), 431

@app.errorhandler(451)
def unavailable_for_legal_reasons(e):
    return render_template('451.html', userID = g.userID, adminStatus = g.adminStatus), 451

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', userID = g.userID, adminStatus = g.adminStatus), 500

"""
Heroku handles each request for maximum 30 seconds as described in the following page:
https://devcenter.heroku.com/articles/request-timeout

I have noted that when the client enters an invalid(?) input for search e.g. arlhgkaerhblgaerkgrae
When deployed in Heroku, the application cannot give output in 30 seconds.
But when the app is runned locally, I do not face this problem.
I have optimised dictionaries.py by removing JSON.dumps() and JSON.load() b/c that is just a repetitive work for 
creating a JSON file and interpreting a JSON file but still the app cannot fully give a result in 30 seconds 
when deployed in Heroku.

Hence I have made a custom web page and displayed a possible reason for the timeout.
"""
@app.errorhandler(503)
def service_unavailable(e):
    return render_template('503.html', userID = g.userID, adminStatus = g.adminStatus), 503

@app.route('/mwcDict/<string:word>', methods = ['GET'])
def getMwcDict(word):
    if request.method == 'GET':
        return mwcDict(word), 200
    
@app.route('/mwlDict/<string:word>', methods = ['GET'])
def getMwlDict(word):
    if request.method == 'GET':
        return mwlDict(word), 200

@app.route('/oxfordDict/<string:word>', methods = ['GET'])
def getOxfordDict(word):
    if request.method == 'GET':
        return oxfordDict(word), 200
    
@app.route('/urbanDict/<string:word>', methods = ['GET'])
def getUrbanDict(word):
    if request.method == 'GET':
        return urbanDict(word), 200
    
@app.route('/wordnetDict/<string:word>', methods = ['GET'])
def getWordNetDict(word):
    if request.method == 'GET':
        return wordnetDict(word), 200

@app.route('/synonymDict/<string:word>', methods = ['GET'])
def getSynonymDict(word):
    if request.method == 'GET':
        synonyms, antonyms = synonymDict(word)
        return json.dumps({"synonyms": synonyms, "antonyms": antonyms}), 200

@app.route('/wikipedia/<string:word>', methods = ['GET'])
def getWikiDict(word):
    if request.method == 'GET':
        return wikiDict(word), 200

@app.route('/wiktionaryDict/<string:word>', methods = ['GET'])
def getWiktionaryDict(word):
    if request.method == 'GET':
        return wiktionaryDict(word), 200

@app.route('/googleNewsDict/<string:word>', methods = ['GET'])
def getGoogleNewsDict(word):
    if request.method == 'GET':
        return googleNewsDict(word), 200

@app.route('/youtubeDict/<string:word>', methods = ['GET'])
def getYouTubeDict(word):
    if request.method == 'GET':
        return youtubeDict(word), 200

@app.route('/about', methods = ['GET'])
def about():
    if request.method == 'GET':
        return render_template('about.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/', methods = ['GET'])
@app.route('/search', methods = ['GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/searchResult', methods = ['GET', 'POST'])
def searchResult():
    defaultOrderList = ["mwl", "mwc", "oxford", "free", "yourdictionary", "urban", "etymonline", "wordnik", "wordnet", "synonym", "wikipedia", "wiktionary", "news", "images", "youtube", "visuwords"]
    word = request.form['word']

    googleImages = googleImageDict(word)
    
    # Case: the user has logged in and is trying to look up a word
    if g.userID != None and g.adminStatus == 0:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        g.dbObject.addSearchHistory(g.userID, timestamp, word)
        
        sourceTable = g.dbObject.getSourceOrder(g.userID)
        sourceOrderList = []
        
        for source in sourceTable:
            sourceOrderList.append(source[0])
        
        return render_template("searchResult.html", word = word, googleImages = googleImages,
                               userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = sourceOrderList)

    # Executed when the client has not logged in or when the client is an administrator
    return render_template("searchResult.html", word = word, googleImages = googleImages,
                           userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = defaultOrderList)

# Used to display the search result of the word shown in the page (used for hyperlink)
@app.route('/searchResult/<string:word>', methods = ['GET', 'POST'])
def searchWordResult(word):
    defaultOrderList = ["mwl", "mwc", "oxford", "free", "yourdictionary", "urban", "etymonline", "wordnik", "wordnet", "synonym", "wikipedia", "wiktionary", "news", "images", "youtube", "visuwords"]

    googleImages = googleImageDict(word)
    
    # Case: the user has logged in and is trying to look up a word
    if g.userID != None and g.adminStatus == 0:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        g.dbObject.addSearchHistory(g.userID, timestamp, word)
        
        sourceTable = g.dbObject.getSourceOrder(g.userID)
        sourceOrderList = []
        
        for source in sourceTable:
            sourceOrderList.append(source[0])
        
        return render_template("searchResult.html", word = word,  googleImages = googleImages,
                               userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = sourceOrderList)
    
    # Executed when the client has not logged in or when the client is an administrator
    return render_template("searchResult.html", word = word, googleImages = googleImages,
                           userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = defaultOrderList)

@app.route('/changeDictionaryOrder', methods = ['GET', 'POST'])
def changeDictionaryOrder():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access Change Dictionary Page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            return render_template("changeDictionaryOrder.html", userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        dictOrderList = []
        sourceList = []

        for i in range(1, 17):
            order = 'order' + str(i)
            value = str(request.form.get(order))
            dictOrderList.append(value)
        
        # Code for checking if there are duplicates    
        dictOrderSet = set(dictOrderList)
        haveDuplicates = len(dictOrderList) != len(dictOrderSet)

        if haveDuplicates == True:
            msg = "Update failed. For each order, the sources shall be different."
            flash(msg)
        else:
            for value in dictOrderList:
                if value == "1":
                    sourceList.append("mwl")
                if value == "2":
                    sourceList.append("mwc")
                if value == "3":
                    sourceList.append("oxford")
                if value == "4":
                    sourceList.append("free")
                if value == "5":
                    sourceList.append("yourdictionary")
                if value == "6":
                    sourceList.append("urban")
                if value == "7":
                    sourceList.append("etymonline")
                if value == "8":
                    sourceList.append("wordnik")
                if value == "9":
                    sourceList.append("wordnet")
                if value == "10":
                    sourceList.append("synonym")
                if value == "11":
                    sourceList.append("wikipedia")
                if value == "12":
                    sourceList.append("wiktionary")
                if value == "13":
                    sourceList.append("news")
                if value == "14":
                    sourceList.append("images")
                if value == "15":
                    sourceList.append("youtube")
                if value == "16":
                    sourceList.append("visuwords")
            
            g.dbObject.updateSourceOrder(g.userID, sourceList[0], sourceList[1], sourceList[2], sourceList[3], 
                                         sourceList[4], sourceList[5], sourceList[6], sourceList[7], sourceList[8], 
                                         sourceList[9], sourceList[10], sourceList[11], sourceList[12], sourceList[13], 
                                         sourceList[14], sourceList[15])
            
            msg = "The order of the sources have been successfully updated"
            flash(msg)
            return redirect(url_for('search')) 

@app.route('/signin', methods =['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html', userID = g.userID)
    
    if request.method == 'POST' and 'userID' in request.form and 'password' in request.form:
        userID = request.form['userID']
        password = request.form['password']
        encryptedPassword = generate_password_hash(password)
        accountExistence = g.dbObject.checkAccountExistence(userID)[0]
        
        # Case: No corresponding account with the userID inputed
        if accountExistence == 0:
            msg = "There is no such account created with the userID inputted."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            adminStatus = g.dbObject.checkAdmin(userID)[0]
            
            # Case: the corresponding account with the userID inputed is an UserAccount
            if adminStatus == 0:
                accountID, accountPassword = g.dbObject.getUserIDandPassword(userID)
                # Case: the user has entered its password correctly
                if userID == accountID and check_password_hash(accountPassword, password):
                    session['userID'] = accountID
                    g.userID = accountID
                    g.adminStatus = 0
                    return redirect(url_for('search')) 
                # Case: the user has not entered its password correctly.
                if userID == accountID and encryptedPassword != accountPassword:
                    msg = 'Incorrect password !'
                    flash(msg)
                    return redirect(url_for('signin')) 
            # Case: the corresponding account with the userID inputed is an AdminAccount    
            if adminStatus == 1:
                accountID, accountPassword = g.dbObject.getAdminIDandPassword(userID)
                # Case: the admin has entered its password correctly
                if userID == accountID and check_password_hash(accountPassword, password):
                    session['userID'] = accountID
                    g.userID = accountID
                    g.adminStatus = 1
                    return redirect(url_for('search')) 
                # Case: the admin has not entered its password correctly
                if userID == accountID and encryptedPassword != accountPassword:
                    msg = 'Incorrect password !'
                    flash(msg)
                    return redirect(url_for('signin')) 
  
@app.route('/signout')
def signout():
    session.pop('userID', None)
    g.dbObject.disconnectDB() # Remove the connection with the database as there is no need after signing out
    return redirect(url_for('search'))

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    if request.method == 'GET':
         return render_template('signup.html', userID = g.userID)
     
    if request.method == 'POST' and 'userID' in request.form and 'password' in request.form and 'confirmpassword' in request.form and 'email' in request.form and 'name' in request.form and 'nickname' in request.form and 'phoneNumber' in request.form:
        userID = request.form['userID']
        isAdmin = False
        fullName = request.form['name']
        nickName = request.form['nickname']
        password = request.form['password']
        confirmPassword = request.form['confirmpassword']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        isPremium = False
        
        encryptedPassword = generate_password_hash(password)
        
        if userID == None or fullName == None or nickName == None or password == None or confirmPassword == None or email == None or phoneNumber == None:
            msg = 'Please fill out the form!'
            flash(msg)
            return redirect(url_for('signup')) 
        elif password != confirmPassword:
            msg = 'Please confirm your password again.'
            flash(msg)
            return redirect(url_for('signup')) 
        else:
            accountExistence = g.dbObject.checkAccountExistence(userID)[0]

            # Case: There is already an account with same userID
            if accountExistence == 1:
                msg = 'Account already exists !'
                flash(msg)
                return redirect(url_for('signup')) 
            # Case: the form has not been filled out completely.
            elif not userID or not password or not email:
                msg = 'Please fill out the form !'
                flash(msg) 
                return redirect(url_for('signup')) 
            # Case: the form has been filled out
            else:
                g.dbObject.addUser(fullName, nickName, userID, encryptedPassword, email, phoneNumber)
                msg = 'You have successfully registered !'
                flash(msg)
                session['userID'] = userID
                g.userID = userID
                g.adminStatus = 0
                return redirect(url_for('search')) 

@app.route('/signupadmin', methods =['GET', 'POST'])
def signupadmin():
    if request.method == 'GET':
         return render_template('signupadmin.html', userID = g.userID)
     
    if request.method == 'POST' and 'userID' in request.form and 'password' in request.form and 'confirmpassword' in request.form and 'email' in request.form and 'name' in request.form and 'nickname' in request.form and 'phoneNumber' in request.form and 'jobTitle' in request.form:
        userID = request.form['userID']
        isAdmin = False
        fullName = request.form['name']
        nickName = request.form['nickname']
        password = request.form['password']
        confirmPassword = request.form['confirmpassword']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        jobTitle = request.form['jobTitle']
        
        encryptedPassword = generate_password_hash(password)
        
        if userID == None or fullName == None or nickName == None or password == None or confirmPassword == None or email == None or phoneNumber == None or jobTitle == None:
            msg = 'Please fill out the form!'
            flash(msg)
            return redirect(url_for('signupadmin'))
        elif password != confirmPassword:
            msg = 'Please confirm your password again.'
            flash(msg)
            return redirect(url_for('signupadmin'))
        else:
            accountExistence = g.dbObject.checkAccountExistence(userID)

            # Case: There is already an account with same userID
            if accountExistence == 1:
                msg = 'Account already exists !'
                flash(msg)
                return redirect(url_for('signupadmin')) 
            # Case: The form has not been filled out completely
            elif not userID or not password or not email:
                msg = 'Please fill out the form !'
                flash(msg) 
                return redirect(url_for('signupadmin')) 
            # Case: The form has been filled out completely.
            else:
                g.dbObject.addAdmin(fullName, nickName, userID, encryptedPassword, email, phoneNumber, jobTitle)
                msg = 'You have successfully registered !'
                flash(msg)
                session['userID'] = userID
                g.userID = userID
                g.adminStatus = 1
                return redirect(url_for('search')) 
        
@app.route('/payment', methods = ['GET'])
def payment():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access Payment Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access Payment Page."
            flash(msg)
            return redirect(url_for('search'))
        else:
            return render_template('payment.html', userID = g.userID, adminStatus = g.adminStatus)
        
if __name__ == '__main__':
    app.run(debug=True)