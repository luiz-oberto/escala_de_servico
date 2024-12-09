from django.shortcuts import render
from escala_servico.models import Militar, Escala
from datetime import date, timedelta
from django.db.models import Q


# Função para deletar a escala do mês anterior e gerar nova
def atualizar_escala():
    # pega a data de hoje
    hoje = date.today()
    # altera o dia data atual para o primeiro dia do mês
    inicio_mes_atual = hoje.replace(day=1)

    # Verificar se existe escala para o mês atual
    escala_mes_atual = Escala.objects.filter(mes_referencia=inicio_mes_atual)

    if not escala_mes_atual.exists():
        # Apagar a escala do mês anterior
        Escala.objects.all().delete()

        # Obter as pessoas e gerar nova escala para o mês
        militares = list(Militar.objects.order_by('-antiguidade'))
        efetivo = len(militares)
        print('efetivo: ',efetivo)

        # Preencher escala para cada dia útil do mês atual (segunda a domingo)
        # while dia <= 31:
            # if mes tiver 31 dias:

            # if mes tiver 30 dias:

        for i in range(efetivo):  # Supondo que serão 5 pessoas na primeira semana
            data_escala = inicio_mes_atual + timedelta(days=i) # soma mais um dia
            # print('data escala: ', data_escala)
            pessoa_escalada = militares[i % len(militares)]  # Pode ser randomizado
            print('Pessoa escalada: ',pessoa_escalada)
            Escala.objects.create(data=data_escala, pessoa=pessoa_escalada, mes_referencia=inicio_mes_atual)

    return Escala.objects.filter(mes_referencia=inicio_mes_atual)



def escala(request):
    escala = atualizar_escala()
    escala_do_mes = Escala.objects.order_by('data')
    print('Escala do mes', escala_do_mes.values())

    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    data_hoje = date.today()
    mes_atual = data_hoje.month
    # ano_atual = data_hoje.year
    mes = meses_do_ano[mes_atual-1]
    
    
    
    context = {
        'mes_atual':mes, # Exibe o mês atual
        'escala': escala,
    }

    return render(request, 'escalas/escala_do_mes.html', context)