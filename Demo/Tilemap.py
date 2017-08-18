import pygame as pg
from Settings import *
import pytmx #library used to load tilemaps

class Map:
    def __init__(self, filename):
        self.data=[]
        with open(filename,"rt") as f:
            for line in f:
                self.data.append(line.strip()) #strip removes the seen '\n' at the end of each line by python so it doesn't count it

        self.tilewidth = len(self.data[0]) #to track the width of our map we loaded    
        self.tileheight = len(self.data) #to track the hight of our map we loaded
        self.width = self.tilewidth * TILESIZE # how many pixels wide the map is
        self.height = self.tileheight * TILESIZE # how many pixels high the map is

class Tiledmap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height): #creating the 'camera' rectangle
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self,entity): #follow the player
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self,target): #keep player at the center of the screen
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)

        #limit the scrolling to the size of the map
        x = min(0,x) # stop the camera from scrolling when it reaches far the maximum limit of the map on the left
        y = min(0,y) # ... the top
        x = max(-(self.width - WIDTH),x) # ... the right
        y = max(-(self.height - HEIGHT),y) # ... the bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
