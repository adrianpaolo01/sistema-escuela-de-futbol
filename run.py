from app import create_app

# Crear la app usando la función
app = create_app()

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)