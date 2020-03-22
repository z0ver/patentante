"""
This file contains all functionality necessary to connect to the database
The following functions are wrapper to be faster creating new database calls
insertIntoDB -> INSERT
getDataFromDB -> SELECT
updateDB -> UPDATE
deleteFromDB -> DELETE
"""

import bcrypt
import mysql.connector

# Get Database connection details from app configuration
from config import db_host as host
from config import db_passwd as passwd
from config import db_session_timeout as timeout
from config import db_user as user
from config import db_name


#--------------------------Database Management--------------------
# todo how to deal with invite mode?

def getDbConnection():
    # Get database connection
    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=db_name, charset="utf8")
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


#-----------------Wrapper functions for different query types (see top of the file)--------------

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
        return {'success': True, 'inserted_id': inserted_row}
    else:
        return {'success': False}


def getDataFromDB(sqlstatement, arguments):
    records = []
    cursor = None
    connection = None
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sqlstatement, arguments)

            data = cursor.fetchall()
            column_names = [one_column[0] for one_column in cursor.description]
            # Put database result in easily usable dict schema
            for row in data:
                record = {}
                for column_index in range(0, len(column_names)):
                    record[column_names[column_index]] = row[column_index]
                records.append(record)
    except mysql.connector.Error as error:
        print("Failed to get {}: {}".format(sqlstatement, error))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return records


def updateDB(sqlstatement, data):
    updated_row = None
    update_success = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount)
            if cursor.rowcount > 0:
                update_success = True
                updated_row = cursor.lastrowid
                print(cursor.rowcount, "record(s) updated successfully")
    except mysql.connector.Error as error:
        print("Failed to update {}: {}".format(sqlstatement, error))
    finally:
        cursor.close()
        connection.close()
    if update_success:
        return {'success': True, 'updated_id': updated_row}
    else:
        return {'success': False}


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



#--------------------------Session management-----------------------

# Create a new session
def insertSessionID(user_id, session_id):
    sqlstatement = """INSERT INTO Sessions(user_id, session_token) 
    VALUES (%s,%s,TIMESTAMPADD(MINUTE, %s, CURRENT_TIMESTAMP))"""
    return insertIntoDB(sqlstatement, (user_id, session_id, timeout))

# Increase duration of session by standard increased time ("timeout")
def updateExpiringSession(session_id):
    sqlstatement = """UPDATE sessions SET end_date=TIMESTAMPADD(MINUTE, %s, CURRENT_TIMESTAMP) where session_token = %s"""
    return updateDB(sqlstatement, (timeout, session_id))

# Get current session of a user
def getSessionIDByUser(user_id):
    sqlstatement = """SELECT session_token FROM sessions where user_id = %s"""
    return getDataFromDB(sqlstatement, (user_id,))

#-----------------------User management--------------------

# Get user information based on email
def getUserByMail(email_address):
    sqlstatement = """SELECT * FROM Users WHERE email_address=%s"""
    return getDataFromDB(sqlstatement, (email_address,))

# register a new customer or vendor
def insertUser(email_address, firstname, lastname, phone_number, password_hash, is_owner):
    sqlstatement = """INSERT INTO Users (email_address, firstname, lastname, phone_number, password_hash, is_verified, is_owner) 
                           VALUES (%s, %s,%s, %s, %s, %s, %s)"""
    data = (email_address, firstname, lastname, phone_number, password_hash, False, is_owner)
    return insertIntoDB(sqlstatement, data)

#Get password for user
def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

#Check entered password against hashed password
def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)

#------------------------Vendor-based functions------------------------

# Issue a new coupon
def insertCoupon(offer_id, customer_id, original_value, current_value, status, date_of_purchase):
    sqlstatement = """INSERT INTO Coupons (offer_id, customer_id, original_value, current_value, status, date_of_purchase)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
    data = (offer_id, customer_id, original_value, current_value, status, date_of_purchase)
    return insertIntoDB(sqlstatement, data)

#retrieve all shops of a vendor
def getShopsByOwner(user_id):
    sqlstatement = """SELECT * FROM Shops WHERE owner_id=%s"""
    return getDataFromDB(sqlstatement, (user_id,))

# create a new offer for a vendor
def createOffer(shop_id, offer_type, name, description, value=0):
    sqlstatement = """INSERT INTO Offers(shop_id, offer_type, name, description, value) 
                              VALUES (%s,%s,%s,%s,%s)"""
    data = (shop_id, offer_type, name, description, value)
    return insertIntoDB(sqlstatement, data)

# add a new shop for a vendor
def insertShopDetails(owner_id, street, zip_code, city, website_url, phone_number, name, logo_url, description_short,
                      description):
    sqlstatement = """INSERT INTO Shops (owner_id, street, zip_code, city, website_url, phone_number, name, logo_url, description_short, description) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    data = (owner_id, street, zip_code, city, website_url, phone_number, name, logo_url, description_short, description)
    return insertIntoDB(sqlstatement, data)

#-------------------------Shop-based functions------------------

# Get all shops with a specific name
def getShopsByName(name):
    sqlstatement = """SELECT * FROM Shops WHERE name=%s"""
    return getDataFromDB(sqlstatement, (name,))

# Get all shops for a specific zip code
def getShopsByZipCode(zipcode):
    sqlstatement = """SELECT * FROM Shops WHERE zip_code=%s"""
    return getDataFromDB(sqlstatement, (zipcode,))

# Get all offers by a shop
def getOffersByShopID(shop_id):
    sqlstatement = """SELECT * FROM Offers WHERE shop_id=%s"""
    return getDataFromDB(sqlstatement, (shop_id,))

# Get all coupons for a shop
def getCouponsByShopID(shop_id):
    sqlstatement = """SELECT coupons.* FROM coupons INNER JOIN Offers on coupons.offer_id=offers.offer_id WHERE offers.shop_id=%s"""
    return getDataFromDB(sqlstatement, (shop_id,))

#-------------------------Coupon-based functions---------------------

# Get all coupons by a customer
def getCouponsByCustomerID(customer_id):
    sqlstatement = """SELECT * FROM coupons WHERE customer_id=%s"""
    return getDataFromDB(sqlstatement, (customer_id,))

#Spare, not in use yet
# Get details about a coupon
def getCouponDetails(coupon_id):
    sqlstatement = """SELECT * FROM Coupons WHERE coupon_id=%s"""
    return getDataFromDB(sqlstatement, (coupon_id,))

# Update value of coupon
def updateCouponValue(coupon_id, new_value, activated):
    sqlstatement = """UPDATE coupons SET current_value=%s,status=%s WHERE coupon_id=%s"""
    data = (new_value, activated, coupon_id)
    return updateDB(sqlstatement, data)

# Change coupon status
def updateCouponStatus(coupon_id, status):
    sqlstatement = """Update Coupons SET status = %s WHERE coupon_id = %s"""
    data = (status, coupon_id)
    return updateDB(sqlstatement, data)

#Spare, not in use yet
# Get buyer information based on coupon id
def getBuyerByCouponID(coupon_id):
    sqlstatement = """SELECT Users.* FROM Users, Coupons WHERE Coupons.coupon_id=%s AND Coupons.customer_id=Users.user_id"""
    return getDataFromDB(sqlstatement, (coupon_id,))

#Spare, not in use yet
# Get vender information based on coupon id
def getVendorByCouponID(coupon_id):
    sqlstatement = """SELECT Users.* FROM Coupons INNER JOIN Offers on Coupons.offer_id=Offers.offer_id INNER JOIN Shops on Offers.shop_id=Shops.shop_id INNER JOIN Users ON Shops.owner_id=Users.user_id WHERE Coupons.coupon_id=%s"""
    getDataFromDB(sqlstatement, (coupon_id,))

#Spare, not in use yet
# Get coupon information based on coupon id
def getCouponByCouponID(coupon_id):
    sqlstatement = """SELECT * FROM coupons WHERE coupon_id=%s"""
    return getDataFromDB(sqlstatement, (coupon_id,))

#Spare, not in use yet
# Get all coupons which are already used up by a user
def getUsedCouponsByUserID(user_id):
    sqlstatement = """SELECT coupon_id,current_value,original_value,status,date_of_purchase FROM coupons WHERE customer_id=%s AND status='USED_UP'"""
    return getDataFromDB(sqlstatement, (user_id,))

















def updateOfferDetail(offer_id, name, description, value):
    sqlstatement = """UPDATE Offers SET name = %s, description = %s, value=%s WHERE offer_id = %s"""
    data = (name, description, value, offer_id)
    return updateDB(sqlstatement, data)


def updateShopDetails(shop_id, name, zip_code, city, street, description, Logo_URL, Link_Website, phone_number):
    sqlstatement = """UPDATE Shops SET name=%s, zip_code=%s, city=%s, street=%s, description=%s, Logo_URL=%s, Link_Website=%s, phone_number=%s WHERE shop_id=%s"""
    data = (name, zip_code, city, street, description, Logo_URL, Link_Website, phone_number, shop_id)
    return updateDB(sqlstatement, data)





def verifyUser(user_id):
    sqlstatement = """UPDATE Users SET is_verified = True WHERE user_id = %s"""
    return updateDB(sqlstatement, (user_id,))


def deleteOffer(offer_id):
    sqlstatement = """DELETE FROM Offers WHERE offer_id = %s"""
    deleteFromDB(sqlstatement, offer_id)


def deleteShop(shop_id):
    sqlstatement = """DELETE FROM Shops WHERE shop_id = %s"""
    deleteFromDB(sqlstatement, shop_id)


def deleteCoupon(coupon_id):
    sqlstatement = """DELETE FROM coupons WHERE coupon_id = %s"""
    deleteFromDB(sqlstatement, coupon_id)


def deleteOwner(user_id):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            # First, check if the user is an owner
            sqlstatement = """SELECT is_owner FROM users WHERE user_id = %s"""
            cursor.execute(sqlstatement, (user_id,))
            result_data = cursor.fetchall()
            if result_data:  # check if result is not empty
                if 'is_owner' in result_data[0].keys():  # check if the wanted field is present
                    if int(result_data[0]['is_owner']) == 1:
                        sqlstatement = """DELETE FROM users WHERE user_id = %s"""
                        result = deleteFromDB(sqlstatement, user_id)
                        deletion_done = result.get('success')
                        if deletion_done:
                            print(cursor.rowcount, "Owner deleted successfully in Users table")
    except mysql.connector.Error as error:
        print("Failed to delete owner {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}


def deleteCustomer(user_id):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            # First, check if the user is a customer
            sqlstatement = """SELECT is_owner FROM users WHERE user_id = %s"""
            cursor.execute(sqlstatement, (user_id,))
            result_data = cursor.fetchall()
            if result_data:  # check if result is not empty
                if 'is_owner' in result_data[0].keys():  # check if the wanted field is present
                    if int(result_data[0]['is_owner']) == 0:
                        sqlstatement = """DELETE FROM users WHERE user_id = %s"""
                        cursor.execute(sqlstatement, user_id)
                        result = deleteFromDB(sqlstatement, user_id)
                        deletion_done = result.get('success')
                        if deletion_done:
                            print(cursor.rowcount, "Customer deleted successfully in Users table")
    except mysql.connector.Error as error:
        print("Failed to delete user {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}
