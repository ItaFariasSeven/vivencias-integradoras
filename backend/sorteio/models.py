from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Curso (models.TextChoices):
        PEDAGOGIA ='PEDAGOGIA','Pedagogia'
        ENFERMAGEM = 'ENFERMAGEM','Enfermagem'
        DIREITO ='DIREITO','Direito'
        ADS = 'ADS','Ads'
        PSICOLOGIA = 'PSICOLOGIA','Psicologia'
        PEDAGOGIA_EAD ='PEDAGOGIA_EAD','Pedagogia EAD'

class Turno(models.TextChoices):
    MATUTINO = 'MATUTINO', 'Matutino'
    NOTURNO = 'NOTURNO', 'Noturno'


class Usuario(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name"]

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'
    


class Aluno (models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_aluno')
    ra = models.CharField(max_length=10, unique=True)
    data_nascimento = models.DateField()
    curso = models.CharField(max_length=25, choices=Curso.choices)
    turno = models.CharField(max_length=10, choices=Turno.choices)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - RA: {self.ra}"

class Professor (models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_professor')

    def __str__(self):
        return f"Prof. {self.usuario.get_full_name()}"

class EdicaoSorteio(models.Model):
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=10 , choices=Turno.choices)
    ativa = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["turno"],
                condition=Q(ativa=True),
                name="uma_edicao_ativa_por_turno"
            )
        ]

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()}"

class Eixo(models.Model):
    edicao = models.ForeignKey(EdicaoSorteio, on_delete=models.CASCADE, related_name='eixos')
    nome_eixo = models.CharField(max_length=100)
    ordem = models.PositiveSmallIntegerField()
    quantidade_grupos = models.PositiveSmallIntegerField(default=4)
    capacidade_grupo = models.PositiveSmallIntegerField(default=10)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordem']

        constraints = [
            models.UniqueConstraint(
                fields=['edicao', 'ordem'],
                name='eixo_ordem_unica_por_edicao'
            )
        ]

    def __str__(self):
        return self.nome_eixo
    

class Grupo (models.Model):
    eixo = models.ForeignKey(Eixo, on_delete=models.CASCADE, related_name='grupos')
    numero = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['numero']

        constraints = [
            models.UniqueConstraint(
                fields=['eixo', 'numero'],
                name='grupo_numero_unico_por_eixo'
            )
        ]

    @property
    def nome(self):
        return f'Grupo {self.numero}'

    def __str__(self):
        return f'{self.eixo.nome_eixo} - Grupo {self.numero}'
    

class InscricaoSorteio(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='inscricoes_sorteio')
    edicao = models.ForeignKey(EdicaoSorteio, on_delete=models.PROTECT, related_name='inscricoes')
    eixo = models.ForeignKey(Eixo, on_delete=models.PROTECT, related_name='inscricoes')
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT, related_name='inscricoes')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['aluno', 'edicao'],
                name='aluno_um_sorteio_por_edicao'
            )
        ]
    def __str__(self):
        return (
            f'{self.aluno}'
            f'{self.eixo}'
            f'{self.grupo.nome}'
        )
    