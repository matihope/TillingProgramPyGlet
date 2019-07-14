import pyglet
import math

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()


def grid(file_name, tile_width, tile_height):
    image = pyglet.resource.image(file_name)
    tiles = pyglet.image.ImageGrid(image, math.ceil(image.height/tile_height), math.ceil(image.width/tile_width))
    return tiles


def read_values_from_line(line, start_letter, amount_of_values, key_separator=','):
    values = []
    letter = start_letter
    new_letter = letter
    while len(values) < amount_of_values:
        new_letter += 1
        if line[new_letter-1:new_letter] == key_separator or new_letter-1 == len(line):
            values.append(line[start_letter:new_letter-1])  # Add value to values
            start_letter = new_letter

        if new_letter > len(line)+10:
            print('Error!!!')
            break

    return values


def decode(list, tile_sprite, batch):
    new_list = []
    area_w = 1
    area_h = 1
    tile_w = 50
    tile_h = 50
    bg = None

    for line in list:
        if line[:1] == '#':
            continue

        for i in range(len(line)):
            if line[:i] == 'create_area:':
                area_w, area_h = read_values_from_line(line, i, 2)
                area_w, area_h = int(area_w), int(area_h)
                break

            if line[:i] == 'background_image:':
                new_bg = read_values_from_line(line, i, 1)
                new_bg = int(new_bg[0])

                bg = new_bg
                if new_bg == -1:
                    bg = None
                break

            if line[:i] == 'tile:':
                values = read_values_from_line(line, i, 8)
                file_name = values[0]

                # Convert values to ints(tile_num, width, height)
                tile_num, width, height = int(values[1]), int(values[4]), int(values[5])
                tile_w, tile_h = width, height
                # Converts the values to float(x,y)
                x, y = float(values[2]), float(values[3])
                rotation = int(values[6])
                tag = values[7]

                tile_images = grid(file_name, width, height)

                new_tile = tile_sprite(tile_images, tile_num, file_name=file_name, batch=batch, tag=tag)
                new_tile.x, new_tile.y = x, y
                new_tile.rotation = rotation
                new_list.append(new_tile)
                break

    return area_w, area_h, tile_w, tile_h, bg, new_list


def strip_from_backslash_n(list):
    new_list = []
    for line in list:
        new_list.append(line[:-1])
    return new_list


def read_file(file_name):
    file = open('levels/' + file_name + '.txt', 'r')
    lines = file.readlines()
    file.close()
    return lines


def read(file_name, tile_sprite, batch):
    tile_list = read_file(file_name)
    tile_list = strip_from_backslash_n(tile_list)
    area_w, area_h, tile_w, tile_h, bg, tile_list = decode(tile_list, tile_sprite, batch)
    return area_w, area_h, tile_w, tile_h, bg, tile_list
