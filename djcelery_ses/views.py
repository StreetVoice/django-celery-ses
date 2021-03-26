# coding: utf-8
import json
import re

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import mail_admins
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Blacklist


@csrf_exempt
def sns_notification(request):
    """
    Receive AWS SES bounce SNS notification
    """

    # decode json
    try:
        data = json.loads(request.read())
    except ValueError:
        return HttpResponseBadRequest('Invalid JSON')

    # handle SNS subscription
    if data['Type'] == 'SubscriptionConfirmation':
        subscribe_url = data['SubscribeURL']
        subscribe_body = """
        Please visit this URL below to confirm your subscription with SNS

        %s """ % subscribe_url

        mail_admins('Please confirm SNS subscription', subscribe_body)
        return HttpResponse('OK')

    try:
        message = json.loads(data['Message'])
    except ValueError:
        assert False, data['Message']

    notification_type = message['notificationType']
    if notification_type not in dict(Blacklist.TYPE_CHOICES).values():
        return HttpResponse('No Email')

    type = 0 if notification_type == 'Bounce' else 1
    email = message['mail']['destination'][0]

    try:
        validate_email(email)
    except ValidationError:
        try:
            email = re.findall(r"<(.+?)>", email)[0]
        except IndexError:
            email = None

    if not email:
        return HttpResponse('Email Error')

    # add email to blacklist
    Blacklist.objects.get_or_create(email=email, defaults={"type": type})

    return HttpResponse('Done')
