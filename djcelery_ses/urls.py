
import django


if django.VERSION >= (3, 1):
    from django.urls import re_path
    from djcelery_ses import views

    urlpatterns = [
        re_path(r'^sns_notification/$', views.sns_notification),
    ]

elif django.VERSION >= (1, 9):
    from django.conf.urls import url
    from djcelery_ses import views

    urlpatterns = [
        url(r'^sns_notification/$', views.sns_notification),
    ]

else:
    from django.conf.urls import url, patterns
    urlpatterns = patterns(
        'djcelery_ses.views',
        url(r'^sns_notification/$', 'sns_notification'),
    )
