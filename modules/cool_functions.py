def get_tile_in_pos(x, y, tiles):
    for t in tiles:
        if [x, y] == [t.x, t.y]:
            return t


def get_number_of_tiles_in_pos(x, y, tiles):
    ts = 0
    for t in tiles:
        if [x, y] == [t.x, t.y]:
            ts += 1
    return ts


def spot_is_free(x, y, tiles):
    for t in tiles:
        if [x, y] == [t.x, t.y]:  # Checking if the spot is free
            return False
    return True


def mouse_in_grid(x, y, area_w, area_h, tile_w, tile_h):
    if (0 > y or y >= area_h * tile_h) or \
       (0 > x or x >= area_w * tile_w):
        return False
    return True
