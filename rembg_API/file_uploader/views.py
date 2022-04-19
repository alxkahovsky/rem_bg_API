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


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

async def async_rembg(remark):
  file = await sync_to_async(File.objects.get, thread_sensitive=True)(remark=remark)
  input_path = file.get_os_path()
  input = Image.open(input_path)
  output = remove(input)
  output.save(input_path, 'PNG')
  file.delete()
  return (status.HTTP_201_CREATED)

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      cd = file_serializer.validated_data
      file_serializer.save()
      rembg_status = str(asyncio.run(async_rembg(cd['remark'])))
      return Response(file_serializer.data, status=rembg_status)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetProcessed(APIView):
  def get (self, request):
    return Response('some_text')

