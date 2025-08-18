@echo off
echo ComeBack Admin Panel Setup
echo =========================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Creating virtual environment...

REM Create virtual environment
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy env_example.txt .env
    echo.
    echo IMPORTANT: Please edit .env file with your Firebase credentials!
    echo.
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo.
echo Creating superuser account...
echo Please enter superuser credentials:
python manage.py createsuperuser

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your Firebase credentials
echo 2. Run: run_server.bat
echo 3. Open browser: http://127.0.0.1:8000
echo.
pause
