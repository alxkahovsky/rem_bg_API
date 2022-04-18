from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    fields = ['file', 'remark', 'timestamp']
    list_display = ['id','file', 'remark', 'timestamp']
    readonly_fields = ['timestamp']
