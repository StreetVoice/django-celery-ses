from django.urls import re_path

from djcelery_ses import views

urlpatterns = [
    re_path(r'^sns_notification/$', views.sns_notification),
]
