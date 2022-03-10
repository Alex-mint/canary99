from django.core.mail import EmailMessage
from django.db.models import Count
from django.forms import model_to_dict
from django.shortcuts import render
from django.template.loader import get_template

from canary99.settings import FROM_EMAIL, EMAIL_ADMIN
from emails.models import EmailSendingFact


menu = [{'title': 'Inicio', 'url_name': 'home'},
        {'title': 'Quen somos', 'url_name': 'about'},
        {'title': 'Acceder', 'url_name': 'login'},
        ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()

        context['menu'] = user_menu
        return context
