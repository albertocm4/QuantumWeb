# Generated by Django 5.0.2 on 2024-05-29 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0007_link_url_desplegada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='url_desplegada',
        ),
    ]
