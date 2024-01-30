from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail

db=SQLAlchemy()
mail = Mail()
DB_NAME = 'database.db'

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

    return app

def create_db(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        
