from flask import Blueprint, render_template, Flask, request, redirect, make_response
from .models import User
from . import db
import time

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user_agent = request.headers.get('User-Agent')
    isLoggedIn = request.cookies.get('isLoggedIn')
    if isLoggedIn=="True":
        isLoggedIn=True
    else:
        isLoggedIn=False
    if 'Mobile' in user_agent:
        return render_template("templates-mobile/home_mobile.html", isLoggedIn=isLoggedIn)
    elif 'Windows' in user_agent:
        return render_template("templates-pc/home.html", isLoggedIn=isLoggedIn)
    else:
        return render_template("templates-pc/home.html", isLoggedIn=isLoggedIn)
    
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
def registersend():
    if request.method=="POST":
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        schoolID = request.form['schoolID']
        classID = request.form['classID']

        #provjera jesu li uneseni podatci valjani
        if len(email)>5:
            if "@" in email:
                if "." in email:
                    pass
                else:
                    return redirect("/register")
            else:
                return redirect("/register")
        else:
            return redirect("/register")
        has_letter = any(char.isalpha() for char in password)
        has_number = any(char.isdigit() for char in password)
        if len(password)>=8:
            if has_letter and has_number:
                pass
            else:
                return redirect("/register")
        else:
            return redirect("/register")
        if len(schoolID)!=0:
            try:
                int(schoolID)
                pass
            except ValueError:
                return redirect("/register")
        if len(classID)!=0:
            try:
                int(classID)
                pass
            except ValueError:
                return redirect("/register")
        

        #provjera postoji li račun s tim emailom
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return redirect("/register")
        else:
            newUser = User(name = name, lastname=surname, email=email, password=password, school_id=schoolID, classroom_id=classID)
            db.session.add(newUser)
            db.session.commit()

            #login novog usera
            user = User.query.filter_by(email=email).first()
            response = make_response(redirect("/"))
            response.set_cookie('isLoggedIn', value="True")
            response.set_cookie('loggedUser', value=str(user.id))
            return response

    
@views.route('/loginsend', methods=['GET', 'POST'])
def loginsend():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password==password:
                response = make_response(redirect("/"))
                response.set_cookie('isLoggedIn', value="True")
                response.set_cookie('loggedUser', value=str(user.id))
                return response
            else:
                response.set_cookie('isLoggedIn', value="False")
                return redirect("/login")
        else:
            response.set_cookie('isLoggedIn', value="False")
            return redirect("/login")
        
@views.route('/logout')
def logout():
    response = make_response(redirect("/"))
    response.set_cookie('isLoggedIn', value="False")
    return response

@views.route('/viewprofile')
def viewprofile():
    loggedUser = User.query.get(int(request.cookies.get('loggedUser')))
    return render_template("templates-pc/profile.html", user=loggedUser)
    
    