#dodavanje razreda u html
#loggedInSkola, isSkolaLoggedin, isUserLoggedin, loggedInSchoolID

from flask import Blueprint, render_template, Flask, request, redirect, make_response, url_for, jsonify
from .models import User, School, Classroom, Zamjene, Obavjesti, RasporedSati, RasporedUcionica
from . import db
import time
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime

views = Blueprint('views', __name__)

#prikazi stranica

#home page stranice
@views.route('/')
def home():
    userDevice = request.headers.get('User-Agent')
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')

    sveObavijesti=[]

    if isSkolaLoggedIn=="True":
        loggedInSkolaID = int(request.cookies.get('loggedInSchoolID'))
        sveObavijesti = Obavjesti.query.filter_by(school_id=loggedInSkolaID).all()
        sveObavijesti = sveObavijesti[::-1]

    if 'Mobile' in userDevice:
        return render_template("templates-mobile/home_mobile.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, isLoggedIn=isUserLoggedIn, sve_obavijesti=sveObavijesti)
    elif 'Windows' in userDevice:
        return render_template("templates-pc/home.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, isLoggedIn=isUserLoggedIn, sve_obavijesti=sveObavijesti)
    else:
        return render_template("templates-pc/home.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, isLoggedIn=isUserLoggedIn, sve_obavijesti=sveObavijesti)

#prikaz login page stranice
@views.route('/login')
def login():
    error=request.args.get("error")
    userDevice = request.headers.get('User-Agent')
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')

    if 'Mobile' in userDevice:
        return render_template("templates-mobile/login_mobile.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    elif 'Windows' in userDevice:
        return render_template("templates-pc/login.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    else:
        return render_template("templates-pc/login.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)

#prikaz login page za admine stranice
@views.route('/loginadmin')
def loginAdmin():
    error=request.args.get("error")
    userDevice = request.headers.get('User-Agent')
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')

    if 'Mobile' in userDevice:
        return render_template("templates-pc/login-admin.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    elif 'Windows' in userDevice:
        return render_template("templates-pc/login-admin.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    else:
        return render_template("templates-pc/login-admin.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)

#prikaz login page za admine stranice
@views.route('/loginskola')
def loginskola():
    error=request.args.get("error")
    userDevice = request.headers.get('User-Agent')
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')

    if 'Mobile' in userDevice:
        return render_template("templates-pc/login-skola.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    elif 'Windows' in userDevice:
        return render_template("templates-pc/login-skola.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    else:
        return render_template("templates-pc/login-skola.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)

#prikaz register page stranice
@views.route('/register')
def register():
    error=request.args.get("error")
    userDevice = request.headers.get('User-Agent')
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')

    if 'Mobile' in userDevice:
        return render_template("templates-mobile/register_mobile.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    elif 'Windows' in userDevice:
        return render_template("templates-pc/register.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    else:
        return render_template("templates-pc/register.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)

#prikaz menu-a za dodavanje skola
@views.route('/add-school-menu', methods=['GET', 'POST'])
def addschoolmenu():
    error=request.args.get("error")
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')
    if isAdminLoggedIn:
        return render_template("templates-pc/add-school-menu.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, error=error, isLoggedIn=isUserLoggedIn)
    else:
        return redirect("/")

#prikaz menu za administraciju skole
@views.route('/skolamenu', methods=['GET'])
def skolamenu():
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')
    loggedInSkolaID = int(request.cookies.get('loggedInSchoolID'))
    loggedInSkola = School.query.filter_by(id=loggedInSkolaID).first()

    obavijesti = Obavjesti.query.filter_by(school_id=loggedInSkolaID).all()
    obavijesti = obavijesti[::-1]
    if isUserLoggedIn and isSkolaLoggedIn:
        classrooms = Classroom.query.filter_by(school_id=loggedInSkolaID).all()
        return render_template("templates-pc/skola-menu.html", admin=isAdminLoggedIn, Skola=isSkolaLoggedIn, skola=loggedInSkola, isLoggedIn=isUserLoggedIn, classrooms=classrooms, obavijesti=obavijesti)
    else:
        return redirect("/")

#prikaz profila ucenika
@views.route('/viewprofileuser', methods=['GET'])
def viewprofileuser():
    isSkolaLoggedIn=request.args.get("skola")
    loggedInUser = User.query.filter_by(id=int(request.cookies.get('loggedInUser'))).first()
    isUserLoggedIn=request.args.get("isLoggedIn")
    isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')

    return render_template("templates-pc/profile.html", admin=isAdminLoggedIn, skola=isSkolaLoggedIn, user=loggedInUser, isLoggedIn=isUserLoggedIn)

#logika za registriranje novog racuna i dodavanje tog racuna u databazu
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

        #provjera emaila
        if len(email)>5 and "@" in email and "." in email:
            pass
        else:
            error="Nevaljani email."
            return redirect(url_for("views.register", error=error))

        #provjera lozinke
        hasGotLetter = any(char.isalpha() for char in password)
        hasGotNumber = any(char.isdigit() for char in password)
        if len(password)>=8:
            if hasGotLetter and hasGotNumber:
                pass
            else:
                error="Loznika mora sadržavati i brojeve i slova."
                return redirect(url_for("views.register", error=error))
        else:
            error="Lozinka mora sadržavati barem 8 znakova."
            return redirect(url_for("views.register", error=error))

        #provjera ID-a skole
        if len(schoolID)!=0:
            try:
                int(schoolID)
                pass
            except ValueError:
                error="Nevaljan ID Škole."
                return redirect(url_for("views.register", error=error))

        #provjera ID-a ucionice
        if len(classID)!=0:
            try:
                int(classID)
                pass
            except ValueError:
                error="Nevaljan ID učionice."
                return redirect(url_for("views.register", error=error))


        #provjera postoji li račun s tim emailom
        user = User.query.filter_by(email=email).first()
        if user:
            error="Korisnik s tim emailom već postoji."
            return redirect(url_for("views.register", error=error))
        else:
            newUser = User(name = name, lastname=surname, email=email, password=password, school_id=schoolID, classroom_id=classID)
            db.session.add(newUser)
            db.session.commit()

            #login novog usera
            user = User.query.filter_by(email=email).first()
            response = make_response(redirect("/"))
            response.set_cookie('isUserLoggedIn', value="True")
            response.set_cookie('loggedInUser', value=str(user.id))
            return response

#logika za ulogiravanje korisnika
@views.route('/loginsend', methods=['POST'])
def loginsend():
    error=""

    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if user.password==password:
            response = make_response(redirect("/"))
            response.set_cookie('isUserLoggedIn', value="True")
            response.set_cookie('loggedInUser', value=str(user.id))
            return response
        else:
            error="Kriva lozinka."
            response = make_response(redirect(url_for("views.login", error=error)))
            response.set_cookie('isUserLoggedIn', value="False")
            return response
    else:
        error="Krivi email."
        response = make_response(redirect(url_for("views.login", error=error)))
        response.set_cookie('isUserLoggedIn', value="False")
        return response

#logika za ulogiravanje admina
@views.route('/loginadminsend', methods=['POST'])
def loginadminsend():
    error=""
    password = request.form['password']
    if password=="lozinka":   ##promjenit!!
        response = make_response(redirect("/adminmenu"))
        response.set_cookie('isAdminLoggedIn', value="True")
        return response
    else:
        error="Kriva lozinka."
        response = make_response(redirect(url_for("views.loginadmin", error=error)))
        return response

#logika za ulogiravanje administracije skola
@views.route('/loginskolasend', methods=['GET', 'POST'])
def loginskolasend():
    error=""
    id = request.form['id']
    school = School.query.filter_by(id=id).first()
    if school:
        instertedpassword = request.form['password']
        password=school.login_password
        if instertedpassword==password:
            response = make_response(redirect("/skolamenu"))
            response.set_cookie('isUserLoggedIn', value="True")
            response.set_cookie('isSkolaLoggedIn', value="True")
            response.set_cookie('loggedInSchoolID', value=str(school.id))
            return response
        else:
            error="Kriva lozinka."
            response = make_response(redirect(url_for("views.loginskola", error=error)))
            response.set_cookie('isUserLoggedIn', value="False")
            return response
    else:
        error="Škola s tim ID-em ne postoji."
        response = make_response(redirect(url_for("views.loginskola", error=error)))
        response.set_cookie('isUserLoggedIn', value="False")
        return response

#logika za izlogiravanje
@views.route('/logout')
def logout():
    response = make_response(redirect("/"))
    cookies_to_delete = request.cookies.keys()
    for cookie_name in cookies_to_delete:
        response.delete_cookie(cookie_name)
    return response

#logika za dodavanje novog razreda
@views.route('/dodajrazred')
def dodajrazred():
    classroom_name = request.form.get('classroom_name')
    loggedInSkolaID = request.cookies.get('loggedInSkolaID')
    db.session.add(Classroom(name=classroom_name, school_id=loggedInSkolaID))
    db.session.commit()
    return redirect(url_for("views.skolamenu"))

#logika za prikaz profila
@views.route('/viewprofile')
def viewprofile():
    isSkolaLoggedIn = request.cookies.get('isSkolaLoggedIn')
    isUserLoggedIn = request.cookies.get('isUserLoggedIn')
    if isSkolaLoggedIn=="True":
        return redirect("/skolamenu")
    else:
        return redirect(url_for("views.viewprofileuser", skola=isSkolaLoggedIn, isLoggedIn=isUserLoggedIn))

@views.route('/addschool', methods=['GET', 'POST'])
def addschool():
    isLoggedIn = request.cookies.get('isUserLoggedIn')
    if request.method=="GET":
        error=request.args.get("error")
        user_agent = request.headers.get('User-Agent')
        isAdminLoggedIn = request.cookies.get('isAdminLoggedIn')
        skola = request.cookies.get('isSkolaLoggedIn')
        if 'Mobile' in user_agent:
            return render_template("templates-pc/add-school-login.html", admin=isAdminLoggedIn, skola=skola, error=error, isLoggedIn=isLoggedIn)
        elif 'Windows' in user_agent:
            return render_template("templates-pc/add-school-login.html",admin=isAdminLoggedIn, skola=skola, error=error, isLoggedIn=isLoggedIn)
        else:
            return render_template("templates-pc/add-school-login.html",admin=isAdminLoggedIn, skola=skola, error=error, isLoggedIn=isLoggedIn)
    elif request.method=="POST":
        password = request.form['password']

        if password=="lozinka":
            response = make_response(redirect("/add-school-menu"))
            response.set_cookie('isUserLoggedIn', value="True")
            response.set_cookie('isAdminLoggedIn', value="True")
            return response
        else:
            error="Kriva lozinka."
            response = make_response(redirect(url_for("views.addschool", error=error)))
            response.set_cookie('isUserLoggedIn', value="True")
            response.set_cookie('isAdminLoggedIn', value="False")
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
            response.set_cookie('isUserLoggedIn', value="True")
            response.set_cookie('loggedInSchoolID', value=str(school.id))
            return response

@views.route('/prikazizamjene', methods=['GET', 'POST'])
def prikazizamjene():
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isUserLoggedIn')
    skola = request.cookies.get('isSkolaLoggedIn')

    if request.method=="POST":
        schoolID = request.form['school_id']
        classroomID = request.form['classroom_id']
    else:
        schoolID = request.args.get("schoolid")
        classroomID = request.args.get("classroomid")
    classroom = Classroom.query.filter_by(id=classroomID, school_id=schoolID).first()

    zamjene = Zamjene.query.filter_by(classroom_id=classroomID).all()

    return render_template("templates-pc/prikaz-zamjena.html", skola=skola, error=error, isLoggedIn=isLoggedIn, sve_zamjene=zamjene, razred=classroom, classroomid=classroomID, schoolid=schoolID)

@views.route('/dodajzamjenu', methods=['GET', 'POST'])
def dodajzamjenu():
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isLoggedIn')

    schoolID = request.form['school_id']
    classroomID = request.form['classroom_id']
    classroom = Classroom.query.filter_by(id=classroomID, school_id=schoolID).first()

    if request.method=="POST":
        od = request.form['from']
        do = request.form['to']
        datum = request.form['date']
        zamjena = request.form['zamjena']

        datum = datetime.strptime(datum, '%Y-%m-%d').date()

        nova_zamjena = Zamjene(od=od, do=do, datum=datum, zamjena=zamjena, classroom_id=classroomID)
        db.session.add(nova_zamjena)
        db.session.commit()

        zamjene = Zamjene.query.filter_by(classroom_id=classroomID).all()

    return redirect(url_for("views.prikazizamjene", error=error, isLoggedIn=isLoggedIn, sve_zamjene=zamjene, razred=classroom, classroomid=classroomID, schoolid=schoolID))

@views.route('/delete_zamjene/<int:zamjene_id>', methods=['POST'])
def delete_zamjene(zamjene_id):
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isUserLoggedIn')

    zamjene = Zamjene.query.get(zamjene_id)

    db.session.delete(zamjene)
    db.session.commit()

    schoolID = request.form['school_id']
    classroomID = request.form['classroom_id']
    classroom = Classroom.query.filter_by(id=classroomID, school_id=schoolID).first()
    zamjene = Zamjene.query.filter_by(classroom_id=classroomID).all()

    return redirect(url_for("views.prikazizamjene", error=error, isLoggedIn=isLoggedIn, sve_zamjene=zamjene, razred=classroom, classroomid=classroomID, schoolid=schoolID))

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
    schoolID = int(request.cookies.get('loggedInSchoolID'))
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
    isLoggedIn = request.cookies.get('isUserLoggedIn')
    skola = request.cookies.get('isSkolaLoggedIn')
    if request.method=='GET':
        classroom_id = request.args.get('classroom_id')
        raspored_sati = RasporedSati.query.filter_by(classroom_id=classroom_id).first()
        if raspored_sati:
            raspored_string = raspored_sati.raspored_string
        else:
            raspored_string = ","*45
        data = raspored_string.split(',')
        return render_template('templates-pc/dodaj-raspored.html', skola=skola, data=data, classroom_id=classroom_id, isLoggedIn=isLoggedIn, error=error)
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
            if data[i]=="x" or data[i]=="X":
                new_data.append("")
            elif data[i]!="" and data[i]!=existing_raspored_data[i]:
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

        return render_template('templates-pc/dodaj-raspored.html', skola=skola, data=new_data, classroom_id=classroom_id, isLoggedIn=isLoggedIn, error=error)


@views.route('/update_table/', methods=['GET', 'POST'])
def update_table():
    error=request.args.get("error")
    isLoggedIn = request.cookies.get('isUserLoggedIn')
    skola = request.cookies.get('isSkolaLoggedIn')
    if request.method=='GET':
        school_id = request.args.get('school_id')
        raspored = RasporedUcionica.query.filter_by(school_id=school_id).first()
        if raspored:
            raspored_string = raspored.raspored_string
        else:
            raspored_string = ","*1125
        data = raspored_string.split(',')


        return render_template('templates-pc/rasporeducionica.html', skola=skola, data=data, school_id=school_id, isLoggedIn=isLoggedIn, error=error)

    elif request.method == 'POST':
        data = []
        for i in range(25):
            for j in range(45):
                input_name = "razred_" + str(i) + "_" + str(j)
                razred_value = request.form.get(input_name)
                if razred_value!=None:
                    data.append(razred_value)
        school_id = request.form['school_id']
        raspored = RasporedUcionica.query.filter_by(school_id=school_id).first()

        if raspored:
            existing_raspored_string = raspored.raspored_string
        else:
            existing_raspored_string = ","*1125
        existing_raspored_data = existing_raspored_string.split(',')

        new_data = []
        for i in range(len(data)):
            if data[i]=="x" or data[i]=="X":
                new_data.append("")
            elif data[i]!="" and data[i]!=existing_raspored_data[i]:
                new_data.append(data[i])
            else:
                new_data.append(existing_raspored_data[i])

        items_string = ','.join(new_data)
        new_raspored = RasporedUcionica(raspored_string=items_string, school_id=school_id)

        existing_raspored = RasporedUcionica.query.filter_by(school_id=school_id).first()
        if existing_raspored:
            db.session.delete(existing_raspored)

        db.session.add(new_raspored)
        db.session.commit()

        return render_template('templates-pc/rasporeducionica.html', skola=skola, school_id=school_id, data=new_data, isLoggedIn=isLoggedIn, error=error)
