from flask import Flask, g, render_template, request, redirect, url_for, session, jsonify, flash, escape, g 
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from python.dictionaries import *
from python.thealldictionariesAPI import DB
import time
import datetime
import requests
import re

# Codes for initialising the flask application
app = Flask(__name__)
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
    try:
        g.dbObject.connectDB()
    except:
        g.dbObject = DB()
        
    if 'userID' in session:
        g.userID = escape(session['userID'])
        checkAdmin = g.dbObject.checkAdmin(str(g.userID))
        
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

@app.route('/400')
def page400():
    return render_template('400.html', userID = g.userID, adminStatus = g.adminStatus), 400

#HTTP status code 404 is given when there is no such page for the given URL.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', userID = g.userID, adminStatus = g.adminStatus), 404
    
@app.errorhandler(408)
def request_timeout(e):
    return render_template('408.html', userID = g.userID, adminStatus = g.adminStatus), 408

@app.route('/408')
def page408():
    return render_template('408.html', userID = g.userID, adminStatus = g.adminStatus), 408

"""
HTTP status code 410 is given when the page for the corresponding URL has been deleted from the server(?),
but the data for this page is stored in the cache of the client's computer.
"""
@app.errorhandler(410)
def gone(e):
    return render_template('410.html', userID = g.userID, adminStatus = g.adminStatus), 410

@app.route('/410')
def page410():
    return render_template('410.html', userID = g.userID, adminStatus = g.adminStatus), 410

@app.errorhandler(429)
def too_many_requests(e):
    return render_template('429.html', userID = g.userID, adminStatus = g.adminStatus), 429

@app.route('/429')
def page429():
    return render_template('429.html', userID = g.userID, adminStatus = g.adminStatus), 429

@app.errorhandler(431)
def request_header_fields_too_large(e):
    return render_template('431.html', userID = g.userID, adminStatus = g.adminStatus), 431

@app.route('/431')
def page431():
    return render_template('431.html', userID = g.userID, adminStatus = g.adminStatus), 431

@app.errorhandler(451)
def unavailable_for_legal_reasons(e):
    return render_template('451.html', userID = g.userID, adminStatus = g.adminStatus), 451

@app.route('/451')
def page451():
    return render_template('451.html', userID = g.userID, adminStatus = g.adminStatus), 451

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', userID = g.userID, adminStatus = g.adminStatus), 500

@app.route('/500')
def page500():
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

@app.route('/503')
def page503():
    return render_template('503.html', userID = g.userID, adminStatus = g.adminStatus), 503

@app.route('/')
@app.route('/search')
def search():
    return render_template('search.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/searchResult', methods = ['GET', 'POST'])
def searchResult():
    defaultOrderList = ["mwl", "mwc", "oxford", "free", "yourdictionary", "urban", "etymonline", "wordnik", "wordnet", "synonym", "wikipedia", "wiktionary", "news", "images", "youtube", "visuwords"]
    word = request.form['word']
    mwlShortDefinitions = mwlDict(word)
    mwcShortDefinitions = mwcDict(word) 
    oxfordDefinitions, oxfordExamples, oxfordPartOfSpeech, oxfordPhoneticSpelling, oxfordAudioFile = oxfordDict(word)
    thefreedictionary = thefreedictionaryDict(word)
    yourdictURL = yourdictionary(word)
    urbanDefinitions, urbanExamples, urbanLink = urbanDict(word)
    etymonline = etymonlineDict(word)
    wordnikURL = wordnik(word)
    wordnetOutputs = wordnetDict(word)
    synonyms, antonyms = synonymDict(word)
    wikiTitle, wikiSummary, wikiURL = wikiDict(word)
    wiktionaryDefinitions, wiktionaryPartOfSpeech, wiktionaryExamples = wiktionaryDict(word)
    googleImages = googleImageDict(word)
    googleNews = googleNewsDict(word)
    youtubeResults = youtubeDict(word)
    visuwordsURL = visuwords(word)
    
    # Case: the user has logged in and is trying to look up a word
    if g.userID != None and g.adminStatus == 0:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        g.dbObject.addSearchHistory(str(g.userID), timestamp, word)
        
        sourceTable = g.dbObject.getSourceOrder(str(g.userID))
        sourceOrderList = []
        
        for source in sourceTable:
            sourceOrderList.append(source[0])
        
        return render_template("searchResult.html", word = word, 
                               mwlShortDefinitions = mwlShortDefinitions, mwcShortDefinitions = mwcShortDefinitions,
                               oxfordDefinitions = oxfordDefinitions, oxfordExamples = oxfordExamples,
                               oxfordPartOfSpeech = oxfordPartOfSpeech, oxfordPhoneticSpelling = oxfordPhoneticSpelling, 
                               oxfordAudioFile = oxfordAudioFile, 
                               thefreedictionary = thefreedictionary, yourdictURL = yourdictURL,
                               urbanDefinitions = urbanDefinitions, urbanExamples = urbanExamples, urbanLink = urbanLink,  
                               etymonline = etymonline, wordnikURL = wordnikURL, wordnetOutputs = wordnetOutputs,
                               synonyms = synonyms, antonyms = antonyms, 
                               wikiTitle = wikiTitle, wikiSummary = wikiSummary, wikiURL = wikiURL, 
                               wiktionaryDefinitions = wiktionaryDefinitions, 
                               wiktionaryPartOfSpeech = wiktionaryPartOfSpeech, wiktionaryExamples = wiktionaryExamples, 
                               googleNews = googleNews, googleImages = googleImages, youtubeResults = youtubeResults,
                               visuwordsURL = visuwordsURL,
                               userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = sourceOrderList)

    # Executed when the client has not logged in or when the client is an administrator
    return render_template("searchResult.html", word = word, 
                           mwlShortDefinitions = mwlShortDefinitions, mwcShortDefinitions = mwcShortDefinitions,
                           oxfordDefinitions = oxfordDefinitions, oxfordExamples = oxfordExamples,
                           oxfordPartOfSpeech = oxfordPartOfSpeech, oxfordPhoneticSpelling = oxfordPhoneticSpelling, 
                           oxfordAudioFile = oxfordAudioFile, 
                           thefreedictionary = thefreedictionary, yourdictURL = yourdictURL,
                           urbanDefinitions = urbanDefinitions, urbanExamples = urbanExamples, urbanLink = urbanLink,  
                           etymonline = etymonline, wordnikURL = wordnikURL, wordnetOutputs = wordnetOutputs, 
                           synonyms = synonyms, antonyms = antonyms, 
                           wikiTitle = wikiTitle, wikiSummary = wikiSummary, wikiURL = wikiURL, 
                           wiktionaryDefinitions = wiktionaryDefinitions, 
                           wiktionaryPartOfSpeech = wiktionaryPartOfSpeech, wiktionaryExamples = wiktionaryExamples, 
                           googleImages = googleImages, googleNews = googleNews, youtubeResults = youtubeResults,
                           visuwordsURL = visuwordsURL,
                           userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = defaultOrderList)

# Used to display the search result of the word shown in the page (used for hyperlink)
@app.route('/searchResult/<string:word>', methods = ['GET', 'POST'])
def searchWordResult(word):
    defaultOrderList = ["mwl", "mwc", "oxford", "free", "yourdictionary", "urban", "etymonline", "wordnik", "wordnet", "synonym", "wikipedia", "wiktionary", "news", "images", "youtube", "visuwords"]
    
    mwlShortDefinitions = mwlDict(word)
    mwcShortDefinitions = mwcDict(word) 
    oxfordDefinitions, oxfordExamples, oxfordPartOfSpeech, oxfordPhoneticSpelling, oxfordAudioFile = oxfordDict(word)
    thefreedictionary = thefreedictionaryDict(word)
    yourdictURL = yourdictionary(word)
    urbanDefinitions, urbanExamples, urbanLink = urbanDict(word)
    etymonline = etymonlineDict(word)
    wordnikURL = wordnik(word)
    wordnetOutputs = wordnetDict(word)
    synonyms, antonyms = synonymDict(word)
    wikiTitle, wikiSummary, wikiURL = wikiDict(word)
    wiktionaryDefinitions, wiktionaryPartOfSpeech, wiktionaryExamples = wiktionaryDict(word)
    googleImages = googleImageDict(word)
    googleNews = googleNewsDict(word)
    youtubeResults = youtubeDict(word)
    visuwordsURL = visuwords(word)
    
    # Case: the user has logged in and is trying to look up a word
    if g.userID != None and g.adminStatus == 0:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        g.dbObject.addSearchHistory(str(g.userID), timestamp, word)
        
        sourceTable = g.dbObject.getSourceOrder(str(g.userID))
        sourceOrderList = []
        
        for source in sourceTable:
            sourceOrderList.append(source[0])
        
        return render_template("searchResult.html", word = word, 
                               mwlShortDefinitions = mwlShortDefinitions, mwcShortDefinitions = mwcShortDefinitions,
                               oxfordDefinitions = oxfordDefinitions, oxfordExamples = oxfordExamples,
                               oxfordPartOfSpeech = oxfordPartOfSpeech, oxfordPhoneticSpelling = oxfordPhoneticSpelling, 
                               oxfordAudioFile = oxfordAudioFile, 
                               thefreedictionary = thefreedictionary, yourdictURL = yourdictURL,
                               urbanDefinitions = urbanDefinitions, urbanExamples = urbanExamples, urbanLink = urbanLink,  
                               etymonline = etymonline, wordnikURL = wordnikURL, wordnetOutputs = wordnetOutputs,
                               synonyms = synonyms, antonyms = antonyms, 
                               wikiTitle = wikiTitle, wikiSummary = wikiSummary, wikiURL = wikiURL, 
                               wiktionaryDefinitions = wiktionaryDefinitions, 
                               wiktionaryPartOfSpeech = wiktionaryPartOfSpeech, wiktionaryExamples = wiktionaryExamples, 
                               googleNews = googleNews, googleImages = googleImages, youtubeResults = youtubeResults,
                               visuwordsURL = visuwordsURL,
                               userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = sourceOrderList)
    
    # Executed when the client has not logged in or when the client is an administrator
    return render_template("searchResult.html", word = word, 
                           mwlShortDefinitions = mwlShortDefinitions, mwcShortDefinitions = mwcShortDefinitions,
                           oxfordDefinitions = oxfordDefinitions, oxfordExamples = oxfordExamples,
                           oxfordPartOfSpeech = oxfordPartOfSpeech, oxfordPhoneticSpelling = oxfordPhoneticSpelling, 
                           oxfordAudioFile = oxfordAudioFile, 
                           thefreedictionary = thefreedictionary, yourdictURL = yourdictURL,
                           urbanDefinitions = urbanDefinitions, urbanExamples = urbanExamples, urbanLink = urbanLink,  
                           etymonline = etymonline, wordnikURL = wordnikURL, wordnetOutputs = wordnetOutputs, 
                           synonyms = synonyms, antonyms = antonyms,
                           wikiTitle = wikiTitle, wikiSummary = wikiSummary, wikiURL = wikiURL, 
                           wiktionaryDefinitions = wiktionaryDefinitions, 
                           wiktionaryPartOfSpeech = wiktionaryPartOfSpeech, wiktionaryExamples = wiktionaryExamples, 
                           googleImages = googleImages, googleNews = googleNews, youtubeResults = youtubeResults,
                           visuwordsURL = visuwordsURL,
                           userID = g.userID, adminStatus = g.adminStatus, sourceOrderList = defaultOrderList)

@app.route('/changeDictionaryOrder', methods = ['GET', 'POST'])
def changeDictionaryOrder():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access Change Dictionary Page."
            flash(msg)
            return redirect(url_for('signin')) 
        
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
            
            g.dbObject.updateSourceOrder(str(g.userID), sourceList[0], sourceList[1], sourceList[2], sourceList[3], 
                                         sourceList[4], sourceList[5], sourceList[6], sourceList[7], sourceList[8], 
                                         sourceList[9], sourceList[10], sourceList[11], sourceList[12], sourceList[13], 
                                         sourceList[14], sourceList[15])
            
            msg = "The order of the sources have been successfully updated"
            flash(msg)
            return redirect(url_for('search')) 

    return render_template("changeDictionaryOrder.html", userID = g.userID, adminStatus = g.adminStatus)

@app.route('/signin', methods =['GET', 'POST'])
def signin():
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
                    msg = 'Signed in successfully !'
                    flash(msg)
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
                    msg = 'Signed in successfully !'
                    flash(msg)
                    return redirect(url_for('search')) 
                # Case: the admin has not entered its password correctly
                if userID == accountID and encryptedPassword != accountPassword:
                    msg = 'Incorrect password !'
                    flash(msg)
                    return redirect(url_for('signin')) 
    
    return render_template('signin.html', userID = g.userID)
  
@app.route('/signout')
def signout():
    session.pop('userID', None)
    g.dbObject.disconnectDB() # Remove the connection with the database as there is no need after signing out
    return redirect(url_for('search'))

@app.route('/signup', methods =['GET', 'POST'])
def signup():
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
        elif password != confirmPassword:
            msg = 'Please confirm your password again.'
            flash(msg)
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
    # Case: the form has not been filled out completely.        
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
        flash(msg)

    return render_template('signup.html', userID = g.userID)

@app.route('/signupadmin', methods =['GET', 'POST'])
def signupadmin():
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
        elif password != confirmPassword:
            msg = 'Please confirm your password again.'
            flash(msg)
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
    # Case: The form has not been filled out completely        
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
        flash(msg)

    return render_template('signupadmin.html', userID = g.userID)

@app.route('/mypage', methods = ['GET', 'POST'])
def mypage():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access My Page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            # Case: the client is a user
            if g.adminStatus == 0:
                accountFullName, accountNickName, accountID, accountPassword, accountEmail, accountPhoneNumber, isPremium, endDate, accountPicture  = g.dbObject.getUserData(str(g.userID))
                
                accountPremium = None # variable to check whether the client is a free user or a premium user
                # Case: the client is a free user
                if isPremium == 0:
                    accountPremium = "Basic"
                # Case: the client is a premium user
                else:
                    accountPremium = "Premium"
                
                accountDate = None # variable for subscription end date
                # Case: subscription end date has not been set
                if endDate == None:
                    accountDate = "Not applicable"
                # Case: subscription end date has been set
                else:
                    accountDate = endDate
                    
                sourceTable = g.dbObject.getSourceOrder(accountID)
                sourceList = []
                for source in sourceTable:
                    if source[0] == "mwl":
                        sourceList.append("Merriam Webster's Learner's Dictionary")
                    if source[0] == "mwc":
                        sourceList.append("Merriam Webster Dictionary")
                    if source[0] == "oxford":
                        sourceList.append("Oxford English Dictionary")
                    if source[0] == "free":
                        sourceList.append("The Free Dictionary")
                    if source[0] == "yourdictionary":
                        sourceList.append("Your Dictionary")
                    if source[0] == "urban":
                        sourceList.append("Urban Dictionary")
                    if source[0] == "etymonline":
                        sourceList.append("Etymonline.com")
                    if source[0] == "wordnik":
                        sourceList.append("Wordnik")
                    if source[0] == "wordnet":
                        sourceList.append("WordNet")
                    if source[0] == "synonym":
                        sourceList.append("Synonym.com")
                    if source[0] == "wikipedia":
                        sourceList.append("Wikipedia")
                    if source[0] == "wiktionary":
                        sourceList.append("Wiktionary")
                    if source[0] == "news":
                        sourceList.append("Google News")
                    if source[0] == "images":
                        sourceList.append("Google Images")
                    if source[0] == "youtube":
                        sourceList.append("YouTube")
                    if source[0] == "visuwords":
                        sourceList.append("Visuwords")
                
                searchHistoryTable = g.dbObject.getSearchHistory(str(g.userID))
                searchHistories = []
                for searchHistoryData in searchHistoryTable:
                    searchHistories.append([searchHistoryData[0], searchHistoryData[1]])
                
                userWordRankData = g.dbObject.getUserWordRank(str(g.userID))
                userSentenceRankData = g.dbObject.getUserSentenceRank(str(g.userID))
                
                return render_template('mypage.html', userID = accountID,
                                       fullName = accountFullName, nickName = accountNickName,
                                       accountPassword = accountPassword, accountEmail = accountEmail,
                                       accountPhoneNumber = accountPhoneNumber, accountPremium = accountPremium,
                                       accountDate = accountDate, accountPicture = accountPicture,
                                       sourceList = sourceList, adminStatus = g.adminStatus, searchHistories = searchHistories,
                                       userWordRankData = userWordRankData, userSentenceRankData = userSentenceRankData)
            # Case: the client is an administrator    
            if g.adminStatus == 1:
                accountFullName, accountNickName, accountID, accountPassword, accountEmail, accountPhoneNumber, accountJobTitle, accountPicture  = g.dbObject.getAdminData(str(g.userID))
                
                return render_template('mypage.html', userID = accountID,
                                       fullName = accountFullName, nickName = accountNickName,
                                       accountPassword = accountPassword, accountEmail = accountEmail,
                                       accountPhoneNumber = accountPhoneNumber, accountJobTitle = accountJobTitle,
                                       accountPicture = accountPicture, adminStatus = g.adminStatus)
    if request.method == 'POST':
        # Case: the delete button for the search history has been clicked
        try:
            historyToDelete = request.form["deleteDistinctWord"]
        except:
            historyToDelete = None
            
        # Case: the delete button for the profile picture has been clicked    
        try:
            deletePicture = request.form["deletePicture"]
        except:
            deletePicture = None
        
        if historyToDelete != None:
            searchHistoryData = str(historyToDelete)[1:-1]
            searchHistoryList = searchHistoryData.rsplit(", ", 1)
 
            wordString = searchHistoryList[1]
            word = wordString[1:-1]
            
            # Code to retrieve searchedDateTime from the page and reformat to delete in the database
            dateTimeString = searchHistoryList[0]
            dateTimeStr  = dateTimeString.replace("datetime.datetime", "")
            dateTime = dateTimeStr[1:-1]
            timestamp = datetime.datetime.strptime(dateTime, '%Y, %m, %d, %H, %M, %S')
            
            g.dbObject.deleteSpecificSearchHistory(str(g.userID), word, timestamp)
            msg = "The word, " + str(word) + ", has been deleted successfully from your search history."
            flash(msg)
            return redirect(url_for('mypage')) 
        
        if deletePicture != None:
            # Differentiated the case as the profile picture URL is stored in different tables
            # Case: the client is a user
            if g.adminStatus == 0:
                g.dbObject.deleteUserProfilePicture(str(g.userID))
                msg = "Profile picture deleted successfully!"
                flash(msg)
                return redirect(url_for('mypage')) 
            # Case: the client is an administrator
            if g.adminStatus == 1:
                g.dbObject.deleteAdminProfilePicture(str(g.userID))
                msg = "Profile picture deleted successfully"
                flash(msg)
                return redirect(url_for('mypage')) 

    return render_template('mypage.html', userID = g.userID, adminStatus = g.adminStatus, accountPicture = None)

@app.route('/changeProfilePicture', methods = ['GET', 'POST'])
def changeProfilePicture():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change profile picture page."
            flash(msg)
            return redirect(url_for('signin')) 
        
    if request.method == 'POST':
        newURL = request.form["newProfile"]
        currentPassword = request.form["currentPassword"]
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its password correctly
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserProfilePictureURL(accountID, newURL)  
                msg = "Your profile picture has been updated successfully!" 
                flash(msg)
                return redirect(url_for('mypage')) 
            # Case: the user has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeProfilePicture')) 
        # Case: the client is an administrator        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its password correctly.    
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminProfilePictureURL(accountID, newURL) 
                msg = "Your profile picture has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('mypage')) 
            # Case: the admin has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeProfilePicture')) 
    
    return render_template('changeProfilePicture.html', userID = g.userID, adminStatus = g.adminStatus)   
                
@app.route('/changeFullName', methods = ['GET', 'POST'])
def changeFullName():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change full name page."
            flash(msg)
            return redirect(url_for('signin')) 
        
    if request.method == 'POST':
        newFullName = request.form["newFullName"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user.
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its password correctly.
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserFullName(accountID, newFullName)  
                msg = "Your full name has been updated successfully!" 
                flash(msg)
                return redirect(url_for('mypage'))    
            # Case: the user has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeFullName'))    
        # Case: the client is an administrator        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its password correctly.    
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminFullName(accountID, newFullName) 
                msg = "Your full name has been updated successfully!" 
                flash(msg)
                return redirect(url_for('mypage'))
            # Case: the admin has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeFullName'))  
    
    return render_template('changeFullName.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/changeNickName', methods = ['GET', 'POST'])
def changeNickName():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change nickname page."
            flash(msg)
            return redirect(url_for('signin')) 
        
    if request.method == 'POST':
        newNickName = request.form["newNickName"]
        currentPassword = request.form["currentPassword"]
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its password correctly
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserNickName(accountID, newNickName)  
                msg = "Your nick name has been updated successfully!" 
                flash(msg)
                return redirect(url_for('mypage'))
            # Case: the user has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeNickName')) 
        # Case: the client is an admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its userID and password correctly    
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminNickName(accountID, newNickName) 
                msg = "Your nick name has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('mypage'))
            # Case: the admin has entered its userID or password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeNickName')) 
    
    return render_template('changeNickName.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/changePassword', methods = ['GET', 'POST'])
def changePassword():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change password page."
            flash(msg)
            return redirect(url_for('signin')) 
        
    if request.method == 'POST':
        currentPassword = request.form["currentPassword"]
        newPassword = request.form["newPassword"]
        confirmPassword = request.form["confirmPassword"]
        
        if currentPassword != confirmPassword:
            msg = "Please confirm your new password correctly"
            flash(msg)
            return redirect(url_for('changePassword')) 
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its password correctly
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                newEncryptedPassword = generate_password_hash(newPassword)
                g.dbObject.updateUserPassword(accountID, newEncryptedPassword)  
                msg = "Your password has been updated successfully!" 
                flash(msg)
                return redirect(url_for('mypage'))
            # Case: the user has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changePassword')) 
        # Case: the client is an admin       
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its password correctly
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                newEncryptedPassword = generate_password_hash(newPassword) 
                g.dbObject.updateAdminPassword(accountID, newEncryptedPassword) 
                msg = "Your password has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changePassword')) 
    
    return render_template('changePassword.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/changeEmail', methods = ['GET', 'POST'])
def changeEmail():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change email page."
            flash(msg)
            return redirect(url_for('signin')) 
        
    if request.method == 'POST':
        newEmail = request.form["newEmail"]
        currentPassword = request.form["currentPassword"]
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its password correctly
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserEmail(accountID, newEmail)  
                msg = "Your email has been updated successfully!" 
                flash(msg)
                return redirect(url_for('mypage'))
            # Case: the user has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeEmail')) 
        # Case: the client is an admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its password correctly    
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminEmail(accountID, newEmail) 
                msg = "Your email has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeEmail')) 
    
    return render_template('changeEmail.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/changePhone', methods = ['GET', 'POST'])
def changePhone():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change phone number page."
            flash(msg)
            return redirect(url_for('signin')) 
        
    if request.method == 'POST':
        newPhone = request.form["newPhone"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its password correctly
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserPhoneNumber(accountID, newPhone)  
                msg = "Your phone number has been updated successfully!" 
                flash(msg)
                return redirect(url_for('mypage'))
            # Case: the user has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changePhone')) 
        # Case: the admin is the client         
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its password correctly
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminPhoneNumber(accountID, newPhone) 
                msg = "Your phone number has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changePhone')) 
            
    return render_template('changePhone.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/unsubscribe', methods = ['GET', 'POST'])
def unsubscribe():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access cancel subscription page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Please users can access cancel subscription page."
            flash(msg)
            return redirect(url_for('search')) 
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its userID and password correctly
            if currentID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserSubscriptionStatus(accountID, 0)  
                msg = "You have unsubscribed successfully." 
                flash(msg)
                return redirect(url_for('mypage'))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your userID and password correctly"
                flash(msg)
                return redirect(url_for('unsubscribe')) 
    
    return render_template('unsubscribe.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/resetSearchHistories', methods = ['GET', 'POST'])
def resetSearchHistories():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access reset search histories page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Please users can access reset search histories page."
            flash(msg)
            return redirect(url_for('search')) 
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its userID and password correctly
            if currentID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.deleteAllSearchHistory(accountID)  
                msg = "You search histories have been all deleted." 
                flash(msg)
                return redirect(url_for('mypage'))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your userID and password correctly"
                flash(msg)
                return redirect(url_for('resetSearchHistories')) 
    
    return render_template('resetSearchHistories.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/resetWordRank', methods = ['GET', 'POST'])
def resetWordRank():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete word rank page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Please users can access delete word rank page."
            flash(msg)
            return redirect(url_for('search')) 
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its userID and password correctly
            if currentID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.deleteWordRanking(accountID)  
                msg = "Your result from the word ranking page have been deleted successfully." 
                flash(msg)
                return redirect(url_for('wordrank'))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your userID and password correctly."
                flash(msg)
                return redirect(url_for('resetWordRank')) 
            
    return render_template('resetWordRank.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/resetSentenceRank', methods = ['GET', 'POST'])
def resetSentenceRank():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete sentence rank page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Please users can access delete sentence rank page."
            flash(msg)
            return redirect(url_for('search')) 
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its userID and password correctly
            if currentID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.deleteSentenceRanking(accountID)  
                msg = "Your result from the sentence ranking page have been deleted successfully." 
                flash(msg)
                return redirect(url_for('sentenceRank'))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your userID and password correctly."
                flash(msg)
                return redirect(url_for('resetWordRank')) 
            
    return render_template('resetSentenceRank.html', userID = g.userID, adminStatus = g.adminStatus)


@app.route('/resetTextRank', methods = ['GET', 'POST'])
@app.route('/resetTextRank/<string:title>', methods = ['GET', 'POST'])
def resetTextRank(title):
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete text rank page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Please users can access delete text rank page."
            flash(msg)
            return redirect(url_for('search')) 
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its userID and password correctly
            if currentID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.deleteTextRanking(accountID, str(title))  
                msg = "Your result from the text ranking page have been deleted successfully." 
                flash(msg)
                return redirect(url_for('textRank', title = title))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your userID and password correctly."
                flash(msg)
                return redirect(url_for('resetTextRank', title = title))
            
    return render_template('resetTextRank.html', userID = g.userID, adminStatus = g.adminStatus, title = title)

@app.route('/changeJob', methods = ['GET', 'POST'])
def changeJob():    
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change job title page."
            flash(msg)
            return redirect(url_for('signin')) 
        if g.adminStatus != 1:
            msg = "Only administrators can access job title page."
            flash(msg)
            return redirect(url_for('search')) 
        
    if request.method == 'POST':
        newNickName = request.form["newJob"]
        currentPassword = request.form["currentPassword"]  
        # Case: the client is the admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its password correctly    
            if str(g.userID) == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminJobTitle(accountID, newNickName) 
                msg = "Your job title has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('changeJob'))  
    
    return render_template('changeJob.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/deleteAccount', methods = ['GET', 'POST'])
def deleteAccount():    
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete account page."
            flash(msg)
            return redirect(url_for('search')) 
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        confirmPassword = request.form["confirmPassword"]
        
        if currentPassword != confirmPassword:
            msg = "Please confirm your password correctly"
            flash(msg)
            return redirect(url_for('deleteAccount')) 
        
        # Case: the client is the user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(str(g.userID))
            # Case: the user has entered its userID and password correctly
            if accountID == currentID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.deleteUser(accountID)  
                msg = "Your account has been deleted successfully!" 
                flash(msg)
                return redirect(url_for('signout'))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('deleteAccount'))    
        # Case: the client is the admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(str(g.userID))
            # Case: the admin has entered its userID and password correctly    
            if accountID == currentID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.deleteAdmin(accountID)  
                msg = "Your account has been deleted successfully!" 
                flash(msg)
                return redirect(url_for('signout'))
            # Case: the admin has not entered its userID or password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('deleteAccount'))  

    return render_template('deleteAccount.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/friends', methods = ['GET', 'POST'])
def friends():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access About Friends Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access About Friends Page"
            flash(msg)
            return redirect(url_for('search')) 
        else:
            friendData = g.dbObject.getFriends(str(g.userID))
            friendList = []
            
            for friendDatum in friendData:
                friendFullName = g.dbObject.getUserFullName(friendDatum[0])[0]
                friendNickName = g.dbObject.getUserNickName(friendDatum[0])[0]
                friendProfilePicture = g.dbObject.getUserProfilePicture(friendDatum[0])[0]
                friendList.append([friendDatum[0], friendFullName, friendNickName, friendProfilePicture])
                
            return render_template('friends.html', userID = g.userID, adminStatus = g.adminStatus, friendList = friendList)
    
    if request.method == 'POST':
        deleteID = request.form["deleteFriend"]
        g.dbObject.deleteFriend(str(g.userID), deleteID)
        return redirect(url_for('friends')) 
        
    return render_template('friends.html', userID = g.userID, adminStatus = g.adminStatus, friendList = g.friendList)

@app.route('/addFriends', methods = ['GET', 'POST'])
def addFriends():        
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access Add Friends Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access Add Friends Page"
            flash(msg)
            return redirect(url_for('search')) 
    
    if request.method == 'POST':
        receiverID = request.form["receiverID"]
        # Case: no corresponding account
        if g.dbObject.checkAccountExistence(receiverID)[0] == 0:
            msg = "Sending friend request has been failed. There is no corresponding account with the userID inputted."
            flash(msg)
            return redirect(url_for('addFriends')) 
        # Case: the user has tried to send a friend request to the admin
        elif g.dbObject.checkUserAccountExistence(receiverID)[0] == 0:
            msg = "Sending friend request has been failed. You cannot send a friend request to the administrator."
            flash(msg)
            return redirect(url_for('addFriends')) 
        # Case: the user has sent the friend request to itself
        elif receiverID == str(g.userID):
            msg = "Sending friend request has been failed. You cannot send a friend request to yourself."
            flash(msg)
            return redirect(url_for('addFriends')) 
        else:
            friendRequestList = g.dbObject.getFriendRequests(str(g.userID)) 
            for friendRequest in friendRequestList:
                # Case: already received a friend request from the receiver
                if receiverID == friendRequest[0]:
                    msg = "Sending a friend request has been failed. The receiver has already sent you the friend request."
                    flash(msg)
                    return redirect(url_for('viewFriendRequests')) 
                
            friendRequestSentList = g.dbObject.getFriendRequestSent(str(g.userID)) 
            for friendRequestSent in friendRequestSentList:
                # Case: already sent a friend request to the receiver
                if receiverID == friendRequestSent[0]:
                    msg = "You have already sent a friend request to " + str(receiverID) + "."
                    flash(msg)
                    return redirect(url_for('friends')) 
                
            friendList = g.dbObject.getFriends(str(g.userID))
            for friend in friendList:
                # Case: already a friend
                if receiverID == friend[0]:
                    msg = "Sending a friend request has been failed. The receiver is already your friend."
                    flash(msg)
                    return redirect(url_for('friends'))
                   
            g.dbObject.addFriendRequests(str(g.userID), receiverID)      
            msg = "A friend request has been sent successfully!" 
            flash(msg)
            return redirect(url_for('friends')) 
        
    return render_template('addFriends.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/viewFriendRequests', methods = ['GET', 'POST'])
def viewFriendRequests():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access View Friend Requests Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access View Friend Requests Page"
            flash(msg)
            return redirect(url_for('search')) 
        else:
            senderTable = g.dbObject.getFriendRequests(str(g.userID))
            senderList = []
            for sender in senderTable:
                senderFullName = g.dbObject.getUserFullName(sender[0])[0]
                senderNickName = g.dbObject.getUserNickName(sender[0])[0]
                senderProfilePicture = g.dbObject.getUserProfilePicture(sender[0])[0]
                senderList.append([sender[0], senderFullName, senderNickName, senderProfilePicture])
            
            print("Sender data:", senderList)
            
            return render_template('viewFriendRequests.html', userID = g.userID, adminStatus = g.adminStatus, senderList = senderList)
    
    if request.method == 'POST':
        # Check whether the user has clicked the reject button
        try:
            rejectID = request.form["reject"]
        except:
            rejectID = None
        # Check whether the user has clicked the accept button
        try:
            friendID = request.form["accept"]
        except:
            friendID = None
        # Case: the user has clicked the reject button
        if rejectID != None and friendID == None:
            msg = "The friend request from " + str(rejectID) + " has been rejected successfully."
            flash(msg)
            g.dbObject.deleteFriendRequests(rejectID, str(g.userID))
            return redirect(url_for('friends')) 
        # Case: the user has clicked the accept button
        else:
            friendFullName = g.dbObject.getUserFullName(friendID)[0]
            msg = "You are now friends with " + friendFullName + "."
            flash(msg)
            g.dbObject.addFriend(friendID, str(g.userID))
            g.dbObject.deleteFriendRequests(friendID, str(g.userID))
            return redirect(url_for('friends')) 
        
    return render_template('viewFriendRequests.html', userID = g.userID, adminStatus = g.adminStatus, senderList = None)

@app.route('/wordTypingChallenge', methods = ['GET', 'POST'])
def wordTypingChallenge():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to participate word typing challenge."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus != 0:
            msg = "Only users can access this page."
            flash(msg)
            return redirect(url_for('search'))
    
    if request.method == 'POST':
        scoreSubmit = request.form["scoreSubmit"]
        
        # Case: The user has not submitted its score yet
        if g.dbObject.getWordRanking(str(g.userID)) == None:
            if scoreSubmit == "0":
                g.dbObject.addWordRanking(str(g.userID), 0)
            else:
                g.dbObject.addWordRanking(str(g.userID), int(scoreSubmit))
            
            flash("You have added your score in the ranking!")
            return redirect(url_for('wordrank'))
        else:
            highestScore = g.dbObject.getWordRanking(str(g.userID))[0]
            if scoreSubmit != "":
                # Case: the user has performed better from its previous results so far
                if highestScore < int(scoreSubmit):
                    g.dbObject.updateWordRanking(str(g.userID), int(scoreSubmit))
                    flash("You have updated your score in the ranking!")
                    return redirect(url_for('wordrank'))
                # Case: the user did not perform best
                else:
                    flash("You did not break your highest record!")
                    return redirect(url_for('wordrank'))
            # Case: the user did not perform best (scoreSubmit is null)
            else:
                flash("You did not make a new record!")
                return redirect(url_for('wordrank'))
        
        return redirect(url_for('wordrank'))
        
    return render_template('wordTypingChallenge.html', userID = g.userID, adminStatus = g.adminStatus, score = 0)

@app.route('/sentenceTypingChallenge', methods = ['GET', 'POST'])
def sentenceTypingChallenge():        
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to participate sentence typing challenge."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus != 0:
            msg = "Only users can access this page."
            flash(msg)
            return redirect(url_for('search'))
    
    if request.method == 'POST':
        scoreSubmit = request.form["scoreSubmit"]
        
        # Case: The user has not submitted its score yet
        if g.dbObject.getSentenceRanking(str(g.userID)) == None:
            if scoreSubmit == "0":
                g.dbObject.addSentenceRanking(str(g.userID), 0)
            else:
                g.dbObject.addSentenceRanking(str(g.userID), int(scoreSubmit))
            flash("You have added your score in the ranking!")
            return redirect(url_for('sentenceRank'))
        else:
            highestScore = g.dbObject.getSentenceRanking(str(g.userID))[0]
            if scoreSubmit != "":
                # Case: the user has performed better from its previous results so far
                if highestScore < int(scoreSubmit):
                    g.dbObject.updateSentenceRanking(str(g.userID), int(scoreSubmit))
                    flash("You have updated your score in the ranking!")
                    return redirect(url_for('sentenceRank'))
                # Case: the user did not perform best
                else:
                    flash("You did not break your highest record!")
                    return redirect(url_for('sentenceRank'))
            # Case: the user did not perform best (scoreSubmit is null)
            else:
                flash("You did not make a new record!")
                return redirect(url_for('sentenceRank'))
        
        return redirect(url_for('sentenceRank'))
        
    return render_template('sentenceTypingChallenge.html', userID = g.userID, adminStatus = g.adminStatus, score = 0)

@app.route('/textTypingChallenge', methods = ['GET', 'POST'])
def textTypingChallenge():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to participate text typing challenge."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus != 0:
            msg = "Only users can access this page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            literatureTable, speechTable, lawTable, articleTable, essayTable = g.dbObject.getTextChallenge()
            return render_template('textTypingChallenge.html', userID = g.userID, adminStatus = g.adminStatus, 
                                   literatureTable = literatureTable, speechTable = speechTable, lawTable = lawTable, 
                                   articleTable = articleTable, essayTable = essayTable)
        
    return render_template('textTypingChallenge.html', userID = g.userID, adminStatus = g.adminStatus, 
                           literatureTable = None, speechTable = None, lawTable = None, articleTable = None, essayTable = None)

@app.route('/createTextChallenge', methods = ['GET', 'POST'])
def createTextChallenge():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access create text challenge Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus != 1:
            msg = "Only administrators can access this page."
            flash(msg)
            return redirect(url_for('search')) 
    
    if request.method == 'POST':
        title = request.form['title']
        textType = request.form['textType']
        text = request.form['text']
        
        checkTitle = g.dbObject.checkTextChallengeTitle(title)[0]
        
        # Case: there is no such text typing challenge with the same title
        if checkTitle == 0:
            ts = time.time()
            dateCreated = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            g.dbObject.addTextChallenge(str(g.userID), title, textType, text, dateCreated)
            msg = "Challenge successfully added."
            flash(msg)
            return redirect(url_for('viewTextChallenge')) 
        # Case: there is a text typing challenge with the same title (checkTitle = 1)
        else:
            msg = "Error. There is already a challenge with the title - " + str(title) + "."
            flash(msg)
            return redirect(url_for('createTextChallenge')) 
        
    return render_template('createTextChallenge.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/viewTextChallenge', methods = ['GET', 'POST'])
def viewTextChallenge():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access create text challenge Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus != 1:
            msg = "Only administrators can access this page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            myLiteratureTable, mySpeechTable, myLawTable, myArticleTable, myEssayTable = g.dbObject.getMyTextChallenge(str(g.userID))
            return render_template('viewTextChallenge.html', userID = g.userID, adminStatus = g.adminStatus, 
                                   myLiteratureTable = myLiteratureTable, mySpeechTable = mySpeechTable, 
                                   myLawTable = myLawTable, myArticleTable = myArticleTable, myEssayTable = myEssayTable)
    
    if request.method == 'POST':
        challengeTitle = request.form["deleteTextChallenge"]
        g.dbObject.deleteMyChallenge(str(g.userID), challengeTitle)
        msg = "Challenge has been deleted successfully"
        flash(msg)
        return redirect(url_for('viewTextChallenge')) 
        
    return render_template('viewTextChallenge.html', userID = g.userID, adminStatus = g.adminStatus,
                           myLiteratureTable = None, mySpeechTable = None, myLawTable = None, myArticleTable = None, 
                           myEssayTable = None)

@app.route('/viewChallengeText', methods = ['GET'])
@app.route('/viewChallengeText/<string:title>', methods = ['GET'])
def viewChallengeText(title):
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access create text challenge Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus != 1:
            msg = "Only administrators can access this page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            challengeText = g.dbObject.getChallengeText(title)
            return render_template('viewChallengeText.html', userID = g.userID, adminStatus = g.adminStatus, challengeText = challengeText)
    
    return render_template('viewChallengeText.html', userID = g.userID, adminStatus = g.adminStatus, challengeText = None)


@app.route('/startTextTyping', methods = ['GET', 'POST'])
@app.route('/startTextTyping/<string:title>', methods = ['GET', 'POST'])
def startTextTyping(title):
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access create text challenge Page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access this page."
            flash(msg)
            return redirect(url_for('search')) 
        else: 
            challengeText = g.dbObject.getChallengeText(title)
            return render_template('startTextTyping.html', userID = g.userID, adminStatus = g.adminStatus, title=title, challengeText = challengeText)
    
    if request.method == 'POST':
        scoreSubmit = request.form.get("scoreSubmit")
        
        # Case: The user has not submitted its score yet
        if g.dbObject.getTextRanking(str(g.userID), title) == None:
            if scoreSubmit == "0":
                g.dbObject.addTextRanking(str(g.userID), 0, title)
            else:
                g.dbObject.addTextRanking(str(g.userID), int(scoreSubmit), title)
            flash("You have added your score in the ranking!")
            return redirect(url_for('textRank', title = title))
        else:
            highestScore = g.dbObject.getTextRanking(str(g.userID), title)[0]
            if scoreSubmit != "":
                # Case: the user performed best this time
                if highestScore < int(scoreSubmit):
                    g.dbObject.updateTextRanking(str(g.userID), int(scoreSubmit), title)
                    flash("You have updated your score in the ranking!")
                    return redirect(url_for('textRank', title = title))
                # Case: the user did not perform best this time
                else:
                    flash("You did not break your highest record!")
                    return redirect(url_for('textRank', title = title))
            # Case: the user did not perform best this time
            else:
                flash("You did not make a new record!")
                return redirect(url_for('textRank', title = title))
        
        return redirect(url_for('textRank', title = title))
            
    return render_template('startTextTyping.html', userID = g.userID, adminStatus = g.adminStatus, title=None, challengeText = None)

@app.route('/textRank', methods = ['GET', 'POST'])
@app.route('/textRank/<string:title>', methods = ['GET', 'POST'])
def textRank(title):
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access the rank page for " + str(title) + "."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access the rank page for " + str(title) + "."
            flash(msg)
            return redirect(url_for('search'))
        else:
            textRankingTable = g.dbObject.getAllTextRanking(str(title))
            return render_template('textRank.html', userID = g.userID, adminStatus = g.adminStatus, title = title, textRankingTable = textRankingTable)

    return render_template('textrank.html', userID = g.userID, adminStatus = g.adminStatus, title = title, textRankingTable = ())

@app.route('/wordrank', methods = ['GET'])
def wordrank():        
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access the rank page for the word typing challenge."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access the rank page for the word typing challenge."
            flash(msg)
            return redirect(url_for('search'))
        else:
            wordRankingTable = g.dbObject.getAllWordRanking()
            return render_template('wordrank.html', userID = g.userID, adminStatus = g.adminStatus, wordRankingTable = wordRankingTable)

    return render_template('wordrank.html', userID = g.userID, adminStatus = g.adminStatus, wordRankingTable = ())

@app.route('/sentenceRank', methods = ['GET'])
def sentenceRank():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access the rank page for the sentence typing challenge."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access the rank page for the sentence typing challenge."
            flash(msg)
            return redirect(url_for('search'))
        else:
            sentenceRankingTable = g.dbObject.getAllSentenceRanking()
            return render_template('sentenceRank.html', userID = g.userID, adminStatus = g.adminStatus, sentenceRankingTable = sentenceRankingTable)    

    return render_template('sentenceRank.html', userID = g.userID, adminStatus = g.adminStatus, sentenceRankingTable = ())

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
        
    return render_template('payment.html', userID = g.userID, adminStatus = g.adminStatus)

@app.route('/groupChatMessage', methods=['GET'])
def getGroupChatMessage():
    groupChatMessages = g.dbObject.getMessage('Group chat')
    groupChatDict = []
    for groupChatMessage in groupChatMessages:
        groupChatDict.append({'senderID': groupChatMessage[0], 'chatMessage': groupChatMessage[1], 
                             'sendDate': str(groupChatMessage[2]), 'nickName': groupChatMessage[3],
                             'profilePictureURL': groupChatMessage[4]})
    return json.dumps(groupChatDict)

@app.route('/groupChat', methods=['GET', 'POST'])
def groupChat():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access Group chatting Page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            messageTable = g.dbObject.getMessage('Group chat')
            return render_template('groupChat.html', userID = g.userID, adminStatus = g.adminStatus, chatroom='Group chat', messageTable = messageTable)
    
    if request.method == 'POST':
        chatMessage = request.form['chatMessageBox']
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        g.dbObject.sendMessage('Group chat', str(g.userID), None, chatMessage, timestamp)
        messageTable = g.dbObject.getMessage('Group chat')
        return render_template('groupChat.html', userID = g.userID, adminStatus = g.adminStatus, messageTable = messageTable)
    
    return render_template('groupChat.html', userID = g.userID, adminStatus = g.adminStatus, messageTable = ())

if __name__ == '__main__':
    app.run(debug=True)