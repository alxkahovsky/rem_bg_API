from django.contrib import admin
from .models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    fields = ['uid', 'username', 'name', 'lang_code', 'timestamp']
    list_display = ['uid', 'username', 'name', 'lang_code', 'timestamp']
    readonly_fields = ['timestamp']
