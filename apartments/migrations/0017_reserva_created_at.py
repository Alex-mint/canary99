# Generated by Django 4.0.1 on 2022-01-31 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0016_reserva_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='created_at',
            field=models.DateField(auto_now=True, verbose_name='Creada'),
        ),
    ]