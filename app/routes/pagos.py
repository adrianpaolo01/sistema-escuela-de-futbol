from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect
from ..models import Alumno, Pago
from .. import db
from ..decorators import login_required
from ..constants import MESES_ES
from ..helpers import calcular_fecha_vencimiento, calcular_dias_restantes, formatear_fecha, obtener_estado_vigencia

pagos_bp = Blueprint('pagos', __name__)


@pagos_bp.route('/pago')
@login_required
def formulario_pago():
    alumnos = Alumno.query.all()
    alumnos_json = [{"id": a.id, "nombre": a.nombre} for a in alumnos]
    mes_actual = datetime.now().strftime('%Y-%m')
    return render_template('pago.html', alumnos=alumnos_json, mes_actual=mes_actual)


@pagos_bp.route('/guardar_pago', methods=['POST'])
@login_required
def guardar_pago():
    alumno_id = request.form['alumno_id']
    mes_raw = request.form['mes']
    monto = request.form['monto']

    try:
        mes_num = datetime.strptime(mes_raw, '%Y-%m').month
        mes = MESES_ES[mes_num]
    except ValueError:
        mes = mes_raw

    pago = Pago(alumno_id=alumno_id, mes=mes, monto=monto)
    db.session.add(pago)

    alumno = Alumno.query.get(int(alumno_id))
    if alumno:
        hoy = datetime.now().date()
        base = alumno.fecha_vencimiento if alumno.fecha_vencimiento and isinstance(alumno.fecha_vencimiento, date) and alumno.fecha_vencimiento > hoy else hoy
        alumno.fecha_vencimiento = calcular_fecha_vencimiento(base)

    db.session.commit()
    return redirect('/')


@pagos_bp.route('/pagos')
@login_required
def ver_pagos():
    pagos = Pago.query.all()
    resultado = []
    for p in pagos:
        alumno = Alumno.query.get(p.alumno_id)
        if alumno:
            resultado.append({
                "nombre": alumno.nombre,
                "mes": p.mes,
                "monto": p.monto
            })
    return render_template('pagos.html', pagos=resultado)


@pagos_bp.route('/alumno/<int:id>')
@login_required
def ver_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    pagos = Pago.query.filter_by(alumno_id=id).all()
    mes_actual = MESES_ES[datetime.now().month]
    activo = any(p.mes == mes_actual for p in pagos)
    meses_pagados = [p.mes for p in pagos]
    fecha_vencimiento = alumno.fecha_vencimiento or calcular_fecha_vencimiento(alumno.fecha_inscripcion)
    return render_template(
        'alumno_detalle.html',
        alumno=alumno,
        activo=activo,
        meses_pagados=meses_pagados,
        mes_actual=mes_actual,
        fecha_vencimiento=formatear_fecha(fecha_vencimiento),
        dias_restantes=calcular_dias_restantes(fecha_vencimiento),
        estado_vigencia=obtener_estado_vigencia(fecha_vencimiento)
    )
