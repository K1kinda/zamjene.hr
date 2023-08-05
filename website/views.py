from flask import Blueprint, render_template, Flask, request, redirect, make_response, url_for, jsonify
from .models import User, School, Classroom, Zamjene, Obavjesti, RasporedSati, RasporedUcionica
from . import db
import time
import pandas as pd
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user_agent = request.headers.get('User-Agent') 
    isLoggedIn = request.cookies.get('isLoggedIn')

    if isLoggedIn=="True":
        isLoggedIn=True
    else:
        isLoggedIn=False

    skola = request.cookies.get('Skola')
    if skola=="True":
        loggedskolaID = int(request.cookies.get('loggedSchool'))
        sve_obavijesti = Obavjesti.query.filter_by(school_id=loggedskolaID).all()
        sve_obavijesti = sve_obavijesti[::-1]
    else:
        sve_obavijesti=[]

    if 'Mobile' in user_agent:
        return render_template("templates-mobile/home_mobile.html", isLoggedIn=isLoggedIn, sve_obavijesti=sve_obavijesti)
    elif 'Windows' in user_agent:
        return render_template("templates-pc/home.html", isLoggedIn=isLoggedIn, sve_obavijesti=sve_obavijesti)
    else:
        return render_template("templates-pc/home.html", isLoggedIn=isLoggedIn, sve_obavijesti=sve_obavijesti)
    
    
@views.route('/login')
def login():
    error=request.args.get("error")
    user_agent = request.headers.get('User-Agent')
    isLoggedIn = request.cookies.get('isLoggedIn')
    if 'Mobile' in user_agent:
        return render_template("templates-mobile/login_mobile.html", error=error, isLoggedIn=isLoggedIn)
    elif 'Windows' in user_agent:
        return render_template("templates-pc/login.html", error=error, isLoggedIn=isLoggedIn)
    else:
        return render_template("templates-pc/login.html", error=error, isLoggedIn=isLoggedIn)
    
@views.route('/loginadmin')
def loginAdmin():
    error=request.args.get("error")
    user_agent = request.headers.get('User-Agent')
    isLoggedIn = request.cookies.get('isLoggedIn')
    if 'Mobile' in user_agent:
        return render_template("templates-pc/login-admin.html", error=error, isLoggedIn=isLoggedIn)
    elif 'Windows' in user_agent:
        return render_template("templates-pc/login-admin.html", error=error, isLoggedIn=isLoggedIn)
    else:
        return render_template("templates-pc/login-admin.html", error=error, isLoggedIn=isLoggedIn)
    
@views.route('/loginskola')
def loginskola():
    error=request.args.get("error")
    user_agent = request.headers.get('User-Agent')
    isLoggedIn = request.cookies.get('isLoggedIn')
    if 'Mobile' in user_agent:
        return render_template("templates-pc/login-skola.html", error=error, isLoggedIn=isLoggedIn)
    elif 'Windows' in user_agent:
        return render_template("templates-pc/login-skola.html", error=error, isLoggedIn=isLoggedIn)
    else:
        return render_template("templates-pc/login-skola.html", error=error, isLoggedIn=isLoggedIn)
    
@views.route('/register')
def register():
    error=request.args.get("error")
    user_agent = request.headers.get('User-Agent')
    isLoggedIn = request.cookies.get('isLoggedIn')
    if 'Mobile' in user_agent:
        return render_template("templates-mobile/register_mobile.html", error=error, isLoggedIn=isLoggedIn)
    elif 'Windows' in user_agent:
        return render_template("templates-pc/register.html", error=error, isLoggedIn=isLoggedIn)
    else:
        return render_template("templates-pc/register.html", error=error, isLoggedIn=isLoggedIn)
    
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
                    error="Nevaljani email."
                    return redirect(url_for("vievs.register", error=error))
            else:
                error="Nevaljani email."
                return redirect(url_for("views.register", error=error))
        else:
            error="Nevaljani email."
            return redirect(url_for("vievs.register", error=error))
        has_letter = any(char.isalpha() for char in password)
        has_number = any(char.isdigit() for char in password)
        if len(password)>=8:
            if has_letter and has_number:
                pass
            else:
                error="Loznika mora sadržavati i brojeve i slova."
                return redirect(url_for("views.register", error=error))
        else:
            error="Lozinka mora sadržavati barem 8 znakova."
            return redirect(url_for("views.register", error=error))
        if len(schoolID)!=0:
            try:
                int(schoolID)
                pass
            except ValueError:
                error="Nevaljan ID Škole."
                return redirect(url_for("views.register", error=error))
        if len(classID)!=0:
            try:
                int(classID)
                pass
            except ValueError:
                error="Nevaljan ID učionice."
                return redirect(url_for("views.register", error=error))
        

        #provjera postoji li račun s tim emailom
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error="Korisnik s tim emailom već postoji."
            return redirect(url_for("views.register", error=error))
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
    error=""
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
                error="Kriva lozinka."
                response = make_response(redirect(url_for("views.login", error=error)))
                response.set_cookie('isLoggedIn', value="False")
                return response
        else:
            error="Krivi email."
            response = make_response(redirect(url_for("views.login", error=error)))
            response.set_cookie('isLoggedIn', value="False")
            return response
        
@views.route('/loginadminsend', methods=['GET', 'POST'])
def loginadminsend():
    error=""
    if request.method=="POST":
        password = request.form['password']

        if password=="lozinka":
            response = make_response(redirect("/adminmenu"))
            response.set_cookie('isLoggedIn', value="True") 
            response.set_cookie('Admin', value="True")
            return response
        else:
            error="Kriva lozinka."
            response = make_response(redirect(url_for("views.loginadmin", error=error)))
            response.set_cookie('isLoggedIn', value="False")
            return response
        
@views.route('/adminmenu', methods=['GET', 'POST'])
def adminmenu():
    isLoggedIn = request.cookies.get('isLoggedIn')
    Admin = request.cookies.get('Admin')
    if isLoggedIn and Admin:
        return render_template("templates-pc/admin-menu.html", isLoggedIn=isLoggedIn)
    else:
        return redirect("/")
    
@views.route('/add-school-menu', methods=['GET', 'POST'])
def addschoolmenu():
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isLoggedIn')
    Admin = request.cookies.get('Admin')
    if isLoggedIn and Admin:
        return render_template("templates-pc/add-school-menu.html", error=error, isLoggedIn=isLoggedIn)
    else:
        return redirect("/")
    
@views.route('/loginskolasend', methods=['GET', 'POST'])
def loginskolasend():
    error=""
    if request.method=="POST":
        #dodat da se ulogira pomocu ovog u pravi racun skole...
        id = request.form['id']
        school = School.query.filter_by(id=id).first()
        if school:
            instertedpassword = request.form['password']
            password=school.login_password
            if instertedpassword==password:
                response = make_response(redirect("/skolamenu"))
                response.set_cookie('isLoggedIn', value="True")
                response.set_cookie('Skola', value="True")
                response.set_cookie('loggedSchool', value=str(school.id))
                return response
            else:
                error="Kriva lozinka."
                response = make_response(redirect(url_for("views.loginskola", error=error)))
                response.set_cookie('isLoggedIn', value="False")
                return response
        else:
            error="Škola s tim ID-em ne postoji."
            response = make_response(redirect(url_for("views.loginskola", error=error)))
            response.set_cookie('isLoggedIn', value="False")
            return response

        
@views.route('/skolamenu', methods=['GET', 'POST'])
def skolamenu():
    isLoggedIn = request.cookies.get('isLoggedIn')
    Skola = request.cookies.get('Skola')
    loggedskolaID = int(request.cookies.get('loggedSchool'))
    loggedskola = School.query.filter_by(id=loggedskolaID).first()

    obavijesti = Obavjesti.query.filter_by(school_id=loggedskolaID).all()
    obavijesti = obavijesti[::-1]

    if request.method == 'POST':
        classroom_name = request.form.get('classroom_name')

        db.session.add(Classroom(name=classroom_name, school_id=loggedskolaID))
        db.session.commit()

    if isLoggedIn and Skola:
        classrooms = Classroom.query.filter_by(school_id=loggedskolaID).all()
        return render_template("templates-pc/skola-menu.html", skola=loggedskola, isLoggedIn=isLoggedIn, classrooms=classrooms, obavijesti=obavijesti)
    else:
        return redirect("/")
    
        
@views.route('/logout')
def logout():
    response = make_response(redirect("/"))
    response.set_cookie('isLoggedIn', value="False")
    response.set_cookie('Skola', value="False")
    response.set_cookie('Admin', value="False")
    response.set_cookie('loggedSchool', value="")
    response.set_cookie('loggedUser', value="")
    return response

@views.route('/viewprofile')
def viewprofile():
    skola = request.cookies.get('Skola')
    isLoggedIn = request.cookies.get('isLoggedIn')
    if skola=="True":
        return redirect("/skolamenu")
    else:
        loggedUser = User.query.get(int(request.cookies.get('loggedUser')))
        return render_template("templates-pc/profile.html", user=loggedUser, isLoggedIn=isLoggedIn)
    
@views.route('/addschool', methods=['GET', 'POST'])
def addschool():
    isLoggedIn = request.cookies.get('isLoggedIn')
    if request.method=="GET":
        error=request.args.get("error")
        user_agent = request.headers.get('User-Agent')
        if 'Mobile' in user_agent:
            return render_template("templates-pc/add-school-login.html", error=error, isLoggedIn=isLoggedIn)
        elif 'Windows' in user_agent:
            return render_template("templates-pc/add-school-login.html", error=error, isLoggedIn=isLoggedIn)
        else:
            return render_template("templates-pc/add-school-login.html", error=error, isLoggedIn=isLoggedIn)
    elif request.method=="POST":
        password = request.form['password']

        if password=="lozinka":
            response = make_response(redirect("/add-school-menu"))
            response.set_cookie('isLoggedIn', value="True") 
            response.set_cookie('Skola', value="True")
            return response
        else:
            error="Kriva lozinka."
            response = make_response(redirect(url_for("views.addschool", error=error)))
            response.set_cookie('isLoggedIn', value="False")
            return response
    
@views.route('/addschoolfunction', methods=['GET', 'POST'])
def addschoolfunction():
    if request.method=="POST":
        name = request.form['name']
        password = request.form['password']
        id = request.form['id']

        has_letter = any(char.isalpha() for char in password)
        has_number = any(char.isdigit() for char in password)
        if len(password)>=8:
            if has_letter and has_number:
                pass
            else:
                error="Loznika mora sadržavati i brojeve i slova."
                return redirect(url_for("views.addschoolmenu", error=error))
        else:
            error="Lozinka mora sadržavati barem 8 znakova."
            return redirect(url_for("views.addschoolmenu", error=error))
        

        #provjera postoji li račun s tim emailom
        existing_user = School.query.filter_by(id=id).first()
        if existing_user:
            error="Korisnik s tim emailom već postoji."
            return redirect(url_for("views.addschoolmenu", error=error))
        else:
            newSchool = School(name = name, login_password=password, id=id)
            db.session.add(newSchool)
            db.session.commit()

            #login novog usera
            school = School.query.filter_by(id=id).first()
            response = make_response(redirect("/skolamenu"))
            response.set_cookie('isLoggedIn', value="True")
            response.set_cookie('loggedSchool', value=str(school.id))
            return response

@views.route('/prikazizamjene', methods=['GET', 'POST'])
def prikazizamjene():
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isLoggedIn')

    schoolID = request.form['school_id']
    classroomID = request.form['classroom_id']
    classroom = Classroom.query.filter_by(id=classroomID, school_id=schoolID).first()

    zamjene = Zamjene.query.filter_by(classroom_id=classroomID).all()

    return render_template("templates-pc/prikaz-zamjena.html", error=error, isLoggedIn=isLoggedIn, sve_zamjene=zamjene, razred=classroom, classroomid=classroomID, schoolid=schoolID)

@views.route('/dodajzamjenu', methods=['GET', 'POST'])
def dodajzamjenu():
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isLoggedIn')

    schoolID = request.form['school_id']
    classroomID = request.form['classroom_id']
    classroom = Classroom.query.filter_by(id=classroomID, school_id=schoolID).first()

    if request.method=="POST":
        zamjena = request.form['zamjena']

        nova_zamjena = Zamjene(zamjena=zamjena, classroom_id=classroomID)
        db.session.add(nova_zamjena)
        db.session.commit()

        zamjene = Zamjene.query.filter_by(classroom_id=classroomID).all()
 
    return render_template("templates-pc/prikaz-zamjena.html", error=error, isLoggedIn=isLoggedIn, sve_zamjene=zamjene, razred=classroom, classroomid=classroomID, schoolid=schoolID)
        

@views.route('/delete_zamjene/<int:zamjene_id>', methods=['POST'])
def delete_zamjene(zamjene_id):
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isLoggedIn')

    zamjene = Zamjene.query.get(zamjene_id)

    db.session.delete(zamjene)
    db.session.commit()

    schoolID = request.form['school_id']
    classroomID = request.form['classroom_id']
    classroom = Classroom.query.filter_by(id=classroomID, school_id=schoolID).first()
    zamjene = Zamjene.query.filter_by(classroom_id=classroomID).all()
    
    return render_template("templates-pc/prikaz-zamjena.html", error=error, isLoggedIn=isLoggedIn, sve_zamjene=zamjene, razred=classroom, classroomid=classroomID, schoolid=schoolID)

@views.route('/obrisirazred', methods=['POST'])
def obriširazred():
    schoolID = request.form['school_id']
    classroomID = request.form['classroom_id']

    classroom = Classroom.query.filter_by(id=classroomID, school_id=schoolID).first()

    db.session.delete(classroom)
    db.session.commit()

    return redirect("/skolamenu")

@views.route('/addad', methods=['POST','GET'])
def addad():
    schoolID = int(request.cookies.get('loggedSchool'))
    msg = request.form['content']
    name = request.form['name']

    obavijest = Obavjesti(school_id=schoolID, name=name, content=msg)

    db.session.add(obavijest)
    db.session.commit()
    
    return redirect("/skolamenu")

@views.route('/obrisiobavijest', methods=['POST'])
def obrisiobavijest():
    school_id = request.form.get('school_id') 
    obavijest_id = request.form.get('obavijest_id')  

    obavijest = Obavjesti.query.filter_by(school_id=school_id, id=obavijest_id).first()

    db.session.delete(obavijest)
    db.session.commit()

    return redirect("/skolamenu")

@views.route('/dodajraspored/', methods=['GET', 'POST'])
def dodajraspored():
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isLoggedIn')
    if request.method=='GET':
        classroom_id = request.args.get('classroom_id')
        raspored_sati = RasporedSati.query.filter_by(classroom_id=classroom_id).first()
        if raspored_sati:
            raspored_string = raspored_sati.raspored_string
        else:
            raspored_string = ","*45
        data = raspored_string.split(',')
        return render_template('templates-pc/dodaj-raspored.html', data=data, classroom_id=classroom_id, isLoggedIn=isLoggedIn, error=error)
    elif request.method == 'POST':
        data = []
        for i in range(9):
            for j in range(5):
                input_name = "predmet_" + str(i) + "_" + str(j)
                predmet_value = request.form.get(input_name)
                data.append(predmet_value)

        classroom_id = request.form['classroom_id']
        raspored_sati = RasporedSati.query.filter_by(classroom_id=classroom_id).first()

        if raspored_sati:
            existing_raspored_string = raspored_sati.raspored_string
        else:
            existing_raspored_string = ","*45
        existing_raspored_data = existing_raspored_string.split(',')

        new_data = []
        for i in range(len(data)):
            if data[i]!="" and data[i]!=existing_raspored_data[i]:
                new_data.append(data[i])
            else:
                new_data.append(existing_raspored_data[i])

        items_string = ','.join(new_data)
        new_raspored_sati = RasporedSati(classroom_id=classroom_id, raspored_string=items_string)

        existing_raspored_sati = RasporedSati.query.filter_by(classroom_id=classroom_id).first()
        if existing_raspored_sati:
            db.session.delete(existing_raspored_sati)

        db.session.add(new_raspored_sati)
        db.session.commit()

        return render_template('templates-pc/dodaj-raspored.html', data=new_data, classroom_id=classroom_id, isLoggedIn=isLoggedIn, error=error)


