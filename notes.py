from app import app, db
from app.models import Benutzer, Favoriten, Notizen

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'benutzer': Benutzer, 'favoriten': Favoriten, 'notizen': Notizen}