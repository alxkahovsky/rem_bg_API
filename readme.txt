https://github.com/danielgatis/rembg - python-библиотека автора Daniel Gatis;
rembg используется в качестве библиотеки для обработки изображений в составе jango/drf приложения;
для запуска на локалке добавить ip адрес в allowed hosts;

python manage.py runserver 192.168.1.220:7070;
python manage.py runbot

Пример клиентской части:
----------------------------------------------------------------
import requests
import os


# path example C:\Users\Пользователь\Desktop\input
path_input = r' ENTER_YOUR_INPUT_PATH_HERE '
path_output = r' ENTER_YOUR_OUTPUT_PATH_HERE '

with os.scandir(path=path_input) as it:
    for entry in it:
        if not entry.is_file():
            break
        else:
            try:
                filename = ((entry.name).split('.'))[0]
                input_path = path_input + '\\' + entry.name
                files = {'file': open(input_path, 'rb')}
                values = {'remark': entry.name}
                url = 'http://127.0.0.1:8000/file/upload/'
                r = requests.post(url, files=files, data=values)
                with open(path_output + '\\' + filename + '.png', "wb") as f:
                    print('Получен файл: ' + path_output + '\\' + filename + '.png')
                    f.write(r.content)
            except:
                continue
----------------------------------------------------------------
testing git change name and email