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

def verifyUser(token):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """UPDATE Users SET isVerified = true WHERE token = %s"""
            cursor.execute(sqlstatement, (token,))
            connection.commit()
            print(cursor.rowcount, "User successfully verified.")

    except mysql.connector.Error as error:
        print("Failed to verify customer {}".format(error))
    finally:
        cursor.close()
        connection.close()

def createOfferFixedValue(shop_ID, offerType, name, description, value) :
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO Offers(shop_ID, offerType, name, description, value) 
                              VALUES (%s,%s,%s,%s,%s)"""
            data = (shop_ID, offerType, name, description, value)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Offer with fixed value successfully created.")

    except mysql.connector.Error as error:
        print("Failed to create offer {}".format(error))
    finally:
        cursor.close()
        connection.close()

def createOfferVariableValue(shop_ID, offerType, name, description) :
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO Offers(shop_ID, offerType, name, description) 
                              VALUES (%s,%s,%s,%s,%s)"""
            data = (shop_ID, offerType, name, description)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Offer with variable value successfully created.")

    except mysql.connector.Error as error:
        print("Failed to create offer {}".format(error))
    finally:
        cursor.close()
        connection.close()

def deleteOffer(offer_ID) :
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """DELETE FROM Offers WHERE offer_ID = %s"""
            cursor.execute(sqlstatement, (offer_ID,))
            connection.commit()
            print(cursor.rowcount, "Offer successfully deleted.")

    except mysql.connector.Error as error:
        print("Failed to delete offer {}".format(error))
    finally:
        cursor.close()
        connection.close()

def updateOfferDetail(offer_ID, detail_column, newValue) :
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """UPDATE Offers SET %s = %s WHERE offer_ID = %s"""
            data = (detail_column, newValue, offer_ID)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Offer successfully updated.")

    except mysql.connector.Error as error:
        print("Failed to update offer {}".format(error))
    finally:
        cursor.close()
        connection.close()

def updateCouponValue(coupon_id, current_value):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """Update Coupons SET current_value = %s WHERE CouponID = %s"""
            data = (current_value, coupon_id)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Current value of coupon sucessfully updated")

    except mysql.connector.Error as error:
        print("Failed to update coupon value {}".format(error))
    finally:
        cursor.close()
        connection.close()


def updateCouponStatus(coupon_id, status):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """Update Coupons SET status = %s WHERE CouponID = %s"""
            data = (status, coupon_id)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Current status of coupon sucessfully updated")

    except mysql.connector.Error as error:
        print("Failed to update coupon status {}".format(error))
    finally:
        cursor.close()
        connection.close()


def insertCoupon(offer_ID, customer_ID, original_value, current_value, status, date_of_purchase):
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

def insertShopDetails(shop_ID,owner_email,name,zipCode,city,street,description,Logo_URL,Link_Website,phoneNumber):
    inserted_row = None
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO Shops (shop_ID,owner_email,name,zipCode,city,street,description,Logo_URL,Link_Website,phoneNumber) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            data = (shop_ID,owner_email,name,zipCode,city,street,description,Logo_URL,Link_Website,phoneNumber)
            cursor.execute(sqlstatement, data)
            inserted_row = cursor.lastrowid
            connection.commit()
            print(cursor.rowcount, "Record(s) inserted successfully into Shops table")

    except mysql.connector.Error as error:
        print("Failed to insert shop {}".format(error))
    finally:
        cursor.close()
        connection.close()
    if inserted_row:
        return {'success':True,'inserted_row':inserted_row}
    else:
        return {'success':False,'inserted_row':inserted_row}

def updateShowDetails(shop_ID,field_name,field_value):
    updated_row = None
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """UPDATE Shops SET %s = %s WHERE shop_ID=%s"""
            data = (field_name, field_value, shop_ID)
            cursor.execute(sqlstatement, data)
            updated_row = cursor.lastrowid
            connection.commit()
            print(cursor.rowcount, "Record(s) updated successfully in Shops table")
    except mysql.connector.Error as error:
        print("Failed to update shop {}".format(error))
    finally:
        cursor.close()
        connection.close()
    if updated_row:
        return {'success':True,'updated_row':updated_row}
    else:
        return {'success':False,'updated_row':updated_row}

def deleteShop(shop_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """DELETE FROM Shops WHERE shop_ID = %s"""
            data = (shop_ID)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Record deleted successfully in Shops table")
            deletion_done = True
    except mysql.connector.Error as error:
        print("Failed to delete shop {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}

def deleteCoupon(coupon_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """DELETE FROM coupons WHERE coupons_ID = %s"""
            data = (coupon_ID)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Record deleted successfully in Coupons table")
            deletion_done = True
    except mysql.connector.Error as error:
        print("Failed to delete coupon {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}

def deleteOwner(user_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            #First, check if the user is an owner
            data = (user_ID)
            sqlstatement = """SELECT isOwner FROM users WHERE user_id = %s"""
            cursor.execute(sqlstatement, data)
            result_data = cursor.fetchall()
            if result_data: #check if result is not empty
                if 'isOwner' in result_data[0].keys(): #check if the wanted field is present
                    if int(result_data[0]['isOwner'])==1:
                        sqlstatement = """DELETE FROM users WHERE user_id = %s"""
                        cursor.execute(sqlstatement, data)
                        connection.commit()
                        print(cursor.rowcount, "Owner deleted successfully in Users table")
                        deletion_done = True
    except mysql.connector.Error as error:
        print("Failed to delete owner {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success':deletion_done}


def deleteCustomer(user_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            #First, check if the user is a customer
            data = (user_ID)
            sqlstatement = """SELECT isOwner FROM users WHERE user_id = %s"""
            cursor.execute(sqlstatement, data)
            result_data = cursor.fetchall()
            if result_data: #check if result is not empty
                if 'isOwner' in result_data[0].keys(): #check if the wanted field is present
                    if int(result_data[0]['isOwner'])==0:
                        sqlstatement = """DELETE FROM users WHERE user_id = %s"""
                        cursor.execute(sqlstatement, data)
                        connection.commit()
                        print(cursor.rowcount, "Customer deleted successfully in Users table")
                        deletion_done = True
    except mysql.connector.Error as error:
        print("Failed to delete user {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success':deletion_done}
    
def getCouponDetails(coupon_id):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Coupons WHERE coupon_ID=%s"""
            cursor.execute(sqlstatement, (coupon_id,))
            records = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to read data from Offers {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?    