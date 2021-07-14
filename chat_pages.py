from flask import Flask, Blueprint, g, render_template, request, redirect, url_for, session, jsonify, flash, escape
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from python.thealldictionariesAPI import DB
import json
import time
import datetime
import requests
import re

chat_pages = Blueprint("chat_pages", __name__, static_folder="static", template_folder="templates")

@chat_pages.route('/groupChatMessage', methods=['GET', 'POST'])
def groupChatMessage():
    if request.method == 'GET':
        groupChatMessages = g.dbObject.getMessage('Group chat')
        groupChatDict = []
        for groupChatMessage in groupChatMessages:
            groupChatDict.append({'senderID': groupChatMessage[0], 'chatMessage': groupChatMessage[1], 
                                'sendDate': str(groupChatMessage[2]), 'nickName': groupChatMessage[3],
                                'profilePictureURL': groupChatMessage[4]})
        return json.dumps(groupChatDict), 200
    if request.method == 'POST':
        newMessage = request.get_json()
        chatMessage = newMessage["message"]
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        g.dbObject.sendMessage('Group chat', g.userID, None, chatMessage, timestamp)
        if g.adminStatus == 0:
            nickName = g.dbObject.getUserNickName(g.userID)[0]
            profilePictureURL = g.dbObject.getUserProfilePicture(g.userID)[0]
        else:
            nickName = g.dbObject.getUserNickName(g.userID)[0]
            profilePictureURL = g.dbObject.getUserProfilePicture(g.userID)[0]
        return json.dumps({'senderID': g.userID, 'chatMessage': chatMessage, 'sendDate': timestamp, 'nickName': nickName,
                           'profilePictureURL': profilePictureURL})

@chat_pages.route('/groupChat', methods=['GET'])
def groupChat():
    if request.method == 'GET':
        if g.userID == None:
            msg = "Please login to access Group chatting Page."
            flash(msg)
            return redirect(url_for('signin')) 
        else:
            messageTable = g.dbObject.getMessage('Group chat')
            return render_template('groupChat.html', userID = g.userID, adminStatus = g.adminStatus, chatroom='Group chat', messageTable = messageTable)