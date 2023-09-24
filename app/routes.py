from flask import Response, request, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from datetime import timedelta
from . import app, db
from .models import User, Account, Country
from .otp import OTPVerificationClient


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

        # send otp

        country = Country.query.filter_by(country_name=country_name).first()

        account = Account(account_type=account_type, country=country)

        db.session.add(account)

        user = User(username=username, msisdn=msisdn, account=account, verification_status='PENDING')
        
        user.set_password(password=password)

        db.session.add(user)

        db.session.commit()

        print(f'{user}\n{account}\n{country}')

        return redirect(url_for('verify_otp', id=user.user_id))
    
    return render_template('register.html', message='')


@app.route('/verify-otp-<int:id>', methods=['GET', 'POST'])
def verify_otp(id):

    user = User.query.get(id)

    if (request.method == 'POST'):

        phone = user.msisdn
        otp_code = request.form.get('otp')
        resend = request.form.get('resend')

        print(f'Phone: {phone}\n OTP: {otp_code}')

        client = OTPVerificationClient()

        if not (request.form.get('phone') == None or phone == '') or resend == 'true':
            
            print(f'Resend: {resend}')

            verification = client.send_otp(phone)
            
            print(f'Verification Status: {verification.status}')
            return render_template('verify_otp.html', user=user)

        if not (request.form.get('otp') == None or otp_code == ''):

            check = client.verify_otp(phone, otp_code)
            
            print(f'Check status: {check.status}')

            if (check.status == 'approved'):
                user.verification_status = 'VERIFIED'
                db.session.add(user)
                db.session.commit()
            
            if user.is_verified():
                login_user(user, duration=timedelta(minutes=10))
                return redirect('account')
            else:
                return render_template('verify_otp.html', user=user, message='Incorrect OTP. Try Again')

        
    return render_template('send_otp.html', user=user)




@app.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html')


@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    
    if request.method == 'POST':
        initial_payment = request.form.get('initialPayment')
        currency = request.form.get('currency')
        monthly_contribution = request.form.get('monthlyContribution')
        time_interval = request.form.get('timeInterval')

        # connect momo account & check balance

        # initiate transaction

        # validate transaction

        # add payment transaction to db

        print(f'{initial_payment}\n{currency}\n{monthly_contribution}\n{time_interval}')

        return redirect('account')

    return render_template('deposit.html')


@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    return render_template('withdraw.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')

