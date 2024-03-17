from app import app, db
from app.models import benutzer, favoriten, notizen

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'benutzer': benutzer, 'favoriten': favoriten, 'notizen': notizen}