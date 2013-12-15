# coding: utf-8
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Blacklist


@csrf_exempt
def sns_notification(request):
    """
    Receive AWS SES bounce SNS notification
    """

    # decode json
    try:
        data = json.loads(request.raw_post_data)
    except json.JSONDecodeError:
        return HttpResponse('Oops')

    try:
        message = json.loads(data['Message'])
    except ValueError:
        assert False, request.raw_post_data

    #
    type = 0 if message['notificationType'] == 'Bounce' else 1
    email = message['mail']['destination'][0]


    # add email to blacklist
    try:
        Blacklist.objects.get(email=email)
    except Blacklist.DoesNotExist:
        Blacklist.objects.create(email=email, type=type)

    return HttpResponse('Done')
