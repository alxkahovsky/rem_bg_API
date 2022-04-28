import time

import telebot
import configparser
import os
from django.core.management.base import BaseCommand
from file_uploader.models import File
from PIL import Image
import requests
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
            src = settings.MEDIA_ROOT + '\\' + 'new_image.png'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            File.objects.create(remark=message.photo[1].file_id)
            file = File.objects.get(remark=message.photo[1].file_id)
            file.file = 'new_image.png'
            file.save()
            bot.send_message(message.from_user.id, 'Создана запись в БД')
            print(file.remark)
            result = sync_rembg(file.remark)
            print(result['path'])
            contents = open(result['path'], 'rb')
            uid = message.from_user.id
            print(uid)
            bot.send_message(message.from_user.id, 'Файл обработан')
            bot.send_photo(uid, contents)










                # time.sleep(5)
                # bot.send_message(message.from_user.id, 'make')
                # files = {'file': new_file}
                # values = {'remark': message.photo[1].file_id + '.png'}
                # url = 'http://192.168.1.220:7070/file/upload/'
                # r = requests.post(url, files=files, data=values)
                #
                # bot.send_message(message.from_user.id, files)



        bot.polling(none_stop=True, interval=0)












