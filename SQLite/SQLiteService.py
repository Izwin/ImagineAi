import sqlite3
from sqlite3 import Error

def CreateConnection(db_file):
    _conn = None
    try:
        _conn = sqlite3.connect(db_file)
        return _conn
    except Error as e:
        print(e)


def CreateTable(_conn):
    try:
        cur = Conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Users ("
                    "Id integer PRIMARY KEY AUTOINCREMENT,"
                    "ChatId integer NOT NULL,"
                    "PremiumStatus integer NOT NULL,"
                    "PaidCount integer NOT NULL,"
                    "Credits integer DEFAULT 2"
                    ");")
    except Error as e:
        print(e)


def AddUser(_conn, _chatId, _premiumStatus, _paidCount, _credits=2, _userName="unknown"):
    try:
        _cur = Conn.cursor()
        _cur.execute("INSERT INTO Users(ChatId, PremiumStatus, PaidCount, Credits, Username) VALUES (" + str(_chatId) + "," + str(
            _premiumStatus) + "," + str(_paidCount) + "," + str(_credits) + "," + '"' + _userName + '"' + ");")
        _conn.commit()
    except Error as e:
        print(e)


def GetUsers(_conn):
    try:
        _cur = Conn.cursor()
        return _cur.execute("SELECT * FROM Users").fetchall()
    except Error as e:
        print(e)


def GetUserCredits(_conn, _chatId):
    try:
        _cur = Conn.cursor()
        return int(_cur.execute("SELECT Credits FROM Users WHERE ChatId = " + str(_chatId)).fetchall()[0][0])
    except Error as e:
        print(e)


def GetUserById(_conn, _id):
    try:
        _cur = Conn.cursor()
        return _cur.execute("SELECT * FROM Users WHERE Id = " + str(_id)).fetchall()
    except Error as e:
        print(e)


def GetUserByChatId(_conn, _chatId):
    try:
        _cur = Conn.cursor()
        return _cur.execute("SELECT * FROM Users WHERE ChatId = " + str(_chatId)).fetchall()
    except Error as e:
        print(e)


Conn = CreateConnection("DataBases/ImagineAI.db")
CreateTable(Conn)