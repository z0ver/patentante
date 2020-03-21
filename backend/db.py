# this file contains all functionality necessary to connect to the database
import mysql.connector

host = "localhost"
user = "root"
passwd = "A1!n3_578"


def getDbConnection():
    # Get database connection
    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd,  charset="utf8")
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))


def closeDbConnection(connection):
    # Close database connection
    try:
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to close database connection {}".format(error))


def getServerInformation():
    try:
        connection = getDbConnection()

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version is ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchall()
            print("Your connected to - ", record)
            cursor.close()

        closeDbConnection(connection)
    except mysql.connector.Error as error:
        print("Failed to read database version {}".format(error))
    finally:
        connection.close()


def getQuery():
    try:
        connection = getDbConnection()
        if connection.is_connected():
            try:
                cursor = connection.cursor()
                sqlstatement = """SELECT * FROM coupons"""
                cursor.execute(sqlstatement)
                records = cursor.fetchall()
                for row in records:
                    print(row)
                    # do sth
                    pass
                cursor.close()
            except mysql.connector.Error as error:
                print("Failed to do simple get query {}".format(error))
    except mysql.connector.Error as error:
        print("Failed to read database version {}".format(error))
    finally:
        connection.close()

getServerInformation()
getQuery()