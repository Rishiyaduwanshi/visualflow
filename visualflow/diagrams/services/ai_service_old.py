"""
AI Service for generating Mermaid.js diagrams using LangChain and Groq
"""

import logging
from typing import Dict, Any, Optional, Tuple
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from config.env_config import EnvConfig
from config.constants import AppConstants, DiagramPrompts

logger = logging.getLogger(__name__)


class AIService:
    """
    Service class for AI-powered diagram generation using Groq and LangChain
    """
    
    def __init__(self):
        """Initialize the AI service with Groq client"""
        self.groq_client = None
        self.setup_groq_client()
    
    def setup_groq_client(self):
        """Setup the Groq client with API key"""
        try:
            if not EnvConfig.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is not set in environment variables")
            
            self.groq_client = ChatGroq(
                groq_api_key=EnvConfig.GROQ_API_KEY,
                model_name=AppConstants.AI_MODELS['GROQ_MODEL'],
                temperature=AppConstants.AI_MODELS['TEMPERATURE'],
                max_tokens=AppConstants.AI_MODELS['MAX_TOKENS']
            )
            logger.info("Groq client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            raise
    
    def detect_diagram_type(self, prompt: str) -> str:
        """
        Automatically detect the diagram type from user prompt
        
        Args:
            prompt (str): User's textual prompt
            
        Returns:
            str: Detected diagram type
        """
        try:
            detection_prompt = f"""
            Analyze the following prompt and determine what type of diagram should be generated.
            
            Choose from these diagram types:
            - uml: For UML class diagrams, sequence diagrams, use case diagrams
            - erd: For Entity Relationship Diagrams, database schemas
            - dfd: For Data Flow Diagrams, system data flow
            - flowchart: For process flowcharts, decision trees
            - system_design: For system architecture, component diagrams
            - custom: For any other type of diagram
            
            User prompt: "{prompt}"
            
            Respond with only the diagram type (one word): uml, erd, dfd, flowchart, system_design, or custom
            """
            
            messages = [
                SystemMessage(content="You are an expert diagram type classifier."),
                HumanMessage(content=detection_prompt)
            ]
            
            response = self.groq_client.invoke(messages)
            diagram_type = response.content.strip().lower()
            
            # Validate the response
            if diagram_type in AppConstants.DIAGRAM_TYPES.values():
                return diagram_type
            else:
                logger.warning(f"Unknown diagram type detected: {diagram_type}, defaulting to 'custom'")
                return 'custom'
                
        except Exception as e:
            logger.error(f"Error detecting diagram type: {str(e)}")
            return 'custom'  # Default fallback
    
    def generate_mermaid_code(self, prompt: str, diagram_type: str) -> Tuple[str, Optional[str]]:
        """
        Generate Mermaid.js code based on user prompt and diagram type
        
        Args:
            prompt (str): User's textual prompt
            diagram_type (str): Type of diagram to generate
            
        Returns:
            Tuple[str, Optional[str]]: (generated_mermaid_code, error_message)
        """
        try:
            # Use simple template-based generation for reliability
            from .mermaid_service import mermaid_service
            
            mermaid_code, error = mermaid_service.generate_mermaid_code(prompt, diagram_type)
            
            if mermaid_code:
                logger.info(f"Successfully generated Mermaid code for {diagram_type} diagram")
                return mermaid_code, None
            else:
                logger.error(f"Failed to generate Mermaid code: {error}")
                return "", error
            
        except Exception as e:
            error_message = f"Error generating Mermaid code: {str(e)}"
            logger.error(error_message)
            return "", error_message
    
    def generate_plantuml_code(self, prompt: str, diagram_type: str) -> Tuple[str, Optional[str]]:
        """DEPRECATED - Use generate_mermaid_code instead"""
        return self.generate_mermaid_code(prompt, diagram_type)
            return cleaned_uml, None
            
        except Exception as e:
            error_message = f"Error generating PlantUML code: {str(e)}"
            logger.error(error_message)
            return "", error_message
    
    def _get_system_prompt(self, diagram_type: str) -> str:
        """
        Get appropriate system prompt based on diagram type
        
        Args:
            diagram_type (str): Type of diagram
            
        Returns:
            str: System prompt for the AI
        """
        base_prompt = """
        You are an expert PlantUML diagram generator. Your task is to create high-quality, 
        professional PlantUML code based on user requirements.
        
        Key requirements:
        1. Generate ONLY PlantUML code, no explanations or markdown
        2. Start with appropriate @start directive and end with @end directive
        3. Use proper PlantUML syntax and formatting
        4. Include colors, styling, and professional appearance
        5. Ensure the diagram is well-structured and readable
        6. Add appropriate comments in PlantUML format (!comment)
        7. Use meaningful names and labels
        """
        
        specific_prompts = {
            'uml': base_prompt + "\n" + DiagramPrompts.UML_PROMPTS['CLASS_DIAGRAM'],
            'erd': base_prompt + "\n" + DiagramPrompts.ERD_PROMPTS['ENTITY_RELATIONSHIP'],
            'flowchart': base_prompt + "\n" + DiagramPrompts.FLOWCHART_PROMPTS['PROCESS_FLOW'],
            'dfd': base_prompt + "\nGenerate a PlantUML data flow diagram showing system processes, data stores, and external entities.",
            'system_design': base_prompt + "\nGenerate a PlantUML system architecture diagram showing components, services, and their interactions.",
            'custom': base_prompt + "\nGenerate a PlantUML diagram based on the user's specific requirements."
        }
        
        return specific_prompts.get(diagram_type, specific_prompts['custom'])
    
    def _create_user_prompt(self, prompt: str, diagram_type: str) -> str:
        """
        Create user prompt with context and requirements
        
        Args:
            prompt (str): Original user prompt
            diagram_type (str): Type of diagram
            
        Returns:
            str: Enhanced user prompt
        """
        return f"""
        Create a {diagram_type.upper()} diagram for the following requirements:
        
        {prompt}
        
        Requirements:
        - Use professional colors and styling
        - Make it visually appealing and easy to understand
        - Include proper relationships and connections
        - Add meaningful labels and descriptions
        - Ensure the diagram is complete and comprehensive
        
        Generate only the PlantUML code, starting with @start and ending with @end.
        """
    
    def _clean_uml_code(self, uml_code: str, diagram_type: str) -> str:
        """
        Clean and validate the generated UML code
        
        Args:
            uml_code (str): Raw UML code from AI
            diagram_type (str): Type of diagram
            
        Returns:
            str: Cleaned UML code
        """
        # Remove markdown code blocks if present
        if "```" in uml_code:
            lines = uml_code.split('\n')
            cleaned_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block or not line.strip().startswith('```'):
                    cleaned_lines.append(line)
            
            uml_code = '\n'.join(cleaned_lines)
        
        # Ensure proper start/end directives
        uml_code = uml_code.strip()
        
        if not uml_code.startswith('@start'):
            uml_code = f"@startuml\n{uml_code}"
        
        if not uml_code.endswith('@enduml'):
            uml_code = f"{uml_code}\n@enduml"
        
        return uml_code
    
    def validate_uml_syntax(self, uml_code: str) -> Tuple[bool, Optional[str]]:
        """
        Basic validation of PlantUML syntax
        
        Args:
            uml_code (str): PlantUML code to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        try:
            # Basic syntax checks
            if not uml_code.strip():
                return False, "UML code is empty"
            
            if not uml_code.strip().startswith('@start'):
                return False, "UML code must start with @start directive"
            
            if not uml_code.strip().endswith('@enduml'):
                return False, "UML code must end with @enduml directive"
            
            # Check for balanced brackets (basic check)
            open_brackets = uml_code.count('{')
            close_brackets = uml_code.count('}')
            
            if open_brackets != close_brackets:
                return False, f"Unbalanced brackets: {open_brackets} open, {close_brackets} close"
            
            return True, None
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"


class DiagramTypeDetector:
    """
    Enhanced diagram type detection with keyword matching
    """
    
    DIAGRAM_KEYWORDS = {
        'uml': [
            'class', 'classes', 'inheritance', 'method', 'attribute', 'interface',
            'sequence', 'actor', 'lifeline', 'use case', 'extends', 'includes'
        ],
        'erd': [
            'entity', 'relationship', 'database', 'table', 'foreign key', 'primary key',
            'schema', 'one-to-many', 'many-to-many', 'cardinality'
        ],
        'dfd': [
            'data flow', 'process', 'external entity', 'data store', 'bubble',
            'flow', 'input', 'output', 'transform'
        ],
        'flowchart': [
            'flowchart', 'decision', 'process', 'start', 'end', 'if', 'then',
            'loop', 'condition', 'branch', 'flow'
        ],
        'system_design': [
            'system', 'architecture', 'component', 'service', 'microservice',
            'api', 'server', 'client', 'load balancer', 'database'
        ]
    }
    
    @classmethod
    def detect_from_keywords(cls, prompt: str) -> str:
        """
        Detect diagram type based on keywords in prompt
        
        Args:
            prompt (str): User prompt
            
        Returns:
            str: Detected diagram type
        """
        prompt_lower = prompt.lower()
        scores = {}
        
        for diagram_type, keywords in cls.DIAGRAM_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            scores[diagram_type] = score
        
        # Get the diagram type with highest score
        if scores:
            best_type = max(scores, key=scores.get)
            if scores[best_type] > 0:
                return best_type
        
        return 'custom'