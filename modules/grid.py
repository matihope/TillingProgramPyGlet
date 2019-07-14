from pyglet.gl import *


class Grid(object):
    def draw(self, tile_width, tile_height, area_w, area_h):
        # glClear(GL_COLOR_BUFFER_BIT)  # draw connected vertices

        glBegin(GL_LINES)

        gl.glColor4f(238/255, 238/255, 238/255, 1)

        # +1 for perfect area, 4 borders
        # Drawing vertical lines
        for i in range(area_w + 1):
            glVertex2i(i * tile_width, 0)  # origin(bottom)
            glVertex2i(i * tile_width, area_h * tile_height)  # end of screen(top)

        # Drawing horizontal lines
        for i in range(area_h + 1):
            glVertex2i(0,                   tile_height * i)  # origin(left)
            glVertex2i(area_w * tile_width, tile_height * i)  # end of screen(right)

        glEnd()
