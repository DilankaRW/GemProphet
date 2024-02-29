from flask import Flask,session, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import pickle
import pymysql
import joblib
pymysql.install_as_MySQLdb()
import numpy as np
import pandas as pd

from cryptography.fernet import Fernet
import json

import xgboost as xgb

app = Flask(__name__)
app.secret_key = '0112602125'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '0112602125'
Session(app)
global_key = 'VW1W78MpaJLEJKGS6MTZuBco_4aJHj80-JEH_iIZ-CQ='

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost:3307/modeldb'
db = SQLAlchemy(app)
model = joblib.load(open('xgboost_model.model', 'rb'))
# model = pickle.load(open('xgboost_model.pkl', 'rb'))

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    carat = db.Column(db.Float)
    cut = db.Column(db.String(800))
    colour = db.Column(db.String(800))
    clarity = db.Column(db.String(800))
    depth = db.Column(db.Float)
    table = db.Column(db.Float)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)
    price = db.Column(db.Float)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(800))
    email = db.Column(db.String(800))
    full_name = db.Column(db.String(800))
    password = db.Column(db.String(800))

#   START ENCRYPTION-DECRYPTION METHODS

# Encrypt data
def encrypt_data(plaintext):
    fernet = Fernet(global_key)
    return fernet.encrypt(plaintext.encode())

# Decrypt data
def decrypt_data(ciphertext):
    fernet = Fernet(global_key)
    return fernet.decrypt(ciphertext).decode()

#   END ENCRYPTION-DECRYPTION METHODS

@app.route('/view', methods=['GET', 'POST'])
def view():

    prediction_data = Record.query.all()
    fistname_json = {}
    i = 0

    prediction_datas_signupid = [(prediction_datas.sign_up_id_) for prediction_datas in prediction_data]
    for sign_up_id_ in prediction_datas_signupid:
        id = sign_up_id_

        users = User.query.filter_by(sign_up_id_=id)
        firstNames = [(user.first_name_) for user in users]
        for fistname_ in firstNames:
            fistname_json[i] = decrypt_data(fistname_)
            i = i + 1


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('fname')

        if username and email and password and first_name: #All fields are not empty
            loan_app = User(
            user_name = encrypt_data(username),
            password = encrypt_data(password),
            email = encrypt_data(email),
            full_name = encrypt_data(first_name),

            )

            db.session.add(loan_app)
            db.session.commit()

            return render_template("login.html")

        else:
            return render_template("signup.html", signup_text="Signup failed. Please fill all fields".format(signup))

    else:
        return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    username = request.form.get('username')
    password = request.form.get('password')


    if request.method == 'POST':

        if not username and not password:
            return render_template("login.html", login_text="Please fill all fields".format(login))

        #Fetch username and password from all data
        users = User.query.all()

        # Extract usernames and passwords from the records
        usernames_and_passwords_and_signupid = [(user.user_id,user.user_name, user.password) for user in users]
        for sign_up_id_,username_, password_ in usernames_and_passwords_and_signupid:
            encryptedUsername = username_
            encryptedPassword = password_

            decyptedUsername = decrypt_data(encryptedUsername)
            decyptedPassword = decrypt_data(encryptedPassword)

            if(decyptedUsername == username and decyptedPassword == password):
                session['user_id'] = sign_up_id_
                session['user_name'] = decyptedUsername

                return render_template('/index.html')

        return render_template("login.html", login_text="Login failed. Please check your username and password".format(login))

    else:
        return render_template("login.html")

@app.route('/')
def home():
        return render_template("index.html")

@app.route('/aboutus')
def aboutus():
        return render_template("aboutus.html")

@app.route('/user_details')
def profile():

        #Check user Login or not
        userId = session.get('user_id')
        if userId is None:
            return render_template("login.html")

        userData_json = {}
        username = session.get('user_name')

        users = User.query.all()

        usernameInUserData = [(user.user_name) for user in users]
        for username_ in usernameInUserData:
            encryptedUsername = username_

            decyptedUsername = decrypt_data(encryptedUsername)
            if(username == decyptedUsername):
                correctUser = User.query.filter_by(user_name = encryptedUsername).first()
                if correctUser is not None:
                    userData_json["username"] = decrypt_data(correctUser.user_name)
                    userData_json["email"] = decrypt_data(correctUser.email)
                    userData_json["first_name"] = decrypt_data(correctUser.full_name)
                    userData_json["password"] = decrypt_data(correctUser.password)
                    return render_template("user_details.html",userDetails = userData_json)

        return render_template("user_details.html",userDetails = None)

@app.route('/update_profile', methods=['GET', 'POST'])
def updateProfile():

    userId = session.get('user_id')
    if userId is None:
        return render_template("login.html")

    username = session.get('user_name')
    userData_json = {}

    if request.method ==  'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        password = request.form.get('password')

        if email and password and fname: #All fields are not empty

            users = User.query.all()

            usernameInUserData = [(user.user_name) for user in users]
            for username_ in usernameInUserData:

                encryptedUsername = username_
                decyptedUsername = decrypt_data(encryptedUsername)

                if(username == decyptedUsername):
                    correctUser = User.query.filter_by(user_name = encryptedUsername).first()
                    if correctUser is not None:
                        correctUser.full_name = encrypt_data(fname)
                        correctUser.email = encrypt_data(email)
                        correctUser.password =encrypt_data(password)

                        db.session.add(correctUser)
                        db.session.commit()

                        userData_json["username"] = username
                        userData_json["email"] = email
                        userData_json["first_name"] = fname
                        userData_json["password"] = password

                        return render_template("user_details.html",userDetails = userData_json, profile_text="Update Success".format(""))

        else:
            userData_json["username"] = username
            userData_json["email"] = email
            userData_json["first_name"] = fname
            userData_json["password"] = password

            return render_template("user_details.html",userDetails = userData_json, profile_text="Update failed. Please fill all fields".format(""))


    users = User.query.all()

    usernameInUserData = [(user.user_name) for user in users]
    for username_ in usernameInUserData:

        encryptedUsername = username_
        decyptedUsername = decrypt_data(encryptedUsername)

        if(username == decyptedUsername):
            correctUser = User.query.filter_by(username_ = encryptedUsername).first()
            if correctUser is not None:
                userData_json["username"] = decrypt_data(correctUser.username_)
                userData_json["email"] = decrypt_data(correctUser.email_)
                userData_json["first_name"] = decrypt_data(correctUser.first_name_)
                userData_json["password"] = decrypt_data(correctUser.password_)

    return render_template("user_details.html",userDetails = userData_json)

@app.route('/logout')
def logout():
        session['user_id'] = None
        session['user_name'] = None
        return render_template("login.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':

        #Check user Login or not
        userId = session.get('user_id')
        if userId is None:
            return render_template("login.html")

        carat = float(request.form['Carat'])
        cut = request.form['Cut']
        color = request.form['Colour']
        clarity = request.form['Clarity']
        depth = float(request.form['Depth'])
        table = float(request.form['Table'])
        x = float(request.form['X'])
        y = float(request.form['Y'])
        z = float(request.form['Z'])


        if carat and cut and color and clarity and depth and table and x and y and z:


            if(cut=='Fair'):
                cut_1 = 1
                cut_2 = 0
                cut_3 = 0
                cut_4 = 0
                cut_5 = 0
            elif(cut=='Good'):
                cut_1 = 0
                cut_2 = 1
                cut_3 = 0
                cut_4 = 0
                cut_5 = 0
            elif(cut=='Very Good'):
                cut_1 = 0
                cut_2 = 0
                cut_3 = 1
                cut_4 = 0
                cut_5 = 0
            elif(cut=='Premium'):
                cut_1 = 0
                cut_2 = 0
                cut_3 = 0
                cut_4 = 1
                cut_5 = 0
            elif(cut=='Ideal'):
                cut_1 = 0
                cut_2 = 0
                cut_3 = 0
                cut_4 = 0
                cut_5 = 1

            else:
                cut_1 = 0
                cut_2 = 0
                cut_3 = 0
                cut_4 = 0
                cut_5 = 0

            if(color=='D'):
                color_1 = 1
                color_2 = 0
                color_3 = 0
                color_4 = 0
                color_5 = 0
                color_6 = 0
                color_7 = 0

            elif(color=='E'):
                color_1 = 0
                color_2 = 1
                color_3 = 0
                color_4 = 0
                color_5 = 0
                color_6 = 0
                color_7 = 0

            elif(color=='F'):
                color_1 = 0
                color_2 = 0
                color_3 = 1
                color_4 = 0
                color_5 = 0
                color_6 = 0
                color_7 = 0

            elif(color=='G'):
                color_1 = 0
                color_2 = 0
                color_3 = 0
                color_4 = 1
                color_5 = 0
                color_6 = 0
                color_7 = 0

            elif(color=='H'):
                color_1 = 0
                color_2 = 0
                color_3 = 0
                color_4 = 0
                color_5 = 1
                color_6 = 0
                color_7 = 0
            
            elif(color=='I'):
                color_1 = 0
                color_2 = 0
                color_3 = 0
                color_4 = 0
                color_5 = 0
                color_6 = 1
                color_7 = 0
            
            elif(color=='J'):
                color_1 = 0
                color_2 = 0
                color_3 = 0
                color_4 = 0
                color_5 = 0
                color_6 = 0
                color_7 = 1

            else:
                color_1 = 0
                color_2 = 0
                color_3 = 0
                color_4 = 0
                color_5 = 0
                color_6 = 0
                color_7 = 0

            if(clarity=='I1'):
                clarity_1 = 1
                clarity_2 = 0
                clarity_3 = 0
                clarity_4 = 0
                clarity_5 = 0
                clarity_6 = 0
                clarity_7 = 0
                clarity_8 = 0

            elif(clarity=='IF'):
                clarity_1 = 0
                clarity_2 = 1
                clarity_3 = 0
                clarity_4 = 0
                clarity_5 = 0
                clarity_6 = 0
                clarity_7 = 0
                clarity_8 = 0

            elif(clarity=='SI1'):
                clarity_1 = 0
                clarity_2 = 0
                clarity_3 = 1
                clarity_4 = 0
                clarity_5 = 0
                clarity_6 = 0
                clarity_7 = 0
                clarity_8 = 0

            elif(clarity=='SI2'):
                clarity_1 = 0
                clarity_2 = 0
                clarity_3 = 0
                clarity_4 = 1
                clarity_5 = 0
                clarity_6 = 0
                clarity_7 = 0
                clarity_8 = 0

            elif(clarity=='VS1'):
                clarity_1 = 0
                clarity_2 = 0
                clarity_3 = 0
                clarity_4 = 0
                clarity_5 = 1
                clarity_6 = 0
                clarity_7 = 0
                clarity_8 = 0

            elif(clarity=='VS2'):
                clarity_1 = 0
                clarity_2 = 0
                clarity_3 = 0
                clarity_4 = 0
                clarity_5 = 0
                clarity_6 = 1
                clarity_7 = 0
                clarity_8 = 0

            elif(clarity=='VVS1'):
                clarity_1 = 0
                clarity_2 = 0
                clarity_3 = 0
                clarity_4 = 0
                clarity_5 = 0
                clarity_6 = 0
                clarity_7 = 1
                clarity_8 = 0

            elif(clarity=='VVS2'):
                clarity_1 = 0
                clarity_2 = 0
                clarity_3 = 0
                clarity_4 = 0
                clarity_5 = 0
                clarity_6 = 0
                clarity_7 = 0
                clarity_8 = 1

            else:
                clarity_1 = 0
                clarity_2 = 0
                clarity_3 = 0
                clarity_4 = 0
                clarity_5 = 0
                clarity_6 = 0
                clarity_7 = 0
                clarity_8 = 0


            carat = (carat)
            depth = (depth)
            table = (table)
            x = (x)
            y = (y)
            z = (z)

            prediction = model.predict([[carat, depth, table, x, y, z, cut_1, cut_2, cut_3, cut_4, cut_5, color_1, color_2,color_3,color_4,color_5,color_6,color_7, clarity_1, clarity_2, clarity_3, clarity_4, clarity_5, clarity_6, clarity_7, clarity_8]])

            print(prediction)


            prediction = '<div class="alert alert-warning" role="alert">Predict Price: ${}</div>'.format(prediction)

            return render_template('prediction.html', prediction=str(prediction))


        else:

            pre_text = '<div class="alert alert-danger" role="alert">{}</div>'.format(pre_text)

            return render_template("prediction.html", pre_text=pre_text)

    else:

        #Check user Login or not
        userId = session.get('user_id')
        if userId is None:
            return render_template("login.html")

        return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True)