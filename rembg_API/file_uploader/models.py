from django.db import models
from django.conf import settings

class File(models.Model):
  file = models.FileField(blank=False, null=False)
  remark = models.CharField(max_length=20)
  timestamp = models.DateTimeField(auto_now_add=True)

  def get_os_path(self):
    return (settings.MEDIA_ROOT+'\\'+ str(self.file))  #for development ONLY

  def get_file_name(self):
    return (str(self.file))

  def get_file_url(self):
    return(self.file.url)