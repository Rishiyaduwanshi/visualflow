"""
Mermaid.js Diagram Service - AI-powered diagram generation with two-step approach
"""

import logging
import json
from typing import Dict, Any, Optional, Tuple
from config.constants import AppConstants
from config.env_config import EnvConfig
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

# Import specialized prompts
from .prompts.analyzer_prompt import ANALYZER_PROMPT
from .prompts.flowchart_prompt import FLOWCHART_PROMPT
from .prompts.class_diagram_prompt import CLASS_DIAGRAM_PROMPT
from .prompts.er_diagram_prompt import ER_DIAGRAM_PROMPT
from .prompts.sequence_diagram_prompt import SEQUENCE_DIAGRAM_PROMPT
from .prompts.state_diagram_prompt import STATE_DIAGRAM_PROMPT
from .prompts.dfd_prompt import DFD_PROMPT
from .prompts.system_design_prompt import SYSTEM_DESIGN_PROMPT
from .prompts.custom_prompt import CUSTOM_PROMPT

logger = logging.getLogger(__name__)


class MermaidService:
    """
    Service for generating Mermaid.js diagrams using two-step AI approach:
    Step 1: Analyze user prompt and enhance it
    Step 2: Generate diagram with specialized prompt for that diagram type
    """
    
    def __init__(self):
        """Initialize Mermaid service"""
        self.diagram_types = {
            'flowchart': 'flowchart TD',
            'sequence': 'sequenceDiagram',
            'class': 'classDiagram', 
            'state': 'stateDiagram-v2',
            'er': 'erDiagram',
            'erd': 'erDiagram',
            'uml': 'classDiagram',
            'gantt': 'gantt',
            'pie': 'pie',
            'journey': 'journey',
            'git': 'gitGraph',
            'mindmap': 'mindmap',
            'timeline': 'timeline',
            'quadrant': 'quadrantChart'
        }
        
        # Map diagram types to their specialized prompts
        self.prompt_map = {
            'flowchart': FLOWCHART_PROMPT,
            'sequence': SEQUENCE_DIAGRAM_PROMPT,
            'class': CLASS_DIAGRAM_PROMPT,
            'uml': CLASS_DIAGRAM_PROMPT,
            'er': ER_DIAGRAM_PROMPT,
            'erd': ER_DIAGRAM_PROMPT,
            'state': STATE_DIAGRAM_PROMPT,
            'dfd': DFD_PROMPT,
            'system_design': SYSTEM_DESIGN_PROMPT,
            'custom': CUSTOM_PROMPT,
        }
        
        # Initialize AI client
        try:
            self.groq_client = ChatGroq(
                groq_api_key=EnvConfig.GROQ_API_KEY,
                model_name="openai/gpt-oss-120b",
                temperature=0.3
            )
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            self.groq_client = None
    
    def generate_mermaid_code(self, prompt: str, diagram_type: str = 'flowchart') -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Generate Mermaid.js code using AI based on prompt and diagram type
        
        Args:
            prompt (str): User prompt describing the diagram
            diagram_type (str): Type of diagram to generate
            
        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]]: (mermaid_code, error_message, detected_diagram_type)
        """
        try:
            if not prompt.strip():
                return None, "Prompt cannot be empty", None
            
            # Use AI to generate if available
            if self.groq_client:
                return self._generate_with_ai(prompt, diagram_type)
            else:
                # Fallback to templates
                code, error = self._generate_fallback(prompt, diagram_type)
                return code, error, None
            
        except Exception as e:
            error_msg = f"Error generating Mermaid code: {str(e)}"
            logger.error(error_msg)
            return None, error_msg, None
            
    def _generate_with_ai(self, prompt: str, diagram_type: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Generate Mermaid code using TWO-STEP AI approach:
        Step 1: Analyze and enhance user prompt
        Step 2: Generate diagram with specialized prompt
        
        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]]: (mermaid_code, error_message, detected_diagram_type)
        """
        try:
            # STEP 1: Analyze user prompt to understand intent and enhance it
            logger.info(f"Step 1: Analyzing user prompt for diagram type: {diagram_type}")
            analysis = self._analyze_prompt(prompt, diagram_type)
            
            detected_type = None
            if not analysis:
                logger.warning("Analysis failed, using original prompt")
                enhanced_prompt = prompt
                final_diagram_type = diagram_type
            else:
                enhanced_prompt = analysis.get('enhanced_prompt', prompt)
                detected_type = analysis.get('diagram_type', diagram_type)
                
                # Use analyzed diagram type if confidence is high
                if analysis.get('confidence', 0) > 0.7:
                    final_diagram_type = detected_type
                else:
                    final_diagram_type = diagram_type
                
                logger.info(f"Analysis complete. Final diagram type: {final_diagram_type}")
                logger.info(f"Enhanced prompt: {enhanced_prompt[:100]}...")
            
            # STEP 2: Generate diagram using specialized prompt
            logger.info(f"Step 2: Generating Mermaid code with specialized prompt")
            mermaid_code = self._generate_with_specialized_prompt(enhanced_prompt, final_diagram_type)
            
            if not mermaid_code:
                logger.error("Failed to generate with specialized prompt, using fallback")
                code, error = self._generate_fallback(prompt, diagram_type)
                return code, error, detected_type
            
            # Clean and fix syntax errors
            mermaid_code = self._clean_ai_response(mermaid_code)
            mermaid_code = self._fix_syntax_errors(mermaid_code)
            
            logger.info(f"Successfully generated Mermaid code for {final_diagram_type} diagram")
            return mermaid_code, None, final_diagram_type
            
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            code, error = self._generate_fallback(prompt, diagram_type)
            return code, error, None
    
    def _analyze_prompt(self, prompt: str, diagram_type: str) -> Optional[Dict]:
        """
        STEP 1: Analyze user prompt to understand requirements
        Returns analysis with enhanced prompt
        """
        try:
            user_message = f"""
User Prompt: "{prompt}"
Suggested Diagram Type: {diagram_type}

Analyze this prompt and return the JSON response.
"""
            
            response = self.groq_client.invoke([
                SystemMessage(ANALYZER_PROMPT),
                HumanMessage(user_message)
            ])
            
            # Parse JSON response
            content = response.content.strip()
            
            # Remove markdown code blocks if present
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            analysis = json.loads(content)
            logger.info(f"Prompt analysis successful: {analysis.get('diagram_type')} (confidence: {analysis.get('confidence')})")
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse analysis JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Prompt analysis failed: {e}")
            return None
    
    def _generate_with_specialized_prompt(self, prompt: str, diagram_type: str) -> Optional[str]:
        """
        STEP 2: Generate diagram using specialized system prompt for the diagram type
        """
        try:
            # Get the specialized prompt for this diagram type
            system_prompt = self.prompt_map.get(diagram_type)
            
            if not system_prompt:
                logger.warning(f"No specialized prompt for {diagram_type}, using generic approach")
                system_prompt = FLOWCHART_PROMPT  # Default fallback
            
            user_message = f"""
User Request: {prompt}

Generate the {diagram_type} diagram now.
"""
            
            response = self.groq_client.invoke([
                SystemMessage(system_prompt),
                HumanMessage(user_message)
            ])
            
            mermaid_code = response.content.strip()
            logger.info(f"Generated Mermaid code using specialized {diagram_type} prompt")
            
            return mermaid_code
            
        except Exception as e:
            logger.error(f"Specialized prompt generation failed: {e}")
            return None
            
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
    
    def _fix_syntax_errors(self, mermaid_code: str) -> str:
        """
        Fix common Mermaid syntax errors
        
        This method fixes:
        1. Emojis in node IDs (moves them to labels only)
        2. ER diagram attribute syntax (type name PK/FK format)
        3. ER diagram invalid relationship cardinality
        4. Reserved keywords as node IDs (adds 'Node' suffix)
        5. Class diagram tilde syntax for generics
        6. Removes unsupported styling directives
        """
        import re
        
        mermaid_code = re.sub(r'(\w+)~([^~]+)~', r'\1<\2>', mermaid_code)
        
        # Fix emojis in node IDs (move them to labels)
        # Pattern: emoji[label] should become nodeId[emoji label]
        def fix_emoji_nodes(match):
            full_match = match.group(0)
            emoji_part = match.group(1)
            label_part = match.group(2)
            
            # Generate a clean node ID from the label
            clean_id = re.sub(r'[^a-zA-Z0-9_]', '', label_part)
            if not clean_id:
                clean_id = f"Node{hash(emoji_part) % 10000}"
            
            # Return the corrected format: nodeId[emoji label]
            return f"{clean_id}[{emoji_part} {label_part}]"
        
        # Match patterns like: 🧑‍🎓[Student] or 🏢[Admin]
        mermaid_code = re.sub(r'([^\w\s\[\]]+)\[([^\]]+)\]', fix_emoji_nodes, mermaid_code)
        
        # Fix ER Diagram attribute syntax
        # Incorrect: PK attributeName or FK attributeName
        # Correct: type attributeName PK or type attributeName FK
        def fix_er_attribute(match):
            indent = match.group(1)
            key_type = match.group(2)  # PK or FK
            attr_name = match.group(3)
            
            # Default to string type, append key constraint
            return f"{indent}string {attr_name} {key_type}"
        
        # Match patterns like: "        PK bookId" or "        FK authorId"
        mermaid_code = re.sub(
            r'^(\s+)(PK|FK)\s+(\w+)\s*$',
            fix_er_attribute,
            mermaid_code,
            flags=re.MULTILINE
        )
        
        # Also fix patterns like "        PK bookId string" (reversed order)
        def fix_er_attribute_reversed(match):
            indent = match.group(1)
            key_type = match.group(2)  # PK or FK
            attr_name = match.group(3)
            attr_type = match.group(4)
            
            return f"{indent}{attr_type} {attr_name} {key_type}"
        
        mermaid_code = re.sub(
            r'^(\s+)(PK|FK)\s+(\w+)\s+(\w+)\s*$',
            fix_er_attribute_reversed,
            mermaid_code,
            flags=re.MULTILINE
        )
        
        # Fix composite keys: int book_id PK FK -> int book_id PK (remove duplicate constraints)
        # Mermaid doesn't support multiple constraints on one attribute
        mermaid_code = re.sub(
            r'(\s+\w+\s+\w+)\s+(PK|FK)\s+(PK|FK)',
            r'\1 \2',  # Keep only first constraint
            mermaid_code
        )
        
        # Fix ER Diagram invalid relationship syntax
        # Valid Mermaid ER relationships: ||--||, ||--o{, }o--||, }|--||, ||--|{, }o--o|, etc.
        # Invalid patterns like }o--o{ need to be fixed
        # Replace invalid combinations with valid ones
        er_relationship_fixes = {
            r'\}o--o\{': '}o--o|',  # many-to-optional-many -> many-to-optional-one
            r'\}\|--\|\{': '}|--|{',  # Fix malformed many-to-many
        }
        
        for invalid_pattern, valid_replacement in er_relationship_fixes.items():
            mermaid_code = re.sub(invalid_pattern, valid_replacement, mermaid_code)
        
        # Fix Class Diagram relationship multiplicity syntax
        # Incorrect: Order "*--" ShoppingCart or Customer "1" --> "*" Order
        # Correct: Order "1" *-- "1" ShoppingCart or Customer "1" --> "0..*" Order
        
        # Fix missing quotes around multiplicity on LEFT side of relationship
        # Pattern: ClassName multiplicity relationship (without quotes)
        mermaid_code = re.sub(
            r'(\w+)\s+(\d+|\*|0\.\.1|1\.\.\*|0\.\.\*)\s+(-->|<\|--|o--|\.\.>|\*--|\.\.)',
            r'\1 "\2" \3',
            mermaid_code
        )
        
        # Fix missing quotes around multiplicity on RIGHT side before second class
        # Pattern: relationship multiplicity ClassName (without quotes)
        mermaid_code = re.sub(
            r'(-->|<\|--|o--|\.\.>|\*--|\.\.)\s+(\d+|\*|0\.\.1|1\.\.\*|0\.\.\*)\s+(\w+)',
            r'\1 "\2" \3',
            mermaid_code
        )
        
        # Fix patterns like: Order "*--" ShoppingCart : contains
        # Should be: Order "1" *-- "*" ShoppingCart : contains
        # Match: ClassName "*--" ClassName (missing multiplicity on one side)
        mermaid_code = re.sub(
            r'(\w+)\s+"([^"]+)"\s+(\*--|o--|<\|--)\s+(\w+)',
            r'\1 "\2" \3 "1" \4',
            mermaid_code
        )
        
        # Reverse case: ClassName *-- "*" ClassName (missing left multiplicity)
        mermaid_code = re.sub(
            r'(\w+)\s+(\*--|o--|<\|--)\s+"([^"]+)"\s+(\w+)',
            r'\1 "1" \2 "\3" \4',
            mermaid_code
        )
        
        # Fix reserved keywords in node IDs
        # Mermaid reserved words that cannot be used as node IDs
        reserved_keywords = ['end', 'start', 'subgraph', 'graph', 'classDef', 'class', 'click', 'callback', 'link', 'style']
        
        for keyword in reserved_keywords:
            # Replace reserved keyword as standalone node ID: end[label] -> endNode[label]
            mermaid_code = re.sub(
                rf'\b{keyword}\[',
                f'{keyword}Node[',
                mermaid_code,
                flags=re.IGNORECASE
            )
            # Also fix in connections: --> end or --> end[label]
            mermaid_code = re.sub(
                rf'(-->|---)\s+{keyword}(?=\[|\s|$)',
                rf'\1 {keyword}Node',
                mermaid_code,
                flags=re.IGNORECASE
            )
            # Fix source nodes: end --> or end[label] -->
            mermaid_code = re.sub(
                rf'\b{keyword}(?=\s*(?:-->|---))',
                f'{keyword}Node',
                mermaid_code,
                flags=re.IGNORECASE
            )
        
        lines = mermaid_code.split('\n')
        clean_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('classDef '):
                logger.debug(f"Removed classDef line: {stripped}")
                continue
            
            if stripped.startswith('class ') and '{' not in line and '--' not in line:
                logger.debug(f"Removed class styling: {stripped}")
                continue
            
            # Keep all other lines
            clean_lines.append(line)
        
        mermaid_code = '\n'.join(clean_lines)
        
        logger.info("Applied syntax fixes to Mermaid code (removed styling, fixed emoji nodes, ER attributes, ER relationships, and reserved keywords)")
        return mermaid_code.strip()
    
    def test_service(self) -> Tuple[bool, Optional[str]]:
        """
        Test the Mermaid service
        
        Returns:
            Tuple[bool, Optional[str]]: (is_working, error_message)
        """
        try:
            test_code, error, _ = self.generate_mermaid_code("test diagram", "flowchart")
            if test_code:
                return True, None
            else:
                return False, error
        except Exception as e:
            return False, str(e)


mermaid_service = MermaidService()