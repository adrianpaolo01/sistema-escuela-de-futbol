from flask import Blueprint, render_template, request, redirect, session
from ..models import Usuario
from .. import db
from ..decorators import login_required

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        usuario = Usuario.query.get(session['user_id'])
        if not usuario or not usuario.is_admin:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/admin')
@admin_required
def panel():
    usuarios = Usuario.query.order_by(Usuario.id).all()
    return render_template('admin.html', usuarios=usuarios)


@admin_bp.route('/admin/bloquear/<int:id>', methods=['POST'])
@admin_required
def bloquear(id):
    usuario = Usuario.query.get(id)
    if usuario and usuario.id != session.get('user_id'):
        usuario.blocked = True
        db.session.commit()
    return redirect('/admin')


@admin_bp.route('/admin/desbloquear/<int:id>', methods=['POST'])
@admin_required
def desbloquear(id):
    usuario = Usuario.query.get(id)
    if usuario:
        usuario.blocked = False
        db.session.commit()
    return redirect('/admin')
