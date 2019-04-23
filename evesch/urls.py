from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('evesch.main_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
