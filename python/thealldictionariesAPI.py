import pymysql
import random

class DB():
    def __init__(self):
        self.conn = pymysql.connect(
                    host =  'database-1.cpvwrnt4qvgc.ap-northeast-2.rds.amazonaws.com',
                    port = 3306,
                    user = 'admin',
                    password = 'bushmoon18',
                    database = 'sys',
                    )
        self.cursor = self.conn.cursor()
        
    def connectDB(self):
        if self.conn.open != True:
            self.conn = pymysql.connect(
                host =  'database-1.cpvwrnt4qvgc.ap-northeast-2.rds.amazonaws.com',
                port = 3306,
                user = 'admin',
                password = 'bushmoon18',
                database = 'sys',
                )
            self.cursor = self.conn.cursor()
    
    def disconnectDB(self):
        self.conn.close()
    
    def getUserID(self, userID):    
        query = "SELECT userID FROM Account WHERE id = %s"
        self.cursor.execute(query, (userID))
        returnValue = self.cursor.fetchone()
        
        return returnValue[0] if returnValue else None

    def addUser(self, fullName, nickName, userID, password, email, phoneNumber):
        query1 = 'INSERT INTO Account VALUES (%s, %s)'
        query2 = 'INSERT INTO UserAccount VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NULL)'
        query3 = 'INSERT INTO HasSourceOrder VALUES (%s, %s, %s)'
    
        isAdmin = False
        isPremium = False
            
        self.cursor.execute(query1, (userID, isAdmin)) #, multi=True
        self.cursor.execute(query2, (fullName, nickName, userID, password, email, phoneNumber, isPremium)) #, multi=True
        
        self.cursor.execute(query3, (userID, 1, 'mwl'))
        self.cursor.execute(query3, (userID, 2, 'mwc'))
        self.cursor.execute(query3, (userID, 3, 'oxford'))
        self.cursor.execute(query3, (userID, 4, 'free'))
        self.cursor.execute(query3, (userID, 5, 'yourdictionary'))
        self.cursor.execute(query3, (userID, 6, 'urban'))
        self.cursor.execute(query3, (userID, 7, 'etymonline'))
        self.cursor.execute(query3, (userID, 8, 'wordnik'))
        self.cursor.execute(query3, (userID, 9, "wordnet"))
        self.cursor.execute(query3, (userID, 10, "synonym"))
        self.cursor.execute(query3, (userID, 11, "wikipedia"))
        self.cursor.execute(query3, (userID, 12, "wiktionary"))
        self.cursor.execute(query3, (userID, 13, "news"))
        self.cursor.execute(query3, (userID, 14, "images"))
        self.cursor.execute(query3, (userID, 15, "youtube"))
        self.cursor.execute(query3, (userID, 16, 'visuwords'))
    
        self.conn.commit()
    
    def addAdmin(self, fullName, nickName, userID, password, email, phoneNumber, jobTitle):
        query1 = 'INSERT INTO Account VALUES (%s, %s)'
        query2 = 'INSERT INTO AdminAccount VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)'
    
        isAdmin = True
            
        self.cursor.execute(query1, (userID, isAdmin)) #, multi=True
        self.cursor.execute(query2, (fullName, nickName, userID, password, email, phoneNumber, jobTitle)) #, multi=True
        self.conn.commit()

    def checkAccountExistence(self, userID):
        query1 = 'SELECT COUNT(userID) FROM Account where userID = (%s)'
        self.cursor.execute(query1, (userID))
        accountExistence = self.cursor.fetchone()
        return accountExistence

    def checkUserAccountExistence(self, userID):
        query1 = 'SELECT COUNT(userID) FROM UserAccount where userID = (%s)'
        self.cursor.execute(query1, (userID))
        accountExistence = self.cursor.fetchone()
        return accountExistence

    def checkAdmin(self, userID):
        query1 = 'SELECT isAdmin FROM Account where userID = (%s)'
        self.cursor.execute(query1, (userID))
        adminStatus = self.cursor.fetchone()
        return adminStatus

    def deleteUser(self, userID):
        query1 = 'DELETE FROM HasSourceOrder WHERE userID = (%s)'
        query2 = 'DELETE FROM HasSearchHistory WHERE userID = (%s)'
        query3 = 'DELETE FROM HasCardPackage WHERE userID = (%s)'
        query4 = 'DELETE FROM HasWordRanking WHERE userID = (%s)'
        query5 = 'DELETE FROM IsFriendWith WHERE userID = (%s) OR friendID = (%s)'
        query6 = 'DELETE FROM SendFriendRequest WHERE senderID = (%s) OR receiverID = (%s)'
        query7 = 'DELETE FROM HasWordRanking WHERE userID = (%s)'
        query8 = 'DELETE FROM UserAccount WHERE userID = (%s)'
        query9 = 'DELETE FROM Account WHERE userID = (%s)'
    
        self.cursor.execute(query1, (userID))
        self.cursor.execute(query2, (userID))
        self.cursor.execute(query3, (userID))
        self.cursor.execute(query4, (userID))
        self.cursor.execute(query5, (userID, userID))
        self.cursor.execute(query6, (userID, userID))
        self.cursor.execute(query7, (userID))
        self.cursor.execute(query8, (userID))
        self.cursor.execute(query9, (userID))
        self.conn.commit()
    
    def deleteAdmin(self, userID):
        query1 = 'DELETE FROM AdminAccount WHERE userID = (%s)'
        query2 = 'DELETE FROM Account WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        self.cursor.execute(query2, (userID))
        self.conn.commit()
    
    def getUserData(self, userID):
        query1 = 'SELECT * FROM UserAccount WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        userDataTable = self.cursor.fetchone()
        return userDataTable

    def getUserIDandPassword(self, userID):
        query1 = 'SELECT userID, password FROM UserAccount WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        userDataTable = self.cursor.fetchone()
        return userDataTable

    def getUserFullName(self, userID):
        query1 = 'SELECT fullName FROM UserAccount WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        userDataTable = self.cursor.fetchone()
        return userDataTable

    def getUserNickName(self, userID):
        query1 = 'SELECT nickName FROM UserAccount WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        userDataTable = self.cursor.fetchone()
        return userDataTable

    def getUserProfilePicture(self, userID):
        query1 = 'SELECT profilePictureURL FROM UserAccount WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        userDataTable = self.cursor.fetchone()
        return userDataTable

    def getAdminData(self, userID):
        query1 = 'SELECT * FROM AdminAccount WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        adminDataTable = self.cursor.fetchone()
        return adminDataTable

    def getAdminIDandPassword(self, userID):
        query1 = 'SELECT userID, password FROM AdminAccount WHERE userID = (%s)'
        self.cursor.execute(query1, (userID))
        adminDataTable = self.cursor.fetchone()
        return adminDataTable

    def updateUserProfilePictureURL(self, userID, newURL):
        query = 'UPDATE UserAccount SET profilePictureURL = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newURL, userID))
        self.conn.commit()
    
    def updateAdminProfilePictureURL(self, userID, newURL):
        query = 'UPDATE AdminAccount SET profilePictureURL = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newURL, userID))
        self.conn.commit()
    
    def deleteUserProfilePicture(self, userID):
        query = 'UPDATE UserAccount SET profilePictureURL = NULL WHERE userID = (%s)'
        self.cursor.execute(query, (userID))
        self.conn.commit()
        
    def deleteAdminProfilePicture(self, userID):
        query = 'UPDATE AdminAccount SET profilePictureURL = NULL WHERE userID = (%s)'
        self.cursor.execute(query, (userID))
        self.conn.commit()
    
    def updateUserFullName(self, userID, newFullName):
        query = 'UPDATE UserAccount SET fullName = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newFullName, userID))
        self.conn.commit()
    
    def updateAdminFullName(self, userID, newFullName):
        query = 'UPDATE AdminAccount SET fullName = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newFullName, userID))
        self.conn.commit()
    
    def updateUserNickName(self, userID, newNickName):
        query = 'UPDATE UserAccount SET nickName = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newNickName, userID))
        self.conn.commit()
    
    def updateAdminNickName(self, userID, newNickName):
        query = 'UPDATE AdminAccount SET nickName = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newNickName, userID))
        self.conn.commit()
    
    def updateUserPassword(self, userID, newPassword):
        query = 'UPDATE UserAccount SET password = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newPassword, userID))
        self.conn.commit()
    
    def updateAdminPassword(self, userID, newPassword):
        query = 'UPDATE AdminAccount SET password = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newPassword, userID))
        self.conn.commit()
    
    def updateUserEmail(self, userID, newEmail):
        query = 'UPDATE UserAccount SET email = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newEmail, userID))
        self.conn.commit()
    
    def updateAdminEmail(self, userID, newEmail):
        query = 'UPDATE AdminAccount SET email = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newEmail, userID))
        self.conn.commit()
    
    def updateUserPhoneNumber(self, userID, newPhoneNumber):
        query = 'UPDATE UserAccount SET phoneNumber = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newPhoneNumber, userID))
        self.conn.commit()
    
    def updateAdminPhoneNumber(self, userID, newPhoneNumber):
        query = 'UPDATE AdminAccount SET phoneNumber = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newPhoneNumber, userID))
        self.conn.commit()
    
    def updateUserSubscriptionStatus(self, userID, premiumStatus):
        query = 'UPDATE UserAccount SET isPremium = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (premiumStatus, userID))
        self.conn.commit()
    
    def updateUserSubscriptionEndDate(self, userID, newEndDate):
        query = 'UPDATE UserAccount SET subscriptionEndDate = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newEndDate, userID))
        self.conn.commit()
    
    def updateAdminJobTitle(self, userID, newJobTitle):
        query = 'UPDATE AdminAccount SET jobTitle = (%s) WHERE userID = (%s)'
        self.cursor.execute(query, (newJobTitle, userID))
        self.conn.commit()
    
    def getSourceOrder(self, userID):
        query = 'SELECT source FROM HasSourceOrder WHERE userID = (%s) ORDER BY sourceOrder ASC'
        self.cursor.execute(query, (userID))
        sourceTable = self.cursor.fetchall()
        return sourceTable
    
    def updateSourceOrder(self, userID, source1, source2, source3, source4, source5, source6, source7, source8, source9, source10, source11, source12, source13, source14, source15, source16):
        query1 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 1'
        query2 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 2'
        query3 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 3'
        query4 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 4'
        query5 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 5'
        query6 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 6'
        query7 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 7'
        query8 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 8'
        query9 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 9'
        query10 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 10'
        query11 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 11'
        query12 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 12'
        query13 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 13'
        query14 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 14'
        query15 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 15'
        query16 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND sourceOrder = 16'
    
        self.cursor.execute(query1, (source1, userID))
        self.cursor.execute(query2, (source2, userID))
        self.cursor.execute(query3, (source3, userID))
        self.cursor.execute(query4, (source4, userID))
        self.cursor.execute(query5, (source5, userID))
        self.cursor.execute(query6, (source6, userID))
        self.cursor.execute(query7, (source7, userID))
        self.cursor.execute(query8, (source8, userID))
        self.cursor.execute(query9, (source9, userID))
        self.cursor.execute(query10, (source10, userID))
        self.cursor.execute(query11, (source11, userID))
        self.cursor.execute(query12, (source12, userID))
        self.cursor.execute(query13, (source13, userID))
        self.cursor.execute(query14, (source14, userID))
        self.cursor.execute(query15, (source15, userID))
        self.cursor.execute(query16, (source16, userID))
    
        self.conn.commit()

    def resetSourceOrder(self, userID, source1, source2, source3, source4, source5, source6, source7, source8, source9, source10, source11, source12, source13):
        query1 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 1'
        query2 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 2'
        query3 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 3'
        query4 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 4'
        query5 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 5'
        query6 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 6'
        query7 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 7'
        query8 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 8'
        query9 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 9'
        query10 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 10'
        query11 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 11'
        query12 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 12'
        query13 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 13'
        query14 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 14'
        query15 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 15'
        query16 = 'UPDATE HasSourceOrder SET source = (%s) WHERE userID = (%s) AND order = 16'
    
        self.cursor.execute(query1, 'mwl', userID)
        self.cursor.execute(query2, 'mwc', userID)
        self.cursor.execute(query3, 'oxford', userID)
        self.cursor.execute(query4, 'thefreedictionary', userID)
        self.cursor.execute(query5, 'yourdictionary', userID)
        self.cursor.execute(query6, 'urban', userID)
        self.cursor.execute(query7, 'etymonline', userID)
        self.cursor.execute(query8, 'wordnik', userID)
        self.cursor.execute(query9, 'wordnet', userID)
        self.cursor.execute(query10, 'synonyms', userID)
        self.cursor.execute(query11, 'wikipedia', userID)
        self.cursor.execute(query12, 'wiktionary', userID)
        self.cursor.execute(query13, 'googleImage', userID)
        self.cursor.execute(query14, 'googeNews', userID)
        self.cursor.execute(query15, 'YouTube', userID)
        self.cursor.execute(query16, 'visuwords', userID)
    
        self.conn.commit()

    def addSearchHistory(self, userID, timestamp, word):
        query = "INSERT INTO HasSearchHistory (userID, searchedDateTime, word) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (userID, timestamp, word))
        self.conn.commit()
    
    def getSearchHistory(self, userID):
        query = "SELECT searchedDateTime, word FROM HasSearchHistory WHERE userID = (%s) ORDER BY searchedDateTime DESC"
        self.cursor.execute(query, (userID))
        searchHistoryTable = self.cursor.fetchall()
        return searchHistoryTable

    def getDistinctWordSearchHistory(self, userID):
        query = "SELECT DISTINCT word FROM HasSearchHistory WHERE userID = (%s) ORDER BY searchedDateTime DESC"
        self.cursor.execute(query, (userID))
        searchHistoryTable = self.cursor.fetchall()
        return searchHistoryTable

    def deleteAllSearchHistory(self, userID):
        query = "DELETE FROM HasSearchHistory WHERE userID = (%s)"
        self.cursor.execute(query, (userID))
        self.conn.commit()
    
    def deleteSearchHistory(self, userID, word):
        query = "DELETE FROM HasSearchHistory WHERE userID = (%s) AND word = (%s)"
        self.cursor.execute(query, (userID, word))
        self.conn.commit()
    
    def deleteSpecificSearchHistory(self, userID, word, searchedDateTime):
        query = "DELETE FROM HasSearchHistory WHERE userID = (%s) AND word = (%s) AND searchedDateTime = (%s)"
        self.cursor.execute(query, (userID, word, searchedDateTime))
        self.conn.commit()
    
    def addFriendRequests(self, senderID, receiverID):
        query = "INSERT INTO SendFriendRequest VALUES (%s, %s)"
        self.cursor.execute(query, (senderID, receiverID))
        self.conn.commit()
    
    def getFriendRequests(self, receiverID):
        query = "SELECT senderID FROM SendFriendRequest WHERE receiverID = (%s)"
        self.cursor.execute(query, (receiverID))
        friendRequestTable = self.cursor.fetchall()
        return friendRequestTable
    
    def getFriendRequestSent(self, senderID):
        query = "SELECT receiverID FROM SendFriendRequest WHERE senderID = (%s)"
        self.cursor.execute(query, (senderID))
        friendRequestSentTable = self.cursor.fetchall()
        return friendRequestSentTable

    def deleteFriendRequests(self, senderID, receiverID):
        query = "DELETE FROM SendFriendRequest WHERE senderID = (%s) AND receiverID = (%s)"
        self.cursor.execute(query, (senderID, receiverID))
        self.conn.commit()
     
    def addFriend(self, userID, friendID):
        query = "INSERT INTO IsFriendWith VALUES (%s, %s)"
        self.cursor.execute(query, (userID, friendID))
        self.conn.commit()

    def getFriends(self, userID):
        query = '''SELECT friendID AS friendUserID FROM IsFriendWith WHERE userID = (%s) UNION 
                   SELECT userID AS friendUserID FROM IsFriendWith WHERE friendID = (%s)'''
        self.cursor.execute(query, (userID, userID))
        friendList = self.cursor.fetchall()
        return friendList

    def deleteFriend(self, userID, friendID):
        query = "DELETE FROM IsFriendWith WHERE userID = (%s) AND friendID = (%s)"
        self.cursor.execute(query, (userID, friendID))
        self.cursor.execute(query, (friendID, userID))
        self.conn.commit()
    
    def addWordRanking(self, userID, newScore):
        query = "INSERT INTO HasWordRanking VALUES (%s, %s)"
        self.cursor.execute(query, (userID, newScore))
        self.conn.commit()    

    def addSentenceRanking(self, userID, newScore):
        query = "INSERT INTO HasSentenceRanking VALUES (%s, %s)"
        self.cursor.execute(query, (userID, newScore))
        self.conn.commit()
    
    def addTextRanking(self, userID, newScore, challengeTitle):
        query = "INSERT INTO HasTextRanking VALUES (%s, %s, %s)"
        self.cursor.execute(query, (challengeTitle, userID, newScore))
        self.conn.commit()
    
    def getWordRanking(self, userID):
        query = "SELECT highestScore FROM HasWordRanking WHERE userID = (%s)"
        self.cursor.execute(query, (userID))
        highestScore = self.cursor.fetchone()
        return highestScore  

    def getSentenceRanking(self, userID):
        query = "SELECT highestScore FROM HasSentenceRanking WHERE userID = (%s)"
        self.cursor.execute(query, (userID))
        highestScore = self.cursor.fetchone()
        return highestScore    
    
    def getTextRanking(self, userID, challengeTitle):
        query = "SELECT highestScore FROM HasTextRanking WHERE userID = (%s) AND challengeTitle = (%s)"
        self.cursor.execute(query, (userID, challengeTitle))
        highestScore = self.cursor.fetchone()
        return highestScore    
    
    def getUserWordRank(self, userID):
        query = '''WITH UserWordRanking AS (SELECT *, row_number() OVER (ORDER BY highestScore DESC) wordRank 
                    FROM HasWordRanking) SELECT highestScore, wordRank FROM UserWordRanking WHERE userID = (%s)'''
        self.cursor.execute(query, (userID))
        userWordRankData = self.cursor.fetchone()
        return userWordRankData
    
    def getUserSentenceRank(self, userID):
        query = '''WITH UserSentenceRanking AS (SELECT *, row_number() OVER (ORDER BY highestScore DESC) sentenceRank 
                    FROM HasSentenceRanking) SELECT highestScore, sentenceRank FROM UserSentenceRanking WHERE userID = (%s)'''
        self.cursor.execute(query, (userID))
        userSentenceRankData = self.cursor.fetchone()
        return userSentenceRankData

    def getAllWordRanking(self):
        query = '''SELECT HasWordRanking.userID, HasWordRanking.highestScore, UserAccount.nickName, UserAccount.profilePictureURL 
                    FROM HasWordRanking LEFT JOIN UserAccount ON HasWordRanking.userID = UserAccount.userID ORDER BY 
                    HasWordRanking.highestScore DESC'''
        self.cursor.execute(query)
        wordRankingFullTable = self.cursor.fetchall()
        return wordRankingFullTable

    def getAllSentenceRanking(self):
        query = '''SELECT HasSentenceRanking.userID, HasSentenceRanking.highestScore, UserAccount.nickName, UserAccount.profilePictureURL 
                    FROM HasSentenceRanking LEFT JOIN UserAccount ON HasSentenceRanking.userID = UserAccount.userID ORDER BY
                    HasSentenceRanking.highestScore DESC'''
        self.cursor.execute(query)
        sentenceRankingFullTable = self.cursor.fetchall()
        return sentenceRankingFullTable
    
    def getAllTextRanking(self, challengeTitle):
        query = '''SELECT HasTextRanking.userID, HasTextRanking.highestScore, UserAccount.nickName, UserAccount.profilePictureURL 
                    FROM HasTextRanking LEFT JOIN UserAccount ON HasTextRanking.userID = UserAccount.userID WHERE 
                    HasTextRanking.challengeTitle = (%s) ORDER BY HasTextRanking.highestScore DESC'''
        self.cursor.execute(query, (challengeTitle))
        textRankingFullTable = self.cursor.fetchall()
        return textRankingFullTable

    def updateWordRanking(self, userID, newScore):
        query = "UPDATE HasWordRanking SET highestScore = (%s) WHERE userID = (%s)"
        self.cursor.execute(query, (newScore, userID))
        self.conn.commit()
    
    def updateSentenceRanking(self, userID, newScore):
        query = "UPDATE HasSentenceRanking SET highestScore = (%s) WHERE userID = (%s)"
        self.cursor.execute(query, (newScore, userID))
        self.conn.commit()
    
    def updateTextRanking(self, userID, newScore, challengeTitle):
        query = "UPDATE HasTextRanking SET highestScore = (%s) WHERE userID = (%s) AND challengeTitle = (%s)"
        self.cursor.execute(query, (newScore, userID, challengeTitle))
        self.conn.commit()

    def deleteWordRanking(self, userID):
        query = "DELETE FROM HasWordRanking WHERE userID = (%s)"
        self.cursor.execute(query, (userID))
        self.conn.commit()
    
    def deleteSentenceRanking(self, userID):
        query = "DELETE FROM HasSentenceRanking WHERE userID = (%s)"
        self.cursor.execute(query, (userID))
        self.conn.commit()
    
    def deleteTextRanking(self, userID, challengeTitle):
        query = "DELETE FROM HasTextRanking WHERE userID = (%s) AND challengeTitle = (%s)"
        self.cursor.execute(query, (userID, challengeTitle))
        self.conn.commit()
    
    def addTextChallenge(self, creatorID, title, textType, challengeText, dateCreated):
        query1 = "INSERT INTO TextChallenge VALUES (%s, %s, %s)"
        query2 = "INSERT INTO GenerateTextChallenge VALUES (%s, %s, %s)"
        
        self.cursor.execute(query1, (title, textType, challengeText))
        self.cursor.execute(query2, (creatorID, title, dateCreated))
        self.conn.commit()

    def getTextChallenge(self):
        query1 = '''SELECT creatorID, title FROM GenerateTextChallenge WHERE title IN 
                    (SELECT title FROM TextChallenge WHERE textType = 'literature') ORDER BY dateCreated DESC'''
        self.cursor.execute(query1)
        literatureTable = self.cursor.fetchall()
    
        query2 = '''SELECT creatorID, title FROM GenerateTextChallenge WHERE title IN 
                    (SELECT title FROM TextChallenge WHERE textType = 'speech') ORDER BY dateCreated DESC'''
        self.cursor.execute(query2)
        speechTable = self.cursor.fetchall()
    
        query3 = '''SELECT creatorID, title FROM GenerateTextChallenge WHERE title IN 
                    (SELECT title FROM TextChallenge WHERE textType = 'law') ORDER BY dateCreated DESC'''
        self.cursor.execute(query3)
        lawTable = self.cursor.fetchall()
    
        query4 = '''SELECT creatorID, title FROM GenerateTextChallenge WHERE title IN 
                    (SELECT title FROM TextChallenge WHERE textType = 'articles') ORDER BY dateCreated DESC'''
        self.cursor.execute(query4)
        articleTable = self.cursor.fetchall()
    
        query5 = '''SELECT creatorID, title FROM GenerateTextChallenge WHERE title IN 
                    (SELECT title FROM TextChallenge WHERE textType = 'essays') ORDER BY dateCreated DESC'''
        self.cursor.execute(query5)
        essayTable = self.cursor.fetchall()
        
        return literatureTable, speechTable, lawTable, articleTable, essayTable
    
    def checkTextChallengeTitle(self, title):
        query = "SELECT COUNT(title) FROM TextChallenge WHERE title = (%s)"
        self.cursor.execute(query, title)
        titleList = self.cursor.fetchone()
        return titleList

    def getMyTextChallenge(self, creatorID):
        query1 = '''SELECT title, textType FROM TextChallenge WHERE title IN 
                    (SELECT title FROM GenerateTextChallenge WHERE creatorID = (%s) ORDER BY dateCreated DESC) 
                    AND texttype = 'literature';'''
        self.cursor.execute(query1, (creatorID))
        myLiteratureTable = self.cursor.fetchall()
    
        query2 = '''SELECT title, textType FROM TextChallenge WHERE title IN 
                    (SELECT title FROM GenerateTextChallenge WHERE creatorID = (%s) ORDER BY dateCreated DESC) 
                    AND texttype = 'speech';'''
        self.cursor.execute(query2, (creatorID))
        mySpeechTable = self.cursor.fetchall()
    
        query3 = '''SELECT title, textType FROM TextChallenge WHERE title IN 
                    (SELECT title FROM GenerateTextChallenge WHERE creatorID = (%s) ORDER BY dateCreated DESC) 
                    AND texttype = 'law';'''
        self.cursor.execute(query3, (creatorID))
        myLawTable = self.cursor.fetchall()
    
        query4 = '''SELECT title, textType FROM TextChallenge WHERE title IN 
                    (SELECT title FROM GenerateTextChallenge WHERE creatorID = (%s) ORDER BY dateCreated DESC) 
                    AND texttype = 'articles';'''
        self.cursor.execute(query4, (creatorID))
        myArticleTable = self.cursor.fetchall()
    
        query5 = '''SELECT title, textType FROM TextChallenge WHERE title IN 
                    (SELECT title FROM GenerateTextChallenge WHERE creatorID = (%s) ORDER BY dateCreated DESC) 
                    AND texttype = 'essays';'''
        self.cursor.execute(query5, (creatorID))
        myEssayTable = self.cursor.fetchall()

        return myLiteratureTable, mySpeechTable, myLawTable, myArticleTable, myEssayTable

    def getChallengeText(self, title):
        query1 = "SELECT challengeText FROM TextChallenge WHERE title = (%s)"
        self.cursor.execute(query1, (title))
        challengeText = self.cursor.fetchone()
        return challengeText

    def deleteMyChallenge(self, creatorID, title):
        query1 = "DELETE FROM HasTextRanking WHERE challengeTitle = (%s)"
        query2 = "DELETE FROM TextChallenge WHERE title = (%s)"
        query3 = "DELETE FROM GenerateTextChallenge WHERE creatorID = (%s) AND title = (%s)"
        self.cursor.execute(query1, (title))
        self.cursor.execute(query2, (title))
        self.cursor.execute(query3, (creatorID, title))
        self.conn.commit()
    
    def sendMessage(self, roomName, senderID, receiverID, chatMessage, sendDate):
        query1 = "INSERT INTO ChatRoom VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query1, (roomName, senderID, receiverID, chatMessage, sendDate))
        self.conn.commit()
    
    def getMessage(self, roomName):
        query1 = '''SELECT ChatRoom.senderID, ChatRoom.chatMessage, ChatRoom.sendDate 
                            as sendDate, UserAccount.nickName as nickName, 
                            UserAccount.profilePictureURL as profilePictureURL 
                            FROM ChatRoom INNER JOIN UserAccount ON 
                            ChatRoom.senderID = UserAccount.userID WHERE ChatRoom.roomName = (%s) 
                            UNION SELECT ChatRoom.senderID, ChatRoom.chatMessage, ChatRoom.sendDate 
                            as sendDate, AdminAccount.nickName as nickName, AdminAccount.profilePictureURL 
                            as profilePictureURL FROM ChatRoom INNER JOIN AdminAccount 
                            ON ChatRoom.senderID = AdminAccount.userID WHERE ChatRoom.roomName = (%s) 
                            ORDER BY sendDate DESC'''
        self.cursor.execute(query1, (roomName, roomName))
        messageTable = self.cursor.fetchall()
        return messageTable