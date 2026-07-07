from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import EmailField,PasswordField,StringField,SubmitField
from wtforms.validators import Email,EqualTo,Length,InputRequired
load_dotenv()
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
app.config['SECRET_KEY']=os.getenv("CSRF_SECRET_KEY")
db=SQLAlchemy(app)
migrate=Migrate(app,db)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/register',methods=["POST","GET"])
def register():
    #create instance of form
    form=RegisterForm()
    if form.validate_on_submit():
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        new_user=Users(username=username,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html",form=form)
@app.route('/login',methods=["POST","GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    return render_template("login.html",form=form)
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


#register form
#inherit from FlaskForm class to use its features
class RegisterForm(FlaskForm):
    username=StringField("Username",validators=[InputRequired(),Length(min=4)])
    email=EmailField("Email address",validators=[InputRequired(),Email()])
    password=PasswordField("Password",validators=[InputRequired(),Length(max=255)])
    confirm_password=PasswordField("Confirm_password",validators=[InputRequired(),Length(min=8),EqualTo("password",message="Passwords must match")])
    submit=SubmitField("Register")
#login form
#inherits from FlaskForm to use its features
class LoginForm(FlaskForm):
    username=StringField("Username",validators=[InputRequired(),Length(min=4)])
    password=PasswordField("Password",validators=[InputRequired(),Length(min=8)])
    submit=SubmitField("Login")
#database models
class Users(db.Model):
    __tablename__="Users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
if __name__=="__main__":
    app.run(debug=True)