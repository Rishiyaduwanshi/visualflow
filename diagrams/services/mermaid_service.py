"""
Mermaid.js Diagram Service - AI-powered diagram generation
"""

import logging
from typing import Dict, Any, Optional, Tuple
from config.constants import AppConstants
from config.env_config import EnvConfig
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

logger = logging.getLogger(__name__)


class MermaidService:
    """
    Service for generating Mermaid.js diagrams (frontend rendering)
    """
    
    def __init__(self):
        """Initialize Mermaid service"""
        self.diagram_types = {
            'flowchart': 'flowchart TD',
            'sequence': 'sequenceDiagram',
            'class': 'classDiagram', 
            'state': 'stateDiagram-v2',
            'er': 'erDiagram',
            'gantt': 'gantt',
            'pie': 'pie',
            'journey': 'journey',
            'git': 'gitGraph',
            'mindmap': 'mindmap',
            'timeline': 'timeline',
            'quadrant': 'quadrantChart'
        }
        
        # Initialize AI client
        try:
            self.groq_client = ChatGroq(
                groq_api_key=EnvConfig.GROQ_API_KEY,
                model_name="openai/gpt-oss-120b"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            self.groq_client = None
    
    def generate_mermaid_code(self, prompt: str, diagram_type: str = 'flowchart') -> Tuple[Optional[str], Optional[str]]:
        """
        Generate Mermaid.js code using AI based on prompt and diagram type
        
        Args:
            prompt (str): User prompt describing the diagram
            diagram_type (str): Type of diagram to generate
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (mermaid_code, error_message)
        """
        try:
            if not prompt.strip():
                return None, "Prompt cannot be empty"
            
            # Use AI to generate if available
            if self.groq_client:
                return self._generate_with_ai(prompt, diagram_type)
            else:
                # Fallback to templates
                return self._generate_fallback(prompt, diagram_type)
            
        except Exception as e:
            error_msg = f"Error generating Mermaid code: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
            
    def _generate_with_ai(self, prompt: str, diagram_type: str) -> Tuple[Optional[str], Optional[str]]:
        """Generate Mermaid code using AI"""
        try:
            # Create comprehensive AI prompt
            ai_prompt = f"""
You are an expert in Mermaid.js diagram generation. Generate a professional, well-structured Mermaid diagram based on the user's description.

User Request: "{prompt}"
Diagram Type: {diagram_type}

Requirements:
1. Generate ONLY valid Mermaid.js syntax
2. Make it visually appealing with proper styling
3. Use appropriate colors and styling
4. Ensure proper node connections and flow
5. Make it comprehensive and detailed based on the description

Generate the Mermaid code now:
"""
            
            # Get AI response
            response = self.groq_client.invoke([HumanMessage(content=ai_prompt)])
            mermaid_code = response.content.strip()
            
            # Clean the response
            mermaid_code = self._clean_ai_response(mermaid_code)
            
            logger.info(f"AI generated Mermaid code for {diagram_type} diagram")
            return mermaid_code, None
            
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            # Fallback to templates
            return self._generate_fallback(prompt, diagram_type)
            
    def _clean_ai_response(self, response: str) -> str:
        """Clean AI response to extract only Mermaid code"""
        # Remove code blocks if present
        if "```mermaid" in response:
            start = response.find("```mermaid") + 10
            end = response.find("```", start)
            if end != -1:
                response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.rfind("```")
            if end != -1 and end > start:
                response = response[start:end].strip()
        
        return response.strip()
        
    def _generate_fallback(self, prompt: str, diagram_type: str) -> Tuple[Optional[str], Optional[str]]:
        """Fallback template generation"""
        try:
            starter = self.diagram_types.get(diagram_type, 'flowchart TD')
            
            if diagram_type == 'flowchart' or diagram_type == 'custom':
                mermaid_code = self._generate_flowchart(prompt, starter)
            elif diagram_type == 'sequence':
                mermaid_code = self._generate_sequence_diagram(prompt)
            elif diagram_type == 'class' or diagram_type == 'uml':
                mermaid_code = self._generate_class_diagram(prompt)
            elif diagram_type == 'er' or diagram_type == 'erd':
                mermaid_code = self._generate_er_diagram(prompt)
            else:
                mermaid_code = self._generate_flowchart(prompt, starter)
            
            return mermaid_code, None
            
        except Exception as e:
            return None, f"Fallback generation failed: {str(e)}"
    
    def _generate_flowchart(self, prompt: str, starter: str = 'flowchart TD') -> str:
        """Generate flowchart Mermaid code"""
        return f"""flowchart TD
    A[Start] --> B[User Input]
    B --> C[Process Request]
    C --> D{{Validate}}
    D -->|Valid| E[Execute Action]
    D -->|Invalid| F[Show Error]
    E --> G[Return Result]
    F --> B
    G --> H[End]"""
    
    def _generate_sequence_diagram(self, prompt: str) -> str:
        """Generate sequence diagram Mermaid code"""
        return """sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database
    
    User->>Frontend: User Action
    Frontend->>Backend: API Request
    Backend->>Database: Query Data
    Database-->>Backend: Return Data
    Backend-->>Frontend: API Response
    Frontend-->>User: Update UI
    
    Note over User,Database: System Interaction Flow"""
    
    def _generate_class_diagram(self, prompt: str) -> str:
        """Generate class diagram Mermaid code"""
        return """classDiagram
    class User {
        +id: int
        +name: string
        +email: string
        +login()
        +logout()
    }
    
    class Session {
        +id: string
        +userId: int
        +createdAt: datetime
        +isActive: boolean
        +create()
        +destroy()
    }
    
    class Diagram {
        +id: string
        +type: string
        +content: string
        +createdAt: datetime
        +generate()
        +save()
    }
    
    User ||--o{ Session : has
    User ||--o{ Diagram : creates
    
    %% Styling
    class User,Session,Diagram fill:#e3f2fd,stroke:#1976d2"""
    
    def _generate_er_diagram(self, prompt: str) -> str:
        """Generate ER diagram Mermaid code"""
        return """erDiagram
    USER {
        int id PK
        string username
        string email
        datetime created_at
    }
    
    SESSION {
        string id PK
        int user_id FK
        string diagram_type
        text prompt
        text generated_code
        datetime created_at
    }
    
    DIAGRAM_TEMPLATE {
        int id PK
        string name
        string type
        text template_code
        boolean is_active
    }
    
    USER ||--o{ SESSION : creates
    DIAGRAM_TEMPLATE ||--o{ SESSION : uses"""
    
    def _generate_state_diagram(self, prompt: str) -> str:
        """Generate state diagram Mermaid code"""
        return """stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : User Input
    Processing --> Generating : Valid Input
    Processing --> Error : Invalid Input
    Generating --> Completed : Success
    Generating --> Error : Failed
    Error --> Idle : Retry
    Completed --> Idle : New Request
    Completed --> [*] : Exit
    
    state Processing {
        [*] --> Validating
        Validating --> Parsing
        Parsing --> [*]
    }"""

    def test_service(self) -> Tuple[bool, Optional[str]]:
        """
        Test the Mermaid service
        
        Returns:
            Tuple[bool, Optional[str]]: (is_working, error_message)
        """
        try:
            test_code, error = self.generate_mermaid_code("test diagram", "flowchart")
            if test_code:
                return True, None
            else:
                return False, error
        except Exception as e:
            return False, str(e)


# Create service instance for easy import
mermaid_service = MermaidService()