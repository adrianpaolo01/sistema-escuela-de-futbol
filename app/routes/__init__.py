from .alumnos import alumnos_bp
from .pagos import pagos_bp
from .control import control_bp
from .auth import auth_bp
from .api import api_bp
from .admin import admin_bp

all_blueprints = [alumnos_bp, pagos_bp, control_bp, auth_bp, api_bp, admin_bp]
