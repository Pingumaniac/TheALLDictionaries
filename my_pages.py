from flask import Flask, Blueprint, g, render_template, request, redirect, url_for, session, jsonify, flash, escape
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from python.thealldictionariesAPI import DB
import requests
import re

my_pages = Blueprint("my_pages", __name__, static_folder="static", template_folder="templates")

@my_pages.route('/mypage', methods = ['GET', 'POST'])
def mypage():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access My Page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            # Case: the client is a user
            if g.adminStatus == 0:
                accountFullName, accountNickName, accountID, accountPassword, accountEmail, accountPhoneNumber, isPremium, endDate, accountPicture  = g.dbObject.getUserData(g.userID)
                
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
                
                return render_template('mypage.html', userID = accountID,
                                       fullName = accountFullName, nickName = accountNickName,
                                       accountPassword = accountPassword, accountEmail = accountEmail,
                                       accountPhoneNumber = accountPhoneNumber, accountPremium = accountPremium,
                                       accountDate = accountDate, accountPicture = accountPicture,
                                       adminStatus = g.adminStatus)
                
            # Case: the client is an administrator    
            if g.adminStatus == 1:
                accountFullName, accountNickName, accountID, accountPassword, accountEmail, accountPhoneNumber, accountJobTitle, accountPicture  = g.dbObject.getAdminData(g.userID)
                
                return render_template('mypage.html', userID = accountID,
                                       fullName = accountFullName, nickName = accountNickName,
                                       accountPassword = accountPassword, accountEmail = accountEmail,
                                       accountPhoneNumber = accountPhoneNumber, accountJobTitle = accountJobTitle,
                                       accountPicture = accountPicture, adminStatus = g.adminStatus)
    if request.method == 'POST':            
        deletePicture = request.form["deletePicture"]
        # Differentiated the case as the profile picture URL is stored in different tables
        # Case: the client is a user
        if g.adminStatus == 0:
            g.dbObject.deleteUserProfilePicture(g.userID)
            msg = "Profile picture deleted successfully!"
            flash(msg)
            return redirect(url_for('my_pages.mypage')) 
        # Case: the client is an administrator
        if g.adminStatus == 1:
            g.dbObject.deleteAdminProfilePicture(g.userID)
            msg = "Profile picture deleted successfully"
            flash(msg)
            return redirect(url_for('my_pages.mypage')) 

@my_pages.route('/sourceOrder', methods=['GET','POST'])
def sourceOrder():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access My source order page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only administrators can access My source order page"
            flash(msg)
            return redirect(url_for('search'))
        else:
            sourceTable = g.dbObject.getSourceOrder(g.userID)
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
                        
            return render_template("sourceOrder.html", userID = g.userID, adminStatus = g.adminStatus, sourceList = sourceList)
            
@my_pages.route('/searchHistories', methods=['GET', 'POST'])
def searchHistories():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access My search history page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only administrators can access My search history page"
            flash(msg)
            return redirect(url_for('search'))
        else:
            searchHistoryTable = g.dbObject.getSearchHistory(g.userID)
            searchHistories = []
            for searchHistoryData in searchHistoryTable:
                searchHistories.append([searchHistoryData[0], searchHistoryData[1]])
                    
            return render_template('searchHistories.html', userID = g.userID, adminStatus = g.adminStatus, 
                                   searchHistories = searchHistories)
    
    if request.method == 'POST':
        historyToDelete = request.form["deleteDistinctWord"]
        searchHistoryData = str(historyToDelete)[1:-1]
        searchHistoryList = searchHistoryData.rsplit(", ", 1)
 
        wordString = searchHistoryList[1]
        word = wordString[1:-1]
            
        # Code to retrieve searchedDateTime from the page and reformat to delete in the database
        dateTimeString = searchHistoryList[0]
        dateTimeStr  = dateTimeString.replace("datetime.datetime", "")
        dateTime = dateTimeStr[1:-1]
        timestamp = datetime.datetime.strptime(dateTime, '%Y, %m, %d, %H, %M, %S')
            
        g.dbObject.deleteSpecificSearchHistory(g.userID, word, timestamp)
        msg = "The word, " + str(word) + ", has been deleted successfully from your search history."
        flash(msg)
        return redirect(url_for('my_pages.searchHistories'))  

@my_pages.route('/gameStatus', methods=['GET', 'POST'])
def gameStatus():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access My game status page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access My game status page"
            flash(msg)
            return redirect(url_for('search'))
        else:
            userWordRankData = g.dbObject.getUserWordRank(g.userID)
            userSentenceRankData = g.dbObject.getUserSentenceRank(g.userID)
            return render_template('gameStatus.html', userID = g.userID, adminStatus = g.adminStatus, 
                                   userWordRankData = userWordRankData, userSentenceRankData = userSentenceRankData)

@my_pages.route('/changeProfilePicture', methods = ['GET', 'POST'])
def changeProfilePicture():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change profile picture page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            return render_template('changeProfilePicture.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        newURL = request.form["newProfile"]
        currentPassword = request.form["currentPassword"]
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its password correctly
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserProfilePictureURL(accountID, newURL)  
                msg = "Your profile picture has been updated successfully!" 
                flash(msg)
                return redirect(url_for('my_pages.mypage')) 
            # Case: the user has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeProfilePicture')) 
        # Case: the client is an administrator        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
            # Case: the admin has entered its password correctly.    
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminProfilePictureURL(accountID, newURL) 
                msg = "Your profile picture has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('my_pages.mypage')) 
            # Case: the admin has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeProfilePicture')) 
                
@my_pages.route('/changeFullName', methods = ['GET', 'POST'])
def changeFullName():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change full name page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            return render_template('changeFullName.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        newFullName = request.form["newFullName"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user.
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its password correctly.
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserFullName(accountID, newFullName)  
                msg = "Your full name has been updated successfully!" 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))    
            # Case: the user has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeFullName'))    
        # Case: the client is an administrator        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
            # Case: the admin has entered its password correctly.    
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminFullName(accountID, newFullName) 
                msg = "Your full name has been updated successfully!" 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))
            # Case: the admin has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeFullName'))  

@my_pages.route('/changeNickName', methods = ['GET', 'POST'])
def changeNickName():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change nickname page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            return render_template('changeNickName.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        newNickName = request.form["newNickName"]
        currentPassword = request.form["currentPassword"]
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its password correctly
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserNickName(accountID, newNickName)  
                msg = "Your nick name has been updated successfully!" 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))
            # Case: the user has not entered its password correctly.
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeNickName')) 
        # Case: the client is an admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
            # Case: the admin has entered its userID and password correctly    
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminNickName(accountID, newNickName) 
                msg = "Your nick name has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('my_pages.mypage'))
            # Case: the admin has entered its userID or password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeNickName')) 

@my_pages.route('/changePassword', methods = ['GET', 'POST'])
def changePassword():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change password page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            return render_template('changePassword.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        currentPassword = request.form["currentPassword"]
        newPassword = request.form["newPassword"]
        confirmPassword = request.form["confirmPassword"]
        
        if currentPassword != confirmPassword:
            msg = "Please confirm your new password correctly"
            flash(msg)
            return redirect(url_for('my_pages.changePassword')) 
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its password correctly
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                newEncryptedPassword = generate_password_hash(newPassword)
                g.dbObject.updateUserPassword(accountID, newEncryptedPassword)  
                msg = "Your password has been updated successfully!" 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))
            # Case: the user has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changePassword')) 
        # Case: the client is an admin       
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
            # Case: the admin has entered its password correctly
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                newEncryptedPassword = generate_password_hash(newPassword) 
                g.dbObject.updateAdminPassword(accountID, newEncryptedPassword) 
                msg = "Your password has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('my_pages.mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changePassword')) 

@my_pages.route('/changeEmail', methods = ['GET', 'POST'])
def changeEmail():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change email page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            return render_template('changeEmail.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        newEmail = request.form["newEmail"]
        currentPassword = request.form["currentPassword"]
        
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its password correctly
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserEmail(accountID, newEmail)  
                msg = "Your email has been updated successfully!" 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))
            # Case: the user has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeEmail')) 
        # Case: the client is an admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
            # Case: the admin has entered its password correctly    
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminEmail(accountID, newEmail) 
                msg = "Your email has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('my_pages.mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeEmail')) 

@my_pages.route('/changePhone', methods = ['GET', 'POST'])
def changePhone():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access change phone number page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            return render_template('changePhone.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        newPhone = request.form["newPhone"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its password correctly
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserPhoneNumber(accountID, newPhone)  
                msg = "Your phone number has been updated successfully!" 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))
            # Case: the user has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changePhone')) 
        # Case: the admin is the client         
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
            # Case: the admin has entered its password correctly
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminPhoneNumber(accountID, newPhone) 
                msg = "Your phone number has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('my_pages.mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changePhone')) 

@my_pages.route('/unsubscribe', methods = ['GET', 'POST'])
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
        else:
            return render_template('unsubscribe.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its userID and password correctly
            if currentID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateUserSubscriptionStatus(accountID, 0)  
                msg = "You have unsubscribed successfully." 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your userID and password correctly"
                flash(msg)
                return redirect(url_for('my_pages.unsubscribe')) 

@my_pages.route('/resetSearchHistories', methods = ['GET', 'POST'])
def resetSearchHistories():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access reset search histories page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access reset search histories page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            return render_template('resetSearchHistories.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
            # Case: the user has entered its userID and password correctly
            if currentID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.deleteAllSearchHistory(accountID)  
                msg = "You search histories have been all deleted." 
                flash(msg)
                return redirect(url_for('my_pages.mypage'))
            # Case: the user has not entered its userID or password correctly
            else:
                msg = "Please enter your userID and password correctly"
                flash(msg)
                return redirect(url_for('my_pages.resetSearchHistories')) 

@my_pages.route('/resetWordRank', methods = ['GET', 'POST'])
def resetWordRank():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete word rank page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access delete word rank page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            return render_template('resetWordRank.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
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
                return redirect(url_for('my_pages.resetWordRank')) 

@my_pages.route('/resetSentenceRank', methods = ['GET', 'POST'])
def resetSentenceRank():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete sentence rank page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access delete sentence rank page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            return render_template('resetSentenceRank.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
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
                return redirect(url_for('my_pages.resetWordRank')) 

@my_pages.route('/resetTextRank', methods = ['GET', 'POST'])
@my_pages.route('/resetTextRank/<string:title>', methods = ['GET', 'POST'])
def resetTextRank(title):
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete text rank page."
            flash(msg)
            return redirect(url_for('signin')) 
        elif g.adminStatus == 1:
            msg = "Only users can access delete text rank page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            return render_template('resetTextRank.html', userID = g.userID, adminStatus = g.adminStatus, title = title)
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        # Case: the client is a user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
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
                return redirect(url_for('my_pages.resetTextRank', title = title))

@my_pages.route('/changeJob', methods = ['GET', 'POST'])
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
        else:
            return render_template('changeJob.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        newNickName = request.form["newJob"]
        currentPassword = request.form["currentPassword"]  
        # Case: the client is the admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
            # Case: the admin has entered its password correctly    
            if g.userID == accountID and check_password_hash(accountPassword, currentPassword):
                g.dbObject.updateAdminJobTitle(accountID, newNickName) 
                msg = "Your job title has been updated successfully!" 
                flash(msg)    
                return redirect(url_for('my_pages.mypage'))
            # Case: the admin has not entered its password correctly
            else:
                msg = "Please enter your current password correctly"
                flash(msg)
                return redirect(url_for('my_pages.changeJob'))  

@my_pages.route('/deleteAccount', methods = ['GET', 'POST'])
def deleteAccount():    
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access delete account page."
            flash(msg)
            return redirect(url_for('search')) 
        else:
            return render_template('deleteAccount.html', userID = g.userID, adminStatus = g.adminStatus)
        
    if request.method == 'POST':
        currentID = request.form["currentID"]
        currentPassword = request.form["currentPassword"]
        confirmPassword = request.form["confirmPassword"]
        
        if currentPassword != confirmPassword:
            msg = "Please confirm your password correctly"
            flash(msg)
            return redirect(url_for('my_pages.deleteAccount')) 
        
        # Case: the client is the user
        if g.adminStatus == 0:
            accountID, accountPassword = g.dbObject.getUserIDandPassword(g.userID)
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
                return redirect(url_for('my_pages.deleteAccount'))    
        # Case: the client is the admin        
        if g.adminStatus == 1:
            accountID, accountPassword = g.dbObject.getAdminIDandPassword(g.userID)
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
                return redirect(url_for('my_pages.deleteAccount'))  

@my_pages.route('/friends', methods = ['GET', 'POST'])
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
            friendData = g.dbObject.getFriends(g.userID)
            friendList = []
            
            for friendDatum in friendData:
                friendFullName = g.dbObject.getUserFullName(friendDatum[0])[0]
                friendNickName = g.dbObject.getUserNickName(friendDatum[0])[0]
                friendProfilePicture = g.dbObject.getUserProfilePicture(friendDatum[0])[0]
                friendList.append([friendDatum[0], friendFullName, friendNickName, friendProfilePicture])

            return render_template('friends.html', userID = g.userID, adminStatus = g.adminStatus, friendList = friendList)
    
    if request.method == 'POST':
        deleteID = request.form["deleteFriend"]
        g.dbObject.deleteFriend(g.userID, deleteID)
        return redirect(url_for('my_pages.friends')) 

@my_pages.route('/addFriends', methods = ['GET', 'POST'])
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
        else:
            return render_template('addFriends.html', userID = g.userID, adminStatus = g.adminStatus)
    
    if request.method == 'POST':
        receiverID = request.form["receiverID"]
        # Case: no corresponding account
        if g.dbObject.checkAccountExistence(receiverID)[0] == 0:
            msg = "Sending friend request has been failed. There is no corresponding account with the userID inputted."
            flash(msg)
            return redirect(url_for('my_pages.addFriends')) 
        # Case: the user has tried to send a friend request to the admin
        elif g.dbObject.checkUserAccountExistence(receiverID)[0] == 0:
            msg = "Sending friend request has been failed. You cannot send a friend request to the administrator."
            flash(msg)
            return redirect(url_for('my_pages.addFriends')) 
        # Case: the user has sent the friend request to itself
        elif receiverID == g.userID:
            msg = "Sending friend request has been failed. You cannot send a friend request to yourself."
            flash(msg)
            return redirect(url_for('my_pages.addFriends')) 
        else:
            friendRequestList = g.dbObject.getFriendRequests(g.userID) 
            for friendRequest in friendRequestList:
                # Case: already received a friend request from the receiver
                if receiverID == friendRequest[0]:
                    msg = "Sending a friend request has been failed. The receiver has already sent you the friend request."
                    flash(msg)
                    return redirect(url_for('my_pages.viewFriendRequests')) 
                
            friendRequestSentList = g.dbObject.getFriendRequestSent(g.userID) 
            for friendRequestSent in friendRequestSentList:
                # Case: already sent a friend request to the receiver
                if receiverID == friendRequestSent[0]:
                    msg = "You have already sent a friend request to " + str(receiverID) + "."
                    flash(msg)
                    return redirect(url_for('my_pages.friends')) 
                
            friendList = g.dbObject.getFriends(g.userID)
            for friend in friendList:
                # Case: already a friend
                if receiverID == friend[0]:
                    msg = "Sending a friend request has been failed. The receiver is already your friend."
                    flash(msg)
                    return redirect(url_for('my_pages.friends'))
                   
            g.dbObject.addFriendRequests(g.userID, receiverID)      
            msg = "A friend request has been sent successfully!" 
            flash(msg)
            return redirect(url_for('my_pages.friends')) 

@my_pages.route('/viewFriendRequests', methods = ['GET', 'POST'])
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
            senderTable = g.dbObject.getFriendRequests(g.userID)
            senderList = []
            for sender in senderTable:
                senderFullName = g.dbObject.getUserFullName(sender[0])[0]
                senderNickName = g.dbObject.getUserNickName(sender[0])[0]
                senderProfilePicture = g.dbObject.getUserProfilePicture(sender[0])[0]
                senderList.append([sender[0], senderFullName, senderNickName, senderProfilePicture])
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
            g.dbObject.deleteFriendRequests(rejectID, g.userID)
            return redirect(url_for('my_pages.friends')) 
        # Case: the user has clicked the accept button
        else:
            friendFullName = g.dbObject.getUserFullName(friendID)[0]
            msg = "You are now friends with " + friendFullName + "."
            flash(msg)
            g.dbObject.addFriend(friendID, g.userID)
            g.dbObject.deleteFriendRequests(friendID, g.userID)
            return redirect(url_for('my_pages.friends')) 