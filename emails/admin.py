from django.contrib import admin

from emails.models import EmailType, EmailSendingFact
from modeltranslation.admin import TranslationAdmin


from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class EmailAdminForm(forms.ModelForm):
    message_1_es = forms.CharField(widget=CKEditorUploadingWidget())
    message_1_en = forms.CharField(widget=CKEditorUploadingWidget())
    message_1_de = forms.CharField(widget=CKEditorUploadingWidget())
    message_2_es = forms.CharField(widget=CKEditorUploadingWidget())
    message_2_en = forms.CharField(widget=CKEditorUploadingWidget())
    message_2_de = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = EmailType
        fields = '__all__'


class EmailTypeAdmin(TranslationAdmin):
    form = EmailAdminForm
    list_display = ('id', 'name', 'created_at',)
    list_display_links = ('id', 'name',)

admin.site.register(EmailType, EmailTypeAdmin)
admin.site.register(EmailSendingFact)

