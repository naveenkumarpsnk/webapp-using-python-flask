from http import server
from lib2to3.pgen2 import driver
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import pydoc
import urllib


app = Flask(__name__)
#params = urllib.parse.quote_plus(
#    'Driver=%s;' % 'ODBC Driver 17 for SQL Server' +    
#    'Server=tcp:%s,1433;' % 'naveenlogistics.database.windows.net' +
#    'Database=%s;' % 'naveenlogistics' +
#    'Uid=%s;' % 'sqluseradmin' +
#    'Pwd={%s};' % 'naveen@PS2000' +
#    'Encrypt=yes;' +
#    'TrustServerCertificate=no;' +
#    'Connection Timeout=30;')
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///database.db" # "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from management import routes