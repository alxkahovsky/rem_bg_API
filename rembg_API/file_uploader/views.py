from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .models import File
from rembg import remove

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetProcessed(APIView):
  def get (self, request):
    file = File.objects.get(id=request.data['id'])
    input_path = 'http://127.0.0.1:8000/media/js_w2YVntT.jpg'
    print(input_path)
    output_path = 'http://127.0.0.1:8000/media/processed/js_w2YVntT.jpg'

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)
    return Response(output_path)

