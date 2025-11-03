from django.db import models
from django.utils import timezone
from config.constants import AppConstants
import uuid


class Session(models.Model):
    """
    Model to store user sessions with prompts, diagram types, and generated UML code
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the session"
    )
    
    prompt = models.TextField(
        help_text="User's textual prompt for diagram generation",
        max_length=2000
    )
    
    diagram_type = models.CharField(
        max_length=20,
        choices=[(value, key) for key, value in AppConstants.DIAGRAM_TYPES.items()],
        help_text="Type of diagram to generate"
    )
    
    generated_uml = models.TextField(
        help_text="Generated Mermaid.js code",
        blank=True,
        null=True
    )
    
    diagram_svg = models.TextField(
        help_text="Generated SVG diagram content",
        blank=True,
        null=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending',
        help_text="Status of diagram generation"
    )
    
    error_message = models.TextField(
        help_text="Error message if generation failed",
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the session was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the session was last updated"
    )
    
    # Optional user association (for future user management)
    user_ip = models.GenericIPAddressField(
        help_text="IP address of the user",
        blank=True,
        null=True
    )
    
    user_agent = models.TextField(
        help_text="User agent string",
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Diagram Session"
        verbose_name_plural = "Diagram Sessions"
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['diagram_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Session {self.id} - {self.diagram_type} - {self.status}"
    
    @property
    def prompt_preview(self):
        """Return a truncated version of the prompt for display"""
        if len(self.prompt) > 100:
            return f"{self.prompt[:100]}..."
        return self.prompt
    
    @property
    def is_completed(self):
        """Check if the session is completed successfully"""
        return self.status == 'completed' and self.generated_uml
    
    @property
    def has_diagram(self):
        """Check if the session has generated diagram content"""
        return bool(self.diagram_svg)
    
    def save(self, *args, **kwargs):
        """Override save to perform validation"""
        # Update status based on content
        if self.generated_uml and not self.error_message:
            if self.status == 'pending' or self.status == 'processing':
                self.status = 'completed'
        elif self.error_message:
            self.status = 'failed'
        
        super().save(*args, **kwargs)


class DiagramTemplate(models.Model):
    """
    Model to store pre-defined diagram templates for different types
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of the template"
    )
    
    diagram_type = models.CharField(
        max_length=20,
        choices=[(value, key) for key, value in AppConstants.DIAGRAM_TYPES.items()],
        help_text="Type of diagram this template is for"
    )
    
    template_prompt = models.TextField(
        help_text="Template prompt with placeholders"
    )
    
    
    description = models.TextField(
        help_text="Description of what this template generates",
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is active"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        ordering = ['diagram_type', 'name']
        verbose_name = "Diagram Template"
        verbose_name_plural = "Diagram Templates"
    
    def __str__(self):
        return f"{self.diagram_type.upper()} - {self.name}"


class DiagramFeedback(models.Model):
    """
    Model to store user feedback on generated diagrams
    """
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rating from 1-5 stars"
    )
    
    feedback_text = models.TextField(
        help_text="User's feedback text",
        blank=True,
        null=True
    )
    
    is_helpful = models.BooleanField(
        help_text="Whether the user found the diagram helpful",
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Diagram Feedback"
        verbose_name_plural = "Diagram Feedback"
    
    def __str__(self):
        return f"Feedback for {self.session.id} - {self.rating} stars"
