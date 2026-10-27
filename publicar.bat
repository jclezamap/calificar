@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
cd /d "C:\Users\JUAN\OneDrive\Servidor\web\python\calificar"

for /f "tokens=2 delims==" %%v in ('findstr /b "__version__" src\calificar\__init__.py') do set actual=%%v
set actual=!actual: =!
set actual=!actual:"=!
echo Version actual: !actual!
set /p version="Nueva version (ej. 0.2.1): "
if "!version!"=="" (echo No se escribio la version. & pause & exit /b 1)

git rev-parse "v!version!" >nul 2>&1 && (echo La version !version! ya existe. & pause & exit /b 1)

:: 1. Escribe la version en src\calificar\__init__.py (pyproject.toml la toma de ahi)
powershell -NoProfile -Command "(Get-Content -Raw -Encoding UTF8 'src\calificar\__init__.py') -replace '__version__ = \"[^\"]*\"', '__version__ = \"!version!\"' | Set-Content -NoNewline -Encoding UTF8 'src\calificar\__init__.py'"

:: 2. Prueba local: que construya antes de subir nada
rd /s /q dist build 2>nul
python -m build || (echo Fallo la construccion. No se subio nada. & pause & exit /b 1)

:: 3. Sube a GitHub con la etiqueta: GitHub Actions publica en PyPI
git add src README.md pyproject.toml LICENSE .github .gitignore publicar.bat
git commit -m "Version !version!"
git tag "v!version!"
git push origin main
git push origin "v!version!"

echo.
echo Listo. GitHub publica la version !version! en PyPI en un par de minutos:
echo https://github.com/jclezamap/calificar/actions
pause
