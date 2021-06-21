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
        self.queryList = []
        
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
    
    def executeAndCommit(self):
        for query in self.queryList:
            self.cursor.exceute(query)
        self.conn.commit()
        self.queryList = []
    
    def getUserID(self, userID):    
        query = f"SELECT userID FROM Account WHERE id = '{userID}'"
        self.cursor.execute(query)
        returnValue = self.cursor.fetchone()
        
        return returnValue[0] if returnValue else None

    def addUser(self, fullName, nickName, userID, password, email, phoneNumber):
        self.queryList.append(f"INSERT INTO Account VALUES ('{userID}', False)")
        self.queryList.append(f"""INSERT INTO UserAccount VALUES ('{fullName}', '{nickName}', '{userID}', '{password}', 
                                '{email}', '{phoneNumber}', False, NULL, NULL)""")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 1, 'mwl')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 2, 'mwc')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 3, 'oxford')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 4, 'free')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 5, 'yourdictionary')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 6, 'urban')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 7, 'etymonline')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 8, 'wordnik')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 9, 'wordnet')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 10, 'synonym')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 11, 'wikipedia')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 12, 'wiktionary')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 13, 'news')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 14, 'images')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 15, 'youtube')")
        self.queryList.append(f"INSERT INTO HasSourceOrder VALUES ('{userID}', 16, 'visuwords')")
        self.executeAndCommit()
    
    def addAdmin(self, fullName, nickName, userID, password, email, phoneNumber, jobTitle):
        self.queryList.append(f"INSERT INTO Account VALUES ('{userID}', True)")
        self.queryList.append(f"""INSERT INTO AdminAccount VALUES ('{fullName}', '{nickName}', '{userID}', 
                         '{password}', '{email}', '{phoneNumber}', '{jobTitle}', NULL)""")
        self.executeAndCommit()

    def checkAccountExistence(self, userID):
        query1 = f"SELECT COUNT(userID) FROM Account where userID = '{userID}'"
        self.cursor.execute(query1)
        accountExistence = self.cursor.fetchone()
        return accountExistence

    def checkUserAccountExistence(self, userID):
        query1 = f"SELECT COUNT(userID) FROM UserAccount where userID = '{userID}'"
        self.cursor.execute(query1)
        accountExistence = self.cursor.fetchone()
        return accountExistence

    def checkAdmin(self, userID):
        query1 = f"SELECT isAdmin FROM Account where userID = '{userID}'"
        self.cursor.execute(query1)
        adminStatus = self.cursor.fetchone()
        return adminStatus

    def deleteUser(self, userID):
        self.queryList.append(f"DELETE FROM HasSourceOrder WHERE userID = '{userID}'")
        self.queryList.append(f"DELETE FROM HasSearchHistory WHERE userID = '{userID}'")
        self.queryList.append(f"DELETE FROM HasWordRanking WHERE userID = '{userID}'")
        self.queryList.append(f"DELETE FROM IsFriendWith WHERE userID = '{userID}' OR friendID = '{userID}'")
        self.queryList.append(f"DELETE FROM SendFriendRequest WHERE senderID = '{userID}' OR receiverID = '{userID}'")
        self.queryList.append(f"DELETE FROM HasSentenceRanking WHERE userID = '{userID}'")
        self.queryList.append(f"DELETE FROM HasTextRanking WHERE userID = '{userID}'")
        self.queryList.append(f"DELETE FROM UserAccount WHERE userID = '{userID}'")
        self.queryList.append(f"DELETE FROM Account WHERE userID = '{userID}'")
        self.executeAndCommit()
    
    def deleteAdmin(self, userID):
        self.queryList.append(f"DELETE FROM AdminAccount WHERE userID = '{userID}'")
        self.queryList.append(f"DELETE FROM Account WHERE userID = '{userID}'")
        self.executeAndCommit()
    
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
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source1}' WHERE userID = '{userID}' AND sourceOrder = 1")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source2}' WHERE userID = '{userID}' AND sourceOrder = 2")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source3}' WHERE userID = '{userID}' AND sourceOrder = 3")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source4}' WHERE userID = '{userID}' AND sourceOrder = 4")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source5}' WHERE userID = '{userID}' AND sourceOrder = 5")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source6}' WHERE userID = '{userID}' AND sourceOrder = 6")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source7}' WHERE userID = '{userID}' AND sourceOrder = 7")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source8}' WHERE userID = '{userID}' AND sourceOrder = 8")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source9}' WHERE userID = '{userID}' AND sourceOrder = 9")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source10}' WHERE userID = '{userID}' AND sourceOrder = 10")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source11}' WHERE userID = '{userID}' AND sourceOrder = 11")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source12}' WHERE userID = '{userID}' AND sourceOrder = 12")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source13}' WHERE userID = '{userID}' AND sourceOrder = 13")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source14}' WHERE userID = '{userID}' AND sourceOrder = 14")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source15}' WHERE userID = '{userID}' AND sourceOrder = 15")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = '{source16}' WHERE userID = '{userID}' AND sourceOrder = 16")
        self.executeAndCommit()

    def resetSourceOrder(self, userID, source1, source2, source3, source4, source5, source6, source7, source8, source9, source10, source11, source12, source13):
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'mwl' WHERE userID = '{userID}' AND sourceOrder = 1")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'mwc' WHERE userID = '{userID}' AND sourceOrder = 2")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'oxford' WHERE userID = '{userID}' AND sourceOrder = 3")
        self.queryList.append(f"""UPDATE HasSourceOrder SET source = 'thefreedictionary' WHERE userID = '{userID}' 
                              AND sourceOrder = 4""")
        self.queryList.append(f"""UPDATE HasSourceOrder SET source = 'yourdictionary' WHERE userID = '{userID}' 
                              AND sourceOrder = 5""")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'urban' WHERE userID = '{userID}' AND sourceOrder = 6")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'etymonline' WHERE userID = '{userID}' AND sourceOrder = 7")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'wordnik' WHERE userID = '{userID}' AND sourceOrder = 8")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'wordnet' WHERE userID = '{userID}' AND sourceOrder = 9")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'synonyms' WHERE userID = '{userID}' AND sourceOrder = 10")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'wikipedia' WHERE userID = '{userID}' AND sourceOrder = 11")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'wiktionary' WHERE userID = '{userID}' AND sourceOrder = 12")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'googleImage' WHERE userID = '{userID}' AND sourceOrder = 13")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'googleNews' WHERE userID = '{userID}' AND sourceOrder = 14")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'YouTube' WHERE userID = '{userID}' AND sourceOrder = 15")
        self.queryList.append(f"UPDATE HasSourceOrder SET source = 'visuwords' WHERE userID = '{userID}' AND sourceOrder = 16")
        self.executeAndCommit()

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
        self.queryList.append(f"INSERT INTO TextChallenge VALUES ('{title}', '{textType}', '{challengeText}')")
        self.queryList.append(f"INSERT INTO GenerateTextChallenge VALUES ('{creatorID}', '{title}', '{dateCreated}')")
        self.executeAndCommit()

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
        self.queryList.append(f"DELETE FROM HasTextRanking WHERE challengeTitle = '{title}'")
        self.queryList.append(f"DELETE FROM TextChallenge WHERE title = '{title}'")
        self.queryList.append(f"DELETE FROM GenerateTextChallenge WHERE creatorID = '{creatorID}' AND title = '{title}'")
        self.executeAndCommit()
    
    def sendMessage(self, roomName, senderID, receiverID, chatMessage, sendDate):
        query1 = "INSERT INTO ChatRoom VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query1, (roomName, senderID, receiverID, chatMessage, sendDate))
        self.conn.commit()
    
    def getMessage(self, roomName):
        query1 = """SELECT ChatRoom.senderID, ChatRoom.chatMessage, ChatRoom.sendDate 
                            as sendDate, UserAccount.nickName as nickName, 
                            UserAccount.profilePictureURL as profilePictureURL 
                            FROM ChatRoom INNER JOIN UserAccount ON 
                            ChatRoom.senderID = UserAccount.userID WHERE ChatRoom.roomName = (%s) 
                            UNION SELECT ChatRoom.senderID, ChatRoom.chatMessage, ChatRoom.sendDate 
                            as sendDate, AdminAccount.nickName as nickName, AdminAccount.profilePictureURL 
                            as profilePictureURL FROM ChatRoom INNER JOIN AdminAccount 
                            ON ChatRoom.senderID = AdminAccount.userID WHERE ChatRoom.roomName = (%s) 
                            ORDER BY sendDate DESC"""
        self.cursor.execute(query1, (roomName, roomName))
        messageTable = self.cursor.fetchall()
        return messageTable