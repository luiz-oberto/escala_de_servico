# Generated by Django 5.1 on 2024-09-28 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escala_servico', '0003_rename_individuo_militar'),
    ]

    operations = [
        migrations.AddField(
            model_name='militar',
            name='ultimo_a_dar_servico',
            field=models.BooleanField(default=False),
        ),
    ]
