from django.contrib import admin
from .models import Usuarios, Professores, Alunos

# Register your models here.

admin.site.register(Usuarios)
admin.site.register(Professores)
admin.site.register(Alunos)