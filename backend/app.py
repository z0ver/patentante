from datetime import datetime

import simplejson as json
from flask import Flask, request, Response

from config import secret_key
import bcrypt
import mysql.connector
from db import *

app = Flask(__name__)
app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'


def response_invalid_request():
    """
    Response to an invalid request.
    :return: JSON
    """
    _response = {}
    _response['Status'] = 400
    _response['Success'] = False
    _response['Result'] = 'Invalid request.'
    return Response(response=json.dumps(_response, sort_keys=True, indent=4),
                    status=400,
                    mimetype="application/json")


def response_unauthorized_request():
    """
    Response to an unauthorized request.
    :return: JSON
    """
    _response = {}
    _response['Success'] = False
    _response['Status'] = 401
    _response['Result'] = 'Unauthorized request.'
    return Response(response=json.dumps(_response, sort_keys=True, indent=4),
                    status=401,
                    mimetype="application/json")


def response_valid_request(data):
    """
    Response to a valid request.
    :return: JSON wthat contains the input data
    """
    # this area converts datetime values from python to strings so they are serializable
    for row in data:
        if isinstance(row, dict):
            for key, value in row.items():
                if isinstance(value, list):
                    for list_index, list_value in enumerate(value):
                        if isinstance(list_value, dict):
                            for list_item_key, list_item_value in list_value.items():
                                if isinstance(list_item_value, datetime):
                                    row[key][list_index][list_item_key] = list_item_value.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(value, datetime):
                    row[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    _response = {}
    _response['Success'] = True
    _response['Status'] = 200
    _response['Result'] = data
    return Response(response=json.dumps(_response, sort_keys=True, indent=4),
                    status=200,
                    mimetype="application/json")


# login user
@app.route('/user/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        hash = getUserByMail(email)
        if hash:
            if check_password(password.encode('utf8'), hash[0].get('password_hash').encode('utf8')):
                return response_valid_request({"user_id": hash[0].get('user_id'), "is_owner": hash[0].get('is_owner')})
        else:
            return response_unauthorized_request()


# register a new customer
@app.route('/user/customer/register', methods=['POST'])
def register_customer():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        phone_number = data.get('phone_number')
        password = data.get('password')
        passwordHash = get_hashed_password(password.encode('utf8'))
        result = insertUser(email, firstname, lastname, phone_number, passwordHash, False)
        if result.get('success'):
            return response_valid_request({"user_id": result.get('inserted_id')})
        else:
            return response_invalid_request()


# Issue a new coupon or retrieve all of a vendor
@app.route('/user/vendor/coupon', methods=['POST', 'GET'])
def vendor_coupon():
    if request.method == 'POST':
        data = request.get_json()
        customer_id = data.get('customer_id')
        offer_id = data.get('offer_id')
        original_value = data.get('original_value')
        query_result = insertCoupon(offer_id=offer_id, customer_id=customer_id, original_value=original_value,
                                    current_value=original_value, status='ACTIVATE',
                                    date_of_purchase=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if query_result.get('success'):
            return response_valid_request({"coupon_id": query_result.get("inserted_id")})
        else:
            return response_invalid_request()
    elif request.method == 'GET':
        owner_id = request.args.get('owner_id')
        database_responses = getShopsByOwner(owner_id)
        final_response = [{
            "shop_id": database_response.get("shop_id"),
            "coupons": getCouponsByShopID(database_response.get("shop_id"))
        } for database_response in database_responses]
        return response_valid_request(final_response)


# register a new vendor
@app.route('/user/vendor/register', methods=['POST'])
def register_vendor():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        phone_number = data.get('phonenumber')
        password = data.get('password')
        passwordHash = get_hashed_password(password.encode('utf8'))
        result = insertUser(email, firstname, lastname, phone_number, passwordHash, True)
        if result.get('success'):
            return response_valid_request({"user_id": result.get('inserted_id')})
        else:
            return response_invalid_request()


# Get all shops with a specific name
@app.route('/shops/name', methods=['GET'])
def shops_by_name():
    if request.method == 'GET':
        shopname = request.args.get('name')
        database_responses = getShopsByName(shopname)
        final_response = [{
            "shop_id": database_response.get("shop_id"),
            "owner_id": database_response.get("owner_id"),
            "address'": {
                "street": database_response.get("street"),
                "zip_code": database_response.get("zip_code"),
                "city": database_response.get("city"),
                "website_url": database_response.get("website_url"),
                "phone_number": database_response.get("phone_number")
            },
            "information_basic'": {
                "name": database_response.get("name"),
                "logo_url": database_response.get("logo_url"),
                "description_short": database_response.get("description_short")
            },
            "description": database_response.get("description"),
        } for database_response in database_responses]
        return response_valid_request(final_response)


# Get all shops for a specific PLZ
@app.route('/shops/zip', methods=['GET'])
def get_shops_by_zip():
    zip_code = request.args.get('zip_code')
    database_responses = getShopsByZipCode(zip_code)
    final_response = [{
        "shop_id": database_response.get("shop_id"),
        "owner_id": database_response.get("owner_id"),
        "address'": {
            "street": database_response.get("street"),
            "zip_code": database_response.get("zip_code"),
            "city": database_response.get("city"),
            "website_url": database_response.get("website_url"),
            "phone_number": database_response.get("phone_number")
        },
        "information_basic'": {
            "name": database_response.get("name"),
            "logo_url": database_response.get("logo_url"),
            "description_short": database_response.get("description_short")
        },
        "description": database_response.get("description"),
        "offers": getOffersByShopID(database_response.get("shop_id"))
    } for database_response in database_responses]
    return response_valid_request(final_response)


# Get all offers by a shop
@app.route('/shops/offer', methods=['GET'])
def get_offer_by_shop():
    shop_id = request.args.get('shop_id')
    return response_valid_request(getOffersByShopID(shop_id))


# Get all coupons for a shop
@app.route('/shops/coupons', methods=['GET'])
def get_coupons_by_shop():
    shop_id = request.args.get('shop_id')
    return response_valid_request(getCouponsByShopID(shop_id))


# Get all coupons by a customer
@app.route('/user/customer/coupons', methods=['GET'])
def get_coupons_by_customer():
    customer_id = request.args.get('customer_id')
    return response_valid_request(getCouponsByCustomerID(customer_id))


@app.route('/user/vendor/offer', methods=['POST', 'GET'])
def vendor_offer():
    if request.method == 'POST':
        data = request.get_json()
        shop_id = data.get('shop_id')
        offerType = data.get('offerType')
        name = data.get('name')
        description = data.get('description')
        value = data.get('value')
        result = createOffer(shop_id=shop_id, offerType=offerType, name=name,
                             description=description, value=value)
        if result.get('success'):
            return response_valid_request({"offer_id": result.get("inserted_id")})
        else:
            return response_invalid_request()
    elif request.method == 'GET':
        shop_id = request.args.get('shop_id')
        return response_valid_request(getOffersByShopID(shop_id))


# add a new shop for a owner and get all shops for an owner
@app.route('/user/vendor/shops', methods=['POST', 'GET'])
def register_shop_and_retrieve_by_owner():
    if request.method == 'POST':
        data = request.get_json()
        owner_id = data.get('owner_id')
        street = data.get('street')
        zip_code = data.get('zip_code')
        city = data.get('city')
        website_url = data.get('website_url')
        phone_number = data.get('phone_number')
        name = data.get('name')
        logo_url = data.get('logo_url')
        description_short = data.get('description_short')
        description = data.get('description')
        result = insertShopDetails(owner_id, street, zip_code, city, website_url, phone_number, name, logo_url,
                                   description_short, description)
        if result.get('success'):
            return response_valid_request({"shop_id": result.get('inserted_id')})
        else:
            return response_invalid_request()
    elif request.method == 'GET':
        owner_id = request.args.get('owner_id')
        database_responses = getShopsByOwner(owner_id)
        final_response = [{
            "shop_id": database_response.get("shop_id"),
            "address'": {
                "street": database_response.get("street"),
                "zip_code": database_response.get("zip_code"),
                "city": database_response.get("city"),
                "website_url": database_response.get("website_url"),
                "phone_number": database_response.get("phone_number")
            },
            "information_basic'": {
                "name": database_response.get("name"),
                "logo_url": database_response.get("logo_url"),
                "description_short": database_response.get("description_short")
            },
            "description": database_response.get("description"),
        } for database_response in database_responses]
        return response_valid_request(final_response)


# Update value of coupon
@app.route('/user/vendor/devalue_coupon', methods=['PUT'])
def coupon_devalue():
    data = request.get_json()
    used_coupon_id = data.get('used_coupon_id')
    new_value = data.get('new_value')
    activated = data.get('activated')
    return response_valid_request(updateCouponValue(used_coupon_id, new_value, activated))


# activate coupon
@app.route('/user/vendor/set_state_coupon', methods=['PUT'])
def coupon_set_state():
    data = request.get_json()
    used_coupon_id = data.get('used_coupon_id')
    status = data.get('status')  # todo check for constraints or just allow active here?
    return response_valid_request(updateCouponStatus(used_coupon_id, status))


if __name__ == '__main__':
    app.run()
