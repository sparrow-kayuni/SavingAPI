from flask import Flask, request

ussd = Flask(__name__)

from ussd import routes
