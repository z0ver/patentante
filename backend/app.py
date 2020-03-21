from flask import Flask, redirect, url_for, session, render_template, request, Response
from flask_login import LoginManager, login_user, current_user, login_required
from flask_session import Session

import simplejson as json
from db import *
from datetime import datetime

from model import User
from config import secret_key

app = Flask(__name__)
app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

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
    #this area converts datetime values from python to strings so they are serializable
    for row in data:
        if isinstance(row,dict):
            for key, value in row.items():
                if isinstance(value,list):
                    for list_index, list_value in enumerate(value):
                        if isinstance(list_value, dict):
                            for list_item_key, list_item_value in list_value.items():
                                if isinstance(list_item_value, datetime):
                                    row[key][list_index][list_item_key] = list_item_value.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(value,datetime):
                    row[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    _response = {}
    _response['Success'] = True
    _response['Status'] = 200
    _response['Result'] = data
    return Response(response=json.dumps(_response, sort_keys=True, indent=4),
                    status=200,
                    mimetype="application/json")

#Main page, ToDo: create main page template
@app.route('/')
@login_required
def index():
    return "Welcome"

#compare the user id with the known sessions
@login_manager.user_loader
def load_user(id):
    if 'users' in session.keys():
        if int(id) in session['users'].keys():
            return session['users'][int(id)]
        else:
            return None
    else:
        session['users'] = {}
    return id

#Login page for the user
@app.route('/login')
def login_page():
    return render_template("login_form.html")

#Page where the data entered in the login page gets validated
#If validation not successful, it moves back to the login page
@app.route('/logged-in', methods=['POST'])
def loggedin_page():
    username = request.form["username"]
    password = request.form["password"]
    #ToDo: database check if we know this user and the password is correct
    if (password == '1234' and username == 'test'):
        session.clear()
        if not 'users' in session.keys():
            session['users'] = {}
        user = User({"id":0, "name":"Horst"})
        session['users'][user.id] = user
        login_user(user)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login_page'))


#Get or create coupons for the dealer
@app.route('/dealer/coupons',methods=['GET','POST'])
def dealer_coupon():
    if request.method == 'POST':
        data = request.get_json()
        profile_id = data.get('profileId')
        offer_id = data.get('offerId')
        coupon_value = data.get('value')
        price = data.get('price')
        status = data.get('status')
        query_result = insertCoupon(offer_ID=offer_id, customer_ID=profile_id, original_value=price,current_value=coupon_value,status=status,date_of_purchase=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return {"couponId": query_result.get("inserted_row")}
    elif request.method ==  'GET':
        profile_id = request.args.get('profileId')
        return response_valid_request(getCouponsByUserID(profile_id))

#Get all coupons for the dealer which are already used up
@app.route('/dealer/used_coupons',methods=['GET'])
def dealer_coupon_used():
    profile_id = request.args.get('profileId')
    return response_valid_request(getUsedCouponsByUserID(profile_id))

#Update value and potentially devalue it
@app.route('/dealer/devalue_coupon',methods=['PUT'])
def dealer_devalue_coupon():
    data = request.get_json()
    used_coupon_id = data.get('used_couponId')
    new_value = data.get('new_value')
    activated = data.get('activated')
    return response_valid_request(updateCouponValue(used_coupon_id,new_value,activated))

#Get all dealers for a specific PLZ
@app.route('/customer/list_dealers',methods=['GET'])
def get_dealers_by_zip():
    plz = request.args.get('plz')
    database_responses = getShopsByZipCode(plz)
    final_response = [{
        "profileId": database_response.get("owner_id"),
        "address'":{
            "postcode": database_response.get("zipCode"),
            "place": database_response.get("street")+" "+database_response.get("city"),
            "number": database_response.get("phoneNumber")
        },
        "description": database_response.get("description"),
        "coupons": getCouponsByUserID(database_response.get("owner_id"))
    } for database_response in database_responses]
    return response_valid_request(final_response)

#Login for users with owner status
@app.route('/dealer/login', methods=['POST'])
def login_dealer():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        hash = getUserByMail(email)
        if check_password(password.encode('utf8'), hash[0].get('passwordHash').encode('utf8')):
            return response_valid_request({"userid": hash[0].get('user_id')})
        else:
            return response_unauthorized_request()

#Check for shops using a part of the name
@app.route('/shops/name', methods=['GET'])
def shops_by_name():
    if request.method == 'GET':
        shopname = request.args.get('name')
        return response_valid_request(getShopsByName(shopname))

#Request a new coupon for a customer
@app.route('/customer/request_coupon', methods=['POST'])
def request_coupon():
    data = request.get_json()
    profile_id = data.get('profileId')
    offer_id = data.get('offerId')
    current_value = data.get('donation')
    original_value = data.get('donation')
    query_result = insertCoupon(offer_ID=offer_id, customer_ID=profile_id, original_value=original_value,current_value=current_value,status='ACTIVATE',date_of_purchase=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return {"couponId":query_result.get("inserted_row")}


if __name__ == '__main__':
    app.run()
