from django.db import models

# Create your models here.
# mudar para Pessoal
class Militar(models.Model):
    nome_de_guerra = models.CharField(max_length=50)
    graduacao = models.CharField(max_length=10)
    antiguidade = models.CharField(max_length=4)
    ultimo_a_dar_servico = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.ultimo_a_dar_servico:
            # Define todos os outros como False antes de salvar
            Militar.objects.filter(ultimo_a_dar_servico=True).update(ultimo_a_dar_servico=False)
        super(Militar, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.nome_de_guerra}'
    
class Escala(models.Model):
    data = models.DateField(unique=True)
    # dia_da_semana = models.CharField(max_length=3, null=False)
    pessoa = models.ForeignKey('Militar', on_delete=models.CASCADE, null=True)
    mes_referencia = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.data} - {self.pessoa}'

