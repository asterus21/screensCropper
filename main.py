from PIL import Image
import files


# upper pixel color
TARGET_UPPER_0    = (187, 187, 187) # check the value
TARGET_UPPER_1    = (186, 186, 186) # check the value
TARGET_UPPER_2    = (112, 112, 112) # check the value
TARGET_UPPER_3    = (153, 153, 153) # check the value
TARGET_UPPER_4    = (182, 182, 182) # check the value
TARGET_UPPER_5    = (162, 162, 162) # check the value
NEIGHBOUR_UPPER_0 = (239, 239, 239) # check the value
NEIGHBOUR_UPPER_1 = (143, 143, 143) # check the value
NEIGHBOUR_UPPER_2 = (238, 238, 238) # check the value
# lower pixel color
TARGET_LOWER_0    = (176, 176, 176) # check the value
TARGET_LOWER_1    = (175, 175, 175) # check the value
TARGET_LOWER_2    = (106, 106, 106) # check the value
TARGET_LOWER_3    = (143, 143, 143) # check the value
TARGET_LOWER_4    = (173, 173, 173) # check the value
TARGET_LOWER_5    = (151, 151, 151) # check the value
NEIGHBOUR_LOWER_0 = (238, 238, 238) # check the value
NEIGHBOUR_LOWER_1 = (143, 143, 143) # check the value
NEIGHBOUR_LOWER_2 = (237, 237, 237) # check the value


def get_targets(image, x, y):
    targets = {}
    targets['target'] = image.getpixel((x, y))
    targets['right']  = image.getpixel((x + 1, y))
    targets['down']   = image.getpixel((x, y + 1))
    targets['left']   = image.getpixel((x - 1, y))
    targets['up']     = image.getpixel((x, y - 1))
    return targets


def find_target_pixels(files: list):
    coordinates = []
    for file in files:
        image = Image.open(file).convert('RGB')
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
                        # or t.get('target')  == TARGET_UPPER_3
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
                        # or t.get('target')  == TARGET_LOWER_3
                        ) 
                        # and t.get('right') != TARGET_LOWER_0                                             
                        and (
                            t.get('left')  == NEIGHBOUR_LOWER_0 or t.get('left') == NEIGHBOUR_LOWER_1) # or t.get('left') == NEIGHBOUR_LOWER_2)
                        and (
                            t.get('up')    == NEIGHBOUR_LOWER_0 or t.get('up')   == NEIGHBOUR_LOWER_1) # or t.get('up') == NEIGHBOUR_LOWER_2)                    
                ): target_right_coordinates.append((x, y))
        c = list(zip(target_left_coordinates, target_right_coordinates))
        coordinates.append(c)
        # coordinates.sort()
    # for i in range(1, len(files)): print(f'{i}: ' + str(files[i]) + ' : ' + str(coordinates[i]))
    return coordinates


def remove_nested_tuples(coordinates: list) -> list:
    # print(coordinates)
    coordinates = [
        # (item[0][0], item[1][1]) if len(item) == 2
        # (item[0][0], item[1][1]) if len(item) > 2
        # (item[0][0], item[-1]-[1]) if len(item) == 2
        # (item[0][0], item[-1]-[1]) if len(item) > 2
        (item[0][0], item[-1][-1]) if len(item) >= 2 
        else tuple(*item) 
        for item in coordinates
        ]
    # print(coordinates)
    return coordinates


def crop_corners(files: list, target_pixels: list) -> None:
    images = [Image.open(image) for image in files]
    for i in range(len(images)):
        # skip empty coordinates 
        if not target_pixels[i]: continue
        crop = images[i].crop((
            target_pixels[i][0][0],     # is it right x?
            target_pixels[i][0][1],     # is it right y?
            target_pixels[i][1][0] + 1, # is it left x?
            target_pixels[i][1][1] + 1  # is it left y?
            ))
        crop.save(f'cropped_{i}.png')


def main(files):
    f = remove_nested_tuples(find_target_pixels(files))
    crop_corners(files, f)


if __name__ == '__main__':
    main(files.get_files_list(path=False))
