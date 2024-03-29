"""agendaCovid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from agenda.views import *


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('pag_inicial', pag_inicial, name='pag_inicial'),
    path('logout', logout_view, name="logout"),
    path('agendamento', agendamento, name="agendamento"),
    path('visu_agendamento', visu_agendamento, name="visu_agendamento"),
    path('telaAdmin', telaAdmin, name="telaAdmin"),
    path('graficoBarra', graficoBarra, name="graficoBarra"),
    path('graficoPizza', graficoPizza, name="graficoPizza"),







]
