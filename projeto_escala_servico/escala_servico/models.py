from django.db import models

# Create your models here.
class Militar(models.Model):
    nome_de_guerra = models.CharField(max_length=50)
    graduacao = models.CharField(max_length=10)
    antiguidade = models.CharField(max_length=4)

    def __str__(self) -> str:
        return f'{self.nome_de_guerra}'