# this file contains all functionality necessary to connect to the database
import mysql.connector

host = "localhost"
user = "root"
passwd = "A1!n3_578"


def getDbConnection():
    # Get database connection
    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database='test', charset="utf8")
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

        closeDbConnection(connection)
    except mysql.connector.Error as error:
        print("Failed to get server information {}".format(error))
    finally:
        cursor.close()
        connection.close()


def getAllCustomerQuery():
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Customers"""
            cursor.execute(sqlstatement)
            records = cursor.fetchall()
            for row in records:
                print(row)
                # do sth
                pass
    except mysql.connector.Error as error:
        print("Failed to read all data from customers {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?


def insertCustomer(emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO Customers (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            data = (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print("Record inserted successfully into Laptop table")

    except mysql.connector.Error as error:
        print("Failed to insert customer {}".format(error))
    finally:
        cursor.close()
        connection.close()


getServerInformation()
getAllCustomerQuery()
insertCustomer("paprikator", "Paprika", "Terminator", "+666", "Hash", "pepper", "p4pr1k4", "1")
getAllCustomerQuery()
