@echo off
cd "C:\Users\JUAN\OneDrive\Universidades\UNAL\Clases UNAL\python\calificar"
dir
set /p version="Ingresa la nueva version (ej. 0.1.1): "

:: 1. Actualizar versión en el pyproject.toml (manual o con este recordatorio)
echo Actualizando a la version %version%...

:: 2. Limpiar y Construir
rd /s /q dist build
python -m build

:: 3. Subir a PyPI
python -m twine upload dist/*

:: 4. Subir a GitHub
git add .
git commit -m "Publicada version %version%"
git push origin main

echo ¡Proceso terminado con exito!
pause