from pyglet.gl import *


class Camera(object):
    zoom_in_factor = 1.2
    zoom_out_factor = 1 / zoom_in_factor

    def __init__(self, window, cameras=1):
        self.window = window
        self.width, self.height = self.window.width, self.window.height
        self.cameras = cameras
        self.current_cam = 0

        # left and right are set for -1, to shift it on start, then full grid is visible
        self.left = -1
        self.right = self.window.width - 1
        self.bottom = 0
        self.top = self.window.height
        self.zoom_level = 1
        self.zoomed_width = self.window.width
        self.zoomed_height = self.window.height

        # For other cameras
        self.left_ = []
        self.right_ = []
        self.bottom_ = []
        self.top_ = []
        self.zoom_level_ = []
        self.zoomed_width_ = []
        self.zoomed_height_ = []
        for c in range(self.cameras):
            self.left_.append(self.left)
            self.right_.append(self.right)
            self.bottom_.append(self.bottom)
            self.top_.append(self.top)
            self.zoom_level_.append(self.zoom_level)
            self.zoomed_width_.append(self.zoomed_width)
            self.zoomed_height_.append(self.zoomed_height)

    def init_gl(self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, self.width, self.height)

    def switch(self, cam):
        # Save previous cam
        self.left_[self.current_cam] = self.left
        self.right_[self.current_cam] = self.right
        self.top_[self.current_cam] = self.top
        self.bottom_[self.current_cam] = self.bottom
        self.zoom_level_[self.current_cam] = self.zoom_level
        self.zoomed_width_[self.current_cam] = self.zoomed_width
        self.zoomed_height_[self.current_cam] = self.zoomed_height

        # Switch cameras
        self.current_cam = cam
        self.left = self.left_[cam]
        self.right = self.right_[cam]
        self.bottom = self.bottom_[cam]
        self.top = self.top_[cam]
        self.zoom_level = self.zoom_level_[cam]
        self.zoomed_width = self.zoomed_width_[cam]
        self.zoomed_height = self.zoomed_height_[cam]

    def reset(self):
        # left and right are set for -1, to shift it on start, then full grid is visible
        self.left = -1
        self.right = self.window.width - 1
        self.bottom = 0
        self.top = self.window.height
        self.zoom_level = 1
        self.zoomed_width = self.window.width
        self.zoomed_height = self.window.height

    def draw(self):
        glClearColor(46 / 255, 46 / 255, 49 / 255, 0.2)

        glPushMatrix()
        glOrtho(self.left, self.right, self.bottom, self.top, 1, -1)

        # Disable anti-aliasing
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.window.clear()

        # Draw stuff here
        self.window.draw_elements()

        glPopMatrix()

    def scroll(self, x, y, dy):
        f = self.zoom_in_factor if dy > 0 else self.zoom_out_factor if dy < 0 else 1
        if .01 < self.zoom_level * f < 5:
            self.zoom_level *= f

            mouse_x = x / self.width
            mouse_y = y / self.height

            mouse_x_in_world = self.left + mouse_x * self.zoomed_width
            mouse_y_in_world = self.bottom + mouse_y * self.zoomed_height

            self.zoomed_width *= f
            self.zoomed_height *= f

            self.left = mouse_x_in_world - mouse_x * self.zoomed_width
            self.right = mouse_x_in_world + (1 - mouse_x) * self.zoomed_width
            self.bottom = mouse_y_in_world - mouse_y * self.zoomed_height
            self.top = mouse_y_in_world + (1 - mouse_y) * self.zoomed_height
