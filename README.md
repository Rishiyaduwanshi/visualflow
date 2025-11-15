# VisualFlow - AI-Powered Diagram Generator

VisualFlow is a fullstack Django application that generates professional, emoji-enhanced diagrams from textual descriptions using AI. Built with Django, PostgreSQL, Mermaid.js v10.9.1, and powered by Groq AI (`openai/gpt-oss-120b`) with intelligent two-step diagram generation.

## 🚀 Features

### 🤖 AI Generation
- **Two-Step AI Approach**: 
  - Step 1: Analyzer extracts diagram type, entities, and relationships from user prompt
  - Step 2: Specialized prompts (9 types) generate diagram with perfect Mermaid v10.9.1 syntax
- **Powered by**: LangChain + Groq AI (`openai/gpt-oss-120b` model at temperature 0.3)
- **Smart Auto-Detection**: Automatically detects best diagram type from natural language

### 🎨 Diagram Types
- **Flowcharts** (📊): Process flows with decision points and loops
- **UML Class Diagrams** (🏗️): Inheritance, composition, aggregation with proper multiplicity
- **ER Diagrams** (🗃️): Entity-relationship with correct cardinality syntax
- **Sequence Diagrams** (📡): Interaction flows with participants and messages
- **State Diagrams** (🔀): State machines with transitions
- **Data Flow Diagrams (DFD)** (🔄): Level 0, 1, 2+ with processes and data stores
- **System Design** (🏗️): Microservices, client-server architectures
- **Custom Diagrams** (🎨): AI auto-detects best type from description

### 🎨 Visual Enhancements
- **Emoji-Enhanced Diagrams**: Safe emoji usage in labels for visual clarity (🎯 ⚙️ 💾 ✅ ❌)
- **Professional Design**: High-quality SVG rendering with proper spacing
- **Color-Coded Elements**: Context-appropriate emojis for better understanding


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

## 🔧 Architecture

### Two-Step AI Generation

```
User Prompt → Step 1: Analyzer → Step 2: Generator → Error Fixing → Mermaid Render
     ↓             (JSON extract)     (specialized         (6 regex         ↓
"Create UML"       diagram_type       prompts)            patterns)    Beautiful SVG
                   entities
                   relationships
```

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