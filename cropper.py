from PIL import Image
import files


TARGET_UPPER_0   = (187, 187, 187)
TARGET_UPPER_1   = (186, 186, 186)
TARGET_UPPER_2   = (112, 112, 112)
NEIGHBOUR_UPPER_0 = (239, 239, 239)
NEIGHBOUR_UPPER_1 = (143, 143, 143)

TARGET_LOWER_0   = (176, 176, 176)
TARGET_LOWER_1   = (175, 175, 175)
TARGET_LOWER_2   = (106, 106, 106)
NEIGHBOUR_LOWER_0 = (238, 238, 238)
NEIGHBOUR_LOWER_1 = (143, 143, 143)


def get_targets(image, x, y):
    targets = {}
    targets['target'] = image.getpixel((x, y))
    targets['right'] = image.getpixel((x + 1, y))
    targets['down'] = image.getpixel((x, y + 1))
    targets['left'] = image.getpixel((x - 1, y))
    targets['up'] = image.getpixel((x, y - 1))
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
                        )                    
                        and (t.get('right') == NEIGHBOUR_UPPER_0 or t.get('right') == NEIGHBOUR_UPPER_1)
                        and (t.get('down')  == NEIGHBOUR_UPPER_0 or t.get('down')  == NEIGHBOUR_UPPER_1)
                ): target_left_coordinates.append((x, y))                
                if (
                        (
                        t.get('target')     == TARGET_LOWER_0
                        or t.get('target')  == TARGET_LOWER_1 
                        or t.get('target')  == TARGET_LOWER_2
                        )
                        and (t.get('left')  == NEIGHBOUR_LOWER_0 or t.get('left') == NEIGHBOUR_LOWER_1)
                        and (t.get('up')    == NEIGHBOUR_LOWER_0 or t.get('up')   == NEIGHBOUR_LOWER_1)
                ): target_right_coordinates.append((x, y))
        c = list(zip(target_left_coordinates, target_right_coordinates))
        coordinates.append(c)
    return coordinates


def remove_nested_tuples(coordinates: list) -> list:
    coordinates = [
        (item[0][0], item[1][1])
        if len(item) == 2
        else tuple(*item)
        for item in coordinates
        ]
    return coordinates


def crop_corners(files: list, target_pixels: list) -> None:
    images = [Image.open(image) for image in files]
    for i in range(len(images)):
        crop = images[i].crop((
            target_pixels[i][0][0],
            target_pixels[i][0][1],
            target_pixels[i][1][0] + 1,
            target_pixels[i][1][1] + 1
            ))
        crop.save(f'cropped_image_{i}.png')


def main(file):
    coordinates = remove_nested_tuples(find_target_pixels(file))
    crop_corners(file, coordinates)


if __name__ == '__main__':    
    main(files.get_files_list(path=False))
