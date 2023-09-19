from flask import Response, request, render_template, redirect
from . import app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('account')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if(request.method == 'POST'):
        country_code = request.form.get('countryCode')
        country_name = request.form.get('country')
        phone_no = country_code + request.form.get('phone')
        password = request.form.get('password')

        return redirect('account')
    
    return render_template('register.html')

@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')
