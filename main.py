import os
from PIL import Image
import misc

# get current time
time = misc.get_time()


# upper pixel color
TARGET_UPPER_0    = (187, 187, 187)
TARGET_UPPER_1    = (186, 186, 186)
TARGET_UPPER_2    = (112, 112, 112)
# TARGET_UPPER_3    = (153, 153, 153)
TARGET_UPPER_4    = (182, 182, 182)
TARGET_UPPER_5    = (162, 162, 162)
NEIGHBOUR_UPPER_0 = (239, 239, 239)
NEIGHBOUR_UPPER_1 = (143, 143, 143)
NEIGHBOUR_UPPER_2 = (238, 238, 238)
# lower pixel color
TARGET_LOWER_0    = (176, 176, 176)
TARGET_LOWER_1    = (175, 175, 175)
TARGET_LOWER_2    = (106, 106, 106)
# TARGET_LOWER_3    = (143, 143, 143)
TARGET_LOWER_4    = (173, 173, 173)
TARGET_LOWER_5    = (151, 151, 151)
NEIGHBOUR_LOWER_0 = (238, 238, 238)
NEIGHBOUR_LOWER_1 = (143, 143, 143)
# NEIGHBOUR_LOWER_2 = (237, 237, 237)


# find target pixels and their neighbours
def get_targets(image, x, y):
    targets = {}
    targets['target'] = image.getpixel((x, y))
    targets['right']  = image.getpixel((x + 1, y))
    targets['down']   = image.getpixel((x, y + 1))
    targets['left']   = image.getpixel((x - 1, y))
    targets['up']     = image.getpixel((x, y - 1))
    return targets


# create a list of coordinates for the target pixels
def find_target_pixels(directory, files: list):
    coordinates = []
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
                        t.get('target')     == TARGET_UPPER_0
                        or t.get('target')  == TARGET_UPPER_1
                        or t.get('target')  == TARGET_UPPER_2
                        or t.get('target')  == TARGET_UPPER_4
                        or t.get('target')  == TARGET_UPPER_5
                        )
                        and (t.get('right') == NEIGHBOUR_UPPER_0 or t.get('right') == NEIGHBOUR_UPPER_1 or t.get('right') == NEIGHBOUR_UPPER_2)
                        and (t.get('down')  == NEIGHBOUR_UPPER_0 or t.get('down')  == NEIGHBOUR_UPPER_1 or t.get('down') == NEIGHBOUR_UPPER_2)
                ): target_left_coordinates.append((x, y))
                if (
                        (
                        t.get('target')     == TARGET_LOWER_0
                        or t.get('target')  == TARGET_LOWER_1
                        or t.get('target')  == TARGET_LOWER_2
                        or t.get('target')  == TARGET_LOWER_4
                        or t.get('target')  == TARGET_LOWER_5
                        )
                        and (
                            t.get('left')  == NEIGHBOUR_LOWER_0 or t.get('left') == NEIGHBOUR_LOWER_1)
                        and (
                            t.get('up')    == NEIGHBOUR_LOWER_0 or t.get('up')   == NEIGHBOUR_LOWER_1)
                ): target_right_coordinates.append((x, y))
        c = list(zip(target_left_coordinates, target_right_coordinates))
        coordinates.append(c)
    # for i in range(1, len(files)): print(f'{i}: ' + str(files[i]) + ' : ' + str(coordinates[i]))
    return coordinates


# unpack coordinates from an array of lists
def remove_nested_tuples(coordinates: list) -> list:
    coordinates = [
        (item[0][0], item[-1][-1]) if len(item) >= 2
        else tuple(*item)
        for item in coordinates
        ]
    return coordinates


# main logic of the script, i.e. image cropping
def crop_corners(directory, files: list, target_pixels: list) -> None:    
    file_number = 1    
    for i in range(len(files)):
        # skip empty coordinates
        if not target_pixels[i]: continue
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
    f = remove_nested_tuples(find_target_pixels(directory, files))
    crop_corners(directory, files, f)
    print(f'{misc.get_time()}', 'The script is finished.')
    misc.close_script()


if __name__ == '__main__':
    directory, files_list = misc.get_input()
    main(directory, files_list)
