from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Usuario (AbstractUser):
    LISTA_CURSOS = (
        ('PEDAGOGIA','Pedagogia'),
        ('ENFERMAGEM','Enfermagem'),
        ('DIREITO','Direito'),
        ('ADS','Ads'),
        ('PSICOLOGIA','Psicologia'),
        ('PEDAGOGIA_EAD','Pedagogia EAD')
    )
    email = models.EmailField(max_length=100, unique=True)
    curso = models.CharField(max_length=25, choices=LISTA_CURSOS)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

class Aluno (models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_aluno')
    ra = models.CharField(max_length=10, unique=True)
    data_nascimento = models.DateField()

    def __str__(self):
        return f"Aluno: {self.usuario.get_full_name()} - RA: {self.ra}"

class Professor (models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_professor')

    def __str__(self):
        return f"Prof. {self.usuario.get_full_name()}"

class Grupo (models.Model):
    nome_grupo = models.CharField(max_length=50)
    integrantes = models.ManyToManyField(Usuario, related_name='grupos')
    lider_grupo = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grupos_liderados'
    )
    foto_perfil = models.ImageField(upload_to='imagens/perfil', null=True, blank=True)
    foto_grupo_em_missao = models.ImageField(upload_to='imagens/emmissao', null=True, blank=True)
    nome_missao = models.ForeignKey('missao.Missao', on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos')

    def __str__(self):
        return self.nome_grupo

class Eixo (models.Model):
    nome_eixo = models.CharField(max_length=100)
    quantidade_grupos_por_eixo = models.IntegerField(default=4)
    quantidade_pessoas_grupo = models.IntegerField(default=10)
    professores_responsaveis = models.ManyToManyField(Professor, related_name='eixos')

    def __str__(self):
        return self.nome_eixo