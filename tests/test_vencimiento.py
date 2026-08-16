from datetime import date
from app.routes import calcular_fecha_vencimiento, calcular_dias_restantes


def test_calcular_fecha_vencimiento():
    assert calcular_fecha_vencimiento(date(2026, 7, 15)) == date(2026, 8, 15)
    assert calcular_fecha_vencimiento(date(2026, 12, 20)) == date(2027, 1, 15)


def test_calcular_dias_restantes():
    assert calcular_dias_restantes(date(2026, 7, 31)) >= 0
