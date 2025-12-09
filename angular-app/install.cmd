@echo off
echo Installation des dependances Angular...
cd /d "%~dp0"
call npm install
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Installation reussie!
    echo ========================================
    echo.
    echo Pour demarrer l'application:
    echo   npm start
    echo.
    echo Puis ouvrez: http://localhost:4200
    echo.
) else (
    echo.
    echo Erreur lors de l'installation!
    echo.
)
pause
