@echo off
echo Starting ComeBack Admin Panel...
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Run Django server
echo Starting Django development server...
python manage.py runserver

pause
