import datetime
"""
-background
-area width
-area height
-----------TILES
-tile width
-tile height
-tile file_name
-tile num
"""


def create_tile_text(tile_list):
    tile_text = []

    for tile in tile_list:
        tile_text.append(f'tile:{tile.file_name},{tile.tile_num},{tile.x},{tile.y},{tile.width},{tile.height},{tile.rotation},{tile.tag}')
        # 'tile:texture.png,0,160,48,16,16,0,DEFAULT'
        # 'tile:file,tile,x,y,width,height,rotation,tag'

    return tile_text


def add_backslash_n(text):
    t = []
    for o in text:
        for line in o:
            t.append(line+'\n')
    return t


def save(file_name, tile_list, bg=None, area_w=1, area_h=1):
    def update(t):
        file = open('levels/' + file_name+'.txt', 'w')
        file.writelines(t)
        file.close()

    text = []

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start = ['#TILES_DATA',
             f'#Update:{time}',
             f'create_area:{area_w},{area_h}',
             f'background_image:{bg if bg is not None else "-1"}']
    text.append(start)

    text.append(create_tile_text(tile_list))

    text = add_backslash_n(text)
    update(text)
