# Application Constants
class AppConstants:
    """Central place for all application constants"""
    
    # Diagram Types
    DIAGRAM_TYPES = {
        'UML': 'uml',
        'ERD': 'erd',
        'DFD': 'dfd',
        'FLOWCHART': 'flowchart',
        'SYSTEM_DESIGN': 'system_design',
        'CUSTOM': 'custom'
    }
    
    # PlantUML Diagram Type Mapping
    PLANTUML_DIAGRAM_MAPPING = {
        'uml': '@startuml',
        'erd': '@startuml',
        'dfd': '@startuml',
        'flowchart': '@startuml',
        'system_design': '@startuml',
        'custom': '@startuml'
    }
    
    # AI Model Configuration
    AI_MODELS = {
        'GROQ_MODEL': 'openai/gpt-oss-120b',
        'TEMPERATURE': 0.7,
        'MAX_TOKENS': 2000
    }
    
    # File Upload Settings
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_FILE_EXTENSIONS = ['.txt', '.md', '.json']
    
    # Pagination Settings
    ITEMS_PER_PAGE = 20
    
    # Session Configuration
    SESSION_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds
    
    # PlantUML Output Formats
    OUTPUT_FORMATS = {
        'SVG': 'svg',
        'PNG': 'png',
        'PDF': 'pdf'
    }
    
    # UI Messages
    MESSAGES = {
        'SUCCESS': {
            'DIAGRAM_GENERATED': 'Diagram generated successfully!',
            'SESSION_SAVED': 'Session saved successfully!',
        },
        'ERROR': {
            'GENERATION_FAILED': 'Failed to generate diagram. Please try again.',
            'INVALID_PROMPT': 'Please provide a valid prompt.',
            'API_ERROR': 'API service unavailable. Please try again later.',
            'DATABASE_ERROR': 'Database error occurred. Please try again.',
        },
        'INFO': {
            'PROCESSING': 'Processing your request...',
            'LOADING': 'Loading...',
        }
    }
    
    # Default Prompts for Different Diagram Types
    DEFAULT_PROMPTS = {
        'uml': 'Create a UML class diagram for a simple e-commerce system',
        'erd': 'Create an ERD for a library management system',
        'dfd': 'Create a DFD for an online banking system',
        'flowchart': 'Create a flowchart for user authentication process',
        'system_design': 'Create a system design for a chat application',
        'custom': 'Create a custom diagram'
    }
    
    # Tailwind CSS Classes
    CSS_CLASSES = {
        'BUTTON_PRIMARY': 'bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200',
        'BUTTON_SECONDARY': 'bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200',
        'INPUT_FIELD': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'TEXTAREA': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none',
        'CARD': 'bg-white rounded-lg shadow-md p-6',
        'CONTAINER': 'max-w-6xl mx-auto px-4 sm:px-6 lg:px-8'
    }
    
    # API Endpoints
    API_ENDPOINTS = {
        'GENERATE_DIAGRAM': '/api/generate-diagram/',
        'GET_HISTORY': '/api/history/',
        'DOWNLOAD_DIAGRAM': '/api/download-diagram/',
    }
    
    # Static File Paths
    STATIC_PATHS = {
        'CSS': 'css/',
        'JS': 'js/',
        'IMAGES': 'images/',
        'FONTS': 'fonts/'
    }


class DiagramPrompts:
    """Pre-defined prompts for different diagram types"""
    
    UML_PROMPTS = {
        'CLASS_DIAGRAM': """
        Generate a PlantUML class diagram for the given requirements.
        Include proper relationships (inheritance, composition, aggregation).
        Use appropriate visibility modifiers (+, -, #, ~).
        Add attributes and methods for each class.
        """,
        
        'SEQUENCE_DIAGRAM': """
        Generate a PlantUML sequence diagram showing the interaction flow.
        Include all actors and participants.
        Show proper message flows and lifelines.
        Add activation boxes where appropriate.
        """,
        
        'USE_CASE_DIAGRAM': """
        Generate a PlantUML use case diagram.
        Include actors and use cases.
        Show relationships (extends, includes).
        Group related use cases in packages if needed.
        """
    }
    
    ERD_PROMPTS = {
        'ENTITY_RELATIONSHIP': """
        Generate a PlantUML ERD (Entity Relationship Diagram).
        Include entities with their attributes.
        Show primary keys (PK) and foreign keys (FK).
        Display relationships with proper cardinality.
        Use proper ERD notation.
        """
    }
    
    FLOWCHART_PROMPTS = {
        'PROCESS_FLOW': """
        Generate a PlantUML flowchart for the described process.
        Use appropriate flowchart symbols (start/end, process, decision).
        Show clear flow direction with arrows.
        Include decision points with yes/no branches.
        Ensure logical flow structure.
        """
    }


class ValidationRules:
    """Validation rules and constraints"""
    
    PROMPT_MIN_LENGTH = 10
    PROMPT_MAX_LENGTH = 2000
    
    DIAGRAM_TYPE_VALIDATION = {
        'required': True,
        'choices': list(AppConstants.DIAGRAM_TYPES.values())
    }
    
    FILE_VALIDATION = {
        'max_size': AppConstants.MAX_FILE_SIZE,
        'allowed_extensions': AppConstants.ALLOWED_FILE_EXTENSIONS
    }