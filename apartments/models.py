from django.conf import settings
from django.db import models
from django.urls import reverse


class Owner(models.Model):
    name = models.CharField('Nombre de dueño', max_length=255)
    comment = models.TextField('Comentario', null=True, blank=True)
    phone = models.CharField('Telefono', max_length=255, null=True, blank=True)
    email = models.EmailField('Correo', null=True, blank=True)
    iban = models.CharField('Iban', max_length=255, null=True, blank=True)
    banco = models.CharField('Banco', max_length=255, null=True, blank=True)
    address = models.CharField('Direccion de Banco', max_length=255, null=True,
                               blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dueño'


class Category(models.Model):
    category = models.CharField('Categoria', max_length=255)
    def __str__(self):
        return self.category

    class Meta(object):
        verbose_name = "Categoria"


class Apartment(models.Model):
    owner = models.ForeignKey(
        Owner, verbose_name='Dueño',
        related_name='apartment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    title = models.CharField('Nombre', max_length=255)
    description_short = models.TextField('Descripción corta',
                                         default='sin descripción')
    description_long = models.TextField('Descripción larga',
                                        default='sin descripción')
    image = models.ImageField('Imagen principal', upload_to='images/')
    rooms = models.PositiveIntegerField('Habitación', default=1)
    adultos = models.PositiveIntegerField('Adultos', default=1)
    children = models.PositiveIntegerField('Niños', default=1)
    max_person = models.PositiveIntegerField('Max. Huéspedes', default=1)
    bed = models.PositiveIntegerField('Camaa pequeñas', default=1)
    double_bed = models.PositiveIntegerField('Camas doble', default=1)
    min_days = models.PositiveIntegerField('Minimo noches', default=5)
    toilet = models.PositiveIntegerField('Baños', default=1)
    square_meters = models.PositiveIntegerField('Metros cuadrados', default=40)
    is_published = models.BooleanField(default=True, verbose_name='Publicado')
    wi_fi = models.BooleanField(default=True, verbose_name='Wi-Fi')
    air_conditioning = models.BooleanField(default=True, verbose_name='Aire')
    slug = models.SlugField()
    lat = models.FloatField(verbose_name="latitud", blank=True, null=True)
    lon = models.FloatField(verbose_name="longitud", blank=True, null=True)
    promo_code = models.CharField('código de promoción', max_length=255,
                                  blank=True, null=True)
    video_code = models.CharField('código de video', max_length=255,
                                  blank=True, null=True)
    cleaning_price = models.DecimalField(
        max_digits=9, decimal_places=2,
        default=50, verbose_name='Precio de limpieza'
    )
    price = models.ForeignKey(
        'Price', on_delete=models.CASCADE,
        verbose_name="Precios",
        related_name='ref_apartment'
    )
    extras = models.ForeignKey(
        'Extras', on_delete=models.CASCADE,
        verbose_name="Extra",
        related_name='all_extra'
    )
    condition = models.TextField('Condiciones', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('apart', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Apartamento'
        verbose_name_plural = 'Apartamentos'
        ordering = ['title']


class Extras(models.Model):
    apartment = models.CharField('Apartamentos', max_length=255)
    extra = models.CharField('Extra', max_length=255, null=True, blank=True)


class Images(models.Model):
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name='images',
        verbose_name="Fotos"
    )
    image = models.ImageField('Foto')
    description = models.CharField('descripcion', max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.id}. {self.apartment.title}'

    class Meta(object):
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"


class Price(models.Model):
    apartment = models.CharField('Nombre de apartamento', max_length=255)
    day_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Precio por dia",
    )
    month_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Precio por mes",
    )
    min_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Precio minimo",
    )
    week_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Precio por semana",
    )

    def __str__(self):
        return f'{self.apartment}'

    class Meta(object):
        verbose_name = "Precio"
        verbose_name_plural = "Precios"


class Reserva(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey('Customer', verbose_name='Покупатель',
                             on_delete=models.CASCADE)
    amount_persons = models.PositiveIntegerField('úmero de huéspedes',
                                                 default=1)
    amount_nights = models.SmallIntegerField('Cantidad de Noches a Reservar',
                                             default=7)
    check_in = models.DateField('Entrada', auto_now=False)
    check_out = models.DateField('Salida', auto_now=False)
    created_at = models.DateField('Creada', auto_now=True)
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name='Precio final')
    price_per_night = models.DecimalField(max_digits=9, decimal_places=2,
                                          default=60,
                                          verbose_name='Precio por noche')
    cleaning_price = models.DecimalField(max_digits=9, decimal_places=2,
                                         default=50,
                                         verbose_name='Precio de limpieza')
    booked = models.BooleanField('Resrvada', default=False)

    class Meta:
        """Meta definition for Reserva."""

        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        """Unicode representation of Reserva."""

        return f'"{self.apartment}": {self.check_in} - {self.check_out}'


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name='Usuario',
                                on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Activo?')
    customer_orders = models.ManyToManyField(
        'Booking', blank=True, verbose_name='Reservas del cliente',
        related_name='related_customer'
    )
    phone = models.CharField(max_length=20, verbose_name='Telefono')

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Ciente'


class Booking(models.Model):
    STATUS_NEW = 'new'
    STATUS_READY = 'is_approved'
    STATUS_BOOKING = 'booking'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Reserva nueva'),
        (STATUS_READY, 'Reserva aprobada'),
        (STATUS_BOOKING, 'Booking')
    )
    is_accept = models.BooleanField('Aceptado ?', default=True)
    user = models.ForeignKey('Customer', verbose_name='Cliente',
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Nombre')
    last_name = models.CharField(max_length=255, verbose_name='Apellidos')
    phone = models.CharField(max_length=20, verbose_name='Telefono')
    country = models.CharField(max_length=20, verbose_name='Pais', null=True)
    reserva = models.ForeignKey(Reserva, verbose_name='Reserva', null=True,
                                related_name='booking',
                                blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, verbose_name='Estatus',
                              choices=STATUS_CHOICES, default=STATUS_NEW)
    comment = models.TextField(verbose_name='Comentario de cliente', null=True,
                               blank=True)
    created_at = models.DateField(verbose_name='Fecha de creacion de reserva',
                                  auto_now=True)
    settle = models.BooleanField('Liqudado ?', default=False)
    my_comment = models.TextField(verbose_name='Comentario mio', null=True,
                                  blank=True)

    class Meta:
        """Meta definition for Reserva."""

        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        """Unicode representation of Reserva."""

        return f'Booking ref: {self.id}'


class BookingDate(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='bk_date',
        verbose_name="Reserva"
    )
    date = models.DateField('Fecha', null=True, blank=True)

    def __str__(self):
        return f'{self.id}. {self.booking.reserva.apartment.title} - {self.date}'

    class Meta(object):
        verbose_name = "Fecha"


class PageInfo(models.Model):
    title = models.CharField('Nombre', max_length=255, default='info')
    info = models.TextField()

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Info"


class PageMessage(models.Model):
    title = models.CharField('Nombre', max_length=255)
    text = models.TextField('Mensaje')

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Mensaje"