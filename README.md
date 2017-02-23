Django Celery SES
=========================

[![PyPI Version](https://badge.fury.io/py/django-celery-ses.png)](https://pypi.python.org/pypi/django-celery-ses)
[![Build Status](https://travis-ci.org/StreetVoice/django-celery-ses.png?branch=master)](https://travis-ci.org/StreetVoice/django-celery-ses)
[![Coverage Status](https://coveralls.io/repos/StreetVoice/django-celery-ses/badge.png?branch=master)](https://coveralls.io/r/StreetVoice/django-celery-ses?branch=master)

Django Email Backend with Amazon Web Service SES and Celery, developed and used by [StreetVoice](http://streetvoice.com/).


This packages provide a EmailBackend to utilize django-celery to send email. You can just plug the EmailBackend in your project without any modify with your code.

Since Amazon SES requires you to handle Bounce email from SNS notification, django-celery-ses also provides view to handle SNS notification for email address which is blacklisted in Amazon SES.

What is provided
=================

1. Celery EmailBackend
2. SNS notification handler
3. Blacklist to handle Bounce email


Installation
================

1. Install from pip / easy_install

  ```sh
  $ pip install django-celery-ses
  ```

2. Add `djcelery_ses` to `INSTALLED_APPS` in `settings.py`

  ```python
  INSTALLED_APPS = (
      ...
      'djcelery_ses',
      ...
  )
  ```

3. migrate the database with South ( you have to install South )

  ```sh
  $ ./manage.py migrate

  ```

4. Change the `EMAIL_BACKEND`

  ```python
  EMAIL_BACKEND = 'djcelery_ses.backends.CeleryEmailBackend'
  ```

5. Add `djcelery_ses` in `urls.py`

  ```python
  urlpatterns = patterns('',
      ...
      (r'^djcelery_ses/', include('djcelery_ses.urls')),
      ...
  )
  ```


Configuration
===============

`django-celery-ses` uses Amazon SES through SMTP, so you have add `EMAIL_*` configuration in `settings.py`

```python
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = '<YOUR_AWS_ACCESS_KEY_ID>'
EMAIL_HOST_PASSWORD = '<YOUR_AWS_SECRET_ACCESS_KEY>'
EMAIL_PORT = 587

SERVER_EMAIL = 'StreetVoice <noreply@streetvoice.com>'
DEFAULT_FROM_EMAIL = 'StreetVoice <noreply@streetvoice.com>'
```

Besides these settings, you also have to setting the SES / SNS on AWS to make this package handle bounce mail for you.


How to use
=============

All you have to do is use `send_mail` or `EmailMessage` just like the old time, you don't have to change your code.



Utilities
==============

This package handle Blacklist for you by default, but sometimes, maybe you want to bypass the "blacklist check", you can use `pass_blacklist` to pass the "backlist check" like this.

```python
from djcelery_ses.utils import pass_blacklist
from django.core.mail import EmailMessage

with pass_blacklist:
    msg = EmailMessage('title', 'body content', 'noreply@example.com', ['noreply@example.com'])
    msg.send()
```

or in some situations, you don't want the email to send through Celery queue, you can use `no_delay`, for example.

> since version 0.9

```python
from djcelery_ses.utils import no_delay
from django.core.mail import send_mail

with no_delay:
    send_mail('title', 'body content', 'noreply@example.com', ['noreply@example.com'])
```

with `no_delay` your email will send out directly without Celey queue.


Test
==============
In order to ensure your changed which can pass in local environment, please run the script:

```
make test
```
