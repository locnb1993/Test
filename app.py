from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def showLoginPage():
    return render_template('Welcome.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    print('login')
    if request.method == 'POST':
        try:
            error = None
            username = request.json['username']
            password = request.json['password']
            client = MongoClient('mongodb://'+username+':'+password+'@localhost:27017')
            db = client.AbcBank
            LoginInformation ={
                'auth': db.auth(username, password),
                'username': username,
                'password': password
                }
            if db.auth(username, password) == '1':
                redirect(url_for('home'))
            else:
                redirect(url_for('/'))
        except Exception as e:
           return str(e)
    return json.dumps(LoginInformation)

@application.route('/home')
def showAccountList():
    print('showAccountList')
    return render_template('Home.html')

@application.route("/addAccount",methods=['POST'])
def addAccount():
    print('addAccount')
    try:
        json_data = request.json['info']
        account_number = json_data['account_number']
        balance = json_data['balance']
        firstname = json_data['firstname']
        lastname = json_data['lastname']
        age = json_data['age']
        gender = json_data['gender']
        address = json_data['address']
        employer = json_data['employer']
        email = json_data['email']
        city = json_data['city']
        state = json_data['state']

        db.accounts.insert_one({
            'account_number':account_number,
            'balance':balance,
            'firstname':firstname,
            'lastname':lastname,
            'age':age,
            'gender':gender,
            'address':address,
            'employer':employer,
            'email':email,
            'city':city,
            'state':state
            })
        return jsonify(status='OK',message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/getAccount',methods=['POST'])
def getAccount():
    print('getAccount')
    try:
        AccountId = request.json['id']
        Account = db.accounts.find_one({'_id':ObjectId(AccountId)})
        AccountDetail = {
               'account_number':Account['account_number'],
               'balance':Account['balance'],
               'firstname':Account['firstname'],
               'lastname':Account['lastname'],
               'age':Account['age'],
               'gender':Account['gender'],
               'address':Account['address'],
               'employer':Account['employer'],
               'email':Account['email'],
               'city':Account['city'],
               'state':Account['state'],
               'id': str(Account['_id'])
                }
        return json.dumps(AccountDetail)
    except Exception as e:
        return str(e)

@application.route('/updateAccount',methods=['POST'])
def updateAccount():
    print('updateAccount')
    try:
        accountInfo = request.json['info']
        accountID = accountInfo['id']
        account_number = accountInfo['account_number']
        balance = accountInfo['balance']
        firstname = accountInfo['firstname']
        lastname = accountInfo['lastname']
        age = accountInfo['age']
        gender = accountInfo['gender']
        address = accountInfo['address']
        employer = accountInfo['employer']
        email = accountInfo['email']
        city = accountInfo['city']
        state = accountInfo['state']

        db.accounts.update_one({'_id':ObjectId(accountID)},
		{'$set':{'account_number':account_number,
                'balance':balance,
			    'firstname':firstname,
				'lastname': lastname,
				'age':age,
				'gender':gender,
				'address':address,
				'employer':employer,
				'email':email,
				'city':city,
				'state': state
				}
		})
        return jsonify(status='OK',message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getAccountList",methods=['POST'])
def getAccountList():
    print(getAccountList)
    try:
        Accounts = db.accounts.find().limit(10)
        
        AccountList = []
        for Account in Accounts:
            #print Account
            AccountItem = {
                    'account_number':Account['account_number'],
                    'balance':Account['balance'],
                    'firstname':Account['firstname'],
                    'lastname':Account['lastname'],
                    'age':Account['age'],
                    'gender':Account['gender'],
                    'address':Account['address'],
                    'employer':Account['employer'],
                    'email':Account['email'],
                    'city':Account['city'],
                    'state':Account['state'],
                    'id': str(Account['_id'])
                    }
            AccountList.append(AccountItem)
    except Exception as e:
        return str(e)
    return json.dumps(AccountList)

@application.route("/deleteAccount",methods=['POST'])
def deleteAccount():
    print('deleteAccount')
    try:
        AccountId = request.json['id']
        db.accounts.remove({'_id':ObjectId(AccountId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.run(host='127.0.0.1')

