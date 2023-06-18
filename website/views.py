from flask import Blueprint, render_template, Flask, request, redirect, url_for
from .models import User
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user_agent = request.headers.get('User-Agent')
    if 'Mobile' in user_agent:
        return render_template("templates-mobile/home_mobile.html")
    elif 'Windows' in user_agent:
        return render_template("templates-pc/home.html")
    else:
        return render_template("templates-pc/home.html")
    
@views.route('/login')
def login():
    user_agent = request.headers.get('User-Agent')
    if 'Mobile' in user_agent:
        return render_template("templates-mobile/login_mobile.html")
    elif 'Windows' in user_agent:
        return render_template("templates-pc/login.html")
    else:
        return render_template("templates-pc/login.html")
    
@views.route('/register')
def register():
    user_agent = request.headers.get('User-Agent')
    if 'Mobile' in user_agent:
        return render_template("templates-mobile/register_mobile.html")
    elif 'Windows' in user_agent:
        return render_template("templates-pc/register.html")
    else:
        return render_template("templates-pc/register.html")
    
@views.route('/registersend', methods=['GET', 'POST'])
def signup():
    if request.method=="POST":
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        schoolID = request.form['schoolID']
        classID = request.form['classID']

        newUser = User(name = name, lastname=surname, email=email, password=password, school_id=schoolID, classroom_id=classID)
        db.session.add(newUser)
        db.session.commit()
        return redirect("/")