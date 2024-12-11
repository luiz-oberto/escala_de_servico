from django.shortcuts import render
from escala_servico.models import Militar, Escala
from datetime import date, timedelta
from django.db.models import Q
import calendar
import locale

locale.setlocale(locale.LC_TIME, "pt_br.UTF-8")

data_hoje = date.today()
mes_atual = data_hoje.month
ano_atual = data_hoje.year

def escala(request):
    atualizar_escala()
    data_escala = Escala.objects.order_by('data')

    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    mes = meses_do_ano[mes_atual-1]

    
    context = {
        'mes_atual':mes, 
        'ano_atual': ano_atual,
        'escala': data_escala,
    }

    return render(request, 'escalas/escala_do_mes.html', context)



# Função para gerar um nova escala e deletar a do mês anterior quando necessário
def atualizar_escala():
    # altera o dia data atual para o primeiro dia do mês
    inicio_mes_atual = data_hoje.replace(day=1)
    quantidade_de_dias = calendar.monthrange(ano_atual, mes_atual)[1]

    # Verificar se existe escala para o mês atual
    escala_mes_atual = Escala.objects.filter(mes_referencia=inicio_mes_atual)
    if not escala_mes_atual.exists():
        # Apagar a escala do mês anterior
        Escala.objects.all().delete()
        # Pegar os dias da semana desse mês
        dias_da_semana = generate_weekday(ano_atual, mes_atual)
        # Obter as pessoas e gerar nova escala para o mês
        militares = list(Militar.objects.order_by('-antiguidade'))
 

        indice = 0
        indice_militar = 0
        while indice < quantidade_de_dias:
            data_escala = inicio_mes_atual + timedelta(days=indice) # soma mais um dia
            pessoa_escalada = militares[indice_militar % len(militares)]
            if dias_da_semana[indice] == 'sábado' or dias_da_semana[indice] == 'domingo':
                Escala.objects.create(data=data_escala, dias_da_semana=dias_da_semana[indice],  mes_referencia=inicio_mes_atual)
                indice+=1
            else:
                Escala.objects.create(data=data_escala, pessoa=pessoa_escalada, dias_da_semana=dias_da_semana[indice] ,  mes_referencia=inicio_mes_atual)
                indice+=1
                indice_militar+=1

    return Escala.objects.filter(mes_referencia=inicio_mes_atual)



def generate_weekday(ano_atual, mes_atual):
    # Obter o número de dias no mês de dezembro
    from calendar import monthrange
    dias_no_mes = monthrange(ano_atual, mes_atual)[1]

    # Gerar uma lista com os dias da semana por extenso
    dias_da_semana = [
        (date(ano_atual, mes_atual, dia).strftime("%A"))  # Data e nome do dia
        for dia in range(1, dias_no_mes + 1)
    ]
    # print(dias_da_semana.index('domingo'))
    for dia in dias_da_semana:
        # print(dia)
        if dia == 'terÃ§a-feira':
            index = dias_da_semana.index('terÃ§a-feira')
            dias_da_semana.pop(index)
            dias_da_semana.insert(index, 'terça-feira')
        elif dia == 'sÃ¡bado':
            index = dias_da_semana.index('sÃ¡bado')
            dias_da_semana.pop(index)
            dias_da_semana.insert(index, 'sábado')

    print(dias_da_semana)

    return dias_da_semana