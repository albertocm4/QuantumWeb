# Generated by Django 5.0.2 on 2024-04-10 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuitIdentity', '0006_remove_circuitidentity_codigo_circuito'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='id_circuito',
        ),
        migrations.AddField(
            model_name='results',
            name='circuito',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='circuitIdentity.circuitidentity'),
        ),
    ]
