from flask import Flask, render_template, session, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]



local_server = "True"
app = Flask(__name__)




if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'sfhuewihf2@33r7h'


class Users(db.Model, UserMixin):

    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), unique=False, nullable=False)
    active = db.Column(db.Boolean, default=False)
    date = db.Column(db.String(), nullable=True)


class Contact(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(15), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    ph_no = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(), nullable=True)


class Comments(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    rep_to = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(), nullable=True)
    aso_slug = db.Column(db.String(50), nullable=True)


    



class Websites(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(), nullable=True)
    date = db.Column(db.String(), nullable=True)


class Apps(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(), nullable=True)
    date = db.Column(db.String(), nullable=True)




@app.route('/login', methods=['GET', 'POST'])
def login():
    uname = request.form.get('name')
    password = request.form.get('password')
    user = Users.query.filter_by(name=uname).first()
    if ('user' in session and session['user'] == user):
        return redirect('/Apps')
    elif (request.method == 'POST'):
        if user:
            if check_password_hash(user.password_hash, password):
                session['user'] = user
                return redirect('/Apps')
        else:
            flask.flash('Invalid username or password')
    return render_template('login.html', params=params)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')



@app.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if (request.method == 'POST'):
        uname = request.form.get('name')
        email = request.form.get('email')
        pas = request.form.get('password')
        encr_pass = generate_password_hash(pas)
        entry = Users(name = uname, email = email, active = False, password_hash = encr_pass, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html', params=params)




@app.route('/')
def hello_world():
    websites = Websites.query.filter_by().all()[0:params['nav_posts']]
    return render_template('index.html', params=params, websites=websites)




@app.route('/Websites')
def websites():
    websites = Websites.query.filter_by().all()[0:params['nav_posts']]
    return render_template('Websites.html', params=params, websites=websites)

@app.route('/Websites/<string:website_slug>', methods=['GET', 'POST'])
def website_route(website_slug):
    rep = {'key':''}
    def web(cname):
        comments = Comments.query.filter_by(aso_slug=website_slug).all()
        for comment in comments:
            if comment.name == cname:
                reply = comment.name
                rep['key'] = 'reply'
                return
                
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Comments(msg = message, name = name, email = email, rep_to = rep['key'], aso_slug = (Websites.query.filter_by(slug=website_slug).first()).slug, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
    comments = Comments.query.filter_by(aso_slug=website_slug).all()
    website = Websites.query.filter_by(slug=website_slug).first()  
    return render_template('website.html', params=params, website=website, comments=comments)




@app.route('/Apps')
def apps():
    apps = Apps.query.filter_by().all()
    apps.reverse()
    apps[0:params['nav_posts']]
    return render_template('Apps.html', params=params, apps=apps)

@app.route('/Apps/<string:app_slug>', methods=['GET', 'POST'])
def app_route(app_slug):
    rep = {'key':''}
    def ap(cname):
        comments = Comments.query.filter_by(aso_slug=app_slug).all()
        for comment in comments:
            if comment.name == cname:
                reply = comment.name
                rep['key'] = 'reply'
                return
                
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Comments(msg = message, name = name, email = email, rep_to = rep['key'], aso_slug = (Apps.query.filter_by(slug=app_slug).first()).slug, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
    comments = Comments.query.filter_by(aso_slug=app_slug).all()
    app = Apps.query.filter_by(slug=app_slug).first()  
    return render_template('app.html', params=params, app=app, comments=comments)




@app.route('/Contacts', methods = ['GET', 'POST'])
def contacts():
    if (request.method == 'POST'):
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('tel')
        message = request.form.get('message')
        entry = Contact(f_name = fname, l_name = lname, email = email, ph_no = phone, msg = message, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        
    return render_template('Contacts.html', params=params)




