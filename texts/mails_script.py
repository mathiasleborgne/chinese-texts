import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.',
          'mathias.leborgne@gmail.com', ['mathias.leborgne@gmail.com'],
          fail_silently=False)