from flask import Flask, escape, request, render_template, url_for, redirect,session,redirect, url_for, flash
from yelp import yelp_scrapper
from tripadvisor import tripadvisor_scrapper
from zomato import zomato_scrapper
from my_google import google_scrapper
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
import os
import time
from flask_login import LoginManager,login_user, logout_user, current_user,login_required
from flask_session import Session
from passlib.hash import pbkdf2_sha256
from forms import RegistrationForm,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from models import db
from flask_bootstrap import Bootstrap

# from .auth import bp as auth_bp

app = Flask(__name__,template_folder='templates', static_folder='static',)

POSTGRES = {
    'user': 'myuser',
    'pw': '12345',
    'db': 'flaskdb',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)
bootstrap = Bootstrap(app)
sSESSION_TYPE='redis'
PERMANENT_SESSION_LIFETIME=1800

app.config.update(
SECRET_KEY=os.urandom(24)
)

# Initialize login manager
login_manage = LoginManager(app)
login_manage.init_app(app)

@login_manage.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@login_manage.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/')
        flash('Username or password is incorrect !')
    return render_template('login.html', form=form)

@app.route("/logout", methods=['GET'])
def logout():
    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template("home.html")


@app.route('/process', methods=["POST"])
# @login_required
def hello():
    if request.method == "POST":
        if request.form["submit_button"] == 'yelp':
            result = request.form["yelp-search"]
            session['yelp-search'] = result
            yelp_scrapper(result)
            file="yelp_csv"
        elif request.form["submit_button"] == 'google':
            result = request.form["google-search"]
            session['google-search'] = result
            google_scrapper(result)
            file="google_map_csv"
        elif request.form["submit_button"] == 'tripadvisor':
            result = request.form["tripadvisor-search"]
            session['tripadvisor-search'] = result
            tripadvisor_scrapper(result)
            file="trip_advisor_csv"
        elif request.form["submit_button"] == 'zomato':
            result = request.form["zomato-search"]
            session['zomato-search'] = result
            print(" session['zomato-search']", session['zomato-search'],'====Reult===',result)
            zomato_scrapper(result)
            file="zomato_csv"
            path = result +".csv"
            if os.path.exists(path):
                return redirect(url_for('success',download=file))
            else:
                flash(' Please enter a valid url !')
                return redirect("/")
        return redirect(url_for('success',download=file))
        
@app.route('/success')
@login_required
def success():
    return render_template('download.html',download = request.args.get('download') )


@app.route('/google_map_csv/')  
def download():
    if 'google-search' in session:
        google_search = session['google-search']
        path = google_search +".csv"
        return send_file(path, as_attachment=True)

@app.route('/yelp_csv/')  
def download_yelp():
    if 'yelp-search' in session:
        yelp_search = session['yelp-search']
        path = yelp_search +".csv"
        return send_file(path, as_attachment=True)

@app.route('/trip_advisor_csv/')  
def download_trip_advisor():
    if 'tripadvisor-search' in session:
        tripadvisor_search = session['tripadvisor-search']
        path = tripadvisor_search +".csv"
        return send_file(path, as_attachment=True)

@app.route('/zomato_csv/')  
def download_zomato():
    if 'zomato-search' in session:
        zomato_search = session['zomato-search']
        print("zomato_search",zomato_search)
        path = zomato_search +".csv"
        print("path",path)
        return send_file(path, as_attachment=True)


if __name__ == '__main__':
    Session(app)
    app.debug = True
    app.run(debug=True)
