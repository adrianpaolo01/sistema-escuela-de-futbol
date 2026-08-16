from datetime import date
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import Usuario
from app.routes import calcular_fecha_vencimiento, calcular_dias_restantes

app = create_app()
app.testing = True

with app.app_context():
    db.create_all()
    user = Usuario.query.filter_by(username='test').first()
    if not user:
        db.session.add(Usuario(username='test', password=generate_password_hash('123')))
        db.session.commit()
    else:
        user.password = generate_password_hash('123')
        db.session.commit()

client = app.test_client()
resp = client.post('/login', data={'username': 'test', 'password': '123'}, follow_redirects=True)
print('login', resp.status_code)
resp2 = client.get('/', follow_redirects=True)
print('root', resp2.status_code)
print('contains_vencimiento', 'Vence la mensualidad' in resp2.get_data(as_text=True))
print('vencimiento', calcular_fecha_vencimiento(date(2026, 7, 15)))
print('dias', calcular_dias_restantes(date(2026, 8, 16)))
