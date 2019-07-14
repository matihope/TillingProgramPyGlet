import pyglet
from pyglet.gl import *
from modules import grid
from modules import tile
import math


class TileChoose(object):
    def __init__(self, editor, tiles, tile_width, tile_height, tile_file):
        self.main_batch = pyglet.graphics.Batch()
        self.editor = editor

        self.tile_file = tile_file
        self.tiles = tiles
        self.chosen_tile = 0
        self.chosen_w = 1
        self.chosen_h = 1
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.grid_width = math.ceil(self.tile_file.width / self.tile_width)
        self.grid_height = math.ceil(self.tile_file.height / self.tile_height)

        self.tile_list = []

        self.grid = grid.Grid()

        for i in range(len(self.tiles)):
            t = tile.Tile(self.tiles, i, batch=self.main_batch, tag=self.editor.tag[i])
            SLOTS_IN_ROW = math.ceil(self.tile_file.width / self.tile_width)
            t.x = self.tile_width * (i % SLOTS_IN_ROW)
            t.y = self.tile_height * int(i / SLOTS_IN_ROW)
            self.tile_list.append(t)

    def draw(self):
        self.main_batch.draw()
        self.grid.draw(self.tile_width, self.tile_height, self.grid_width, self.grid_height)
        self.draw_tile_outline()

    def draw_tile_outline(self):
        SLOTS_IN_ROW = math.ceil(self.tile_file.width / self.tile_width)
        left = self.tile_width * (self.chosen_tile % SLOTS_IN_ROW)
        bottom = self.tile_height * int(self.chosen_tile / SLOTS_IN_ROW)
        right = left + self.tile_width * self.chosen_w
        top = bottom + self.tile_height * self.chosen_h

        glLineWidth(3.0)
        glBegin(GL_LINES)
        gl.glColor4f(255/255, 50/255, 50/255, 1)

        # Left border
        glVertex2f(left, bottom)
        glVertex2f(left, top)

        # Right border
        glVertex2f(right, bottom)
        glVertex2f(right, top)

        # Top border
        glVertex2f(left, top)
        glVertex2f(right, top)

        # Bottom border
        glVertex2f(left, bottom)
        glVertex2f(right, bottom)

        glEnd()
        glLineWidth(1.0)

    def reload(self, editor, tiles, tile_width, tile_height, tile_file):
        self.editor = editor

        self.tile_file = tile_file
        self.tiles = tiles
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.grid_width = math.ceil(self.tile_file.width / self.tile_width)
        self.grid_height = math.ceil(self.tile_file.height / self.tile_height)

        self.tile_list = []

        self.grid = grid.Grid()

        for i in range(len(self.tiles)):
            t = tile.Tile(self.tiles, i, batch=self.main_batch, tag=self.editor.tag[i])
            SLOTS_IN_ROW = math.ceil(self.tile_file.width / self.tile_width)
            t.x = self.tile_width * (i % SLOTS_IN_ROW)
            t.y = self.tile_height * int(i / SLOTS_IN_ROW)
            self.tile_list.append(t)
