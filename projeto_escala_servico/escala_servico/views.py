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
    # Generate duty roster
    Escala.atualizar_escala()

    # fetch duty roster
    data_escala = Escala.objects.order_by('data')

    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    mes = meses_do_ano[mes_atual-1]

    
    context = {
        'mes_atual':mes, 
        'ano_atual': ano_atual,
        'escala': data_escala,
    }

    return render(request, 'escalas/escala_do_mes.html', context)



def verify_last_duty():
    # LÓGICA PARA ACERTAR A LISTA DO ÚLTIMO QUE DEU SERVIÇO
    militares = list(Militar.objects.order_by('-antiguidade'))
    lista_atualizada = []
    for militar in militares:
        if militar.ultimo_a_dar_servico == True:
            # print(f'{militar.nome_de_guerra} foi o último a dar serviço')
            ultimo_que_deu_servico = militar.nome_de_guerra
        else:
            # print(f'{militar.nome_de_guerra} não foi o último')
            lista_atualizada.append(militar.nome_de_guerra)

    lista_atualizada.append(ultimo_que_deu_servico)
    return lista_atualizada
        
