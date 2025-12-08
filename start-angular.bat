@echo off
REM Script d'installation et de lancement de l'application Angular (Windows)

echo.
echo ================================
echo Angular IoT Dashboard - Setup
echo ================================
echo.

REM Vérifier Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Node.js n'est pas installe.
    echo Telechargez Node.js depuis: https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Node.js version:
node --version
echo [OK] NPM version:
npm --version
echo.

REM Se déplacer dans le dossier angular-app
cd angular-app

REM Vérifier si node_modules existe
if not exist "node_modules" (
    echo [INFO] Installation des dependances npm...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERREUR] Installation des dependances echouee
        pause
        exit /b 1
    )
    echo [OK] Dependances installees avec succes
) else (
    echo [OK] Les dependances sont deja installees
)

echo.
echo [INFO] Configuration de l'environnement...
echo        API URL: http://localhost:8000/api
echo        Upload URL: http://localhost:8000/upload
echo.

REM Vérifier le backend
echo [INFO] Verification du backend Django...
curl -s http://localhost:8000/api/health/ >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Backend Django accessible
) else (
    echo [AVERTISSEMENT] Backend Django non accessible
    echo                 Assurez-vous que le backend tourne: docker-compose up -d
)

echo.
echo ================================
echo Demarrage de l'application...
echo Application: http://localhost:4200
echo ================================
echo.

REM Démarrer l'application
call npm start
