from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .models import File
from rembg import remove
from PIL import Image
import asyncio
from asgiref.sync import sync_to_async
import os
from django.http import HttpResponse
from django.conf import settings


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

async def async_rembg(remark):
  file = await sync_to_async(File.objects.get, thread_sensitive=True)(remark=remark)
  input_path = file.get_os_path()
  input_name = file.get_file_name()
  input = Image.open(input_path)
  output = remove(input)
  output.save(input_path, 'PNG')
  file.delete()
  return {'path': input_path,
          'name': input_name,
          }

def sync_rembg(remark):
  file = File.objects.get(remark=remark)
  input_path = file.get_os_path()
  input_name = file.get_file_name()
  input = Image.open(input_path)
  output = remove(input)
  output.save(input_path, 'PNG')
  file.delete()
  return {'path': input_path,
          'name': input_name,
          }

def clear_media():
  media_path = settings.MEDIA_ROOT
  for files in os.scandir(media_path):
    os.remove(files)
    return media_path + 'is clear !'


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    # clear_media()
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      cd = file_serializer.validated_data
      file_serializer.save()
      # rembg_status = asyncio.run(async_rembg(cd['remark']))
      rembg_status = sync_rembg(cd['remark'])
      path = rembg_status['path']
      with open(path, 'rb') as image:
        file = image.read()
        response = HttpResponse(file, content_type='image/png')
        filename = rembg_status['name']
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetProcessed(APIView):
  def get (self, request):
    return Response('some_text')

