@echo off
REM VisualFlow Setup Script for Windows

echo 🚀 Setting up VisualFlow - AI Diagram Generator

REM Check Python version
python -c "import sys; print('Python version:', '.'.join(map(str, sys.version_info[:2])))"

REM Create virtual environment if not exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing Python packages...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚙️ Creating .env file from template...
    copy .env.example .env
    echo 📝 Please edit .env file with your API keys and database credentials
)

echo ✅ Setup complete! Next steps:
echo 1. Edit .env file with your credentials
echo 2. Setup PostgreSQL database
echo 3. Run: python manage.py makemigrations
echo 4. Run: python manage.py migrate
echo 5. Run: python manage.py setup_visualflow --create-admin
echo 6. Start server: python manage.py runserver

pause