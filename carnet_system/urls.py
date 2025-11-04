"""
URL configuration for carnet_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from generator import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estudiantes/nuevo/', views.add_student, name='add_student'),
    path('carnet/<int:estudiante_id>/', views.generar_carnet, name='generar_carnet'),
    path('estudiantes/', views.lista_estudiantes, name='lista_estudiantes'),
    path('carnet/pdf/<int:estudiante_id>/', views.carnet_pdf, name='carnet_pdf'),
    path('estudiante/<int:estudiante_id>/carnet/pdf/', views.carnet_pdf, name='carnet_pdf'),
    path('carnets/pdf_todos/', views.carnets_pdf_todos, name='carnets_pdf_todos'),
    path('', views.home, name='home'),
    path('carnet/', views.generar_carnet, name='generar_carnet'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
