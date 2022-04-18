from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    fields = ['file', 'remark', 'timestamp']
    list_display = ['file', 'remark', 'timestamp']
