from django.conf import settings

class PassBlacklist(object):
    def __enter__(self):
        settings.DJCELERY_SES_CHECK_BLACKLIST = False

    def __exit__(self, type, value, tb):
        settings.DJCELERY_SES_CHECK_BLACKLIST = True

pass_blacklist = PassBlacklist()
