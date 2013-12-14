# coding: utf-8

from django.http import HttpResponse
from django.utils import simplejson
from django.utils.simplejson import JSONDecodeError
from django.views.decorators.csrf import csrf_exempt

from svcelery_email.models import Blacklist


@csrf_exempt
def sns_notification(request):
    """
    Receive AWS SES bounce SNS notification
    """

    # decode json
    try:
        json = request.raw_post_data
        data = simplejson.loads(json)
    except JSONDecodeError:
        return HttpResponse('Oops')

    try:
        message = simplejson.loads(data['Message'])
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
