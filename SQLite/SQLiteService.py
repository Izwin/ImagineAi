import sqlite3
from datetime import datetime
from sqlite3 import Error, OperationalError
import mysql.connector


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
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        cur = _conn.cursor(buffered=True)
        stat = "CREATE TABLE IF NOT EXISTS Users(" \
               "ChatId int PRIMARY KEY NOT NULL," \
               "Credits int DEFAULT 1," \
               "Username varchar(255)" \
               ");"
        print(stat)
        cur.execute(stat)
        cur.close()
    except Error as e:
        print(e)


#
# CreateTable(Conn)
def AddUser(_chatId, _credits=1, _userName="unknown"):
    try:
        print("Adding")
        ConnForAdd = mysql.connector.connect(
            host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
            user="uikvsb6zrtvrgmqc",
            password="k6HKrlPgbn5gUxCRjL8i",
            database="bgqbgvhtkl5ebugndbag"
        )
        _cur = ConnForAdd.cursor()
        if _userName is None:
            _userName = "unknown"

        stat = "SELECT * FROM Users WHERE ChatId = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        try:
            print(_cur.fetchall()[0][0])
            print("Не добавил")
        except:
            print("Добавил")
            now = datetime.now()
            stat = "INSERT IGNORE INTO Users(ChatId, Credits, Username, Date) VALUES (" + str(_chatId) + "," + str(
                _credits) + "," + "'" + _userName + "'" + "," + "'" + now.strftime("%d-%m-%Y %H:%M:%S") + "'" + ");"
            print(stat)
            _cur.execute(stat)
            ConnForAdd.commit()


    except Error as e:
        print(e)
    finally:
        _cur.close()
        ConnForAdd.close()


def GetUserCredits(_chatId):
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        _cur = Conn.cursor(buffered=True)
        state = "SELECT Credits FROM Users WHERE ChatId = " + str(_chatId)
        print(state)
        _cur.execute(state)
        return int(_cur.fetchall()[0][0])
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.close()


def getAll():
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        _cur = Conn.cursor(buffered=True)
        state = "SELECT * FROM Users"
        _cur.execute(state)
        return _cur.fetchall()
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.close()


def getAllChatIds():
    ConnForChatId = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )
    try:
        _cur = ConnForChatId.cursor(buffered=True)
        _cur.execute("select ChatId from Users")
        return _cur.fetchall()
    except Error as e:
        print(e)
    finally:
        _cur.close()
        ConnForChatId.close()


def GetUserByChatId(_chatId):
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        _cur = Conn.cursor(buffered=True)
        return _cur.execute("SELECT * FROM Users WHERE ChatId = " + str(_chatId)).fetchall()
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.close()


def decreaseCredits(_chatId):
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        _cur = Conn.cursor(buffered=True)
        stat = "UPDATE Users SET Credits = Credits - 1 WHERE ChatId = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        Conn.commit()
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.close()


def increaseCredits(_chatId):
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        _cur = Conn.cursor(buffered=True)
        stat = "UPDATE Users SET Credits = Credits + 1 WHERE ChatId = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        Conn.commit()
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.close()


def LastQuery(_chatId, _lastQuery):
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        now = datetime.now()
        _cur = Conn.cursor()
        stat = "UPDATE Users SET LastUse = " + "'" + now.strftime("%d-%m-%Y %H:%M:%S") + "'" + "," + " LastQuery =" + "'" + _lastQuery + "'" + " WHERE ChatId = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
        Conn.commit()
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.close()
