import sqlite3
from sqlite3 import Error
import mysql.connector


Conn = mydb = mysql.connector.connect(
        host="sql6.freesqldatabase.com",
        user="sql6524007",
        password="35KvqfVJ4C",
        database="sql6524007"
    )



# def CreateConnection(db_file):
#
#     print(mydb)
#     CreateTable(mydb)
#     return mydb
#
#
#     try:
#         _conn = sqlite3.connect(db_file)
#         return _conn
#     except Error as e:
#         print(e)


def CreateTable(_conn):
    try:
        cur = _conn.cursor(buffered=True)
        stat = "CREATE TABLE IF NOT EXISTS Users("\
                    "ChatId int PRIMARY KEY NOT NULL,"\
                    "Credits int DEFAULT 1,"\
                    "Username varchar(255)"\
                    ");"
        print(stat)
        cur.execute(stat)
        cur.close()
    except Error as e:
        print(e)


def AddUser(_chatId, _credits=1, _userName="unknown"):
    try:
        print("Adding")
        _cur = Conn.cursor(buffered=True)
        if _userName is None:
            _userName = "unknown"
        stat = "INSERT IGNORE INTO Users(ChatId,Credits, Username) VALUES (" + str(
            _chatId) + "," + str(
            _credits) + "," + '"' + _userName + '"' + ");"
        print(stat)
        _cur.execute(stat)
        Conn.commit()
        _cur.close()
    except Error as e:
        print(e)


def GetUserCredits(_chatId):
    try:
        _cur = Conn.cursor(buffered=True)
        state = "SELECT Credits FROM Users WHERE ChatId = " + str(_chatId)
        print(state)
        _cur.execute(state)
        _cur.close()
        return int(_cur.fetchall()[0][0])
    except Error as e:
        print(e)



def getAll():
    try:
        _cur = Conn.cursor(buffered=True)
        state = "SELECT * FROM Users"
        _cur.execute(state)
        _cur.close()
        return _cur.fetchall()
    except Error as e:
        print(e)


def getAllChatIds():
    try:
        _cur = Conn.cursor(buffered=True)
        _cur.execute("select ChatId from Users")
        _cur.close()
        return _cur.fetchall()
    except Error as e:
        print(e)


def GetUserByChatId(_chatId):
    try:
        _cur = Conn.cursor(buffered=True)
        _cur.close()
        return _cur.execute("SELECT * FROM Users WHERE ChatId = " + str(_chatId)).fetchall()
    except Error as e:
        print(e)


def decreaseCredits(_chatId):
    try:
        _cur = Conn.cursor(buffered=True)
        stat = "UPDATE Users SET Credits = Credits - 1 WHERE ChatId = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        Conn.commit()
        _cur.close()
    except Error as e:
        print(e)


def increaseCredits(_chatId):
    try:
        _cur = Conn.cursor(buffered=True)
        stat = "UPDATE Users SET Credits = Credits + 1 WHERE ChatId = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        Conn.commit()
        _cur.close()
    except Error as e:
        print(e)


