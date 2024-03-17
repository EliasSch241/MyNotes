from flask import render_template
from app import app, db

# Fehlerbehandlung für 403 Forbidden Error
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

# Fehlerbehandlung für 404 Not Found Error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Fehlerbehandlung für 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500