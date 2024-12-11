from django.test import TestCase

# Create your tests here.
from datetime import date, timedelta

# Definir o mês e ano desejados
ano = 2024
mes = 12

# Obter o número de dias no mês de dezembro
from calendar import monthrange
dias_no_mes = monthrange(ano, mes)[1]

# Gerar uma lista com os dias da semana por extenso
dias_da_semana = [
    (date(ano, mes, dia), date(ano, mes, dia).strftime("%A"))  # Data e nome do dia
    for dia in range(1, dias_no_mes + 1)
]

# Exibir os dias do mês e seus respectivos nomes
for dia, nome_dia in dias_da_semana:
    print(f"{dia.strftime('%d/%m/%Y')} é {nome_dia}")
