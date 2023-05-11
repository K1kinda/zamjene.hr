from flask import Blueprint, render_template, Flask, request, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user_agent = request.headers.get('User-Agent')
    if 'Mobile' in user_agent:
        return render_template("home_mobile.html")
    elif 'Windows' in user_agent:
        return render_template("home.html")
    else:
        return render_template("home.html")