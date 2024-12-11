from django.contrib import admin
from escala_servico import models

# Register your models here.
@admin.register(models.Militar)
class IndividuoAdmin(admin.ModelAdmin):
    list_display = 'id', 'graduacao', 'nome_de_guerra', 'antiguidade', 'ultimo_a_dar_servico',
    ordering = 'antiguidade',

@admin.register(models.Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = 'data', 'dias_da_semana', 'pessoa',
    ordering = 'data',