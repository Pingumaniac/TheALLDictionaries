DROP DATABASE IF EXISTS cse416; -- Temporary code
CREATE DATABASE IF NOT EXISTS cse416 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; -- Temporary code
USE cse416; -- Temporary code

GRANT ALL PRIVILEGES ON cse416.* to 'database-1.cpvwrnt4qvgc.ap-northeast-2.rds.amazonaws.com' IDENTIFIED BY '416final'; -- Temporary code

CREATE TABLE IF NOT EXISTS Account (
  userID VARCHAR(50) NOT NULL,
  isAdmin BOOLEAN,
  PRIMARY KEY (userID)
); 

CREATE TABLE IF NOT EXISTS AdminAccount (
  fullName VARCHAR(1000) NOT NULL,
  nickName VARCHAR(1000),
  userID VARCHAR(50) NOT NULL,
  password VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  phoneNumber VARCHAR(11) NOT NULL,
  jobTitle VARCHAR(50) NOT NULL,
  profilePictureURL VARCHAR(65535),
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES Account(userID) ON DELETE CASCADE
); 

CREATE TABLE IF NOT EXISTS UserAccount (
  fullName VARCHAR(1000) NOT NULL,
  nickName VARCHAR(1000) NOT NULL,
  userID VARCHAR(50) NOT NULL,
  password VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  phoneNumber VARCHAR(11) NOT NULL,
  isPremium BOOLEAN,
  subscriptionEndDate DATE,
  profilePictureURL VARCHAR(65535),
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES Account(userID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SendFriendRequest (
  senderID VARCHAR(50) NOT NULL,
  receiverID VARCHAR(50) NOT NULL,
  PRIMARY KEY (senderID, receiverID),
  FOREIGN KEY (senderID) REFERENCES UserAccount(userID) ON DELETE NO ACTION,
  FOREIGN KEY (receiverID) REFERENCES UserAccount(userID) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS IsFriendWith (
  userID VARCHAR(50) NOT NULL,
  friendID VARCHAR(50) NOT NULL,
  PRIMARY KEY (userID, friendID),
  FOREIGN KEY (userID) REFERENCES UserAccount(userID) ON DELETE NO ACTION,
  FOREIGN KEY (friendID) REFERENCES UserAccount(userID) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS HasSearchHistory (
  userID VARCHAR(50) NOT NULL,
  searchedDateTime TIMESTAMP NOT NULL,
  word VARCHAR(100) NOT NULL,
  PRIMARY KEY (userID, searchedDateTime),
  FOREIGN KEY (userID) REFERENCES UserAccount(userID) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS HasSourceOrder (
  userID VARCHAR(50) NOT NULL,
  sourceOrder INTEGER NOT NULL,
  source VARCHAR(500) NOT NULL,
  PRIMARY KEY (userID, sourceOrder),
  FOREIGN KEY (userID) REFERENCES UserAccount(userID) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS HasWordRanking (
  userID VARCHAR(50) NOT NULL,
  highestScore INTEGER,
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES UserAccount(userID) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS HasSentenceRanking (
  userID VARCHAR(50) NOT NULL,
  highestScore INTEGER,
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES UserAccount(userID) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS TextChallenge (
  title VARCHAR(256) NOT NULL,
  textType VARCHAR(50) NOT NULL,
  challengeText MEDIUMTEXT NOT NULL,
  PRIMARY KEY (title)
);

CREATE TABLE IF NOT EXISTS GenerateTextChallenge (
  creatorID VARCHAR(50),
  title VARCHAR(50) NOT NULL, 
  dateCreated TIMESTAMP NOT NULL,
  PRIMARY KEY (creatorID, title),
  FOREIGN KEY (creatorID) REFERENCES AdminAccount(userID) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS HasTextRanking (
  challengeTitle VARCHAR(256) NOT NULL,
  userID VARCHAR(50) NOT NULL,
  highestScore INTEGER,
  PRIMARY KEY (challengeTitle, userID),
  FOREIGN KEY (userID) REFERENCES UserAccount(userID) ON DELETE NO ACTION,
  FOREIGN KEY (challengeTitle) REFERENCES TextChallenge(title) ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS ChatRoom(
  roomName VARCHAR(256),
  senderID VARCHAR(50),
  receiverID VARCHAR(50),
  chatMessage VARCHAR(10000),
  sendDate TIMESTAMP,
  PRIMARY KEY (roomName, senderID, sendDate),
  FOREIGN KEY (senderID) REFERENCES Account(userID) ON DELETE NO ACTION,
  FOREIGN KEY (receiverID) REFERENCES Account(userID) ON DELETE NO ACTION
);
