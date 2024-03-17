from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# Erstellen einer SQLAlchemy-Datenbankinstanz
db = SQLAlchemy(app)
# Erstellen einer Migrate-Instanz für die Datenbankmigration
migrate = Migrate(app, db)

# Erstellen des Loginmanagers für die Benutzerauthentifizierung
login = LoginManager(app)
# Festlegen der Login-Route für den Loginmanager
login.login_view = 'login'

# Import der Routen und Fehler
from app import routes, models, errors