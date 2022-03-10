from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from apartments.views import page_no_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    #path('', include('apartments.urls')),
]

urlpatterns += i18n_patterns(path('', include('apartments.urls')),)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_no_found