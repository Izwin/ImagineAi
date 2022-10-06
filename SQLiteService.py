from datetime import datetime
from sqlite3 import Error
import mysql.connector

import DB_credits


def addUser(chatId, credits=1, username="unknown"):
    if username is None:
        username = "unknown"


    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )
        cur = Conn.cursor()

        stat = "SELECT * FROM Users WHERE ChatId = " + str(chatId)

        cur.execute(stat)

        try:
            print(cur.fetchall()[0][0]) # Exception если юзера нет
            print("Пользователь не был добавлен!")
        except:
            now = datetime.now()
            stat = "INSERT IGNORE INTO Users(ChatId, Credits, Username, Date) VALUES (" + str(chatId) + "," + str(
                credits) + "," + "'" + username + "'" + "," + "'" + now.strftime("%d-%m-%Y %H:%M:%S") + "'" + ");"
            cur.execute(stat)
            Conn.commit()
            print("Пользователь был добавлен!")


    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()


def getUserCredits(chatId):

    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )
        cur = Conn.cursor()

        state = "SELECT Credits FROM Users WHERE ChatId = " + str(chatId)

        cur.execute(state)

        return int(cur.fetchall()[0][0])
    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()


def getAll():
    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )
        cur = Conn.cursor()

        state = "SELECT * FROM Users"

        cur.execute(state)

        return cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()


def getAllChatIds():
    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )
        cur = Conn.cursor()
        stat = "select ChatId from Users"
        cur.execute(stat)
        return cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()


def getUserByChatId(chatId):
    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )
        cur = Conn.cursor()
        stat = "SELECT * FROM Users WHERE ChatId = " + str(chatId)
        cur.execute(stat)
        return cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()


def decreaseCredits(chatId):
    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )

        cur = Conn.cursor()

        stat = "UPDATE Users SET Credits = Credits - 1 WHERE ChatId = " + str(chatId)

        cur.execute(stat)

        Conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()


def increaseCredits(chatId):
    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )
        cur = Conn.cursor()

        stat = "UPDATE Users SET Credits = Credits + 1 WHERE ChatId = " + str(chatId)

        cur.execute(stat)

        Conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()


def lastQuery(chatId, lastQuery):
    try:
        Conn = mysql.connector.connect(
            host=DB_credits.HOST,
            user=DB_credits.USER,
            password=DB_credits.PASSWORD,
            database=DB_credits.DATABASE
        )
        now = datetime.now()
        cur = Conn.cursor()
        stat = "UPDATE Users SET LastUse = " + "'" + now.strftime("%d-%m-%Y %H:%M:%S") + "'" + "," + " LastQuery =" + "'" + lastQuery + "'" + " WHERE ChatId = " + str(chatId)

        cur.execute(stat)
        print(stat)
        Conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()
        Conn.close()
