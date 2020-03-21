# this file contains all functionality necessary to connect to the database
import mysql.connector

# Get Database connection details from app configuration
from config import db_host as host
from config import db_passwd as passwd
from config import db_user as user
from config import db_session_timeout as timeout


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
    cursor = None
    connection = None
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
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def insertIntoDB(sqlstatement, data):
    inserted_row = None
    cursor = None
    connection = None
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sqlstatement, data)
            connection.commit()
            if cursor.rowcount > -1:
                inserted_row = cursor.lastrowid
                print(cursor.rowcount, "Record inserted successfully")
    except mysql.connector.Error as error:
        print("Failed to insert {}: {}".format(sqlstatement, error))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    if inserted_row:
        return {'success': True, 'inserted_row': inserted_row}
    else:
        return {'success': False, 'inserted_row': inserted_row}


def getDataFromDB(sqlstatement, arguments):
    records = []
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sqlstatement, arguments)
            data = cursor.fetchall()[0]
            column_names = [one_column[0] for one_column in cursor.description]
            for row in data:
                record = {}
                for column_index in range(0, len(column_names) - 1):
                    record[column_names[column_index]] = data[column_index]
                records.append(record)
    except mysql.connector.Error as error:
        print("Failed to get {}: {}".format(sqlstatement, error))
    finally:
        cursor.close()
        connection.close()
    return records


def updateDB(sqlstatement, data):
    updated_row = None
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sqlstatement, data)
            connection.commit()
            if cursor.rowcount > -1:
                updated_row = cursor.lastrowid
                print(cursor.rowcount, "record(s) updated successfully")
    except mysql.connector.Error as error:
        print("Failed to update {}: {}".format(sqlstatement, error))
    finally:
        cursor.close()
        connection.close()
    if updated_row:
        return {'success': True, 'updated_row': updated_row}
    else:
        return {'success': False, 'updated_row': updated_row}


def deleteFromDB(sqlstatement, delete_id):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sqlstatement, (delete_id,))
            connection.commit()
            if cursor.rowcount > -1:
                deletion_done = True
                print(cursor.rowcount, "record(s) updated successfully")
    except mysql.connector.Error as error:
        print("Failed to delete {} {}".format(sqlstatement, error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}

def getSessionIDByUser(user_ID):
    sqlstatement = """SELECT session_token FROM sessions where user_ID = %s"""
    return getDataFromDB(sqlstatement, (user_ID,))

def insertSessionID(user_ID, session_ID):
    sqlstatement = """INSERT INTO Sessions(user_ID, session_token) 
    VALUES (%s,%s,TIMESTAMPADD(MINUTE, %s, CURRENT_TIMESTAMP))"""
    return insertIntoDB(sqlstatement, (user_ID, session_ID, db_session_timeout))

def updateExpiringSession(session_ID):
    sqlstatement = """UPDATE sessions SET end_date=TIMESTAMPADD(MINUTE, %s, CURRENT_TIMESTAMP) where session_token = %s"""
    return updateDB(sqlstatement, (db_session_timeout, session_ID))

def getShopsByZipCode(zipcode):
    sqlstatement = """SELECT * FROM Shops WHERE zipCode=%s"""
    return getDataFromDB(sqlstatement, (zipcode,))


def getShopsByName(name):
    sqlstatement = """SELECT * FROM Shops WHERE name=%s"""
    return getDataFromDB(sqlstatement, (name,))


def getCouponDetails(coupon_id):
    sqlstatement = """SELECT * FROM Coupons WHERE coupon_ID=%s"""
    return getDataFromDB(sqlstatement, (coupon_id,))


def getOffersByShopID(shop_id):
    sqlstatement = """SELECT * FROM Offers WHERE shop_ID=%s"""
    return getDataFromDB(sqlstatement, (shop_id,))


def getBuyerByCouponID(coupon_id):
    sqlstatement = """SELECT Users.* FROM Users, Coupons WHERE Coupons.coupons_ID=%s AND Coupons.customer_id=Users.user_id"""
    return getDataFromDB(sqlstatement, (coupon_id,))


def getVendorByCouponID(coupon_id):
    sqlstatement = """SELECT Users.* FROM `Coupons` INNER JOIN Offers on Coupons.offer_ID=Offers.offer_ID INNER JOIN Shops on Offers.shop_ID=Shops.shop_ID INNER JOIN Users ON Shops.owner_id=Users.user_id WHERE Coupons.coupons_ID=%s"""
    getDataFromDB(sqlstatement, (coupon_id,))


def getCouponsByUserID(user_ID):
    sqlstatement = """SELECT * FROM coupons WHERE customer_id=%s"""
    return getDataFromDB(sqlstatement, (user_ID,))


def insertUser(emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified, isOwner):
    sqlstatement = """INSERT INTO User (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified, isOwner) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    data = (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, False, isOwner)
    return insertIntoDB(sqlstatement, data)


def createOfferFixedValue(shop_ID, offerType, name, description, value):
    sqlstatement = """INSERT INTO Offers(shop_ID, offerType, name, description, value) 
                              VALUES (%s,%s,%s,%s,%s)"""
    data = (shop_ID, offerType, name, description, value)
    return insertIntoDB(sqlstatement, data)


def createOfferVariableValue(shop_ID, offerType, name, description):
    sqlstatement = """INSERT INTO Offers(shop_ID, offerType, name, description) 
                              VALUES (%s,%s,%s,%s,%s)"""
    data = (shop_ID, offerType, name, description)
    return insertIntoDB(sqlstatement, data)


def insertCoupon(offer_ID, customer_ID, original_value, current_value, status, date_of_purchase):
    sqlstatement = """INSERT INTO Coupons (offer_ID, customer_ID, original_value, current_value, status, date_of_purchase)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
    data = (offer_ID, customer_ID, original_value, current_value, status, date_of_purchase)
    return insertIntoDB(sqlstatement, data)


def insertShopDetails(shop_ID, owner_email, name, zipCode, city, street, description, Logo_URL, Link_Website,
                      phoneNumber):
    sqlstatement = """INSERT INTO Shops (shop_ID,owner_email,name,zipCode,city,street,description,Logo_URL,Link_Website,phoneNumber) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    data = (shop_ID, owner_email, name, zipCode, city, street, description, Logo_URL, Link_Website, phoneNumber)
    return insertIntoDB(sqlstatement, data)


def updateOfferDetail(offer_ID, newName, newDesciption, newValue):
    sqlstatement = """UPDATE Offers SET name = %s, description = %s, value=%s WHERE offer_ID = %s"""
    data = (newName, newDesciption, newValue, offer_ID)
    return updateDB(sqlstatement, data)


def updateShowDetails(shop_ID, name, zipCode, city, street, description, Logo_URL, Link_Website, phoneNumber):
    sqlstatement = """UPDATE Shops SET name=%s, zipCode=%s, city=%s, street=%s, description=%s, Logo_URL=%s, Link_Website=%s, phoneNumber=%s WHERE shop_ID=%s"""
    data = (name, zipCode, city, street, description, Logo_URL, Link_Website, phoneNumber, shop_ID)
    return updateDB(sqlstatement, data)


def updateCurrentCouponValue(coupon_id, current_value):
    sqlstatement = """Update Coupons SET current_value = %s WHERE CouponID = %s"""
    data = (current_value, coupon_id)
    return updateDB(sqlstatement, data)


def updateCouponStatus(coupon_id, status):
    sqlstatement = """Update Coupons SET status = %s WHERE CouponID = %s"""
    data = (status, coupon_id)
    return updateDB(sqlstatement, data)


def verifyUser(user_ID):
    sqlstatement = """UPDATE Users SET isVerified = True WHERE user_ID = %s"""
    return updateDB(sqlstatement, (user_ID,))


def deleteOffer(offer_ID):
    sqlstatement = """DELETE FROM Offers WHERE offer_ID = %s"""
    deleteFromDB(sqlstatement, offer_ID)


def deleteShop(shop_ID):
    sqlstatement = """DELETE FROM Shops WHERE shop_ID = %s"""
    deleteFromDB(sqlstatement, shop_ID)


def deleteCoupon(coupon_ID):
    sqlstatement = """DELETE FROM coupons WHERE coupons_ID = %s"""
    deleteFromDB(sqlstatement, coupon_ID)


def deleteOwner(user_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            # First, check if the user is an owner
            sqlstatement = """SELECT isOwner FROM users WHERE user_id = %s"""
            cursor.execute(sqlstatement, (user_ID,))
            result_data = cursor.fetchall()
            if result_data:  # check if result is not empty
                if 'isOwner' in result_data[0].keys():  # check if the wanted field is present
                    if int(result_data[0]['isOwner']) == 1:
                        sqlstatement = """DELETE FROM users WHERE user_id = %s"""
                        result = deleteFromDB(sqlstatement, user_ID)
                        deletion_done = result.get('success')
                        if deletion_done:
                            print(cursor.rowcount, "Owner deleted successfully in Users table")
    except mysql.connector.Error as error:
        print("Failed to delete owner {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}


def deleteCustomer(user_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            # First, check if the user is a customer
            sqlstatement = """SELECT isOwner FROM users WHERE user_id = %s"""
            cursor.execute(sqlstatement, (user_ID,))
            result_data = cursor.fetchall()
            if result_data:  # check if result is not empty
                if 'isOwner' in result_data[0].keys():  # check if the wanted field is present
                    if int(result_data[0]['isOwner']) == 0:
                        sqlstatement = """DELETE FROM users WHERE user_id = %s"""
                        cursor.execute(sqlstatement, user_ID)
                        result = deleteFromDB(sqlstatement, user_ID)
                        deletion_done = result.get('success')
                        if deletion_done:
                            print(cursor.rowcount, "Customer deleted successfully in Users table")
    except mysql.connector.Error as error:
        print("Failed to delete user {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}
