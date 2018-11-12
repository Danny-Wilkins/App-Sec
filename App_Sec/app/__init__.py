from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_talisman import Talisman, GOOGLE_CSP_POLICY

app = Flask(__name__)
talisman = Talisman(app, content_security_policy=GOOGLE_CSP_POLICY) #This seems to still be a little too restrictive
login = LoginManager(app)
login.session_protection = "strong"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models