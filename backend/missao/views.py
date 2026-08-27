from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .models import Usuario, Aluno, Professor, Grupo, Eixo

# Create your views here.

class Homepage(TemplateView):
    template_name = "homepage"

class Login(LoginView):
    template_name = "login"
    redirect_authenticated_user = True

