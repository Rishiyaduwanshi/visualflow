"""
URL configuration for diagrams app
"""

from django.urls import path
from . import views

app_name = 'diagrams'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('generate/', views.GenerateDiagramView.as_view(), name='generate'),
    path('display/<uuid:session_id>/', views.DiagramDisplayView.as_view(), name='display'),
    path('download/<uuid:session_id>/', views.DownloadView.as_view(), name='download'),
    path('history/', views.SessionHistoryView.as_view(), name='history'),
]