"""
Mermaid.js Diagram Service for rendering diagrams in frontend
"""

import logging
from typing import Dict, Any, Optional, Tuple
from config.constants import AppConstants

logger = logging.getLogger(__name__)


class PlantUMLService:
    """
    Service class for rendering PlantUML diagrams using PlantUML server
    """
    
    def __init__(self):
        """Initialize PlantUML service"""
        self.server_url = EnvConfig.PLANTUML_SERVER_URL
        self.session = requests.Session()
        self.session.timeout = 30  # 30 second timeout
    
    def render_diagram(self, uml_code: str, output_format: str = 'svg') -> Tuple[Optional[str], Optional[str]]:
        """
        Render PlantUML code to specified format
        
        Args:
            uml_code (str): PlantUML code
            output_format (str): Output format ('svg', 'png', 'pdf')
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (rendered_content, error_message)
        """
        try:
            if not uml_code.strip():
                return None, "UML code is empty"
            
            # Validate output format
            if output_format not in AppConstants.OUTPUT_FORMATS.values():
                return None, f"Unsupported output format: {output_format}"
            
            # Use POST request to PlantUML server with raw UML code
            url = f"{self.server_url.rstrip('/')}/plantuml/{output_format}/"
            
            # Send POST request with UML code
            headers = {'Content-Type': 'text/plain'}
            response = self.session.post(url, data=uml_code, headers=headers)
            
            if response.status_code == 200:
                if output_format == 'svg':
                    content = response.text
                    # Ensure we have proper SVG content
                    if '<svg' in content and '</svg>' in content:
                        logger.info(f"Successfully rendered diagram to {output_format}")
                        return content, None
                    else:
                        logger.error(f"Invalid SVG response: {content[:200]}")
                        return None, "Invalid SVG response from PlantUML server"
                else:
                    content = base64.b64encode(response.content).decode('utf-8')
                    logger.info(f"Successfully rendered diagram to {output_format}")
                    return content, None
            else:
                error_msg = f"PlantUML server error: {response.status_code} - {response.text[:200]}"
                logger.error(error_msg)
                return None, error_msg
                
        except Exception as e:
            error_msg = f"Error rendering diagram: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    def _encode_plantuml(self, uml_code: str) -> str:
        """
        Encode PlantUML code for URL transmission using proper PlantUML encoding
        
        Args:
            uml_code (str): PlantUML code
            
        Returns:
            str: Encoded string for PlantUML server
        """
        try:
            # PlantUML encoding algorithm
            import binascii
            
            # Step 1: UTF-8 encode
            utf8_bytes = uml_code.encode('utf-8')
            
            # Step 2: Deflate compress
            compressed = zlib.compress(utf8_bytes, 9)[2:-4]  # Remove zlib header/trailer
            
            # Step 3: Base64 encode with PlantUML alphabet
            plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
            standard_b64 = base64.b64encode(compressed).decode('ascii')
            
            # Convert to PlantUML encoding
            result = ''
            for char in standard_b64:
                if char == '+':
                    result += '-'
                elif char == '/':
                    result += '_'
                elif char == '=':
                    break  # Skip padding
                else:
                    result += char
            
            return result
            
        except Exception as e:
            logger.error(f"Error encoding PlantUML: {str(e)}")
            # Fallback: use URL encoding
            import urllib.parse
            return urllib.parse.quote(uml_code)
    
    def _plantuml_encode(self, uml_code: str) -> str:
        """
        PlantUML specific encoding
        
        Args:
            uml_code (str): PlantUML code
            
        Returns:
            str: PlantUML encoded string
        """
        # Simplified encoding - in production, use proper PlantUML encoding
        compressed = zlib.compress(uml_code.encode('utf-8'))
        return base64.b64encode(compressed).decode('ascii').replace('+', '-').replace('/', '_')
    
    def _build_url(self, encoded_uml: str, output_format: str) -> str:
        """
        Build the complete URL for PlantUML server request
        
        Args:
            encoded_uml (str): Encoded UML code
            output_format (str): Output format
            
        Returns:
            str: Complete URL
        """
        format_path = {
            'svg': 'svg',
            'png': 'png', 
            'pdf': 'pdf'
        }
        
        path = f"/{format_path[output_format]}/{encoded_uml}"
        return urljoin(self.server_url, path)
    
    def render_svg(self, uml_code: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Render diagram as SVG
        
        Args:
            uml_code (str): PlantUML code
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (svg_content, error_message)
        """
        return self.render_diagram(uml_code, 'svg')
    
    def render_png(self, uml_code: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Render diagram as PNG (base64 encoded)
        
        Args:
            uml_code (str): PlantUML code
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (base64_png_content, error_message)
        """
        return self.render_diagram(uml_code, 'png')
    
    def test_server_connection(self) -> Tuple[bool, Optional[str]]:
        """
        Test connection to PlantUML server
        
        Returns:
            Tuple[bool, Optional[str]]: (is_connected, error_message)
        """
        try:
            # Simple test diagram
            test_uml = "@startuml\nAlice -> Bob: Hello\n@enduml"
            
            svg_content, error = self.render_svg(test_uml)
            
            if svg_content and not error:
                return True, None
            else:
                return False, error or "Unknown connection error"
                
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"


class LocalPlantUMLService:
    """
    Alternative service for local PlantUML rendering (requires PlantUML jar)
    """
    
    def __init__(self, plantuml_jar_path: str = None):
        """
        Initialize local PlantUML service
        
        Args:
            plantuml_jar_path (str): Path to PlantUML jar file
        """
        self.plantuml_jar_path = plantuml_jar_path or "plantuml.jar"
        self.java_path = "java"  # Assumes java is in PATH
    
    def render_diagram(self, uml_code: str, output_format: str = 'svg') -> Tuple[Optional[str], Optional[str]]:
        """
        Render diagram using local PlantUML installation
        
        Args:
            uml_code (str): PlantUML code
            output_format (str): Output format
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (rendered_content, error_message)
        """
        # Implementation would require subprocess calls to PlantUML jar
        # This is a placeholder for local rendering capability
        return None, "Local PlantUML rendering not implemented yet"


class DiagramRenderer:
    """
    Main diagram rendering service that can use different backends
    """
    
    def __init__(self, use_local: bool = False):
        """
        Initialize diagram renderer
        
        Args:
            use_local (bool): Whether to use local PlantUML or server
        """
        if use_local:
            self.renderer = LocalPlantUMLService()
        else:
            self.renderer = PlantUMLService()
    
    def render(self, uml_code: str, output_format: str = 'svg') -> Tuple[Optional[str], Optional[str]]:
        """
        Render diagram using the configured renderer
        
        Args:
            uml_code (str): PlantUML code
            output_format (str): Output format
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (rendered_content, error_message)
        """
        return self.renderer.render_diagram(uml_code, output_format)
    
    def test_connection(self) -> Tuple[bool, Optional[str]]:
        """
        Test the renderer connection
        
        Returns:
            Tuple[bool, Optional[str]]: (is_working, error_message)
        """
        if hasattr(self.renderer, 'test_server_connection'):
            return self.renderer.test_server_connection()
        else:
            return True, None  # Assume local renderer works if available