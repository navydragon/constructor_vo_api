assets = ['/datasets/ds_bert/bert_config.json']

import os
import requests
import time
import random

my_url = 'https://code.s3.yandex.net'


count = 0
skip_count = 0
except_count = 0
all_count = len(assets)
except_items = []

# получаем путь, по которому мы будем сохранять файлы
save_path = os.getcwd()
# или можно задать папку в домашней директории.
# Например: save_path = os.path.join(os.path.expanduser("~"), 'download')

for item in assets:
    try:
        # получаем имя каталога и имя файла из item
        dir_name, file_name = os.path.split(item)

        # убираем символ "/" у dir_name, чтобы сделать имя относительным
        dir_name = dir_name[1:] if dir_name.startswith('/') else dir_name

        # создаём каталог на диске, если он не существует
        os.makedirs(os.path.join(save_path, dir_name), exist_ok=True)

        # проверить, существует ли уже файл в директории
        if os.path.exists(os.path.join(save_path, dir_name + '/' + file_name)):
            print(f"{item} уже существует, пропускаем загрузку...")
            skip_count += 1 # пропускаем загрузку в случае уже существующего файла
        else:
            # скачиваем item и записываем его в переменную "r"
            r = requests.get(my_url + item)

            # сохраняем файл в директории заданной в переменной save_path.
            with open(os.path.join(save_path,  dir_name + '/' + file_name), 'wb') as f:
                f.write(r.content)

            # условие для добавления паузы
            # условие будет истинным только тогда, когда значение count будет кратно случайному целому числу от 3 до 5.
            if count % random.randint(3, 5) == 0:
                print(f"Загружено {count} файлов из {all_count}")
                # добавляем рандомную паузу перед загрузкой нового файла
                # устанавливаем длительность паузы между загрузками = случайному целому числу от 2 до 8 секунд.
                pause = random.randint(2, 8)
                print(f"пауза между загрузкой файлов составляет {pause} секунд")
                time.sleep(pause)
            count += 1
            upload_percentage = count / all_count  # вычисляем процент загруженных файлов
            print(f"{upload_percentage:.2%}", item)
    except:
        except_count += 1
        except_items.append(item)
        print(f'{item}!! не удалось скачать! номер итерации {count}')

print("Все файлы скачаны!")
print(f"Всего загружено {count} файла(ов) из {all_count}. Процент загруженных файлов составляет {count / all_count:.2%}")
print(f"Пропущено (уже существуют) {skip_count} файла(ов) из {all_count}. ")
print(f"Всего загрузок {count - except_count}")
print(f"Не удалось скачать по причине каких-то ошибок/прерываний: {except_count} файла(ов)")
print(f"Список пропущенных файлов по причине каких-то ошибок/прерываний: {except_items}")