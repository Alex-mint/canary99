# Generated by Django 4.0.1 on 2022-01-31 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0013_alter_bookingdate_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('new', 'Reserva nueva'), ('is_approved', 'Reserva aprobada'), ('completed', 'Reserva realizada')], default='new', max_length=100, verbose_name='Estatus'),
        ),
    ]
