'''The script is aimed to crop wizard windows of the PolyAnalyst nodes.'''


import os
from PIL import Image
import data
import misc

# import target colors
target_upper = data.get_upper_target()
target_upper_neighbor = data.get_upper_neighbors()
target_lower = data.get_lower_target()
target_lower_neighbor = data.get_lower_neighbors()


# find target pixels and their neighbours
def get_targets(image: any, x: int, y: int) -> dict:
    targets = dict(
        target = image.getpixel((x, y)),
        right  = image.getpixel((x + 1, y)),
        down   = image.getpixel((x, y + 1)),
        left   = image.getpixel((x - 1, y)),
        up     = image.getpixel((x, y - 1))
    )
    return targets

# create a list of coordinates for the target pixels
def find_target_pixels(directory: str, files: list) -> list:
    c = []
    print(f'{misc.get_time()}', 'Getting a list of files...')
    print(f'{misc.get_time()}', 'There are ' + str(len(files)) + ' files found that match the pattern.')
    for file in files:
        print(f'{misc.get_time()}', 'Processing: ' + file)
        # concatenate a path and file, e.g. 'D:/folder/screenshot_1.png')
        image_full_path = os.path.join(directory, file)
        image = Image.open(image_full_path).convert('RGB')
        width, height = image.size
        target_left_coordinates = []
        target_right_coordinates = []
        for x in range(width - 1):
            for y in range(height - 1):
                t = get_targets(image, x, y)
                if (
                        (
                        t.get('target')       == target_upper.get('upper_0')
                        or t.get('target')    == target_upper.get('upper_1')
                        or t.get('target')    == target_upper.get('upper_2')
                        or t.get('target')    == target_upper.get('upper_4')
                        or t.get('target')    == target_upper.get('upper_5')
                        or t.get('target')    == target_upper.get('upper_6')
                        )
                        and (
                            t.get('right')    == target_upper_neighbor.get('neighbor_0')
                            or t.get('right') == target_upper_neighbor.get('neighbor_1')
                            or t.get('right') == target_upper_neighbor.get('neighbor_2')
                        )
                        and (
                            t.get('down')     == target_upper_neighbor.get('neighbor_0')
                            or t.get('down')  == target_upper_neighbor.get('neighbor_1')
                            or t.get('down')  == target_upper_neighbor.get('neighbor_2')
                        )
                ): target_left_coordinates.append((x, y))
                if (
                        (
                        t.get('target')       == target_lower.get('lower_0')
                        or t.get('target')    == target_lower.get('lower_1')
                        or t.get('target')    == target_lower.get('lower_2')
                        or t.get('target')    == target_lower.get('lower_4')
                        or t.get('target')    == target_lower.get('lower_5')
                        or t.get('target')    == target_lower.get('lower_6')
                        )
                        and ( 
                            t.get('left')     == target_lower_neighbor.get('neighbor_0')
                            or t.get('left')  == target_lower_neighbor.get('neighbor_1')
                            or t.get('left')  == target_lower_neighbor.get('neighbor_2')
                        )
                        and ( 
                            t.get('up')       == target_lower_neighbor.get('neighbor_0')
                            or t.get('up')    == target_lower_neighbor.get('neighbor_1')
                            or t.get('up')    == target_lower_neighbor.get('neighbor_2')
                        )
                ): target_right_coordinates.append((x, y))
        coordinates = target_left_coordinates + target_right_coordinates
        # print(coordinates)
        c.append(coordinates)
    # c = [(item[0], item[-1]) for item in c if item]
    # print(c)
    # for i in range(0, len(files)): print(f'{i}: ' + str(files[i]) + ' : ' + str(c[i]))
    return c


def edit_coordinates_lists(coordinates: list) -> list:
    # print(coordinates)
    coordinates = [
        (item[0], item[-1]) for item in coordinates if item
    ]
    # print(coordinates)
    # print(len(coordinates))
    return coordinates

# TODO: нужно сделать функцию, которая принимает список файлов
# ищет целевые пиксели для каждого файла
# и возвращает новый список файлов
# только с теми файлами, где есть целевые пиксели
# а потом этот список нужно использовать в функции crop_corners()
# потому что сейчас обрезаются все файлы


# main logic of the script, i.e. image cropping
def crop_corners(directory, files: list, target_pixels: list) -> None:
    file_number = 1
    # print(len(files))
    # print(len(target_pixels))
    for i in range(len(files)):
    # for i in range(len(target_pixels)):
        # skip empty coordinates
        if not target_pixels[i]:
            continue
        # concatenate a path and file, e.g. 'D:/folder/screenshot_1.png')
        full_path = os.path.join(directory, files[i])
        image = Image.open(full_path)
        crop = image.crop((
            target_pixels[i][0][0],
            target_pixels[i][0][1],
            target_pixels[i][1][0] + 1,
            target_pixels[i][1][1] + 1
            ))
        crop.save(f'Cropped_{file_number}.png')
        file_number += 1


def main(directory, files):
    targets = find_target_pixels(directory, files)
    coordinates = edit_coordinates_lists(targets)
    # print(coordinates)

    # main logic of the program
    # crop_corners(directory, files, coordinates)
    crop_corners(directory, files, targets)

    print(f'{misc.get_time()}', 'The script is finished.')
    # close the script
    misc.close_script()


if __name__ == '__main__':
    directory, files_list = misc.get_input()
    # start the main script
    main(directory, files_list)
