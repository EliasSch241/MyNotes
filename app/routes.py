from flask import render_template, flash, redirect, url_for, request, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from app import app, db
from app.forms import LoginForm, RegistrationForm, NotizForm
from app.models import Benutzer, Notizen

# Index-Seite
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = NotizForm()
    if form.validate_on_submit():
        notiz = Notizen(Inhalt=form.notiz.data, user=current_user)
        db.session.add(notiz)
        db.session.commit()
        flash('Deine Notiz wurde angelegt')
        return redirect(url_for('index'))

    # Holen aller Notizen des aktuellen Benutzers und sortieren Sie sie nach dem Erstellungsdatum
    alle_notizen = current_user.notizen.order_by(Notizen.Erstellungsdatum.desc()).all()

    # Trennen der Favoriten von den anderen Notizen
    favoriten = [notiz for notiz in alle_notizen if notiz.favorit]
    andere_notizen = [notiz for notiz in alle_notizen if notiz not in favoriten]

    return render_template("index.html", title="Hauptseite", form=form, favoriten=favoriten, andere_notizen=andere_notizen)


# Anmeldung
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Route /login wurde mit POST betreten. Prüfung, ob alles o.k ist:
        benutzer = Benutzer.query.filter_by(Benutzername=form.Benutzername.data).first()
        if benutzer is None or not benutzer.check_password(form.Passwort.data):
            flash('fehlerhafter Benutzer oder Passwort.')
            return redirect(url_for('login'))
        # Alles o.k., Login kann erfolgen
        login_user(benutzer, remember=form.remember_me.data)
        return redirect(url_for('index'))
    #Route /login wurde mit GET betreten
    return render_template('login.html', title='Anmeldung', form=form)

# Abmeldung
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Registrierung
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Route /register wurde mit POST betreten. Prüfung, ob alles in Ordnung ist:
        benutzer = Benutzer(Benutzername=form.Benutzername.data, email=form.email.data)
        benutzer.set_password(form.Passwort.data)
        db.session.add(benutzer)
        db.session.commit()
        flash('Gratulation deine Registrierung ist abgeschlossen!')
        return redirect(url_for('login'))
    # Route /register wurde mit GET betreten
    return render_template('register.html', title='Registrierung', form=form)

#Benutzerprofil
@app.route('/benutzer/<int:benutzer_id>', methods=['GET', 'POST'])
@login_required
def benutzer(benutzer_id):
    benutzer = Benutzer.query.get_or_404(benutzer_id)

    # Kontrolle, dass nur der Eigentümer der Seite seine Notizen bearbeiten kann
    if current_user.id != benutzer.id:
        abort(403)  # 403 Nicht erlaubt, sofern nicht autorisiert

    form = NotizForm()

    if form.validate_on_submit():
        notiz = Notizen(Inhalt=form.notiz.data, user=current_user)
        db.session.add(notiz)
        db.session.commit()
        flash('Deine Notiz wurde angelegt')
        return redirect(url_for('benutzer', benutzer_id=benutzer.id))

    notizen = benutzer.notizen.all()
    return render_template("benutzer.html", title="Benutzerprofil", form=form, benutzer=benutzer, notizen=notizen)

# Bearbeiten einer Notiz
@app.route('/edit_note/<int:notiz_id>', methods=['GET', 'POST'])
@login_required
def edit_note(notiz_id):
    notiz = Notizen.query.get_or_404(notiz_id)

    # Überprüfen, ob der aktuelle Benutzer der Eigentümer der Notiz ist
    if current_user != notiz.user:
        abort(403) # Nicht erlaubt, sofern nicht autorisiert
    form = NotizForm()

    if form.validate_on_submit():
        notiz.Inhalt = form.notiz.data  # Nur das Notizfeld aktualisieren
        db.session.commit()
        flash('Notiz erfolgreich bearbeitet')
        return redirect(url_for('index'))

    form.notiz.data = notiz.Inhalt

    print("Notiz-ID:", notiz.id)
    print("Notiz-Inhalt vor der Formularaktualisierung:", notiz.Inhalt)

    return render_template('edit_note.html', title='Notiz bearbeiten', form=form, notiz=notiz)

from flask import redirect, url_for

# Löschen einer Notiz
@app.route('/delete_note/<int:notiz_id>', methods=['GET', 'POST'])
@login_required
def delete_note(notiz_id):
    notiz = Notizen.query.get_or_404(notiz_id)

    # Überprüfen, ob der aktuelle Benutzer der Eigentümer der Notiz ist
    if current_user != notiz.user:
        abort(403)  # Nicht erlaubt, sofern nicht autorisiert

    db.session.delete(notiz)
    db.session.commit()
    flash('Notiz erfolgreich gelöscht')
    return redirect(url_for('benutzer', benutzer_id=current_user.id))

# Hinzufügen und entfernen einer Notiz als Favorit
@app.route('/toggle_favorite/<int:notiz_id>', methods=['POST'])
@login_required
def toggle_favorite(notiz_id):
    notiz = Notizen.query.get_or_404(notiz_id)

    if notiz.favorit:
        # Notiz aus den Favoriten entfernen
        notiz.favorit = False
        db.session.commit()
        flash('Notiz wurde erfolgreich aus den Favoriten entfernt.', 'success')
    else:
        # Notiz als Favorit markieren
        notiz.favorit = True
        db.session.commit()
        flash('Notiz wurde erfolgreich als Favorit markiert.', 'success')

    return redirect(url_for('index'))

# API für die Benutzerdetails
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = Benutzer.query.get_or_404(user_id)
    data = {
        'id': user.id,
        'Benutzername': user.Benutzername,
        'email': user.email,
        '_links': {
            'self': url_for('get_user', user_id=user.id)
        }
    }
    return jsonify(data)

# Route für die Liste aller Benutzer
@app.route('/api/users')
def get_all_users():
    users = Benutzer.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'Benutzername': user.Benutzername,
            'email': user.email,
            '_links': {
                'self': url_for('get_user', user_id=user.id)
            }
        }
        user_list.append(user_data)
    return jsonify({'users': user_list})

# Route für die Details einer Notiz
@app.route('/api/notizen/<int:notiz_id>')
def get_notiz(notiz_id):
    notiz = Notizen.query.get_or_404(notiz_id)
    data = {
        'id': notiz.id,
        'Inhalt': notiz.Inhalt,
        'user_id': notiz.user_id,
        '_links': {
            'self': url_for('get_notiz', notiz_id=notiz.id)
        }
    }
    return jsonify(data)

# Route für die Liste aller Notizen
@app.route('/api/notizen')
def get_all_notizen():
    notizen = Notizen.query.all()
    notiz_list = []
    for notiz in notizen:
        notiz_data = {
            'id': notiz.id,
            'Inhalt': notiz.Inhalt,
            'user_id': notiz.user_id,
            '_links': {
                'self': url_for('get_notiz', notiz_id=notiz.id)
            }
        }
        notiz_list.append(notiz_data)
    return jsonify({'notizen': notiz_list})

