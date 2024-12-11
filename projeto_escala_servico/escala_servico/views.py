from django.shortcuts import render
from escala_servico.models import Militar, Escala
from datetime import date, timedelta
from django.db.models import Q
import calendar

data_hoje = date.today()
mes_atual = data_hoje.month
ano_atual = data_hoje.year
dia_da_semana = data_hoje.isoweekday()

# Função para deletar a escala do mês anterior e gerar nova
def atualizar_escala():
    # altera o dia data atual para o primeiro dia do mês
    inicio_mes_atual = data_hoje.replace(day=1)
    quantidade_de_dias = calendar.monthrange(ano_atual, mes_atual)[1]

    # Verificar se existe escala para o mês atual
    escala_mes_atual = Escala.objects.filter(mes_referencia=inicio_mes_atual)

    if not escala_mes_atual.exists():
        # Apagar a escala do mês anterior
        Escala.objects.all().delete()

        # Obter as pessoas e gerar nova escala para o mês
        militares = list(Militar.objects.order_by('-antiguidade'))
 

        i = 0
        while i < quantidade_de_dias:
            data_escala = inicio_mes_atual + timedelta(days=i) # soma mais um dia
            print(data_escala)
            pessoa_escalada = militares[i % len(militares)]
            print('Pessoa escalada: ',pessoa_escalada)
            Escala.objects.create(data=data_escala, pessoa=pessoa_escalada, mes_referencia=inicio_mes_atual)
            i+=1

    return Escala.objects.filter(mes_referencia=inicio_mes_atual)



def escala(request):
    print(dia_da_semana)
    escala = atualizar_escala()
    data_escala = Escala.objects.order_by('data')

    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    mes = meses_do_ano[mes_atual-1]

    
    context = {
        'mes_atual':mes, 
        'ano_atual': ano_atual,
        'escala': data_escala,
    }

    return render(request, 'escalas/escala_do_mes.html', context)