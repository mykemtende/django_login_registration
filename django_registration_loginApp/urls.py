from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mtende/', include('loginApp.urls')),
    url(r'^', include('loginApp.urls')),
]
if settings.DEBUG:
	urlpatterns += patterns(
		'django.views.static',
		(r'media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}),)

	admin.site.site_header = _("Mtende website Administration Dashboard")
	admin.site.site_title = _("Mtende website admin")