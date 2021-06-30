# TheALLDictionaries
Spring 2021 CSE 416 final project at the State University of New York Korea (SUNY Korea).

Note that the team has been splitted into two separate teams after project milestone 2.

## About Members and Roles

#### Young-jae (Bush) Moon
* Roles: Product owner, Project manager, Lead programmer and Designer
* Email: youngjae.moon@stonybrook.edu

## Past Members and Roles

#### Yoo-ra Kim 
* Role: Lead programmer
* Email: yoora.kim@stonybrook.edu

#### Seo-young Ko 
* Role: Designer
* Email: seoyoung.ko@stonybrook.edu

#### Seung-jae Kang 
* Role: Designer
* Email: seungjae.kang@stonybrook.edu

## Advisor

#### Professor Alexander Kuhn
* Teaching Assistant Professor in Computer Science at SUNY Korea

## Problem

When people do not know an English word, they have to search its definition from a dictionary. Although they may be satisfied with the meanings and the example sentences given from the dictionary, they may also be dissatisfied when they cannot fully grasp the word after reading the dictionary’s explanations. In this case, they then have to search its meaning through other dictionaries, encyclopedias or search relevant photos or videos from Google or YouTube for full understandings.

## Solution 

“TheALLDictionary” is a web-based application that helps people to search the meanings of the term from Merriam-Webster’s Learner’s dictionary, Merriam-Webster dictionary, Oxford English Dictionary, The Free Dictionary, Your Dictionary, Urban dictionary, Etymonline, Wordnik WordNet, synonym.com, Wiktionary, Wikipedia, Google News, Google Images, YouTube, Visuwords at once. Here Merriam-Webster’s Learner’s is the easiest dictionary in which the terms are explained in most simple and plain English. By contrast, the Merriam-Webster dictionary explains the terms at the intermediate level, and the Oxford English Dictionary explains them at more advanced levels. Thus, the Urban dictionary is especially useful for finding the definitions of slang words. Hence the user can find the explanations of the term at various levels from each dictionary. Thus, if a dictionary is not sufficient to understand the meaning of the word, then the user can refer to Wikipedia, Google News, Google Images and YouTube videos to understand more thoroughly.

The target audience of TheALLDictionary is someone who wants to search for the definition of an English word. Nonetheless, it is expected that students who learn English at school will use this application most frequently. Therefore, TheALLDictionary will include various typing challenges that will help them to memorise the new vocabularies and practice writing exemplar sentences, paragraphs and texts. Thus, by typing exemplar sentences, paragraphs and texts, they will be able to improve their grammar.

## Tools and technologies

### Programming languages and Database Management System (DBMS) used

1. JavaScript (ECMAScript 2020)
2. MySQL (MySQL Community Edition 8.0.24)
3. Python (3.8.11)

### Frameworks used

1. Bootstrap front-end framework (v5.0.0-beta 3)
2. Flask framework (v1.1.2)
3. jQuery (v3.6.0)

### Libraries used

1. WerkZeug (1.0.1)

### Application Programming Interfaces (API) used

1. Custom Search JSON API (v1)
2. Merriam-Webster's Learner's Dictionary with Audio (v3)
3. Merriam-Webster's Collegiate® Dictionary with Audio (v3)
4. Oxford Dictionaries API (v2.5)

### External Storage used

1. Amazon Relational Database Service (RDS)
2. GitHub (Check https://github.com/Pingumaniac/TheALLDictionaries-Image-Storage)

### Third-party packages used

1. beautifulsoup4 (4.9.3)
2. Flask-Bootstrap (3.3.7.1)
3. GoogleNews (1.5.7)
4. gunicorn (20.1.0)
5. PyDictionary (2.0.1)
6. PyMySQL (1.0.2)
7. requests (2.25.1)
8. udpy (2.0.0)
9. Wikipedia-API (0.5.4)
10. wiktionaryparser (0.0.97)
11. youtube-search-python (1.4.3)

## Instructions for checking out the latest stable version

### Method 1:
1. Open the main page for our GitHub repository: https://github.com/Pingumaniac/TheALLDictionaries
2. Click the following button: <img src = "https://user-images.githubusercontent.com/63883314/115416097-69ade280-a232-11eb-8401-8c41362ab4c2.png" width="44" height="14">
3. Click 'Download ZIP' option.
4. Unzip the folder.

### Method 2:
1.  Copy the web URL to your clipboard.
2.  Open 'Git Bash' from your local computer. You must have installed Git from the following page to do this: https://git-scm.com/downloads
3.  Move to the preferred directory.
4.  Next, type the following:
```
git clone
```
5. Then, all the codes and documents in the repository can be accessed.

Note: For Method 2, if you have already cloned the repository before, then you can skip the first two steps. And type this instead for step 4:
```
git type
```

## How to build this software

### 1. Please make sure you have downloaded MySQL (v8.0.24).

* Here is the URL for downloading the MySQL installer for Windows: https://dev.mysql.com/downloads/installer/
* Here is the URL that shows the instructions to install MySQL on macOS: https://dev.mysql.com/doc/mysql-osx-excerpt/5.7/en/osx-installation.html 

### 2. Install the following python packages using pip in the terminal:

```
pip install beautifulsoup4
pip install flask 
pip install Flask-Bootstrap
pip install GoogleNews
pip3 install gunicorn
pip install PyDictionary
pip install PyMySQL
pip install requests
pip install udpy
pip install Werkzeug
pip install wikipedia-api
pip install wiktionaryparser
pip3 install youtube-search-python
```

### 3. Deployment method

#### We will use Heroku to deploy the Flask. Note that:
 1. Git must be installed since Heroku uses Git. Please install Git from this website unless you have already installed: https://git-scm.com/downloads
 2. Python must be installed to use Flask. Please install Python 3.8.10 from this website unless you have already installed: https://www.python.org/downloads/

#### To install Heroku,
 1. Open the Heroku website. Here is the link for the Heroku website: https://www.heroku.com/
 2. Sign up a Heroku account.
 3. Install Heroku command-line interface (CLI) in your Terminal by following the instructions from this website: https://devcenter.heroku.com/articles/heroku-cli
 
 #### To use Heroku for deploying our application,
1. Make sure you have already installed Flask and Gunicorn. Check "How to build software" section to refer the installation processes for each of them.
2. Refer "Instructions for checking out the latest stable version" to download all the files needed to build this software.
3. Open the terminal and move to the folder directory which contains all the files for this project.
4. Login to your Heroku account in the terminal.
  ```
 heroku login
 ```
5. Use Procfice, requirements.txt and runtime.text given in the file.
6. Go to Heroku website again and create an application (name: thealldictionaries).
7. Clone the repository using Git.  
 ```
 heroku git:clone -a thealldictionaries
 ```
8. Make the following changes to Heroku using Git.
 Move to the folder which contains all the files for this project in the terminal. Example:
 ```
 cd thealldictionaries
 ```
 Then,
 ```
 heroku git:remote -a "thealldictionaries"
 git add .
 git commit -am "type whatever you wanna say here"
 git push heroku HEAD:master
```
9. If the following steps run successfully, the website URL will be printed in the console. 
```
https://thealldictionaries.herokuapp.com/
```

## How to test this software

* To test the software, you shall initially download the latest stable version of this software or instead visit https://thealldictionaries.herokuapp.com/. Please refer "Instructions for checking out the latest stable version" to download the correct version.
* You can download MySQL workbench (v8.0.24) and then connect with my Amazon RDS cloud. Refer def __init__() or connectDB() methods in the class DB in thealldictionariesAPI.py to view information about the Amazon RDS cloud. 
* If you have decided to run the software in your local terminal, move to the right folder and then run the app.py in the terminal.
* Now, you can test various functionalities and non-functional requirements. 

## Bug tracking

* All users can view and report a bug in "GitHub Issues" of our repository. 
* Here is the URL for viewing and reporting a list of bugs: https://github.com/Pingumaniac/TheALLDictionaries/issues
