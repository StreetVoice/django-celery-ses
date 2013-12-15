from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^djcelery_ses/', include('djcelery_ses.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
