import sqlite3
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
        stat = "CREATE TABLE IF NOT EXISTS Users("\
                    "ChatId int PRIMARY KEY NOT NULL,"\
                    "Credits int DEFAULT 1,"\
                    "Username varchar(255)"\
                    ");"
        cur.execute(stat)
        cur.close()
    except Error as e:
        print(e)
#
# CreateTable(Conn)
def AddUser(_chatId, _credits=1, _userName="unknown"):
    ConnForAdd = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )
    try:

        _cur = ConnForAdd.cursor()
        if _userName is None:
            _userName = "unknown"

        stat = "SELECT * FROM Users WHERE ChatId = " + str(_chatId)
        _cur.execute(stat)
        try:
            _cur.fetchall()[0][0]
        except:
            print("Добваил")
            stat = "INSERT IGNORE INTO Users(ChatId,Credits, Username) VALUES (" + str(
                _chatId) + "," + str(
                _credits) + "," + '"' + _userName + '"' + ");"
            print(stat)
            print(_cur.execute(stat))
        finally:
            _cur.close()
            ConnForAdd.commit()



    except Error as e:
        print(e)


def GetUserCredits(_chatId):

    try:
        Conn = mydb = mysql.connector.connect(
            host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
            user="uikvsb6zrtvrgmqc",
            password="k6HKrlPgbn5gUxCRjL8i",
            database="bgqbgvhtkl5ebugndbag"
        )

        _cur = Conn.cursor(buffered=True)
        state = "SELECT Credits FROM Users WHERE ChatId = " + str(_chatId)
        print(state)
        _cur.execute(state)

        return int(_cur.fetchall()[0][0])
    except Error as e:
        print(e)
    finally:
        _cur.close()




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
        _cur.close()
        return _cur.fetchall()
    except Error as e:
        print(e)


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
        _cur.close()
        return _cur.fetchall()
    except Error as e:
        print(e)


def removeByChatId(_chatId):
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        _cur = Conn.cursor(buffered=True)
        stat = "delete from `Users` where `ChatId` = " + str(_chatId)
        _cur.execute(stat)
        Conn.commit()
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.close()
def GetUserByChatId(_chatId):
    Conn = mydb = mysql.connector.connect(
        host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
        user="uikvsb6zrtvrgmqc",
        password="k6HKrlPgbn5gUxCRjL8i",
        database="bgqbgvhtkl5ebugndbag"
    )

    try:
        _cur = Conn.cursor(buffered=True)
        _cur.close()
        return _cur.execute("SELECT * FROM Users WHERE ChatId = " + str(_chatId)).fetchall()
    except Error as e:
        print(e)


def decreaseCredits(_chatId):

    try:
        print("Descrease")
        Conn = mydb = mysql.connector.connect(
            host="bgqbgvhtkl5ebugndbag-mysql.services.clever-cloud.com",
            user="uikvsb6zrtvrgmqc",
            password="k6HKrlPgbn5gUxCRjL8i",
            database="bgqbgvhtkl5ebugndbag"
        )

        _cur = Conn.cursor(buffered=True)
        stat = "UPDATE Users SET Credits = Credits - 1 WHERE ChatId = " + str(_chatId)
        print(stat)
        _cur.execute(stat)
    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.commit()


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

    except Error as e:
        print(e)
    finally:
        _cur.close()
        Conn.commit()



