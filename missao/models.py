from django.db import models

# Create your models here.

class Missao (models.Model):
    nome_missao = models.CharField(max_length=100)
    descricao_missao = models.TextField(max_length=500)
    pontuacao_missao = models.IntegerField()

    def __str__(self):
        return self.nome_missao

class Ranking(models.Model):
    pontuacao_total = models.IntegerField()
    missao = models.ForeignKey(Missao, on_delete=models.CASCADE, related_name='rankings')
    grupo = models.ForeignKey('sorteio.Grupo', on_delete=models.CASCADE, related_name='rankings')

    def __str__(self):
        return f"{self.grupo} - {self.missao}: {self.pontuacao_total} pts"