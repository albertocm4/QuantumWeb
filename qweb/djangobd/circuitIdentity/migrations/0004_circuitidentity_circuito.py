# Generated by Django 5.0.2 on 2024-04-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuitIdentity', '0003_circuitidentity_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuitidentity',
            name='circuito',
            field=models.TextField(null=True),
        ),
    ]
