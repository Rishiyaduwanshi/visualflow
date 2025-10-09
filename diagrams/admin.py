from django.contrib import admin
from .models import Session, DiagramTemplate, DiagramFeedback
from config.constants import AppConstants


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
        return '✅' if obj.has_diagram else '❌'
    has_diagram.short_description = 'Has Diagram'
    has_diagram.boolean = True


@admin.register(DiagramTemplate)
class DiagramTemplateAdmin(admin.ModelAdmin):
    """Admin interface for DiagramTemplate model"""
    
    list_display = [
        'name', 'diagram_type', 'is_active', 'created_at'
    ]
    
    list_filter = [
        'diagram_type', 'is_active', 'created_at'
    ]
    
    search_fields = [
        'name', 'description', 'template_prompt'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'diagram_type', 'is_active')
        }),
        ('Template Content', {
            'fields': ('template_prompt', 'sample_uml', 'description')
        }),
    )


@admin.register(DiagramFeedback)
class DiagramFeedbackAdmin(admin.ModelAdmin):
    """Admin interface for DiagramFeedback model"""
    
    list_display = [
        'session', 'rating', 'is_helpful', 'created_at'
    ]
    
    list_filter = [
        'rating', 'is_helpful', 'created_at'
    ]
    
    search_fields = [
        'feedback_text', 'session__prompt'
    ]
    
    readonly_fields = [
        'session', 'created_at'
    ]
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('session')
