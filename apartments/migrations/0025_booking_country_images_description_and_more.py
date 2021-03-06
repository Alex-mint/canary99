# Generated by Django 4.0.2 on 2022-03-04 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0024_alter_pagemessage_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='country',
            field=models.CharField(max_length=20, null=True, verbose_name='Pais'),
        ),
        migrations.AddField(
            model_name='images',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='descripcion'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('new', 'Reserva nueva'), ('is_approved', 'Reserva aprobada'), ('booking', 'Booking')], default='new', max_length=100, verbose_name='Estatus'),
        ),
    ]
