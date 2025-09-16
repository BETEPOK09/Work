# Необходимые библиотеки

import argparse
from tkinter import filedialog
from PIL import Image, UnidentifiedImageError, ImageFilter
import os

# Максимальная ширина и неизменные данные

MAX_WIDTH = 1200
SUFFIX = '_process'


# Функция для обработки изображений
def processed_image(path, out_jpegs_dir, out_webps_dir):
    try:

        # Открытие изображения

        with Image.open(path) as img:
            img.load()

        # Проверка на подходящий формат

        if img.format == 'PNG' or img.format == 'JPEG':

            width, height = img.size

            if img.mode != "RGBA":
                img = img.convert('RGBA')


            # Манипуляция изменения размеров картинки

            if width > MAX_WIDTH:
                new_w = MAX_WIDTH
                new_h = int(height * (new_w / width))
                img = img.resize((new_w, new_h), Image.LANCZOS)

                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img)

            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img)

            if background.mode != "RGB":
                background = background.convert('RGB')

            # Создание путей для сохранения измененного файла

            base = os.path.splitext(os.path.basename(path))[0]
            out_jpeg = os.path.join(out_jpegs_dir, f"{base}{SUFFIX}.jpg")
            out_webp = os.path.join(out_webps_dir, f"{base}{SUFFIX}.webp")

            # Сохранение измененного файла

            if width < 65535 or height < 65535:
                try:
                    background.save(out_jpeg, format='JPEG')
                    print(f"Сохранение JPEG -> {out_jpeg}")
                except Exception as e:
                    print(f"Ошибка при сохранении JPEG: {e}")
            else:
                print('Слишком большой размер файла для jpeg')
                return

            if width < 16383 or height < 16383:
                try:
                    background.save(out_webp, format='WEBP')
                    print(f"Сохранение WEBP -> {out_webp}")
                except Exception as e:
                    print(f"Ошибка при сохранении WEBP: {e}")
            else:
                print('Слишком большой размер файла для webp')

                return

        # Различные ошибки

        else:
            print('Неправильное расширение файла')
            return

    except UnidentifiedImageError:
        print(f'Непонятный файл {path}')
    except Exception as e:
        print(f'Ошибка обработки {path}: {e}')


# Основной процесс

if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Создание путей для сохранения файла

    out_dir = os.path.join(script_dir, 'out')
    out_jpegs = os.path.join(out_dir, 'jpegs')
    out_webps = os.path.join(out_dir, 'webps')

    # Создание катологов

    os.makedirs(out_jpegs, exist_ok=True)
    os.makedirs(out_webps, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True,
                        help="Выберите формат работы: file - с файлом, papka - с папкой и укажите путь к файлу")
    parser.add_argument('path')
    args = parser.parse_args()
    f = args.f
    if f == 'file':
        images_dir = args.path

        if images_dir == '':
            print('Файл отсутствует')

        processed_image(images_dir, out_jpegs, out_webps)

    elif f == 'papka':
        images_dir = args.path

        if images_dir == '':
            print('Файл отсутствует')

        files = [os.path.join(images_dir, f) for f in os.listdir(images_dir)]

        if not files:
            print('Папка с файлами пустая')

        for file in files:
            processed_image(file, out_jpegs, out_webps)