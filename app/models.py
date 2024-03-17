from app import db, login
from flask_login import UserMixin
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash

# Definition der Benutzerklasse
class Benutzer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Benutzername = db.Column(db.String(11), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))

    # Rückgabeformat
    def __repr__(self):
        return '<Benutzer {}>'.format(self.Benutzername)

    # Methode zum Setzen des Passworts
    def set_password(self, Passwort):
        self.password_hash = generate_password_hash(Passwort)

    # Methode zur Überprüfung des Passworts
    def check_password(self, Passwort):
        return check_password_hash(self.password_hash, Passwort)
    
    # Definieren der Beziehung zu den Notizen
    notizen = db.relationship('Notizen', back_populates='user', lazy='dynamic')

# Laden des Benutzers für Flask-Login    
@login.user_loader
def load_user(id):
    return Benutzer.query.get(int(id))

# Definition der Notizenklasse
class Notizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Titel = db.Column(db.String(255))
    Inhalt = db.Column(db.String(255))
    Erstellungsdatum = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('benutzer.id'))
    user = db.relationship('Benutzer', back_populates='notizen')
    favorit = db.Column(db.Boolean, default=False)

    # Rückgabeformat
    def __repr__(self):
        return '<Notizen {}>'.format(self.Inhalt)

# Definition der Favoriten Klasse
class Favoriten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NoteID = db.Column(db.Integer, db.ForeignKey('notizen.id'))
    UserID = db.Column(db.Integer, db.ForeignKey('benutzer.id'))