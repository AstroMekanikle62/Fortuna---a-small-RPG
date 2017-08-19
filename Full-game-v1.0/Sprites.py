#!/usr/bin/env python
import pygame as pg
from Settings import *
vec =  pg.math.Vector2

class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self, filenam):
        self.spriteesheet = pg.image.load(filenam).convert_alpha()

    def get_image(self, x, y, width, height,add = None):
        # to grap a certain image out of the spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spriteesheet, (0,0), (x,y,width,height))
        if add == "yes":
            image = pg.transform.scale(image,(28*2,46*2)) # rescale the cut image, numbers are place holders for now
        elif add == "devil":
            image = pg.transform.scale(image,(28*3,46*2))
        elif add == "devil2":
            image = pg.transform.scale(image,(135,136))
        elif add == "grave":
            image = pg.transform.scale(image,(88,68))
        else:
            image = pg.transform.scale(image,(28,46))

        return image
       

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player_walking_vertical = False
        self.player_walking_horizental = False
        self.current_frame = 0
        self.last_update = 0
        self.load_player_images()
        self.image = self.walking_front_frames[0]
        self.rect.center = (x,y)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0) # velocity vector
        self.pos = vec(x,y) #* TILESIZE #position vector
        self.inventory = {}
        self.dialogue = [None]
        self.playerMatter = 0
        self.playerSpirit = 0
        self.playerFortune = 0

    def playerStats(self):
        if self.game.characterClass == FIRST_CLASS:
            self.playerMatter = 2
            self.playerSpirit = 5
            self.playerFortune = 2
        elif self.game.characterClass == SECOND_CLASS:
            self.playerMatter = 4
            self.playerSpirit = 1
            self.playerFortune = 4
        elif self.game.characterClass == THIRD_CLASS:
            self.playerMatter = 3
            self.playerSpirit = 3
            self.playerFortune = 3
        return self.playerMatter, self.playerSpirit

    def load_player_images(self):
        self.walking_front_frames = [self.game.player_spritesheet.get_image(48,123,38,62),
                                     self.game.player_spritesheet.get_image(0,123,38,62),
                                     self.game.player_spritesheet.get_image(91,123,38,62)]
        for frame in self.walking_front_frames:
            frame.set_colorkey(BLACK)

        self.walking_back_frames = [self.game.player_spritesheet.get_image(48,0,38,62),
                                     self.game.player_spritesheet.get_image(0,0,38,62),
                                     self.game.player_spritesheet.get_image(94,0,38,62)]
        for frame in self.walking_back_frames:
            frame.set_colorkey(BLACK)

        self.walking_left_frames = [self.game.player_spritesheet.get_image(52,187,34,56),
                                     self.game.player_spritesheet.get_image(0,187,38,56),
                                     self.game.player_spritesheet.get_image(96,187,39,56)]
        for frame in self.walking_left_frames:
            frame.set_colorkey(BLACK)

        self.walking_right_frames = [self.game.player_spritesheet.get_image(51,64,33,56,0),
                                     self.game.player_spritesheet.get_image(0,64,38,56,0),
                                     self.game.player_spritesheet.get_image(94,64,38,56,0)]
        for frame in self.walking_right_frames:
            frame.set_colorkey(BLACK)

    def get_keys(self): #to move diagonally replace the three 'elif's by 'if'
        
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        elif keys[pg.K_RIGHT] or keys[pg.K_d]: 
            self.vel.x = PLAYER_SPEED
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
             self.vel *= 0.7071

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx,dy): #if you don't move into a wall, move normally
             self.x += dx
             self.y += dy

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    #def collide_wtih_paths(self):
    #    hits = pg.sprite.spritecollide(self, self.game.paths, False)
    #    if hits:
    #        self.game.current_level +=1

    def collide_with_others(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.talking_sprites , False)
            for hit in hits:
                interactiveCharacter = hit.interact()
                #print(interactiveCharacter) #just checking if it is working
                self.updateDialogue(interactiveCharacter)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.talking_sprites, False)
            for hit in hits:
                interactiveCharacter = hit.interact()
                #print(interactiveCharacter) 
                self.updateDialogue(interactiveCharacter)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def get_dialogue(self):
        return self.dialogue

    def get_pos(self):
        #print(self.pos)
        return self.pos

    def updateDialogue(self,interactiveCharacter):
        self.dialogue[0] = interactiveCharacter
        #print(self.dialogue[0])

    def get_inventory(self):
        return self.game.inventorydic

    def itemsCollision(self):
        itemCollisionList = pg.sprite.spritecollide(self, self.game.items, True)
        for collision in itemCollisionList:
            item = collision.pickUp()
            self.game.itemlist.append(item)
            item = {item:1}
            self.updateInventory(item)

    def updateInventory(self,item):
        items = self.game.items
        for key in item.keys():
            if key in self.game.inventorydic:
                self.game.inventorydic[key] += item[key]
            else:
                self.game.inventorydic = dict(self.game.inventorydic.items() | item.items())


    def update(self):
        self.animate()
        self.playerStats()
        self.get_keys()
        self.pos += self.vel * self.game.dt 
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.collide_with_others('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_others('y')
        #self.collide_wtih_paths()
        self.itemsCollision()

    def animate(self):
        now = pg.time.get_ticks()
        #showing walking animation horziental
        if self.vel.x != 0:
            self.player_walking_horizental = True
        else: 
            self.player_walking_horizental = False
        
        if self.player_walking_horizental:
            if now - self.last_update > WALKING_FRAME_SPEED: # to slow how often the frame changes increase this number
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_left_frames)
                bottom = self.rect.bottom
                if self.vel.x > 0: # right direction
                    self.image = self.walking_right_frames[self.current_frame]
                else: #left direction
                    self.image = self.walking_left_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                #collision mask
        #self.mask = pg.mask.from_surface(self.image)

        #showing walking animation vertical
        if self.vel.y != 0:
            self.player_walking_vertical = True
        else: 
            self.player_walking_vertical = False
        
        if self.player_walking_vertical:
            if now - self.last_update > WALKING_FRAME_SPEED: # to slow how often the frame changes increase this number
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_front_frames)
                bottom = self.rect.bottom
                if self.vel.y > 0: # down direction
                    self.image = self.walking_front_frames[self.current_frame]
                else: #up direction
                    self.image = self.walking_back_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    
class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, type,dir):
        self.groups = game.all_sprites, game.enemies, game.talking_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.dir = dir
        self.current_frame = 0
        self.last_update = 0
        self.load_enemy_images(type,dir)
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) #* TILESIZE #position vector
        self.enemyMatter = 0
        self.enemySpirit = 0

    def enemyStats(self):
        if self.type == "The Fool":
            self.enemyMatter = 2
            self.enemySpirit = 2
        elif self.type == "The Hanged Man":
            self.enemyMatter = 3
            self.enemySpirit = 4
        elif self.type == "The Empress":
            self.enemyMatter = 10
            self.enemySpirit = 2
        elif self.type == "The Emperor":
            self.enemyMatter = 3
            self.enemySpirit = 10
        elif self.type == "The Magician":
            self.enemyMatter = 3
            self.enemySpirit = 3
        elif self.type == "The Hermit":
            self.enemyMatter = 1
            self.enemySpirit = 9
        elif self.type == "The Devil":
            self.enemyMatter = 6
            self.enemySpirit = 6
        elif self.type == "Death":
            self.enemyMatter = 6
            self.enemySpirit = 7
        elif self.type == "The World":
            self.enemyMatter = 8
            self.enemySpirit = 9
        return self.enemyMatter, self.enemySpirit

    def load_enemy_images(self ,type, dir):
        if dir == "down":
            if type == "Death":
                self.idle_frames = [self.game.enemy_images[type].get_image(22,12,89,125,"devil2"),
                                             self.game.enemy_images[type].get_image(175,11,90,124,"devil2")] 
            elif type == "The Hanged Man":
                self.idle_frames = [self.game.enemy_images[type].get_image(36,17,84,126,"yes"),
                                             self.game.enemy_images[type].get_image(167,11,84,132,"yes")] 
            elif type == "The Devil":
                self.idle_frames = [self.game.enemy_images[type].get_image(0,6,137,135,"devil2"),
                                             self.game.enemy_images[type].get_image(144,6,136,135,"devil2")] 
            elif type == "The World":
                self.idle_frames = [self.game.enemy_images[type].get_image(6,2,131,140,"devil2"),
                                             self.game.enemy_images[type].get_image(149,2,131,140,"devil2")] 
            else:
                self.idle_frames = [self.game.enemy_images[type].get_image(48,123,38,62),
                                             self.game.enemy_images[type].get_image(8,123,38,62),
                                             self.game.enemy_images[type].get_image(92,123,38,62)]
        elif dir == "up":
            self.idle_frames = [self.game.enemy_images[type].get_image(48,0,38,64),
                                         self.game.enemy_images[type].get_image(0,0,43,66),
                                         self.game.enemy_images[type].get_image(94,0,38,64)]
        elif dir == "left":
            self.idle_frames = [self.game.enemy_images[type].get_image(52,187,34,56),
                                         self.game.enemy_images[type].get_image(0,187,41,56),
                                         self.game.enemy_images[type].get_image(96,187,39,55)]
        elif dir == "right":
            self.idle_frames = [self.game.enemy_images[type].get_image(50,64,32,57),
                                         self.game.enemy_images[type].get_image(6,65,30,55)]#,
                                         #self.game.enemy_images[type].get_image(95,64,35,56)]
        for frame in self.idle_frames:
              frame.set_colorkey(BLACK)

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > IDLE_FRAME_SPEED:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]

    def interact(self):
        return self.type

    def get_pos(self):
        #print(self.pos)
        return self.pos

    def update(self):
       self.animate()
       self.enemyStats()
       self.rect.x = self.pos.x
       self.rect.y = self.pos.y

class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.npcs, game.talking_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.current_frame = 0
        self.last_update = 0
        self.load_npc_images(type)
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) #* TILESIZE #position vector

    def load_npc_images(self,type):
        if type == "Zara":
            self.idle_frames = [self.game.npc_images[type].get_image(48,123,38,62),
                                         self.game.npc_images[type].get_image(0,123,38,62),
                                         self.game.npc_images[type].get_image(91,123,38,62)]
        elif type == "Grave":
            self.idle_frames = [self.game.npc_images[type].get_image(644,416,88,68,"grave")]

        for frame in self.idle_frames:
              frame.set_colorkey(BLACK)

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > IDLE_FRAME_SPEED:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]

    def interact(self):
        return self.type

    def get_pos(self):
        return self.pos

    def update(self):
       self.animate()
       self.rect.x = self.pos.x
       self.rect.y = self.pos.y

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type, sound=None):
        #self.groups = game.items#, game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.type = type
        self.loadSound(sound)

    def loadSound(self, sound):
        if sound != None:
            self.sound = pg.mixer.Sound(sound)
        else:
            self.sound = None

    def playSound(self):
        if self.sound != None:
            self.sound.play()

    def pickUp(self):
        self.playSound()
        return self.type

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y 

class Path(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.paths
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y 
