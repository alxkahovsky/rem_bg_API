from django.urls import path
from .views import FileView, GetProcessed

urlpatterns = [
    path('upload/', FileView.as_view(), name='file-upload'),
    path('get/', GetProcessed.as_view(), name='get-processd'),
]