# VisualFlow - AI-Powered Diagram Generator

VisualFlow is a fullstack Django application that generates professional diagrams from textual descriptions using AI. It supports various diagram types including UML, ERD, DFD, flowcharts, system design diagrams, and custom diagrams.

## 🚀 Features

- **AI-Powered Generation**: Uses LangChain + Groq LLM to generate PlantUML code from natural language prompts
- **Multiple Diagram Types**: Supports UML, ERD, DFD, flowcharts, system design, and custom diagrams
- **Auto-Detection**: Automatically detects diagram type from user prompts
- **Professional Rendering**: High-quality SVG/PNG diagram output via PlantUML server
- **Session Management**: Stores all generated diagrams with full history
- **Responsive UI**: Modern, mobile-friendly interface built with Tailwind CSS
- **Download Options**: Export diagrams as SVG, PNG, or PlantUML code
- **Admin Interface**: Full Django admin for managing sessions and templates

## 🏗️ Architecture

```
visualflow/
├── config/                    # Configuration management
│   ├── env_config.py         # Environment variables
│   └── constants.py          # Application constants
├── diagrams/                 # Main application
│   ├── models.py            # Session, Template, Feedback models
│   ├── views.py             # Class-based views
│   ├── admin.py             # Admin interface
│   ├── services/            # Business logic
│   │   ├── ai_service.py    # LangChain + Groq integration
│   │   └── plantuml_service.py  # PlantUML rendering
│   └── urls.py              # URL routing
├── templates/               # Django templates
│   └── diagrams/           # App-specific templates
├── theme/                   # Tailwind CSS theme
└── static/                  # Static files
```

## 📋 Requirements

- Python 3.10+
- PostgreSQL 12+
- Node.js 16+ (for Tailwind CSS)
- Groq API Key
- Internet connection (for PlantUML server)

## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd visualflow
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
DB_NAME=visualflow_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# AI/ML API Keys
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=visualflow

# PlantUML Configuration
PLANTUML_SERVER_URL=http://www.plantuml.com/plantuml

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Application Configuration
APP_NAME=VisualFlow
APP_VERSION=1.0.0
```

### 5. Database Setup

```bash
# Create PostgreSQL database
createdb visualflow_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Tailwind CSS Setup

```bash
# Install Tailwind dependencies
python manage.py tailwind install

# Build CSS (for production)
python manage.py tailwind build
```

### 7. Run Development Server

```bash
# Start Tailwind watcher (in one terminal)
python manage.py tailwind start

# Start Django server (in another terminal)
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 🔧 Configuration

### Environment Variables

All configuration is managed through environment variables in the `config/` directory:

- **`config/env_config.py`**: Environment variable loading and validation
- **`config/constants.py`**: Application constants and default values

### Key Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for AI generation | Required |
| `DB_PASSWORD` | PostgreSQL password | Required |
| `PLANTUML_SERVER_URL` | PlantUML server endpoint | `http://www.plantuml.com/plantuml` |
| `DEBUG` | Django debug mode | `True` |

## 📊 Supported Diagram Types

| Type | Description | Use Cases |
|------|-------------|-----------|
| **UML** | Unified Modeling Language | Class diagrams, sequence diagrams |
| **ERD** | Entity Relationship Diagrams | Database schema design |
| **DFD** | Data Flow Diagrams | System data flow analysis |
| **Flowchart** | Process flowcharts | Business processes, algorithms |
| **System Design** | Architecture diagrams | System components, microservices |
| **Custom** | Any other diagram type | General purpose diagrams |

## 🎨 Usage Examples

### UML Class Diagram
```
Create a UML class diagram for an e-commerce system with User, Product, Order, and ShoppingCart classes. Include inheritance, composition, and proper attributes and methods.
```

### ERD Database Schema
```
Design an ERD for a library management system with entities: Book, Author, Member, Loan, and Category. Show primary keys, foreign keys, and relationships.
```

### System Architecture
```
Create a system architecture diagram for a microservices-based chat application with API gateway, user service, message service, notification service, and database.
```

## 🔄 API Endpoints

### REST API

- `POST /api/generate/` - Generate diagram via AJAX
- `GET /api/status/<session_id>/` - Check generation status

### Web Interface

- `/` - Homepage with generation form
- `/display/<session_id>/` - View generated diagram
- `/history/` - Browse all diagrams
- `/download/<session_id>/` - Download diagram files

## 🛠️ Development

### Project Structure

```
visualflow/
├── config/                    # Configuration and constants
├── diagrams/                  # Main Django app
│   ├── services/             # Business logic services
│   ├── migrations/           # Database migrations
│   └── templates/            # App templates
├── templates/                # Global templates
├── theme/                    # Tailwind CSS theme
├── static/                   # Static files
├── media/                    # User uploads
└── logs/                     # Application logs
```

### Key Components

1. **AI Service** (`diagrams/services/ai_service.py`)
   - LangChain integration
   - Groq LLM communication
   - Diagram type detection
   - PlantUML code generation

2. **PlantUML Service** (`diagrams/services/plantuml_service.py`)
   - Server communication
   - SVG/PNG rendering
   - Format conversion

3. **Models** (`diagrams/models.py`)
   - Session management
   - Template storage
   - User feedback

4. **Views** (`diagrams/views.py`)
   - Class-based views
   - API endpoints
   - Error handling

### Adding New Diagram Types

1. Update `config/constants.py`:
```python
DIAGRAM_TYPES = {
    'NEW_TYPE': 'new_type',
    # ... existing types
}
```

2. Add prompts to `DiagramPrompts` class
3. Update templates and UI
4. Run migrations if needed

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=production-secret-key
```

2. **Static Files**
```bash
python manage.py collectstatic
python manage.py tailwind build
```

3. **Database**
```bash
python manage.py migrate --run-syncdb
```

4. **Web Server** (using Gunicorn)
```bash
gunicorn visualflow.wsgi:application --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "visualflow.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support, email support@visualflow.com or create an issue on GitHub.

## 🙏 Acknowledgments

- [Django](https://djangoproject.com/) - Web framework
- [LangChain](https://langchain.com/) - AI framework
- [Groq](https://groq.com/) - LLM provider
- [PlantUML](https://plantuml.com/) - Diagram generation
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

---

**VisualFlow** - Transform ideas into professional diagrams with AI 🚀