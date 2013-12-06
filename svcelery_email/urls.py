from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('svcelery_email.views',
    url(r'^sns_feedback/$', 'sns_feedback'),
)
