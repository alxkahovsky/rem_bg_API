from django.db import models
from django.urls import reverse

class File(models.Model):
  file = models.FileField(blank=False, null=False)
  remark = models.CharField(max_length=20)
  timestamp = models.DateTimeField(auto_now_add=True)

  # def get_absolute_url_img(self):
  #   return reverse('file_uploader:get-processd', args=[self.id])