import random
import time
from django.shortcuts import get_object_or_404
import telebot
import configparser
import os
from django.core.management.base import BaseCommand
from file_uploader.models import File
from bot.models import TelegramUser
from django.conf import settings
from file_uploader.views import sync_rembg


class Command(BaseCommand):
    def handle(self, *args, **options):
        config = configparser.ConfigParser()
        config.read(r'C:\Users\Пользователь\django\PycharmProjects\rem_bg_test\telebot.cfg')
        bot_key = config.get('TELEBOT', 'BOT_KEY')
        bot = telebot.TeleBot(bot_key)
        @bot.message_handler(content_types=['photo'])
        def get_text_messages(message):
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = str(random.randint(0, 999999)) + '.png'
            src = settings.MEDIA_ROOT + '\\' + file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            File.objects.create(remark=message.photo[1].file_id)
            file = File.objects.get(remark=message.photo[1].file_id)
            file.file = file_name
            file.save()
            bot.send_message(message.from_user.id, 'Создана запись в БД')
            result = sync_rembg(file.remark)
            contents = open(result['path'], 'rb')
            uid = message.from_user.id
            name = message.from_user.first_name
            username = message.from_user.username
            lang_code = message.from_user.language_code
            telegram_user = get_object_or_404(TelegramUser, uid=uid)
            if not telegram_user:
                TelegramUser.objects.create(uid=uid, name=name, username=username, lang_code=lang_code)
            bot.send_message(message.from_user.id, 'Файл обработан')
            bot.send_photo(uid, contents)

        bot.polling(none_stop=True, interval=0)












