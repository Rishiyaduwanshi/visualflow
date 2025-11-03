# VisualFlow - AI-Powered Diagram Generator

VisualFlow is a fullstack Django application that generates professional diagrams from textual descriptions using AI. Built with Django, PostgreSQL, Mermaid.js, and powered by Groq AI for intelligent diagram generation.

## 🚀 Features

- **AI-Powered Generation**: Uses LangChain + Groq LLM (`llama3-8b-8192`) to generate Mermaid.js diagrams
- **Multiple Diagram Types**: Supports flowcharts, sequence diagrams, class diagrams, ER diagrams, and more
- **Auto-Detection**: Automatically detects diagram type from user prompts
- **Professional Rendering**: High-quality SVG/PNG diagram output via Mermaid.js
- **Session Management**: Stores all generated diagrams with full history
- **Responsive UI**: Modern, mobile-friendly interface built with Tailwind CSS
- **Download Options**: Export diagrams as SVG or PNG images
- **Clean User Experience**: Users see only diagrams, technical code is hidden
- **PostgreSQL Database**: Production-ready database with SSL support

## 🏗️ Architecture

```
visualflow/
├── config/                    # Modular configuration
│   ├── env_config.py         # Environment variables & SSL config
│   └── constants.py          # Application constants
├── diagrams/                 # Main Django application
│   ├── models.py            # Session model with UUID primary keys
│   ├── views.py             # Clean class-based views
│   ├── admin.py             # Admin interface
│   ├── services/            # Business logic
│   │   ├── ai_service.py    # Template-based generation
│   │   └── mermaid_service.py  # AI-powered Mermaid generation
│   └── urls.py              # Simple URL routing
├── templates/               # Django templates
│   └── diagrams/           # Clean user-focused templates
├── theme/                   # Tailwind CSS theme
└── static/                  # Static files
```

## 📋 Requirements

- Python 3.10+
- PostgreSQL 12+ (with SSL support)
- Node.js 16+ (for Tailwind CSS)
- Groq API Key
- Internet connection (for AI generation)

## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/rishiyaduwanshi/visualflow
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
# Database Configuration (PostgreSQL with SSL)
DB_NAME=visualflow_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_SSL_REQUIRE=false
DB_SSL_MODE=prefer
DB_SSL_CERT_PATH=
DB_SSL_KEY_PATH=
DB_SSL_CA_PATH=
# CA Certificate content (paste your CA cert here for cloud databases)
DB_SSL_CA_CERT=

# AI/ML API Keys
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=visualflow

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Application Configuration
APP_NAME=VisualFlow
APP_VERSION=1.0.0
```

**For cloud PostgreSQL (like Aiven):**
```env
DB_NAME=your_cloud_db_name
DB_USER=your_cloud_user
DB_PASSWORD=your_cloud_password
DB_HOST=your-cloud-host.com
DB_PORT=your_cloud_port
DB_SSL_REQUIRE=true
DB_SSL_MODE=require
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
| `DB_SSL_REQUIRE` | Enable SSL for database | `false` |
| `DEBUG` | Django debug mode | `True` |

## 📊 Supported Diagram Types

| Type | Description | Mermaid Support |
|------|-------------|-----------------|
| **Flowchart** | Process flowcharts | `flowchart TD/LR` |
| **Sequence** | Interaction diagrams | `sequenceDiagram` |  
| **Class** | UML class diagrams | `classDiagram` |
| **ER** | Entity relationship diagrams | `erDiagram` |
| **State** | State transition diagrams | `stateDiagram-v2` |
| **Gantt** | Project timelines | `gantt` |
| **Pie** | Statistical charts | `pie` |
| **Custom** | Any other diagram type | Auto-detected |

## 🎨 Usage Examples

### Flowchart Example
```
Create a user login process flowchart showing authentication steps, validation, and error handling
```

### Sequence Diagram Example  
```
Design a sequence diagram for user registration with email verification between Frontend, Backend, and Email Service
```

### ER Diagram Example
```
Create an ER diagram for an e-commerce database with User, Product, Order, and Category entities with proper relationships
```

### Class Diagram Example
```
Generate a class diagram for a payment processing system with Payment, PaymentMethod, and Transaction classes
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
   - Diagram type detection
   - Template-based generation fallback

2. **Mermaid Service** (`diagrams/services/mermaid_service.py`)
   - LangChain + Groq LLM integration
   - AI-powered Mermaid.js code generation
   - Syntax validation and cleanup
   - Multiple diagram type support

3. **Models** (`diagrams/models.py`)
   - Session management
   - Template storage
   - User feedback

4. **Views** (`diagrams/views.py`)
   - Class-based views
   - API endpoints
   - Error handling

## 🛠️ Technology Stack

### Backend
- **Django 5.2.7** - Web framework
- **PostgreSQL** - Production database with SSL support  
- **LangChain** - AI framework for LLM integration
- **Groq** - Fast LLM inference (`llama3-8b-8192`)

### Frontend  
- **Mermaid.js 10.6.1** - Diagram rendering engine
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - Interactive features

### DevOps
- **Python-dotenv** - Environment management
- **Modular Configuration** - Clean separation of concerns

### Adding New Diagram Types

1. Update `config/constants.py`:
```python
DIAGRAM_TYPES = {
    'NEW_TYPE': 'new_type',
    # ... existing types
}
```

2. Add generation logic to `mermaid_service.py`
3. Update templates and UI
4. Test with various prompts

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

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=production-secret-key
DB_SSL_REQUIRE=true
DB_SSL_MODE=require
```

2. **Static Files & Tailwind**
```bash
python manage.py collectstatic
python manage.py tailwind build
```

3. **Database Migration**
```bash
python manage.py migrate
```

4. **Web Server** (using Gunicorn)
```bash
gunicorn visualflow.wsgi:application --bind 0.0.0.0:8000
```

### Cloud Database Setup (Aiven, AWS RDS, etc.)

1. **Create PostgreSQL database** in your cloud provider
2. **Enable SSL** and download certificates if needed
3. **Update .env** with cloud database credentials:
   ```env
   DB_SSL_REQUIRE=true
   DB_SSL_MODE=require
   DB_SSL_CA_CERT=-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----
   ```
4. **Test connection** before deploying

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support, email hello@iamabhinav.dev or create an issue on GitHub.

## 🙏 Acknowledgments

- [Django](https://djangoproject.com/) - Web framework
- [LangChain](https://langchain.com/) - AI framework  
- [Groq](https://groq.com/) - Fast LLM inference
- [Mermaid.js](https://mermaid.js.org/) - Diagram rendering
- [PostgreSQL](https://postgresql.org/) - Database
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

---

**VisualFlow** - Transform ideas into professional diagrams with AI 🚀