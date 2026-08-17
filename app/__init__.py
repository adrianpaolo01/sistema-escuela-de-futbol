import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # DATABASE_URL: Render provee PostgreSQL, local usa SQLite
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///../instance/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_secreta_local')

    db.init_app(app)

    # Context processor: inyecta el usuario actual en TODOS los templates
    @app.context_processor
    def inject_user():
        from .models import Usuario
        if 'user_id' in session:
            user = db.session.get(Usuario, session['user_id'])
            return dict(current_user=user)
        return dict(current_user=None)

    from .models import Alumno, Pago, Usuario
    from .routes import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)

        # Migraciones alumno
        columnas = [col['name'] for col in inspector.get_columns('alumno')]
        for col_name, col_type in [
            ('categoria', 'VARCHAR(100)'), ('plan', 'VARCHAR(50)'),
            ('monto_inscripcion', 'FLOAT'), ('nombre_padre', 'VARCHAR(100)'),
            ('telefono_padre', 'VARCHAR(20)'), ('fecha_inscripcion', 'DATE'),
            ('fecha_vencimiento', 'DATE')
        ]:
            if col_name not in columnas:
                with db.engine.begin() as conn:
                    conn.execute(text(f"ALTER TABLE alumno ADD COLUMN {col_name} {col_type}"))

        # Migraciones usuario
        columnas_usuario = [col['name'] for col in inspector.get_columns('usuario')]
        for col_name, col_type in [
            ('is_admin', 'BOOLEAN DEFAULT 0'),
            ('blocked', 'BOOLEAN DEFAULT 0')
        ]:
            if col_name not in columnas_usuario:
                with db.engine.begin() as conn:
                    conn.execute(text(f"ALTER TABLE usuario ADD COLUMN {col_name} {col_type}"))

    return app

app = create_app()
