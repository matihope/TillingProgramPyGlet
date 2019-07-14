# Mateusz Kolpa
# 2019
# Tiling Tool
import pyglet
import math
from modules import tile, grid, camera, tile_choose, saver, reader
from modules import cool_functions as cf
from pyglet.window import mouse, key


pyglet.resource.path = ["resources"]
pyglet.resource.reindex()


class EditorWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(EditorWindow, self).__init__(*args, **kwargs)

        # Mouse coordinates
        self.mouse_x = 0
        self.mouse_y = 0

        # Set key handler.
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.current_screen = 0  # 0 - drawing, 1 - choosing tiles

        self.main_batch = pyglet.graphics.Batch()
        self.tiles_batch = pyglet.graphics.Batch()

        self.camera = camera.Camera(self, cameras=2)  # 2 cameras, for 2 different views, grid and choosing
        self.invert_scroll = True

        self.replace_occupied_slots = False  # If on, then you will be able to just switch the tile in drawing

        self.draw_tags = True
        self.tag_label = pyglet.text.Label('', font_name='Born2bSportyV2', font_size=12)

        self.tile_width = 50
        self.tile_height = 50

        self.screen_ratio = (16, 9)

        self.drag_button = mouse.MIDDLE

        self.drawing_area_width = 20
        self.drawing_area_height = 10
        self.background = None  # This is not working yet :PP

        self.brush_size = 1
        self.brush_rotation = 0
        self.draw_tile = 0
        self.current_tile_file = 'texture_example.png'
        self.tiles_image = pyglet.resource.image(self.current_tile_file)  # Tile file not stripped
        self.tile_images = pyglet.image.ImageGrid(self.tiles_image,
                                                  math.ceil(self.tiles_image.height/self.tile_height),
                                                  math.ceil(self.tiles_image.width/self.tile_width))
        self.tag = []
        for i in range(len(self.tile_images)):
            self.tag.append('DEFAULT')

        self.grid = grid.Grid()

        self.draw_preview = tile.Tile(self.tile_images, self.draw_tile)
        self.new_draw_preview()  # Set everything

        self.tile_list = []  # This list contains all the tiles in the editor

        self.choose_area = tile_choose.TileChoose(self, self.tile_images, self.tile_width, self.tile_height, self.tiles_image)
        # This object has it's own variables, I recommend check the tile_choose file out

        self.current_level_file = ''  # The file, that we are working with, very useful, makes everything quicker

        pyglet.clock.schedule_interval(self.window_tick, 1/120)

        # Gets print put every time we run a program
        print('---------------------------------------------------------')
        print('Press [SPACE] to show settings')
        print('Press [C] to change tile graphically, [T] on tile to change tag')
        print('Use mouse [MIDDLE] to drag menu, [LEFT] to draw, [RIGHT] to delete')
        print('---------------------------------------------------------')

    def window_tick(self, dt):
        self.update_tag_label()
        self.camera.draw()  # Drawing the camera draws everything to the screen

    def crazy_draw_preview(self):
        # This functions draws preview with custom brush size

        start_x = self.draw_preview.x  # Get start points
        start_y = self.draw_preview.y
        self.draw_preview.rotation = self.brush_rotation

        for i in range(self.brush_size):
            xx = start_x + (self.tile_width * i)
            for j in range(self.brush_size):
                yy = start_y + (self.tile_height * j)

                self.draw_preview.x, self.draw_preview.y = xx, yy  # New pos
                if cf.mouse_in_grid(xx, yy, self.drawing_area_width, self.drawing_area_height, self.tile_width, self.tile_height):
                    self.draw_preview.draw()

        self.draw_preview.x, self.draw_preview.y = start_x, start_y  # Default

    def on_key_press(self, symbol, modifiers):
        if symbol == key.C:  # Open tile menu
            self.current_screen = 1 if self.current_screen == 0 else 0
            self.camera.switch(self.current_screen)

        if symbol == key.SPACE:  # Drawing menu
            self.draw_menu()

        if symbol == key.T:  # Switch tag
            self.switch_tag()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x, self.mouse_y = self.get_mouse_pos(x, y)  # Update the mouse position variables

        # In editor, update position of preview
        if self.current_screen == 0:
            x, y = self.mouse_x, self.mouse_y
            if not cf.mouse_in_grid(x, y, self.drawing_area_width, self.drawing_area_height, self.tile_width, self.tile_height):
                if self.brush_size == 1:  # Don't draw preview outside the grid, when size is 1
                    return

            self.draw_preview.x, self.draw_preview.y = x, y

    def get_mouse_pos(self, x, y):
        # This function calculates the position (x, y) of mouse

        t_w = self.tile_width
        t_h = self.tile_height
        x /= self.width
        y /= self.height
        x = self.camera.left + x * self.camera.zoomed_width
        y = self.camera.bottom + y * self.camera.zoomed_height
        x = x // t_w * t_w
        y = y // t_h * t_h
        return x, y

    def on_resize(self, width, height):
        # Update the camera settings
        self.camera.init_gl(self.width, self.height)

    def on_mouse_scroll(self, x, y, dx, dy):
        dy = -dy if self.invert_scroll else dy

        if self.keys[key.LCTRL]:
            self.camera.scroll(x, y, dy)  # Scroll camera

        elif self.keys[key.LSHIFT]:
            # Camera move horizontally
            self.move_camera(dx=-dy*50)
        else:
            # Camera move vertically
            self.move_camera(dy=dy*50)

    def update_tag_label(self):
        # Updating the tag_label text, for tile that the mouse is on

        if self.draw_tags:
            x, y = self.mouse_x, self.mouse_y
            self.tag_label.x, self.tag_label.y = x, y
            tile_list = self.tile_list if self.current_screen == 0 else self.choose_area.tile_list

            if not cf.spot_is_free(x, y, tile_list):
                t = cf.get_tile_in_pos(x, y, tile_list)
                self.tag_label.text = t.tag
            else:
                self.tag_label.text = ''

    def draw_elements(self):
        # Camera calls this method after cleaning the screen

        if self.current_screen == 0:  # Editor
            self.tiles_batch.draw()
            self.crazy_draw_preview()
            self.grid.draw(self.tile_width, self.tile_height, self.drawing_area_width, self.drawing_area_height)
            self.main_batch.draw()

        elif self.current_screen == 1:  # Choose tiles
            self.choose_area.draw()

        self.tag_label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Drawing and other stuff happens here

        x, y = self.mouse_x, self.mouse_y

        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)  # Setting a cool cursor
        self.set_mouse_cursor(cursor)

        # Drawing here
        if self.current_screen == 0:
            for i in range(self.brush_size):  # Drawing more tiles because of brush size
                new_x = x + self.tile_width*i
                for j in range(self.brush_size):
                    new_y = y + self.tile_height*j

                    if cf.mouse_in_grid(new_x, new_y, self.drawing_area_width, self.drawing_area_height, self.tile_width, self.tile_height):
                        spot_free = cf.spot_is_free(new_x, new_y, self.tile_list)
                        draw_tile_on_tile = (self.keys[key.LCTRL])

                        # Place a tile
                        if button == mouse.LEFT and (spot_free or draw_tile_on_tile or self.replace_occupied_slots):
                            if not spot_free:
                                tile_in_the_spot = cf.get_tile_in_pos(x, y, self.tile_list)

                                if draw_tile_on_tile:
                                    if tile_in_the_spot.tile_num == self.draw_tile:
                                        # Return when the tile there is the same as the one that we are trying to draw
                                        return
                                    if cf.get_number_of_tiles_in_pos(x, y, self.tile_list) > 1:
                                        # Return if in the spot there is already more than one tile
                                        return

                                if self.replace_occupied_slots and not draw_tile_on_tile:
                                    # We don't want to do this part if we are drawing tile on tile
                                    if tile_in_the_spot.tile_num == self.draw_tile:
                                        # Quit if there is this tile already
                                        return

                                    else:
                                        # Delete the tile if it's different than the one we are trying to draw
                                        tile_in_the_spot.delete()
                                        self.tile_list.remove(tile_in_the_spot)

                            t = tile.Tile(self.tile_images, self.draw_tile, self.current_tile_file,
                                          batch=self.tiles_batch, tag=self.tag[self.draw_tile])
                            t.x = new_x
                            t.y = new_y
                            t.rotation = self.brush_rotation
                            self.tile_list.append(t)

                            # Delete a tile
                        if button == mouse.RIGHT and not spot_free:
                            t = cf.get_tile_in_pos(new_x, new_y, self.tile_list)
                            t.delete()
                            self.tile_list.remove(t)

        # Choosing new tiles here
        elif self.current_screen == 1:
            if button == mouse.LEFT:
                if not cf.mouse_in_grid(x, y, self.choose_area.grid_width, self.choose_area.grid_height, self.tile_width, self.tile_height):
                    return
                self.update_tiles(new_draw_tile=cf.get_tile_in_pos(x, y, self.choose_area.tile_list).tile_num)

    def change_tile_size(self, new_tile_width, new_tile_height):
        # When changing the tile dimensions, it's necessary to change some other stuff

        image = pyglet.resource.image(self.current_tile_file)
        tiles_w, tiles_h = image.width // new_tile_width, image.height // new_tile_height  # Changing the preloaded tiles
        self.tile_images = pyglet.image.ImageGrid(image, tiles_h, tiles_w)

        self.tile_width, self.tile_height = new_tile_width, new_tile_height

        self.update_tiles(change_tile_size=True)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # To allow drawing while dragging, we're calling those methods
        self.on_mouse_motion(x, y, dx, dy)  # For drawing the tiles
        self.on_mouse_press(x, y, buttons, modifiers)  # For drawing the preview

        if buttons == self.drag_button:
            self.move_camera(dx, dy)

    def move_camera(self, dx=0, dy=0):
        # Move camera
        self.camera.left -= dx * self.camera.zoom_level
        self.camera.right -= dx * self.camera.zoom_level
        self.camera.bottom -= dy * self.camera.zoom_level
        self.camera.top -= dy * self.camera.zoom_level

    def on_mouse_release(self, x, y, button, modifiers):
        # Setting a default cursor back
        cursor = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
        self.set_mouse_cursor(cursor)

    def update_tiles(self, new_draw_tile=None, new_file=None, change_tile_size=None):
        # Important function, that takes care of changing the tiles

        if new_draw_tile is not None:
            self.draw_tile = new_draw_tile
            self.choose_area.chosen_tile = new_draw_tile

        if new_file is not None:
            self.current_tile_file = new_file
            self.choose_area.chosen_tile = 0
            self.choose_area.chosen_w = 1
            self.choose_area.chosen_h = 1
            change_tile_size = True

        self.tiles_image = pyglet.resource.image(self.current_tile_file)
        self.tile_images = pyglet.image.ImageGrid(self.tiles_image,
                                                  math.ceil(self.tiles_image.height / self.tile_height),
                                                  math.ceil(self.tiles_image.width / self.tile_width))

        if change_tile_size is not None:
            self.tag = []
            for i in range(len(self.tile_images)):
                self.tag.append('DEFAULT')

        self.new_draw_preview()
        self.choose_area.reload(self, self.tile_images, self.tile_width, self.tile_height, self.tiles_image)

    def new_draw_preview(self):
        # When changing the draw_tile, it's necessary to create a new draw_preview
        self.draw_preview.delete()
        self.draw_preview = tile.Tile(self.tile_images, self.draw_tile)
        self.draw_preview.opacity = 100  # (0-255)

    def draw_menu(self, option=None):
        # Drawing menu, and changing options

        try:
            menu = [
                f' Exit menu',
                f' Change current drawing tile, current: {self.draw_tile}',
                f' Change the tile image, current: {self.current_tile_file}',
                f' Change tile dimensions, current: W:{self.tile_width}, H:{self.tile_height}',
                f' Change drawing area dimensions, current: {self.drawing_area_width, self.drawing_area_height}',
                f' Change brush size, current: {self.brush_size}',
                f' Change brush rotation(0 is standard), current: {self.brush_rotation}',
                f' Change window size, current: {self.width, self.height}',
                f' Replace occupied slots with new tile, current: {self.replace_occupied_slots}',
                f' Save level to file {"NO_FILE_YET" if self.current_level_file == "" else self.current_level_file}',
                f' Read level from file {"NO_FILE_YET" if self.current_level_file == "" else self.current_level_file}',
                f' Changing working file from file {"NO_FILE_YET" if self.current_level_file == "" else self.current_level_file}',
                f' Choose this option to reset current camera to default'
            ]

            if option is None:
                print('Hey, choose what to change: ')

                for opt in range(len(menu)):
                    print(str(opt) + "." + menu[opt])

                option = int(input("Choose variable to change: "))
                print("---------------------------")
            option = menu[option]

            # exit menu
            if option == f' Exit menu':
                return

            # drawing tile
            elif option == f' Change current drawing tile, current: {self.draw_tile}':
                self.update_tiles(new_draw_tile=int(input("Give me new drawing tile: ")))

            elif option == f' Replace occupied slots with new tile, current: {self.replace_occupied_slots}':
                self.replace_occupied_slots = bool(int(input("Set replace_occupied_slots (0=False, 1=True): ")))

            # tile file
            elif option == f' Change the tile image, current: {self.current_tile_file}':
                self.update_tiles(new_file=input("Give me new file name, from resources: "))
                self.draw_menu(option=3)
                return

            # tile width, and height
            elif option == f' Change tile dimensions, current: W:{self.tile_width}, H:{self.tile_height}':
                if len(self.tile_list) == 0:
                    self.change_tile_size(int(input("Give me new tile width: ")), int(
                        input("Give me new tile height: ")))

                else:
                    print('---------------------------------------------------')
                    print('Can\'t change tile_dimensions, when tiles are placed')
                    print('---------------------------------------------------')

            # drawing area size
            elif option == f' Change drawing area dimensions, current: {self.drawing_area_width, self.drawing_area_height}':
                self.drawing_area_width, self.drawing_area_height = int(input("Give me new drawing area width: ")), \
                                                                    int(input("Give me new drawing area height: "))

            # brush size
            elif option == f' Change brush size, current: {self.brush_size}':
                self.brush_size = int(input("Give me new brush size: "))

            elif option == f' Change brush rotation(0 is standard), current: {self.brush_rotation}':
                self.brush_rotation = int(input("Give me new brush angle: "))

            # window size
            elif option == f' Change window size, current: {self.width, self.height}':
                print(f"Screen dimensions have to be: {self.screen_ratio}")
                new_dimensions = [int(input("Give me new screen width: ")), int(input("Give me new screen height: "))]

                w_ratio = new_dimensions[0] / self.screen_ratio[0]
                if self.screen_ratio[1] != new_dimensions[1] / w_ratio:  # Setting the screen ratio to correct
                    new_dimensions[1] = int(self.screen_ratio[1] * w_ratio)

                self.set_size(new_dimensions[0], new_dimensions[1])
                self.camera.init_gl(new_dimensions[0], new_dimensions[1])

            elif option == f' Save level to file {"NO_FILE_YET" if self.current_level_file == "" else self.current_level_file}':
                self.save(input('Give me a text file from levels/.. : ') if self.current_level_file == "" else self.current_level_file)

            elif option == f' Read level from file {"NO_FILE_YET" if self.current_level_file == "" else self.current_level_file}':
                self.read(input('Give me a text file from levels/.. : ') if self.current_level_file == "" else self.current_level_file)

            elif option == f' Changing working file from file {"NO_FILE_YET" if self.current_level_file == "" else self.current_level_file}':
                self.current_level_file = input("Give me new name of working file: ")

            elif option == f' Choose this option to reset current camera to default':
                self.camera.reset()

            self.draw_menu()

        except IndexError:
            print('There is no such tile, index out of range')
            self.update_tiles(new_draw_tile=0)

    def save(self, file_name):
        # This function calls saver module to allow us to save level into the file

        print('----------------------------------')
        print(f'Saving to {file_name}...')
        print('----------------------------------')
        saver.save(file_name, self.tile_list, area_w=self.drawing_area_width, area_h=self.drawing_area_height)

    def read(self, file_name):
        # This function calls reader module to allow us to read level from the file

        print('----------------------------------')
        print(f'Reading from {file_name}...')
        print('----------------------------------')
        new_stuff = reader.read(file_name, tile.Tile, self.tiles_batch)
        # returned = drawing_area_width, drawing_area_height, tile_width, tile_height, background, tile_list

        # Updating the properties of our drawing area
        self.drawing_area_width = new_stuff[0]
        self.drawing_area_height = new_stuff[1]
        self.change_tile_size(new_stuff[2], new_stuff[3])
        self.background = new_stuff[4]
        self.tile_list = new_stuff[5]

        self.update_tiles()

    def switch_tag(self):
        # This function changes the tiles' tags

        x, y = self.mouse_x, self.mouse_y

        tile_list = self.choose_area.tile_list if self.current_screen == 1 else self.tile_list
        t = cf.get_tile_in_pos(x, y, tile_list)

        print('------------------------------------')

        new_tag = input(f"Give me new tile tag for tile {t.tile_num}, leave empty for DEFAULT: ")
        new_tag = new_tag if new_tag != '' else 'DEFAULT'

        if self.current_screen == 1:  # Update default tag for tile in tile choose
            self.tag[t.tile_num] = new_tag

        t.tag = new_tag
        print('------------------------------------')


if __name__ == '__main__':
    program_window = EditorWindow(1280, 720, caption='Tiling tool v1.1')
    pyglet.app.run()
