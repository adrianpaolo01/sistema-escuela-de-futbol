import io
import csv
from datetime import datetime
from flask import Blueprint, render_template, make_response
from ..models import Alumno, Pago
from .. import db
from ..decorators import login_required
from ..constants import MESES_ES
from ..helpers import obtener_meses_anteriores

control_bp = Blueprint('control', __name__)


@control_bp.route('/control')
@login_required
def control_mensual():
    alumnos = Alumno.query.all()
    meses = obtener_meses_anteriores(3)
    pagos = db.session.query(Pago.alumno_id, Pago.mes).all()
    pagos_set = set(pagos)
    tabla = []
    for alumno in alumnos:
        fila = {"nombre": alumno.nombre, "pagos": {}}
        for mes in meses:
            fila["pagos"][mes] = (alumno.id, mes) in pagos_set
        tabla.append(fila)
    return render_template('control.html', tabla=tabla, meses=meses)


@control_bp.route('/control_cuentas')
@login_required
def control_cuentas():
    mes_actual = MESES_ES[datetime.now().month]
    pagos = Pago.query.all()
    alumnos = Alumno.query.order_by(Alumno.nombre).all()
    pagos_por_alumno = {}
    total_mes = 0.0
    total_general = 0.0

    for a in alumnos:
        pagos_por_alumno[a.id] = {"nombre": a.nombre, "mes": 0.0, "total": 0.0}

    for p in pagos:
        if p.alumno_id in pagos_por_alumno:
            pagos_por_alumno[p.alumno_id]["total"] += float(p.monto or 0)
            total_general += float(p.monto or 0)
            if p.mes == mes_actual:
                pagos_por_alumno[p.alumno_id]["mes"] += float(p.monto or 0)
                total_mes += float(p.monto or 0)

    lista = sorted(pagos_por_alumno.values(), key=lambda x: x["nombre"])
    return render_template('control_cuentas.html', lista=lista, total_mes=total_mes, total_general=total_general, mes=mes_actual)


@control_bp.route('/control_cuentas/export_csv')
@login_required
def control_cuentas_export_csv():
    mes_actual = MESES_ES[datetime.now().month]
    pagos = Pago.query.all()
    alumnos = Alumno.query.order_by(Alumno.nombre).all()
    pagos_por_alumno = {}
    total_mes = 0.0
    total_general = 0.0

    for a in alumnos:
        pagos_por_alumno[a.id] = {"nombre": a.nombre, "mes": 0.0, "total": 0.0}

    for p in pagos:
        if p.alumno_id in pagos_por_alumno:
            pagos_por_alumno[p.alumno_id]["total"] += float(p.monto or 0)
            total_general += float(p.monto or 0)
            if p.mes == mes_actual:
                pagos_por_alumno[p.alumno_id]["mes"] += float(p.monto or 0)
                total_mes += float(p.monto or 0)

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(["Alumno", f"Pagado {mes_actual}", "Total acumulado"])
    for row in sorted(pagos_por_alumno.values(), key=lambda x: x["nombre"]):
        writer.writerow([row["nombre"], f"{row['mes']:.2f}", f"{row['total']:.2f}"])
    writer.writerow(["Totales", f"{total_mes:.2f}", f"{total_general:.2f}"])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=control_cuentas_{mes_actual}.csv"
    output.headers["Content-Type"] = "text/csv; charset=utf-8"
    return output


@control_bp.route('/informacion_padres')
@login_required
def informacion_padres():
    alumnos = Alumno.query.order_by(Alumno.id.desc()).all()
    return render_template('informacion_padres.html', alumnos=alumnos)


@control_bp.route('/cron/generar_pagos_mes')
@login_required
def cron_generar_pagos_mes():
    mes_actual = MESES_ES[datetime.now().month]
    alumnos = Alumno.query.all()
    creados = 0
    for a in alumnos:
        existe = Pago.query.filter_by(alumno_id=a.id, mes=mes_actual).first()
        if not existe:
            monto = a.monto_inscripcion or 180
            nuevo = Pago(alumno_id=a.id, mes=mes_actual, monto=monto)
            db.session.add(nuevo)
            creados += 1
    db.session.commit()
    return f"Pagos creados: {creados}", 200
