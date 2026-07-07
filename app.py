from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import EmailField,PasswordField,StringField,SubmitField
from wtforms.validators import Email,EqualTo,Length
load_dotenv()
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
db=SQLAlchemy(app)
migrate=Migrate(app,db)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/register',methods=["POST","GET"])
def register():
    return render_template("register.html")
@app.route('/login')
def login():
    return render_template("login.html")
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")
if __name__=="__main__":
    app.run(debug=True)