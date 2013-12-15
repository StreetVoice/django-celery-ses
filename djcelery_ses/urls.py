from django.conf.urls import url, patterns

urlpatterns = patterns('djcelery_ses.views',
    url(r'^sns_notification/$', 'sns_notification'),
)
