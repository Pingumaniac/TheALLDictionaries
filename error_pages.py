from flask import Flask, Blueprint, g, render_template, request, redirect, url_for, session, jsonify, flash, escape
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from python.thealldictionariesAPI import DB
import requests
import re

error_pages = Blueprint("error_pages", __name__, static_folder="static", template_folder="templates")

@error_pages.route('/400', methods = ['GET'])
def page400():
    if request.method == 'GET':
        return render_template('400.html', userID = g.userID, adminStatus = g.adminStatus), 400

@error_pages.route('/408', methods = ['GET'])
def page408():
    if request.method == 'GET':
        return render_template('408.html', userID = g.userID, adminStatus = g.adminStatus), 408

"""
HTTP status code 410 is given when the page for the corresponding URL has been deleted from the server(?),
but the data for this page is stored in the cache of the client's computer.
"""
@error_pages.route('/410', methods = ['GET'])
def page410():
    if request.method == 'GET':
        return render_template('410.html', userID = g.userID, adminStatus = g.adminStatus), 410

@error_pages.route('/429', methods = ['GET'])
def page429():
    if request.method == 'GET':
        return render_template('429.html', userID = g.userID, adminStatus = g.adminStatus), 429

@error_pages.route('/431', methods = ['GET'])
def page431():
    if request.method == 'GET':
        return render_template('431.html', userID = g.userID, adminStatus = g.adminStatus), 431

@error_pages.route('/451', methods = ['GET'])
def page451():
    if request.method == 'GET':
        return render_template('451.html', userID = g.userID, adminStatus = g.adminStatus), 451

@error_pages.route('/500', methods = ['GET'])
def page500():
    if request.method == 'GET':
        return render_template('500.html', userID = g.userID, adminStatus = g.adminStatus), 500

"""
Heroku handles each request for maximum 30 seconds as described in the following page:
https://devcenter.heroku.com/articles/request-timeout

I have noted that when the client enters an invalid(?) input for search e.g. arlhgkaerhblgaerkgrae
When deployed in Heroku, the application cannot give output in 30 seconds.
But when the error_pages is runned locally, I do not face this problem.
I have optimised dictionaries.py by removing JSON.dumps() and JSON.load() b/c that is just a repetitive work for 
creating a JSON file and interpreting a JSON file but still the error_pages cannot fully give a result in 30 seconds 
when deployed in Heroku.

Hence I have made a custom web page and displayed a possible reason for the timeout.
"""
@error_pages.route('/503', methods = ['GET'])
def page503():
    if request.method == 'GET':
        return render_template('503.html', userID = g.userID, adminStatus = g.adminStatus), 503