from django.shortcuts import render


# Create your views here.
def escala(request):

    return render(request, 'escalas/escala_do_mes.html')

'''
### código para montar o calendário 
obs: execute este código em outro ambiente ou no terminal
import datetime

for i in range(1, 31, 1): # começa de 1,vai até 30 de 1 passo em 1
    x = datetime.datetime(2024, 4, i)
    print(x.strftime("%A"), i)

'''