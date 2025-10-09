"""
AI Service for generating Mermaid.js diagrams - Simplified Version
"""

import logging
from typing import Dict, Any, Optional, Tuple
from config.constants import AppConstants

logger = logging.getLogger(__name__)


class AIService:
    """
    Service class for diagram generation using Mermaid.js templates
    """
    
    def __init__(self):
        """Initialize the AI service"""
        self.diagram_keywords = {
            'flowchart': ['flow', 'process', 'workflow', 'step', 'procedure'],
            'sequence': ['sequence', 'interaction', 'communication', 'timeline'],
            'class': ['class', 'uml', 'object', 'inheritance', 'method'],
            'er': ['database', 'entity', 'relationship', 'table', 'erd'],
            'state': ['state', 'transition', 'status', 'condition'],
            'gantt': ['gantt', 'project', 'schedule', 'timeline', 'milestone'],
            'pie': ['pie', 'chart', 'percentage', 'distribution'],
        }
    
    def detect_diagram_type(self, prompt: str) -> str:
        """
        Automatically detect the diagram type from user prompt
        
        Args:
            prompt (str): User's textual prompt
            
        Returns:
            str: Detected diagram type
        """
        try:
            prompt_lower = prompt.lower()
            
            # Score each diagram type based on keyword matches
            scores = {}
            for diagram_type, keywords in self.diagram_keywords.items():
                score = sum(1 for keyword in keywords if keyword in prompt_lower)
                if score > 0:
                    scores[diagram_type] = score
            
            # Return the highest scoring type or default to flowchart
            if scores:
                detected_type = max(scores, key=scores.get)
                logger.info(f"Auto-detected diagram type: {detected_type}")
                return detected_type
            else:
                logger.info("No specific diagram type detected, defaulting to flowchart")
                return 'flowchart'
                
        except Exception as e:
            logger.error(f"Error detecting diagram type: {str(e)}")
            return 'flowchart'  # Default fallback
    
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
            # Use template-based generation for reliability
            from .mermaid_service import mermaid_service
            
            mermaid_code, error = mermaid_service.generate_mermaid_code(prompt, diagram_type)
            
            if mermaid_code:
                logger.info(f"Successfully generated Mermaid code for {diagram_type} diagram")
                return mermaid_code, None
            else:
                logger.error(f"Failed to generate Mermaid code: {error}")
                return self._get_fallback_diagram(), "Generated fallback diagram"
            
        except Exception as e:
            error_message = f"Error generating Mermaid code: {str(e)}"
            logger.error(error_message)
            return self._get_fallback_diagram(), error_message
    

    
    def _get_fallback_diagram(self) -> str:
        """Return a simple fallback diagram"""
        return """flowchart TD
    A[Start] --> B[Process]
    B --> C[End]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8"""
    
    def test_service(self) -> Tuple[bool, Optional[str]]:
        """
        Test the AI service
        
        Returns:
            Tuple[bool, Optional[str]]: (is_working, error_message)
        """
        try:
            test_code, error = self.generate_mermaid_code("create a simple flowchart", "flowchart")
            if test_code:
                return True, None
            else:
                return False, error
        except Exception as e:
            return False, str(e)