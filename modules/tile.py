import pyglet
from pyglet.gl import *

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()


class Tile(pyglet.sprite.Sprite):
    def __init__(self, texture, tile_num, file_name=None, batch=None, tag='DEFAULT'):
        self.tile_num = tile_num
        self.file_name = file_name
        self.tag = tag
        super(Tile, self).__init__(img=texture[tile_num], batch=batch)
