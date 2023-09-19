from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    msisdn = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))
    
    def get_id(self):
        return self.user_id
    
    
    def __repr__(self):
        return f'User<{self.username}, {self.msisdn}>'
    

    def msisdn_exists(self, msisdn):
        if (User.query.filter_by(msisdn=msisdn).first() != None):
            return True
        
        return False
    
    def username_exists(self, username):      
        if (User.query.filter_by(username=username).first() != None):
            return True
        
        return False
    

    def set_password(self, password):
        self.password = generate_password_hash(password)
    

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, default=0)
    members = db.relationship('User', backref='account', lazy='dynamic')
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))


    def __repr__(self):
        return f'Account<{self.account_type}, {self.balance}>, {self.members}'
    

class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(40), nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    # currency = db.Column(db.String(5))
    accounts = db.relationship('Account', backref='country', lazy='dynamic')

    def __repr__(self):
        return f'Country<{self.country_name}, {self.country_code}>'
    