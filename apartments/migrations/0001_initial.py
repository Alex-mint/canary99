# Generated by Django 4.0.1 on 2022-01-17 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Nombre')),
                ('description_short', models.TextField(default='sin descripción', verbose_name='Descripción corta')),
                ('description_long', models.TextField(default='sin descripción', verbose_name='Descripción larga')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Imagen principal')),
                ('rooms', models.PositiveIntegerField(default=1, verbose_name='Habitación')),
                ('adultos', models.PositiveIntegerField(default=1, verbose_name='Adultos')),
                ('children', models.PositiveIntegerField(default=1, verbose_name='Niños')),
                ('min_days', models.PositiveIntegerField(default=5, verbose_name='Minimo noches')),
                ('square_meters', models.PositiveIntegerField(default=40, verbose_name='Metros cuadrados')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publicado')),
                ('wi_fi', models.BooleanField(default=True, verbose_name='Wi-Fi')),
                ('air_conditioning', models.BooleanField(default=True, verbose_name='Aire')),
                ('slug', models.SlugField()),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='latitud')),
                ('lon', models.FloatField(blank=True, null=True, verbose_name='longitud')),
            ],
            options={
                'verbose_name': 'Apartamento',
                'verbose_name_plural': 'Apartamentos',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('status', models.CharField(choices=[('new', 'Новый заказ'), ('in_progress', 'Заказ в обработке'), ('is_ready', 'Заказ готов'), ('completed', 'Заказ получен покупателем')], default='new', max_length=100, verbose_name='Статус заказа')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Дата создания заказа')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('customer_orders', models.ManyToManyField(blank=True, related_name='related_customer', to='apartments.Booking', verbose_name='Заказы покупателя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Extras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartment', models.CharField(max_length=255, verbose_name='Apartamentos')),
                ('extra', models.CharField(blank=True, max_length=255, null=True, verbose_name='Extra')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartment', models.CharField(max_length=255, verbose_name='Nombre de apartamento')),
                ('day_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio por dia')),
                ('month_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio por mes')),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio minimo')),
                ('week_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio por semana')),
            ],
            options={
                'verbose_name': 'Precio',
                'verbose_name_plural': 'Precios',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_nights', models.SmallIntegerField(default=7, verbose_name='Cantidad de Noches a Reservar')),
                ('check_in', models.DateField(verbose_name='Check-In')),
                ('check_out', models.DateField(verbose_name='Check-Out')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая цена')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.apartment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Foto')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='apartments.apartment', verbose_name='Fotos')),
            ],
            options={
                'verbose_name': 'Foto',
                'verbose_name_plural': 'Fotos',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='reserva',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='apartments.reserva', verbose_name='Reserva'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.customer', verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='extras',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_extra', to='apartments.extras', verbose_name='Extra'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ref_apartment', to='apartments.price', verbose_name='Precios'),
        ),
    ]