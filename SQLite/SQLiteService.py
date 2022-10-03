import sqlite3
from sqlite3 import Error


def CreateConnection(db_file):
    try:
        _conn = sqlite3.connect(db_file)
        return _conn
    except Error as e:
        print(e)


def CreateTable(_conn):
    try:
        cur = Conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Logs ("
                    "ChatId integer PRIMARY KEY NOT NULL,"
                    "Credits integer DEFAULT 1,"
                    "Username varchar"
                    ");")
    except Error as e:
        print(e)


def AddUser(_chatId, _credits=1, _userName="unknown"):
    try:
        Conn = CreateConnection("SQLite/DataBases/ImagineDB.db")
        _cur = Conn.cursor()
        stat = "INSERT OR IGNORE INTO \"Users\"(\"ChatId\",\"Credits\", \"Username\") VALUES (" + str(
            _chatId) + "," + str(
            _credits) + "," + '"' + _userName + '"' + ");"
        print(stat)
        _cur.execute(stat)

        Conn.commit()
    except Error as e:
        print(e)


def GetUserCredits(_chatId):
    try:
        Conn = CreateConnection("SQLite/DataBases/ImagineDB.db")
        _cur = Conn.cursor()
        state = "SELECT Credits FROM Users WHERE ChatId = " + str(_chatId)
        return int(_cur.execute(state).fetchall()[0][0])
    except Error as e:
        print(e)


def getAllChatIds():
    try:
        Conn = CreateConnection("SQLite/DataBases/ImagineDB.db")
        _cur = Conn.cursor()
        return _cur.execute("select ChatId from \"Users\"").fetchall()
    except Error as e:
        print(e)


def GetUserByChatId(_chatId):
    try:
        Conn = CreateConnection("SQLite/DataBases/ImagineDB.db")
        _cur = Conn.cursor()
        return _cur.execute("SELECT * FROM Users WHERE ChatId = " + str(_chatId)).fetchall()
    except Error as e:
        print(e)


def decreaseCredits(_chatId):
    try:
        Conn = CreateConnection("SQLite/DataBases/ImagineDB.db")
        _cur = Conn.cursor()
        stat = "UPDATE \"Users\" SET \"Credits\" = \"Credits\" - 1 WHERE \"ChatId\" = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        Conn.commit()
    except Error as e:
        print(e)


def increaseCredits(_chatId):
    try:
        Conn = CreateConnection("SQLite/DataBases/ImagineDB.db")
        _cur = Conn.cursor()
        stat = "UPDATE \"Users\" SET \"Credits\" = \"Credits\" + 1 WHERE \"ChatId\" = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        Conn.commit()

    except Error as e:
        print(e)


