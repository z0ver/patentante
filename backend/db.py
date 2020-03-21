# this file contains all functionality necessary to connect to the database
import mysql.connector

host = "localhost"
user = "root"
passwd = "A1!n3_578"  # extract as env variable


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


def printServerInformation():
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


def getShopsByZipCode(zipcode):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Shops WHERE zipCode=%s"""
            cursor.execute(sqlstatement, (zipcode,))
            records = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to read data from Shops {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?


def getShopsByName(name):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Shops WHERE name=%s"""
            cursor.execute(sqlstatement, (name,))
            records = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to read data from Shops {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?


def getOffersByShopID(shop_id):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Offers WHERE shop_ID=%s"""
            cursor.execute(sqlstatement, (shop_id,))
            records = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to read data from Offers {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?


def insertUser(emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified, isOwner):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO User (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified, isOwner) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            data = (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, False, isOwner)
            cursor.execute(sqlstatement, data)
            connection.commit()

            print(cursor.rowcount, "Record inserted successfully into User table")

    except mysql.connector.Error as error:
        print("Failed to insert customer {}".format(error))
    finally:
        cursor.close()
        connection.close()


def insertCouponForCustomer(offer_ID, customer_ID, original_value, current_value, status, date_of_purchase):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO Coupons (offer_ID, customer_ID, original_value, current_value, status, date_of_purchase)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (offer_ID, customer_ID, original_value, current_value, status, date_of_purchase)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Coupons table")

    except mysql.connector.Error as error:
        print("Failed to insert customer {}".format(error))
    finally:
        cursor.close()
        connection.close()



