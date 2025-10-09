#!/bin/bash

# VisualFlow Setup Script
echo "🚀 Setting up VisualFlow - AI Diagram Generator"

# Check Python version
python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python_version"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate  # Linux/Mac
# For Windows: venv\Scripts\activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys and database credentials"
fi

echo "✅ Setup complete! Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Setup PostgreSQL database"
echo "3. Run: python manage.py makemigrations"
echo "4. Run: python manage.py migrate"
echo "5. Run: python manage.py setup_visualflow --create-admin"
echo "6. Start server: python manage.py runserver"