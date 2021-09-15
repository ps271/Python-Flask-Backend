from flask import Flask, render_template, session, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_manager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import date, datetime
import math


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

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    staff = db.Column(db.Boolean, default=False)
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

class Careers(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(), nullable=True)
    date = db.Column(db.String(), nullable=True)
    def __str__(self):
        return 'Careers'
    



class Websites(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(), nullable=True)
    date = db.Column(db.String(), nullable=True)
    def __str__(self):
        return 'Websites'


class Apps(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(), nullable=True)
    date = db.Column(db.String(), nullable=True)
    def __str__(self):
        return 'Apps'







class Subscribers(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)




@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# dashboard starts

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    career = Careers.query.all()
    l1 = len(career)
    website = Websites.query.all()
    l2 = len(website)
    ap = Apps.query.all()
    l3 = len(ap)
    return render_template('dashboard.html',lc = l1, lw = l2, la = l3, params=params)

# career area start

@app.route('/dashboard/career', methods=['GET', 'POST'])
@login_required
def c_dash():
    careers = Careers.query.order_by(Careers.date.desc()).all()
    return render_template('car_dash.html', params=params, careers=careers)


@app.route('/edit/career/<string:sno>', methods=['GET', 'POST'])
@login_required
def c_edit(sno):
    if request.method == 'POST':
        box_title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        img_file = request.form.get('image')
        date = datetime.now()

        if sno=='0':
            post = Careers(title=box_title, slug=slug, content=content, img_url=img_file, date=date)
            db.session.add(post)
            db.session.commit()
        else:
            post = Careers.query.filter_by(sno=sno).first()
            post.title = box_title
            post.slug = slug
            post.content = content
            post.img_url = img_file
            post.date = date
            db.session.commit()
            return redirect('/edit/career/'+sno)
    career = Careers.query.filter_by(sno=sno).first()
    return render_template('edit.html', params = params, dash = 'c', career = career, sno = sno)

@app.route('/delete/career/<string:sno>', methods=['GET', 'POST'])
@login_required
def c_del(sno):
    career = Careers.query.filter_by(sno=sno).first()
    db.session.delete(career)
    db.session.commit()
    return redirect('/dashboard')

# website area start

@app.route('/dashboard/website', methods=['GET', 'POST'])
@login_required
def w_dash():
    websites = Websites.query.order_by(Websites.date.desc()).all()
    return render_template('web_dash.html', params=params, websites=websites)


@app.route('/edit/website/<string:sno>', methods=['GET', 'POST'])
@login_required
def w_edit(sno):
    if request.method == 'POST':
        box_title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        img_file = request.form.get('image')
        date = datetime.now()

        if sno=='0':
            post = Websites(title=box_title, slug=slug, content=content, img_url=img_file, date=date)
            db.session.add(post)
            db.session.commit()
        else:
            post = Websites.query.filter_by(sno=sno).first()
            post.title = box_title
            post.slug = slug
            post.content = content
            post.img_url = img_file
            post.date = date
            db.session.commit()
            return redirect('/edit/website/'+sno)
    website = Websites.query.filter_by(sno=sno).first()
    return render_template('edit.html', params = params, dash = 'w', website = website, sno = sno)



@app.route('/delete/website/<string:sno>', methods=['GET', 'POST'])
@login_required
def w_del(sno):
    post = Websites.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/dashboard')

# app area start

@app.route('/dashboard/app', methods=['GET', 'POST'])
@login_required
def a_dash():
    apps = Apps.query.order_by(Apps.date.desc()).all()
    return render_template('app_dash.html', params=params, apps=apps)



@app.route('/edit/app/<string:sno>', methods=['GET', 'POST'])
@login_required
def a_edit(sno):
    if request.method == 'POST':
        box_title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        img_file = request.form.get('image')
        date = datetime.now()

        if sno=='0':
            post = Apps(title=box_title, slug=slug, content=content, img_url=img_file, date=date)
            db.session.add(post)
            db.session.commit()
        else:
            post = Apps.query.filter_by(sno=sno).first()
            post.title = box_title
            post.slug = slug
            post.content = content
            post.img_url = img_file
            post.date = date
            db.session.commit()
            return redirect('/edit/website/'+sno)
    app = Apps.query.filter_by(sno=sno).first()
    return render_template('edit.html', params = params, dash = 'a', app = app, sno = sno)



@app.route('/delete/app/<string:sno>', methods=['GET', 'POST'])
@login_required
def a_del(sno):
    post = Apps.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/dashboard')


# dashboard ending




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('name')
        password = request.form.get('password')
        user = Users.query.filter_by(name = uname).first()
        if not user and not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect('/login')
        if user.staff:
            login_user(user)
            return redirect('/dashboard')
        login_user(user)
        flash('Logged In Successfully')
        return redirect('/')
    return render_template('login.html', params = params)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



@app.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if (request.method == 'POST'):
        uname = request.form.get('name')
        email = request.form.get('email')
        pas = request.form.get('password')
        encr_pass = generate_password_hash(pas)
        user = Users.query.filter_by(name=uname).first()
        if user:
            flash('User already exists.')
            return redirect('/sign-up')
        entry = Users(name = uname, email = email, active = False, password = encr_pass, staff = False, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html', params=params)




@app.route('/')
def hello_world():
    careers = Careers.query.filter_by().all()[0:params['nav_posts']]
    websites = Websites.query.filter_by().all()[0:params['nav_posts']]
    return render_template('index.html', params=params, careers=careers, websites=websites)


@app.route('/Career-Path')
def careers():
    q = request.args.get('q')
    if q:
        careers = Careers.query.filter(Careers.title.contains(q))
        Careers.content.contains(q)
    else:
        careers = Careers.query.order_by(Careers.date.desc())
    
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    pages = careers.paginate(page=page, per_page=2)
    return render_template('Careers.html', params=params, careers=careers, pages = pages)

@app.route('/Career-Path/<string:career_slug>', methods=['GET', 'POST'])
def career_route(career_slug):                
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        reply = request.form.get('reply')
        entry = Comments(msg = message, name = name, email = email, rep_to = reply, aso_slug = (Careers.query.filter_by(slug=career_slug).first()).slug, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
    comments = Comments.query.filter_by(aso_slug=career_slug).all()
    career = Careers.query.filter_by(slug=career_slug).first()  
    return render_template('career.html', params=params, career=career, comments=comments)




@app.route('/Websites')
def websites():
    q = request.args.get('q')
    if q:
        websites = Websites.query.filter(Websites.title.contains(q))
        Websites.content.contains(q)
    else:
        websites = Websites.query.order_by(Websites.date.desc())
    
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    pages = websites.paginate(page=page, per_page=2)
    return render_template('Websites.html', params=params, websites=websites, pages = pages, dash = False)

@app.route('/Websites/<string:website_slug>', methods=['GET', 'POST'])
def website_route(website_slug):                
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        reply = request.form.get('reply')
        entry = Comments(msg = message, name = name, email = email, rep_to = reply, aso_slug = (Websites.query.filter_by(slug=website_slug).first()).slug, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
    comments = Comments.query.filter_by(aso_slug=website_slug).all()
    website = Websites.query.filter_by(slug=website_slug).first()  
    return render_template('website.html', params=params, website=website, comments=comments)




@app.route('/Apps')
def apps():
    q = request.args.get('q')
    if q:
        apps = Apps.query.filter(Apps.title.contains(q))
        Apps.content.contains(q)
    else:
        apps = Apps.query.order_by(Apps.date.desc())
    
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    pages = apps.paginate(page=page, per_page=2)
    return render_template('Apps.html', params=params, apps=apps, pages = pages, dash = False)

@app.route('/Apps/<string:app_slug>', methods=['GET', 'POST'])
def app_route(app_slug):                
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        reply = request.form.get('reply')
        entry = Comments(msg = message, name = name, email = email, rep_to = reply, aso_slug = (Apps.query.filter_by(slug=app_slug).first()).slug, date = datetime.now())
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


@app.route('/subscribe', methods = ['GET', 'POST'])
def subscribe():
    if (request.method == 'POST'):
        email = request.form.get('email')
        entry = Subscribers(email = email)
        db.session.add(entry)
        db.session.commit()
    return redirect('/')


@app.route('/About')
def about():
    return render_template('About.html', params=params)


@app.route('/TOU')     # terms of use
def tou():
    return render_template('Terms.html', params=params)


@app.route('/privacy-policy')
def pri_poli():
    return render_template('privacy.html', params=params)




