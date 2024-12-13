from django.db import models
from datetime import date, timedelta
import calendar
import locale


locale.setlocale(locale.LC_TIME, "pt_br.UTF-8")

# Create your models here.
# mudar para Pessoal
class Militar(models.Model):
    nome_de_guerra = models.CharField(max_length=50)
    graduacao = models.CharField(max_length=10)
    antiguidade = models.IntegerField()
    # disponibilidadde = models.BooleanField(default=True)
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
    dias_da_semana = models.CharField(max_length=50)
    pessoa = models.ForeignKey('Militar', on_delete=models.CASCADE, null=True, blank=True)
    mes_referencia = models.DateField(null=True, blank=True)
    # mes = atributo que salvará o mês da escala
    # ano = atributo que vai salvar o ano da escala

    def __str__(self):
        return f'{self.data} - {self.pessoa}'

    @classmethod
    def atualizar_escala(cls):
        data_hoje = date.today()
        ano_atual = data_hoje.year
        mes_atual = data_hoje.month

        ##### DATAS PARA TESTES #########
        # data_hoje = date(2025, 2, 1)
        # ano_atual = data_hoje.year
        # mes_atual = data_hoje.month

        # Altera o dia data atual para o primeiro dia do mês
        inicio_mes_atual = data_hoje.replace(day=1)
        quantidade_de_dias = calendar.monthrange(ano_atual, mes_atual)[1]

        # Verificar se existe escala para o mês atual
        escala_mes_atual = cls.objects.filter(mes_referencia=inicio_mes_atual)
        if not escala_mes_atual.exists():
            # Apagar a escala do mês anterior
            cls.objects.all().delete()

            # Pegar os dias da semana desse mês
            dias_da_semana = cls.generate_weekday(ano_atual, mes_atual)

            # Obter as pessoas e gerar nova escala para o mês
            militares = list(Militar.objects.order_by('-antiguidade'))

            indice = 0
            indice_militar = 0
            while indice < quantidade_de_dias:
                data_escala = inicio_mes_atual + timedelta(days=indice)  # Soma mais um dia
                pessoa_escalada = militares[indice_militar % len(militares)]

                if dias_da_semana[indice] in ['sábado', 'domingo']:
                    cls.objects.create(data=data_escala, dias_da_semana=dias_da_semana[indice], mes_referencia=inicio_mes_atual)
                else:
                    cls.objects.create(data=data_escala, pessoa=pessoa_escalada, dias_da_semana=dias_da_semana[indice], mes_referencia=inicio_mes_atual)

                indice += 1
                if dias_da_semana[indice - 1] not in ['sábado', 'domingo']:
                    indice_militar += 1

        return data_hoje, cls.objects.filter(mes_referencia=inicio_mes_atual)

    @staticmethod
    def generate_weekday(ano_atual, mes_atual):
        # Obter o número de dias no mês de dezembro
        from calendar import monthrange
        dias_no_mes = monthrange(ano_atual, mes_atual)[1]

        # Gerar uma lista com os dias da semana por extenso
        dias_da_semana = [
            (date(ano_atual, mes_atual, dia).strftime("%A"))  # Data e nome do dia
            for dia in range(1, dias_no_mes + 1)
        ]
        
        # Ajusta o nome dos dias da semana
        for dia in dias_da_semana:
            if dia == 'terÃ§a-feira':
                index = dias_da_semana.index('terÃ§a-feira')
                dias_da_semana.pop(index)
                dias_da_semana.insert(index, 'terça-feira')
            elif dia == 'sÃ¡bado':
                index = dias_da_semana.index('sÃ¡bado')
                dias_da_semana.pop(index)
                dias_da_semana.insert(index, 'sábado')

        return dias_da_semana

