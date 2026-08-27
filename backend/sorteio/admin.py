from django.contrib import admin
from .models import Grupo, Eixo, Usuario, Aluno, Professor, EdicaoSorteio, InscricaoSorteio
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "ra",
        "curso",
        "turno",
    )

    search_fields = (
        "ra",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
    )

    list_filter = (
        "curso",
        "turno",
    )


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
    )


@admin.register(EdicaoSorteio)
class EdicaoSorteioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "turno",
        "ativa",
    )

    list_filter = (
        "turno",
        "ativa",
    )


@admin.register(Eixo)
class EixoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome_eixo",
        "ordem",
        "edicao",
        "quantidade_grupos",
        "capacidade_grupo",
        "ativo",
    )

    list_filter = (
        "edicao",
        "ativo",
    )

    ordering = (
        "edicao",
        "ordem",
    )


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "eixo",
        "numero",
    )

    list_filter = (
        "eixo__edicao",
        "eixo",
    )

    ordering = (
        "eixo",
        "numero",
    )


@admin.register(InscricaoSorteio)
class InscricaoSorteioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "aluno",
        "edicao",
        "eixo",
        "grupo",
        "criado_em",
    )

    list_filter = (
        "edicao",
        "eixo",
        "grupo",
    )

    search_fields = (
        "aluno__ra",
        "aluno__usuario__first_name",
        "aluno__usuario__last_name",
    )