
import django

from django.conf.urls import url, patterns
from djcelery_ses import views


if django.get_version() >= '1.8':
    urlpatterns = [
        url(r'^sns_notification/$', views.sns_notification),
    ]
else:
    urlpatterns = patterns(
        'djcelery_ses.views',
        url(r'^sns_notification/$', 'sns_notification'),
    )
