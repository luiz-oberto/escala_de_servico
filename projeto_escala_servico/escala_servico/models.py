from django.db import models
from datetime import date, timedelta
import calendar
import locale


locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

class Militar(models.Model):
    nome_de_guerra = models.CharField(max_length=50)
    graduacao = models.CharField(max_length=10)
    antiguidade = models.IntegerField()
    # disponibilidadde = models.BooleanField(default=True)
    ultimo_a_dar_servico = models.BooleanField(default=False)

    # Método para salvar as alterções no banco de dados
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


    def __str__(self):
        return f'{self.data} - {self.pessoa}'

    @classmethod
    def atualizar_escala(cls):
        data_hoje = date.today()
        ano_atual = data_hoje.year
        mes_atual = data_hoje.month

        ##### DATAS PARA TESTES #########
        # data_hoje = date(2025, 5, 1)
        # ano_atual = data_hoje.year
        # mes_atual = data_hoje.month

        # Altera o dia data atual para o primeiro dia do mês
        inicio_mes_atual = data_hoje.replace(day=1)
        quantidade_de_dias = calendar.monthrange(ano_atual, mes_atual)[1]

        # Verificar se existe escala para o mês atual
        print('verificando a escala mais atualizada...')
        escala_mes_atual = cls.objects.filter(mes_referencia=inicio_mes_atual)
        if not escala_mes_atual.exists():
            print('Criando nova escala... AGUARDE')
            # Apagar a escala do mês anterior
            cls.objects.all().delete()

            print('Achando os dias da semana...')
            dias_da_semana = cls.generate_weekday(ano_atual, mes_atual)

            print('Procurando por militares para escalar...')
            militares = cls.verify_last_duty()

            if militares:
                indice = 0
                indice_militar = 0

                while indice < quantidade_de_dias:
                    data_escala = inicio_mes_atual + timedelta(days=indice)  # Soma mais um dia
                    pessoa_escalada = militares[indice_militar % len(militares)] # 

                    if dias_da_semana[indice] in ['sábado', 'domingo']:
                        cls.objects.create(data=data_escala, dias_da_semana=dias_da_semana[indice], mes_referencia=inicio_mes_atual)

                    else:
                        cls.objects.create(data=data_escala, pessoa=pessoa_escalada, dias_da_semana=dias_da_semana[indice], mes_referencia=inicio_mes_atual)

                    indice += 1
                    
                    # Salvar o último que deu serviço no mês 
                    if indice == quantidade_de_dias:
                        militar = Militar.objects.get(nome_de_guerra=pessoa_escalada)
                        militar.ultimo_a_dar_servico = True
                        militar.save()

                        

                    if dias_da_semana[indice - 1] not in ['sábado', 'domingo']:
                        indice_militar += 1
            
            else:
                return print('Não há militares cadastrados.')

        print('Escala criada com sucesso!')
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

    # FUNÇÃO PARA ACERTAR A LISTA DO ÚLTIMO QUE DEU SERVIÇO
    '''
    Algumas falhas ainda pode acontecer caso haja militares cadastrados porém sem ter um que tenha dado serviço
    '''
    @staticmethod
    def verify_last_duty():
        militares = list(Militar.objects.order_by('-antiguidade'))
        try:
            ultimo_que_deu_servico = Militar.objects.get(ultimo_a_dar_servico=True)
            indice = militares.index(ultimo_que_deu_servico)
            nova_ordem = militares[indice + 1:] + militares[:indice + 1]
            print('Nova sequencia criada com sucesso!')
            return nova_ordem
        except Exception as e:
            print(f'Falha: {e}')
            print(f'Nenhum militar deu o último serviço, reiniciando escala a partir do mais moderno... Aguarde')
            # militar mais moderno (antigo) será o primeiro da escala
            Escala.estabelecer_o_ultimo_que_deu_servico()
            


    @classmethod
    def estabelecer_o_ultimo_que_deu_servico(cls):
        mais_moderno = Militar.objects.order_by('-antiguidade').last()
        mais_moderno.ultimo_a_dar_servico = True
        mais_moderno.save()
        cls.verify_last_duty()
        return