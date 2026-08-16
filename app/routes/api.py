from flask import Blueprint, jsonify
from ..models import Alumno
from ..decorators import login_required

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/alumnos_json')
@login_required
def api_alumnos_json():
    alumnos = Alumno.query.order_by(Alumno.nombre).all()
    data = [{"id": a.id, "nombre": a.nombre} for a in alumnos]
    return jsonify(data)
