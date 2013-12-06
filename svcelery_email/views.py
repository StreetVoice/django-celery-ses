# coding: utf-8

from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.models import User
from django.utils.simplejson import JSONDecodeError

from svcelery_email.models import Blacklist


def sns_feedback(request):
    """
    Receive AWS SES bounce SNS notification
    """

    # decode json
    try:
        json = request.raw_post_data
        data = simplejson.loads(json)
    except JSONDecodeError:
        return HttpResponse('ops')

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
        Blacklist.objects.create(email=email)


    # mark user as not active
    if type == 0:
        try:
            user = User.objects.get(email=email)
            user.is_active = False
            user.save()
        except User.DoesNotExist:
            pass
        
    return HttpResponse('Done')
