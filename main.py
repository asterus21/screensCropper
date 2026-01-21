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
    targets = []
    print(f'{misc.print_time()}', 'Getting a list of files...')
    print(f'{misc.print_time()}', 'There ' + str(len(files)) + ' file(s) found that match the pattern.')
    for file in files:
        print(f'{misc.print_time()}', 'Processing: ' + file)
        # concatenate a path and file, e.g. 'D:/folder/screenshot_1.png')
        image = Image.open(os.path.join(directory, file)).convert('RGB')
        width, height = image.size
        target_left_coordinates = []
        target_right_coordinates = []
        for x in range(width - 1):
            for y in range(height - 1):
                t = get_targets(image, x, y)
                if (
                        (
                        t.get('target') == target_upper.get('upper_0') or 
                        t.get('target') == target_upper.get('upper_1') or 
                        t.get('target') == target_upper.get('upper_2') or 
                        t.get('target') == target_upper.get('upper_4') or 
                        t.get('target') == target_upper.get('upper_5') or 
                        t.get('target') == target_upper.get('upper_6') or
                        t.get('target') == target_upper.get('upper_7')
                        ) and 
                        (
                        t.get('right')  == target_upper_neighbor.get('neighbor_0') or 
                        t.get('right')  == target_upper_neighbor.get('neighbor_1') or 
                        t.get('right')  == target_upper_neighbor.get('neighbor_2')
                        )
                        and 
                        (
                        t.get('down')   == target_upper_neighbor.get('neighbor_0') or 
                        t.get('down')   == target_upper_neighbor.get('neighbor_1') or 
                        t.get('down')   == target_upper_neighbor.get('neighbor_2')
                        )
                ): target_left_coordinates.append((x, y))
                if (
                        (
                        t.get('target') == target_lower.get('lower_0') or
                        t.get('target') == target_lower.get('lower_1') or
                        t.get('target') == target_lower.get('lower_2') or
                        t.get('target') == target_lower.get('lower_4') or
                        t.get('target') == target_lower.get('lower_5') or
                        t.get('target') == target_lower.get('lower_6') or
                        t.get('target') == target_lower.get('lower_7')
                        ) and 
                        ( 
                        t.get('left')   == target_lower_neighbor.get('neighbor_0') or
                        t.get('left')   == target_lower_neighbor.get('neighbor_1') or
                        t.get('left')   == target_lower_neighbor.get('neighbor_2') or
                        t.get('left')   == target_lower_neighbor.get('neighbor_3')
                        ) and
                        (
                        t.get('up')     == target_lower_neighbor.get('neighbor_0') or
                        t.get('up')     == target_lower_neighbor.get('neighbor_1') or
                        t.get('up')     == target_lower_neighbor.get('neighbor_2') or
                        t.get('left')   == target_lower_neighbor.get('neighbor_3')
                        )
                ): target_right_coordinates.append((x, y))
        coordinates = target_left_coordinates + target_right_coordinates
        targets.append(coordinates)
    # for i in range(0, len(files)): print(f'{i}: ' + str(files[i]) + ' : ' + str(c[i]))
    return targets


def remove_empty_targets(coordinates: list, files: list) -> dict:
    # get a dictionary with file names as keys and their coordinates as values
    s = {
        str(files[i]): coordinates[i] for i in range(0, len(files)) if coordinates[i]
    }
    return s


def edit_coordinates_list_as_dictionary(coordinates: dict) -> list:
    # fetch only the first and the last targets in case there are several ones
    coors = [
        (item[0], item[-1]) for item in coordinates.values() if item
    ]
    return coors


def get_new_list_of_files(files: dict) -> list:
    # fetch only the keys of the dictionary, i.e. files names
    return(list(files.keys()))


# main logic of the script, i.e. image cropping
def crop_corners(directory: str, files: list, target_pixels: list) -> None:
    file_number = 1
    for i in range(len(files)):
        # skip empty coordinates
        if not target_pixels[i]: continue
        # concatenate a path and file, e.g. 'D:/folder/screenshot_1.png')
        image = Image.open(os.path.join(directory, files[i]))
        crop = image.crop((
            target_pixels[i][0][0],
            target_pixels[i][0][1],
            target_pixels[i][1][0] + 1,
            target_pixels[i][1][1] + 1
            ))
        crop.save(f'Cropped_{file_number}.png')
        file_number += 1


def main(directory, files):
    # find target pixels
    targets = find_target_pixels(directory, files)
    # create a dictionary with names of files and pixel coordinates
    dictionary = remove_empty_targets(targets, files)
    # save pixel coordinates
    coordinates = edit_coordinates_list_as_dictionary(dictionary)
    # find only those files which contain target pixels
    new_list_of_files = get_new_list_of_files(dictionary)
    # main logic of the program
    crop_corners(directory, new_list_of_files, coordinates)
    # show that the script is finished
    print(f'{misc.print_time()}', 'The script is finished.')
    # close the script
    misc.close_script()


if __name__ == '__main__':
    # get the user's input
    directory, files_list = misc.get_input()
    # start the main script
    main(directory, files_list)
