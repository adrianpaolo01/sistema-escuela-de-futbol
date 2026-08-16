from . import db  # Importamos la DB desde __init__

# =========================
# MODELO ALUMNO
# =========================
class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único
    nombre = db.Column(db.String(100))            # Nombre del alumno
    edad = db.Column(db.Integer)                  # Edad
    telefono = db.Column(db.String(20))           # Teléfono
    categoria = db.Column(db.String(100))         # Categoría asignada
    plan = db.Column(db.String(50))               # Plan de inscripción
    monto_inscripcion = db.Column(db.Float)       # Monto exacto del plan especial
    nombre_padre = db.Column(db.String(100))      # Nombre del padre/tutor
    telefono_padre = db.Column(db.String(20))     # Teléfono del padre/tutor
    fecha_inscripcion = db.Column(db.Date)        # Fecha de inscripción
    fecha_vencimiento = db.Column(db.Date)        # Fecha de vencimiento de la mensualidad

# =========================
# MODELO PAGO
# =========================
class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))  # Relación con Alumno
    mes = db.Column(db.String(20))   # Mes del pago
    monto = db.Column(db.Float)      # Cantidad pagada

#Modelo Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)
    
