from flask import Blueprint, render_template, request, redirect, session
from ..models import Usuario
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = generate_password_hash(password)
        usuario = Usuario(username=username, password=hashed)
        db.session.add(usuario)
        db.session.commit()
        return redirect('/login')
    return render_template('registro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario or not check_password_hash(usuario.password, password):
            error = 'Credenciales incorrectas'
        elif usuario.blocked:
            error = 'Tu cuenta ha sido bloqueada. Contacta al administrador.'
        else:
            session['user_id'] = usuario.id
            return redirect('/')

    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
