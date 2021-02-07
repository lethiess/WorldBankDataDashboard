from flask import Flask

app = Flask(__name__)

from worldbankapp import routes
from .data import return_figures