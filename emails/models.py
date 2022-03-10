from django.db import models
from django.forms import model_to_dict
from django.template.loader import get_template

from apartments.models import Booking, Reserva
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, pre_delete, pre_save, \
    post_delete
from django.dispatch import receiver

from canary99.settings import FROM_EMAIL, EMAIL_ADMIN


class EmailType(models.Model):
    name = models.CharField('titulo', max_length=255, blank=True, null=True,
                            default=None)
    subject = models.CharField('subject', max_length=255, blank=True,
                               null=True)
    message_1 = models.TextField('mensaje 1', blank=True, null=True)
    message_2 = models.TextField('mensaje 2', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    updated_at = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Tipe de email'

    def __str__(self):
        return f'{self.name}'


class EmailSendingFact(models.Model):
    type = models.ForeignKey(EmailType, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Booking, blank=True, null=True, default=None,
                              on_delete=models.CASCADE)
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    updated_at = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Email enviado'

    def __str__(self):
        return f'{self.type.name}'


class SendingEmail(object):
    from_email = "Canary99 <%s>" % FROM_EMAIL
    reply_to_emails = [from_email]

    def sendig_email(self, type_id, email=None, order=None):
        if not email:
            email = EMAIL_ADMIN
        target_emails = [email]
        booking = model_to_dict(order)
        reserva = Reserva.objects.get(pk=booking['reserva'])
        context = {
            'booking': booking,
            'reserva': model_to_dict(reserva),
            'apartment': reserva.apartment.title
        }

        if type_id == 1:  # admin
            email_type = EmailType.objects.get(name='Nueva reserva - admin')
            subject = email_type.subject

            message = get_template(
                'emails/admin_order_notification.html').render(context)
        elif type_id == 2:  # cliente
            email_type = EmailType.objects.get(name='Nueva reserva - cliente')
            context['message_1'] = email_type.message_1
            context['message_2'] = email_type.message_2
            subject = email_type.subject
            message = get_template(
                'emails/customer_order_notification.html').render(context)
        elif type_id == 3:  # admin
            email_type = EmailType.objects.get(
                name='Reserva cancelada - admin')
            subject = email_type.subject
            message = get_template('emails/admin_cancel_reserva.html').render(
                context)
        elif type_id == 4:  # cliente
            email_type = EmailType.objects.get(
                name='Reserva cancelada - cliente')
            subject = email_type.subject
            message = get_template(
                'emails/customer_cancel_reserva.html').render(context)
        mail = EmailMessage(subject, message, from_email=self.from_email,
                            to=target_emails,
                            reply_to=self.reply_to_emails)
        mail.content_subtype = 'html'
        mail.mixed_subtype = 'related'
        mail.send()

        kwargs = {
            'type_id': type_id,
            'email': email
        }

        if order:
            kwargs['order'] = order

        EmailSendingFact.objects.create(**kwargs)


@receiver(post_save, sender=Booking, dispatch_uid="send email")
def new_reserva(created, instance, **kwargs):
    if created:
        email = SendingEmail()
        email.sendig_email(type_id=1, order=instance)
        email.sendig_email(type_id=2, order=instance,
                           email=instance.user.user.email)
        reserva = instance.reserva
        reserva.booked = True
        reserva.save()


@receiver(post_delete, sender=Booking, dispatch_uid='reserva_cancel')
def reserva_cancel(sender, instance, using, **kwargs):
    try:
        reserva = instance.reserva
        reserva.delete()
    except:
        pass


@receiver(pre_delete, sender=Booking, dispatch_uid='email_reserva_cancel')
def reserva_cancel(sender, instance, using, **kwargs):
    email = SendingEmail()
    email.sendig_email(type_id=3, order=instance)
    email.sendig_email(type_id=4, order=instance,
                       email=instance.user.user.email)
