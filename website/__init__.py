from flask import Flask
from os import path
from flask_mail import Mail
import locale
from datetime import datetime
from .models import db
from .models import Classroom

mail = Mail()
DB_NAME = 'database.db'
locale.setlocale(locale.LC_TIME, 'hr_HR.UTF-8')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'diwadhuawidhaa'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'zamjenehr@gmail.com'
    app.config['MAIL_PASSWORD'] = 'npqr xggb wcss qzsc' #zamjenehrlozinka
    app.config['MAIL_DEFAULT_SENDER'] = 'zamjenehr@gmail.com'

    mail.init_app(app)
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    create_db(app)

    @app.template_filter('split')
    def split_filter(value, delimiter='|'):
        return value.split(delimiter)
    
    @app.template_filter('dan')
    def dan_filter(value):
        date = datetime.strptime(value, '%Y-%m-%d')
        day_of_week = date.weekday()
        day_names = {0: 'Ponedjeljak', 1: 'Utorak', 2: 'Srijeda', 3: 'Četvrtak', 4: 'Petak', 5: 'Subota', 6: 'Nedjelja'}
        return day_names[day_of_week]
    
    @app.template_filter('razred')
    def razred_filter(value):
        classroom = Classroom.query.get(value)
        return classroom.name

    return app

def create_db(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        
