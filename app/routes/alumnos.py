from datetime import datetime
from flask import Blueprint, render_template, request, redirect
from ..models import Alumno, Pago
from .. import db
from ..decorators import login_required
from ..constants import CATEGORIAS
from ..helpers import (
    parsear_fecha, calcular_fecha_vencimiento, calcular_dias_restantes,
    formatear_fecha, obtener_estado_vigencia
)
from ..constants import MESES_ES

alumnos_bp = Blueprint('alumnos', __name__)


@alumnos_bp.route('/')
@login_required
def alumnos():
    alumnos = Alumno.query.order_by(Alumno.id.desc()).all()
    pagos = Pago.query.all()
    mes_actual = MESES_ES[datetime.now().month]
    lista = []

    for alumno in alumnos:
        estado = 'Inactivo'
        for p in pagos:
            if p.alumno_id == alumno.id and p.mes == mes_actual:
                estado = 'Activo'

        fecha_vencimiento = alumno.fecha_vencimiento or calcular_fecha_vencimiento(alumno.fecha_inscripcion)
        dias_restantes = calcular_dias_restantes(fecha_vencimiento)
        vigencia = obtener_estado_vigencia(fecha_vencimiento)

        lista.append({
            "id": alumno.id,
            "nombre": alumno.nombre,
            "edad": alumno.edad,
            "telefono": alumno.telefono,
            "categoria": alumno.categoria or 'Sin categoría',
            "plan": alumno.plan or 'Sin plan',
            "monto_inscripcion": alumno.monto_inscripcion,
            "estado": estado,
            "fecha_inscripcion": formatear_fecha(alumno.fecha_inscripcion),
            "fecha_vencimiento": formatear_fecha(fecha_vencimiento),
            "dias_restantes": dias_restantes,
            "vigencia": vigencia,
        })

    return render_template('alumnos.html', alumnos=lista)


@alumnos_bp.route('/nuevo')
@login_required
def nuevo():
    return render_template('nuevo_alumno.html', categorias=CATEGORIAS, hoy=datetime.now().strftime('%Y-%m-%d'))


@alumnos_bp.route('/guardar', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    edad = request.form['edad']
    telefono = request.form['telefono']
    categoria = request.form.get('categoria', 'Sin categoría')
    nombre_padre = request.form.get('nombre_padre', '')
    telefono_padre = request.form.get('telefono_padre', '')
    fecha_inscripcion = parsear_fecha(request.form.get('fecha_inscripcion'))
    fecha_vencimiento = calcular_fecha_vencimiento(fecha_inscripcion)
    plan = request.form['plan']

    if plan == 'normal':
        monto = 180
    elif plan == 'especial':
        monto = float(request.form['monto'])
    else:
        return "Plan no válido", 400

    nuevo_alumno = Alumno(
        nombre=nombre,
        edad=edad,
        telefono=telefono,
        categoria=categoria,
        plan=plan,
        monto_inscripcion=monto if plan == 'especial' else 180,
        nombre_padre=nombre_padre,
        telefono_padre=telefono_padre,
        fecha_inscripcion=fecha_inscripcion,
        fecha_vencimiento=fecha_vencimiento
    )

    db.session.add(nuevo_alumno)
    db.session.flush()

    mes_actual = MESES_ES[datetime.now().month]
    nuevo_pago = Pago(
        alumno_id=nuevo_alumno.id,
        mes=mes_actual,
        monto=monto
    )

    db.session.add(nuevo_pago)
    db.session.commit()
    return redirect('/')


@alumnos_bp.route('/buscar_alumno')
@login_required
def buscar_alumno():
    nombre = request.args.get('nombre', '').strip()
    if not nombre:
        return redirect('/')
    coincidencias = Alumno.query.filter(Alumno.nombre.ilike(f'%{nombre}%')).all()
    if len(coincidencias) == 1:
        return redirect(f"/alumno/{coincidencias[0].id}")
    return render_template('buscar_alumno.html', alumnos=coincidencias, query=nombre)


@alumnos_bp.route('/editar_alumno/<int:id>')
@login_required
def editar_alumno(id):
    alumno = Alumno.query.get(id)
    return render_template('editar_alumno.html', alumno=alumno, categorias=CATEGORIAS)


@alumnos_bp.route('/actualizar_alumno/<int:id>', methods=['POST'])
@login_required
def actualizar_alumno(id):
    alumno = Alumno.query.get(id)
    if alumno:
        alumno.nombre = request.form['nombre']
        alumno.edad = request.form['edad']
        alumno.telefono = request.form['telefono']
        alumno.categoria = request.form.get('categoria', alumno.categoria)
        alumno.plan = request.form.get('plan', alumno.plan)
        alumno.monto_inscripcion = float(request.form['monto_inscripcion']) if request.form.get('monto_inscripcion') else alumno.monto_inscripcion
        alumno.nombre_padre = request.form.get('nombre_padre', alumno.nombre_padre)
        alumno.telefono_padre = request.form.get('telefono_padre', alumno.telefono_padre)
        alumno.fecha_inscripcion = parsear_fecha(request.form.get('fecha_inscripcion'))
        alumno.fecha_vencimiento = calcular_fecha_vencimiento(alumno.fecha_inscripcion)
        db.session.commit()
    return redirect('/')


@alumnos_bp.route('/test')
def test():
    return render_template('test.html')


@alumnos_bp.route('/eliminar_alumno/<int:id>', methods=['POST'])
@login_required
def eliminar_alumno(id):
    alumno = Alumno.query.get(id)
    if alumno:
        Pago.query.filter_by(alumno_id=id).delete()
        db.session.delete(alumno)
        db.session.commit()
    return redirect('/')
