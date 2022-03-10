from django.contrib import admin
from django.shortcuts import redirect
from django.utils.encoding import iri_to_uri
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin


class ApartmentAdminForm(forms.ModelForm):
    condition_es = forms.CharField(widget=CKEditorUploadingWidget())
    condition_en = forms.CharField(widget=CKEditorUploadingWidget())
    condition_de = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Apartment
        fields = '__all__'


class PageInfoAdminForm(forms.ModelForm):
    info_es = forms.CharField(widget=CKEditorUploadingWidget())
    info_en = forms.CharField(widget=CKEditorUploadingWidget())
    info_de = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = PageInfo
        fields = '__all__'


class ImageInline(admin.TabularInline):
    model = Images
    fields = ['apartment', 'image', 'description', 'get_preview']
    readonly_fields = ["get_preview"]

    def get_preview(self, apartment):
        return format_html(
            f'<img src="{apartment.image.url}" width="auto" height="200px" />'
    )


class ReservaInline(admin.TabularInline):
    model = Reserva
    fields = ['apartment', 'amount_nights', 'check_in', 'check_out', 'final_price']
    extra = 0
    #readonly_fields = ["get_preview"]


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'status', 'phone', 'settle', 'my_comment',)
    list_display_links = ('id', 'reserva',)
    list_editable = ('status', 'settle', 'my_comment',)
    search_fields = ('status',)
    def response_change(self, request, obj):
        if url_has_allowed_host_and_scheme('/staff_page/', None):
            url = iri_to_uri('/staff_page/')
            return redirect(url)
        else:
            pass


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'apartment', 'booked',)
    list_display_links = ('id', 'apartment',)
    list_editable = ('booked',)


#@admin.register(Apartment)
class ApartmentAdmin(TranslationAdmin):
    form = ApartmentAdminForm
    list_display = ('id', 'title', 'is_published', 'get_preview',)
    list_display_links = ('id', 'title',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        ImageInline,
    ]
    def get_preview(self, apartment):
        return format_html(
            f'<img src="{apartment.image.url}" width="auto" height="150px" />'
    )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone',)
    list_display_links = ('user',)
    #prepopulated_fields = {'slug': ('title',)}
    inlines = [
        ReservaInline,
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                #'user',
                # 'firstname',
                # 'lastname',
                'phone',
            ]
        }),)

@admin.register(Extras)
class ExtrasAdmin(TranslationAdmin):
    pass


@admin.register(PageInfo)
class PageInfoAdmin(TranslationAdmin):
    form = PageInfoAdminForm


@admin.register(PageMessage)
class PageMessageAdmin(TranslationAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Images)
admin.site.register(Price)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Booking, BookingAdmin)
#admin.site.register(Extras)
admin.site.register(BookingDate)
admin.site.register(Owner)
admin.site.register(Category)
#admin.site.register(PageInfo)
