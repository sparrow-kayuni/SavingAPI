from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='static')
Bootstrap(app)

from app import routes