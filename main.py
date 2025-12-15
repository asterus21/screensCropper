import os
from PIL import Image


"""
условный exe-файл закидывается в папку со скриншотами и запускается через терминал
по умолчанию два ключевых аргумента булевого типа: path --false, source --false
если передать path=true или не передавать, то скрипт будет брать скриншоты из текущей директори
если передать source=true или не передавать, то исходные файлы будут перезаписаны

после запуска скрипта проверять: есть ли png-файлы
если нет - выходить, если есть - проверять: есть ли нужные пиксели сверху и снизу
если нет - выходить, если есть - резать изображение

проверять: есть ли пиксели только сверху, если есть - пропускать пиксели снизу
проверять: есть ли пиксели только снизу, если есть - пропускать пиксели сверху

выводить в консоль: 
1) список файлов
2) сообщение типа: screenshot_1.png was cropped
3) сообщение о том, что скрипт завершен
"""

def get_list_of_files() -> list:
    # print('Enter a path to the folder containing screens (e.g. D:/py/screensCutter): ', end='')
    # user_input = input()
    DEFAULT_PATH = 'D:/py/screensCutter'
    files = [f for f in os.listdir(DEFAULT_PATH) if f.endswith('.png')]
    # print('files: ' + str(files))
    return files


def find_target_pixels(file: bytes):
    TARGET_UPPER = (186, 186, 186)
    NEIGHBOR_UPPER = (239, 239, 239)
    TARGET_LOWER = (175, 175, 175)
    NEIGHBOR_LOWER = (238, 238, 238)
    image = Image.open(file).convert('RGB')
    width, height = image.size
    target_left_coordinates = []
    target_right_coordinates = []
    for x in range(width - 1):
        for y in range(height - 1):
            pixel = image.getpixel((x, y))
            pixel_right = image.getpixel((x + 1, y))
            pixel_down = image.getpixel((x, y + 1))
            pixel_left = image.getpixel((x - 1, y))
            pixel_up = image.getpixel((x, y - 1))
            if pixel == TARGET_UPPER and pixel_right == NEIGHBOR_UPPER and pixel_down == NEIGHBOR_UPPER:
                target_left_coordinates.append((x, y))
            if pixel == TARGET_LOWER and pixel_left == NEIGHBOR_LOWER and pixel_up == NEIGHBOR_LOWER:
                target_right_coordinates.append((x, y))
    coordinates = list(zip(target_left_coordinates, target_right_coordinates))
    # print('coordinates: ' + str(coordinates))
    return coordinates


def crop_corners(file: bytes, target_pixels: tuple) -> None:
    image = Image.open(file)
    crop = image.crop((
        target_pixels[0][0][0],
        target_pixels[0][0][1],
        target_pixels[0][1][0] + 1,
        target_pixels[0][1][1] + 1
        ))
    crop.save(f'crop_test_2.png')


def main():
    file = 'D:/py/screensCutter/Screenshot_3.png'
    find_target_pixels('D:/py/screensCutter/Screenshot_3.png')
    crop_corners(file, find_target_pixels('D:/py/screensCutter/Screenshot_3.png'))


if __name__ == '__main__':
    # main()
    pass
