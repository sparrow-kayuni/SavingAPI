from flask import Response, request, render_template, redirect
from flask_login import current_user, login_user, logout_user, login_required
from datetime import timedelta
from . import app, db
from .models import User, Account, Country


@app.route('/')
@app.route('/index')
def index():
    if(current_user.is_authenticated):
        return redirect('account')
    
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect('account')

    if request.method == 'POST':
        country_code = request.form.get('countryCode')
        msisdn = country_code + request.form.get('msisdn')
        password = request.form.get('password')

        user = User()

        if(not user.msisdn_exists(msisdn=msisdn)):
            return render_template('login.html', message='User MSISDN doesn\'t exist')
        
        user = User.query.filter_by(msisdn=msisdn).first()

        if(not user.check_password_hash(password)):
            return render_template('login.html', message='Incorrect password')
        
        login_user(user, duration=timedelta(minutes=10))

        return redirect('account')

    return render_template('login.html', message='')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()

    if(request.method == 'POST'):
        country_code = request.form.get('countryCode')
        country_name = request.form.get('country')
        msisdn = country_code + request.form.get('msisdn')
        username = ''.join(request.form.get('username').split(' '))
        password = request.form.get('password')

        user = User()

        if (user.msisdn_exists(msisdn)):
            return render_template('register.html', message='MSISDN already exists')
        
        if (user.username_exists(username)):
            return render_template('register.html', message='Username already taken')

        if request.form.get('accountType') == '1':
            account_type = 'Individual'
        elif request.form.get('accountType') == '2':
            account_type = 'Group'
        else:
            account_type = 'Individual'
        
        country = Country.query.filter_by(country_name=country_name).first()

        account = Account(account_type=account_type, country=country)

        db.session.add(account)

        user = User(username=username, msisdn=msisdn, account=account)
        
        user.set_password(password=password)

        db.session.add(user)

        db.session.commit()

        print(f'{user}\n{account}\n{country}')

        login_user(user, duration=timedelta(minutes=10))

        return redirect('account')
    
    return render_template('register.html', message='')


@app.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html')
