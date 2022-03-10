from modeltranslation.translator import register, TranslationOptions
from .models import Apartment, PageInfo, Extras, PageMessage
from emails.models import EmailType


@register(Apartment)
class ApartmentTranslationOptions(TranslationOptions):
    fields = ('description_short', 'description_long', 'condition',)


@register(PageInfo)
class PageInfoTranslationOptions(TranslationOptions):
    fields = ('title', 'info',)


@register(Extras)
class ExtrasTranslationOptions(TranslationOptions):
    fields = ('extra',)


@register(PageMessage)
class PageMessageTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(EmailType)
class EmailTypeTranslationOptions(TranslationOptions):
    fields = ('message_2', 'message_1', 'subject')
