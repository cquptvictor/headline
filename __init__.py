from flask import Flask
import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_compress import Compress
app=Flask(__name__)
app.config.from_object(config)
mail=Mail(app)
login_manager=LoginManager(app)
db=SQLAlchemy(app)
Compress(app)