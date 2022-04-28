from django.db import models
from django.conf import settings

class TelegramUser(models.Model):
  name = models.CharField(max_length=120)
  uid = models.CharField(max_length=120)
  username = models.CharField(max_length=120, null=True, blank=True)
  lang_code = models.CharField(max_length=120, null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)

