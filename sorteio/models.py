from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
LISTA_CURSOS = (
    ('PEDAGOGIA','Pedagogia')
    ('ENFERMAGEM','Enfermagem')
    ('DIREITO','Direito')
    ('ADS','Ads')
    ('PSICOLOGIA','Psicologia')
    ('PEDAGOGIA EAD','Pedagogia EAD')
)


class Usuarios (models.Model):
    id_usuario = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=25)
    senha = models.CharField(max_length=130)
    nome = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.senha.startswith('pbkdf2_'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

class Alunos (models.Model):
    id_aluno = models.AutoField(primary_key=True)
    ra = models.CharField(max_length=6)
    data_nascimento = models.DateField()
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

class Professores (models.Model):
    id_professor = models.AutoField(primary_key=True)
    curso = models.CharField(max_length=25, choices=LISTA_CURSOS)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)