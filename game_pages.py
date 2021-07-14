from flask import Flask, Blueprint, g, render_template, request, redirect, url_for, session, jsonify, flash, escape
from flask_bootstrap import Bootstrap
import pymysql
from python.thealldictionariesAPI import DB
import json
import time
import datetime
import requests
import re

game_pages = Blueprint("game_pages", __name__, static_folder="static", template_folder="templates")

@game_pages.route('/wordTypingChallenge', methods = ['GET', 'POST'])
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
        else:
            return render_template('wordTypingChallenge.html', userID = g.userID, adminStatus = g.adminStatus, score = 0)
    
    if request.method == 'POST':
        scoreSubmit = request.form["scoreSubmit"]
        
        # Case: The user has not submitted its score yet
        if g.dbObject.getWordRanking(g.userID) == None:
            if scoreSubmit == "0":
                g.dbObject.addWordRanking(g.userID, 0)
            else:
                g.dbObject.addWordRanking(g.userID, int(scoreSubmit))
            
            flash("You have added your score in the ranking!")
            return redirect(url_for('game_pages.wordrank'))
        else:
            highestScore = g.dbObject.getWordRanking(g.userID)[0]
            if scoreSubmit != "":
                # Case: the user has performed better from its previous results so far
                if highestScore < int(scoreSubmit):
                    g.dbObject.updateWordRanking(g.userID, int(scoreSubmit))
                    flash("You have updated your score in the ranking!")
                    return redirect(url_for('game_pages.wordrank'))
                # Case: the user did not perform best
                else:
                    flash("You did not break your highest record!")
                    return redirect(url_for('game_pages.wordrank'))
            # Case: the user did not perform best (scoreSubmit is null)
            else:
                flash("You did not make a new record!")
                return redirect(url_for('game_pages.wordrank'))

@game_pages.route('/sentenceTypingChallenge', methods = ['GET', 'POST'])
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
        else:
            return render_template('sentenceTypingChallenge.html', userID = g.userID, adminStatus = g.adminStatus, score = 0)
    
    if request.method == 'POST':
        scoreSubmit = request.form["scoreSubmit"]
        
        # Case: The user has not submitted its score yet
        if g.dbObject.getSentenceRanking(g.userID) == None:
            if scoreSubmit == "0":
                g.dbObject.addSentenceRanking(g.userID, 0)
            else:
                g.dbObject.addSentenceRanking(g.userID, int(scoreSubmit))
            flash("You have added your score in the ranking!")
            return redirect(url_for('game_pages.sentenceRank'))
        else:
            highestScore = g.dbObject.getSentenceRanking(g.userID)[0]
            if scoreSubmit != "":
                # Case: the user has performed better from its previous results so far
                if highestScore < int(scoreSubmit):
                    g.dbObject.updateSentenceRanking(g.userID, int(scoreSubmit))
                    flash("You have updated your score in the ranking!")
                    return redirect(url_for('game_pages.sentenceRank'))
                # Case: the user did not perform best
                else:
                    flash("You did not break your highest record!")
                    return redirect(url_for('game_pages.sentenceRank'))
            # Case: the user did not perform best (scoreSubmit is null)
            else:
                flash("You did not make a new record!")
                return redirect(url_for('game_pages.sentenceRank'))

@game_pages.route('/textTypingChallenge', methods = ['GET', 'POST'])
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

@game_pages.route('/createTextChallenge', methods = ['GET', 'POST'])
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
        else:
            return render_template('createTextChallenge.html', userID = g.userID, adminStatus = g.adminStatus)
    
    if request.method == 'POST':
        title = request.form['title']
        textType = request.form['textType']
        text = request.form['text']
        
        checkTitle = g.dbObject.checkTextChallengeTitle(title)[0]
        
        # Case: there is no such text typing challenge with the same title
        if checkTitle == 0:
            ts = time.time()
            dateCreated = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            g.dbObject.addTextChallenge(g.userID, title, textType, text, dateCreated)
            msg = "Challenge successfully added."
            flash(msg)
            return redirect(url_for('game_pages.viewTextChallenge')) 
        # Case: there is a text typing challenge with the same title (checkTitle = 1)
        else:
            msg = "Error. There is already a challenge with the title - " + str(title) + "."
            flash(msg)
            return redirect(url_for('game_pages.createTextChallenge')) 

@game_pages.route('/viewTextChallenge', methods = ['GET', 'POST'])
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
            myLiteratureTable, mySpeechTable, myLawTable, myArticleTable, myEssayTable = g.dbObject.getMyTextChallenge(g.userID)
            return render_template('viewTextChallenge.html', userID = g.userID, adminStatus = g.adminStatus, 
                                   myLiteratureTable = myLiteratureTable, mySpeechTable = mySpeechTable, 
                                   myLawTable = myLawTable, myArticleTable = myArticleTable, myEssayTable = myEssayTable)
    
    if request.method == 'POST':
        challengeTitle = request.form["deleteTextChallenge"]
        g.dbObject.deleteMyChallenge(g.userID, challengeTitle)
        msg = "Challenge has been deleted successfully"
        flash(msg)
        return redirect(url_for('game_pages.viewTextChallenge')) 

@game_pages.route('/viewChallengeText', methods = ['GET'])
@game_pages.route('/viewChallengeText/<string:title>', methods = ['GET'])
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

@game_pages.route('/startTextTyping', methods = ['GET', 'POST'])
@game_pages.route('/startTextTyping/<string:title>', methods = ['GET', 'POST'])
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
        if g.dbObject.getTextRanking(g.userID, title) == None:
            if scoreSubmit == "0":
                g.dbObject.addTextRanking(g.userID, 0, title)
            else:
                g.dbObject.addTextRanking(g.userID, int(scoreSubmit), title)
            flash("You have added your score in the ranking!")
            return redirect(url_for('game_pages.textRank', title = title))
        else:
            highestScore = g.dbObject.getTextRanking(g.userID, title)[0]
            if scoreSubmit != "":
                # Case: the user performed best this time
                if highestScore < int(scoreSubmit):
                    g.dbObject.updateTextRanking(g.userID, int(scoreSubmit), title)
                    flash("You have updated your score in the ranking!")
                    return redirect(url_for('game_pages.textRank', title = title))
                # Case: the user did not perform best this time
                else:
                    flash("You did not break your highest record!")
                    return redirect(url_for('game_pages.textRank', title = title))
            # Case: the user did not perform best this time
            else:
                flash("You did not make a new record!")
                return redirect(url_for('game_pages.textRank', title = title))
    
@game_pages.route('/textRank', methods = ['GET', 'POST'])
@game_pages.route('/textRank/<string:title>', methods = ['GET', 'POST'])
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

@game_pages.route('/wordrank', methods = ['GET'])
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
        
@game_pages.route('/sentenceRank', methods = ['GET'])
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
