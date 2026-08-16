import calendar
from datetime import datetime, date
from .constants import MESES_ES


def obtener_meses_anteriores(cantidad=3):
    hoy = datetime.now()
    meses = []
    for i in range(cantidad - 1, -1, -1):
        mes_num = ((hoy.month - i - 1) % 12) + 1
        meses.append(MESES_ES[mes_num])
    return meses


def parsear_fecha(valor):
    if isinstance(valor, date):
        return valor
    if isinstance(valor, datetime):
        return valor.date()
    if not valor:
        return datetime.now().date()
    try:
        return datetime.strptime(valor, '%Y-%m-%d').date()
    except ValueError:
        return datetime.now().date()


def calcular_fecha_vencimiento(fecha_inscripcion):
    fecha = parsear_fecha(fecha_inscripcion)
    year = fecha.year
    month = fecha.month + 1
    if month > 12:
        month = 1
        year += 1
    day = fecha.day
    try:
        return date(year, month, day)
    except ValueError:
        last_day = calendar.monthrange(year, month)[1]
        return date(year, month, min(day, last_day))


def calcular_dias_restantes(fecha_vencimiento):
    fecha_vencimiento = parsear_fecha(fecha_vencimiento)
    hoy = datetime.now().date()
    return (fecha_vencimiento - hoy).days


def formatear_fecha(fecha):
    fecha = parsear_fecha(fecha)
    return fecha.strftime('%d/%m/%Y')


def obtener_estado_vigencia(fecha_vencimiento):
    dias = calcular_dias_restantes(fecha_vencimiento)
    if dias < 0:
        return 'Vencida'
    if dias <= 7:
        return 'Por vencer'
    return 'Vigente'
