from django.contrib import admin
from .models import Session, Contact
from config.constants import AppConstants

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin interface for Session model"""
    
    list_display = [
        'id', 'prompt_preview', 'diagram_type', 'status', 
        'created_at', 'has_diagram'
    ]
    
    list_filter = [
        'diagram_type', 'status', 'created_at'
    ]
    
    search_fields = [
        'prompt', 'id'
    ]
    
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'user_ip', 'user_agent'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'prompt', 'diagram_type', 'status')
        }),
        ('Generated Content', {
            'fields': ('generated_uml', 'diagram_svg', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'user_ip', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def prompt_preview(self, obj):
        """Display truncated prompt"""
        return obj.prompt_preview
    prompt_preview.short_description = 'Prompt Preview'
    
    def has_diagram(self, obj):
        """Display if session has diagram"""
        return obj.has_diagram
    has_diagram.short_description = 'Has Diagram'
    has_diagram.boolean = True

