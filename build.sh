#!/bin/bash
echo "Inicializando base de datos..."
python -c "from app import create_app; app = create_app(); print('BD lista')"
