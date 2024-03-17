from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Benutzer
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

# Definition der Flask Form-Klasse für das Anmeldeformular
class LoginForm(FlaskForm):
    Benutzername = StringField('Benutzername', validators=[DataRequired()])
    Passwort = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Anmeldedaten speichern?')
    submit = SubmitField('Anmelden')

# Definition der Flask Form-Klasse für das Registrierungsformular
class RegistrationForm(FlaskForm):
    Benutzername = StringField('Benutername', validators=[DataRequired()])
    email = StringField('EMail', validators=[DataRequired(), Email()])
    Passwort = PasswordField('Passwort', validators=[DataRequired()])
    Passwort2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('Passwort')])
    submit = SubmitField('Register')

    # Validierungsfunktion für den Benutzernamen
    def validate_Benutzername(self, Benutzername):
        benutzer = Benutzer.query.filter_by(Benutzername=Benutzername.data).first()
        if benutzer is not None:
            raise ValidationError('Bitte einen anderen Benutzernamen wählen')
    
    # Validierungsfunktion für die Mail-Adresse
    def validate_email(self, email):
        benutzer = Benutzer.query.filter_by(email=email.data).first()
        if benutzer is not None:
            raise ValidationError('Bitte eine andre E-Mail Adresse eingeben')

# Definition der Flask Form-Klasse für das Notizformular
class NotizForm(FlaskForm):
    notiz = StringField('Notiz', validators=[DataRequired()])
    submit = SubmitField('Senden')

# Definition der Flas Form-Klasse für das Formular zum Zurücksetzen des Passworts
class ResetPasswordForm(FlaskForm):
    Passwort = PasswordField('Passwort', validators=[DataRequired()])
    Passwort2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('Passwort')])
    submit = SubmitField('Passwort zurücksetzen')