__author__ = "Jafar al hussain , alias: AstroMekanikle62"
__license__ = "Feel free to learn from this program"
__version__ = "1.0"
#!/usr/bin/env python
from os import path
import pygame as pg
import sys
import csv
import random
import time
from itertools import islice
from Settings import *
from Sprites import *
from Tilemap import *
from pygame_functions import *
screenSize(864,512) #This is required by pygame_functions

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #Size of the display screen
        pg.display.set_caption(TITLE) #Title of the game that appears on top of the screen
        self.clock = pg.time.Clock() #pygame clock
        pg.key.set_repeat(500, 100) #keep doing the key action when the user is holding a key
        self.current_level = 0
        self.hermit_counter = 0
        self.graveyard = []
        self.fleeyard = []
        self.itemlist = []
        self.devilbook = ["matter", "spirit"]
        self.bonusnamelist = ["Classified :D"]
        self.inventorydic={}
        self.load_data() #external data (images and other files) that must be loaded
        self.start_font_name = pg.font.match_font(START_FONT) #font of the startup screen
        self.inventory_font_name = pg.font.match_font(INVENTORY_FONT) #font used by the inventory
        self.dialogue_font_name = pg.font.match_font(DIALOGUE_FONT)
        self.normal_font_name = pg.font.match_font(NORMAL_FONT)

    def load_data(self):
        #game_folder = path.dirname(__file__) #game file directory
        if getattr(sys, 'frozen', False):
            # frozen
            game_folder = os.path.dirname(sys.executable)
        else:
            # unfrozen
            game_folder = os.path.dirname(os.path.realpath(__file__))
        img_folder = path.join(game_folder, "img") #img file directory
        self.map_folder = path.join(game_folder, "maps")
        self.sound_folder = path.join(game_folder, "snd")
        player_folder = path.join(img_folder, "player")
        enemies_folder = path.join(img_folder, "enemies")
        npcs_folder = path.join(img_folder, "npc")
        item_folder = path.join(img_folder, "items")
        placeholder_folder = path.join(img_folder, "placeholders")
        ui_folder = path.join(img_folder, "UI")
        cards_folder = path.join(img_folder, "cards")
        class_folder = path.join(img_folder, "class")
        dialogue_folder = path.join(game_folder, "dialogue")
        abilities_folder = path.join(dialogue_folder, "abilities")
        #self.map = Tiledmap(path.join(map_folder,LEVELS[self.current_level])) #loading the tiled map used by "Tiled" software
        #self.map_img = self.map.make_map()
        #self.map_rect = self.map_img.get_rect()
        #load sound files
        self.collect_sound = pg.mixer.Sound(path.join(self.sound_folder, "Menu2A.wav"))
        self.tof_sound = pg.mixer.Sound(path.join(self.sound_folder, "tofcountdown.wav"))
        self.spirit_sound = pg.mixer.Sound(path.join(self.sound_folder, "Magic Smite.wav"))
        self.matter_sound = pg.mixer.Sound(path.join(self.sound_folder, "sword sound.wav"))
        pg.mixer.music.load(path.join(self.sound_folder, "Forest_Ambience.wav"))        
        self.dark_ambience = pg.mixer.Sound(path.join(self.sound_folder, "Dark-Amb.wav"))
        #load player sprite sheet
        self.player_spritesheet = Spritesheet(path.join(player_folder, PLAYER_SPRITESHEET))
        #load enemies sprite sheet
        self.enemy_images = {}
        for enemy in ENEMY_SPRITESHEETS:
            self.enemy_images[enemy] = Spritesheet(path.join(enemies_folder, ENEMY_SPRITESHEETS[enemy]))
        #load npc sprite sheet
        self.npc_images = {}
        for npc in NPC_SPRITESHEETS:
            self.npc_images[npc] = Spritesheet(path.join(npcs_folder, NPC_SPRITESHEETS[npc]))
        #load manifistations sprite sheet
        self.manifistation_images = {}
        for manifistation in CLASS_SPRITESHEETS:
            self.manifistation_images[manifistation] = Spritesheet(path.join(class_folder, CLASS_SPRITESHEETS[manifistation]))
        #load item images
        self.item_images={}
        for item in ITEM_IMGS:
            self.item_images[item] = pg.image.load(path.join(item_folder, ITEM_IMGS[item])).convert_alpha()
            self.item_images[item] = pg.transform.scale(self.item_images[item], (20, 32))
        #load card images
        self.card_images={}
        for card in CARD_IMAGES:
            self.card_images[card] = pg.image.load(path.join(cards_folder, CARD_IMAGES[card])).convert_alpha()
        #load menu images
        self.menu_images={}
        for menu in MENU_IMAGES:
            self.menu_images[menu] = pg.image.load(path.join(ui_folder, MENU_IMAGES[menu])).convert_alpha()
        #load wall images
        #self.wall_img = pg.image.load(path.join(placeholder_folder, WALL_IMG)).convert_alpha()
        #self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        #load UI images
        #self.dialoguearrow_img= pg.image.load(path.join(ui_folder, DIALOGUE_ARROW_IMG)).convert_alpha()
        self.inventory_img = pg.image.load(path.join(ui_folder, INVENTORY_BOX)).convert_alpha()
        self.inventory_img = pg.transform.scale(self.inventory_img, (810, 500))#Width and height of the mneu screen
        self.inventory_imgX = 30 #inventory coordinate, 90 default
        self.inventory_imgY = 0 #inventory coordinate, 70 default
        self.name_scroll_img = pg.image.load(path.join(ui_folder, NAME_SCROLL_IMG)).convert_alpha()
        self.name_scroll_img = pg.transform.scale(self.name_scroll_img, (810, 500))
        self.dialogue_box_img = pg.image.load(path.join(ui_folder, DIALOGUE_BOX_IMG)).convert_alpha()
        self.battle_img = pg.image.load(path.join(ui_folder, BATTLE_UI_IMG)).convert_alpha()
        self.battle_img = pg.transform.scale(self.battle_img, (WIDTH, HEIGHT))
        self.small_blue_square_img = pg.image.load(path.join(ui_folder, "BlueSquareblank.png")).convert_alpha()
        self.upper_left_square_img = pg.image.load(path.join(ui_folder, "Upperleftbox.png")).convert_alpha()
        self.upper_right_square_img = pg.image.load(path.join(ui_folder, "Upperrightbox.png")).convert_alpha()
        self.tof_sheet_img = pg.image.load(path.join(ui_folder, "tofsheet.png")).convert_alpha()
        #load character class images
        self.class_sheet_img = pg.image.load(path.join(class_folder, CLASS_SHEET_IMG)).convert_alpha()
        self.first_class_img = pg.image.load(path.join(class_folder, FIRST_CLASS_PORTRAIT)).convert_alpha()
        self.second_class_img = pg.image.load(path.join(class_folder, SECOND_CLASS_PORTRAIT)).convert_alpha()
        self.third_class_img = pg.image.load(path.join(class_folder, THIRD_CLASS_PORTRAIT)).convert_alpha()
        #load dialogue data
        self.dialogue_data = {}
        for file in DIALOGUE_FILES:
            self.dialogue_data[file] = path.join(dialogue_folder,DIALOGUE_FILES[file])
        #load tof data
        self.ability_data = {}
        for file in ABILITY_FILES:
            self.ability_data[file] = path.join(abilities_folder,ABILITY_FILES[file])

    def load_map(self,level):
        #if getattr(sys, 'frozen', False):
        #    # frozen
        #    game_folder = os.path.dirname(sys.executable)
        #else:
        #    # unfrozen
        #    game_folder = os.path.dirname(os.path.realpath(__file__))
        #map_folder = path.join(game_folder, "maps")
        self.map = Tiledmap(path.join(self.map_folder,LEVELS[level])) #loading the tiled map used by "Tiled" software
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()  
        
    def new(self): 
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group() #group that contains all sprites
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.talking_sprites = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.paths = pg.sprite.Group()
        self.load_map(self.current_level)
        #for row, tiles in enumerate(self.map.data): #enumerate returns index and the element in the 1st and 2nd variables respectivly
        #    for col,tile in enumerate(tiles):
        #        if tile == "1":
        #            Wall(self, col, row)
        #        if tile == "p":
        #            self.player = Player(self, col, row) 
        #        if tile == "e":
        #            Enemy(self, col, row)
        # we used the above code to load objects from a text files, but now that we have a map editor, we will use similar code
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2) #you can assign by x and y too
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'passage':
                Path(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'The Fool' or tile_object.name == 'The Dummy' or tile_object.name == 'The Hanged Man'\
                or tile_object.name == 'The Empress' or tile_object.name == 'The Emperor' or tile_object.name == 'The Devil'\
                or tile_object.name == 'Death' or tile_object.name == 'The World':
                self.enemy = Enemy(self, obj_center.x, obj_center.y, tile_object.name,"down")
            if tile_object.name == 'The Magician':
                self.enemy = Enemy(self, obj_center.x, obj_center.y, tile_object.name,"right")
            if tile_object.name == 'The Hermit':
                self.enemy = Enemy(self, obj_center.x, obj_center.y, tile_object.name,"up")
            if tile_object.name == 'Zara' or tile_object.name == 'Grave':
                self.npc = NPC(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name == 'Cup of Ace' or tile_object.name == 'Queen of Wands' or tile_object.name == 'King of Wands'\
                or tile_object.name == 'Pentacle of Ace':
                self.item = Item(self, obj_center, tile_object.name,self.collect_sound)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False # we will use it to check the hit box of everything on the map by pressing h                                  
        if self.current_level >= 2 and self.current_level < 7:
            pg.mixer.music.play(-1)
        elif self.current_level >= 7:
            pg.mixer.music.load(path.join(self.sound_folder, "ambientmain_0.wav"))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.stop()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        if pg.sprite.spritecollide(self.player, self.paths, False):
            self.current_level += 1
            self.new()
            pause(100)
        
    def draw_grid(self): # to draw the grid of the map, must be disabled for gameplay 
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) #REMOVE WHEN DONE
        self.screen.fill(BLACK)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, LIGHTBLUE, self.camera.apply_rect(sprite.rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, LIGHTBLUE, self.camera.apply_rect(wall.rect), 1)
        pg.display.flip()
    
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                #if event.key == pg.K_h:
                #    self.draw_debug = not self.draw_debug
                if event.key == pg.K_e:
                    self.inventoryMenu()
                if event.key == pg.K_SPACE:
                    self.implement_dialogue()

    def show_start_screen(self):
        # game start screen
        Open = True
        while Open:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.screen.fill(BLACK)
            self.screen.blit(self.menu_images["start"],(0,0))
            self.menu_button(358, 140, 143, 30, BUTTON_TRANSP+35, BUTTON_TRANSP_HOVER+35, "A") 
            if newgame_select == True:
                Open = False
            pg.display.flip()
            self.clock.tick(FPS)
            self.menu_button(359, 190, 146, 30, BUTTON_TRANSP+35, BUTTON_TRANSP_HOVER+35, "B")
            self.menu_button(372, 240, 115, 30, BUTTON_TRANSP+35, BUTTON_TRANSP_HOVER+35, "C")
            self.menu_button(387, 290, 90, 30, BUTTON_TRANSP+35, BUTTON_TRANSP_HOVER+35, "D")
            self.menu_button(400, 340, 65, 30, BUTTON_TRANSP+35, BUTTON_TRANSP_HOVER+35, "E")
            pg.display.flip()
            self.clock.tick(FPS)

    def show_name_entry_screen(self):
        #The name entry screen utilize the input box function from pygame_functions
        self.screen.fill(BLACK)
        self.screen.blit(self.menu_images["background"],(0,0))
        self.screen.blit(self.name_scroll_img, (27, 0))
        self.name_box = makeTextBox(310, 110 , 250 , 1, "    Type then press enter" , 24 , 24)
        showTextBox(self.name_box)
        self.characterName = textBoxInput(self.name_box).capitalize()
        if self.characterName == "Classified :D":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, ORANGE, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, ORANGE, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, ORANGE, WIDTH / 2, 330,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Classified :D":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, PURPLE, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, PURPLE, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, PURPLE, WIDTH / 2, 330,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Classified :D" or self.characterName == "Classified :D":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, CRIMSON, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Classified :D",\
                         28, CRIMSON, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, CRIMSON, WIDTH / 2, 330,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Classified :D":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, RED, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, RED, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, RED, WIDTH / 2, 330,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Classified :D":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, OILY, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, PALEBLUE, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, OILY, WIDTH / 2, 330,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Jafar" or self.characterName == "Ja'far":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, GREEN, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"The creator grants you +3 to Matter and Spirit", 28, GREEN, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Classified :D" or self.characterName == "Classified :D":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, DARKGREY, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, DARKGREY, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, DARKGREY, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Ea" or self.characterName == "Classified :D" or self.characterName == "Classified :D":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS LOCKED!", 35, BLACK, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, BLACK, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"Classified :D", 28, BLACK, WIDTH / 2, 330,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Classified :D" or self.characterName == "Classified :D"\
           or self.characterName == "Classified :D" :
           self.draw_text(self.inventory_font_name,"SUPER SPECIAL NAME BONUS!", 35, WHITE, WIDTH / 2, 250,"c")
           self.draw_text(self.inventory_font_name,"Make your enemies taste the true meaning of despair!", 28, RED, WIDTH / 2, 300,"c")
           self.draw_text(self.inventory_font_name,"you gain +4 to Matter and Spirit", 28, BLUE, WIDTH / 2, 330,"c")
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385,"c")
           pg.display.flip()
           self.wait_for_key()
        else:
           pg.display.flip()
  
    def show_class_screen(self): #class selection screen utilizes the clear_button function from utilities
        Open = True
        while Open:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                #if event.type == pg.MOUSEBUTTONDOWN:
                #    Open = False

            self.screen.fill(BLACK)
            self.screen.blit(self.menu_images["background"],(0,0))
            self.screen.blit(self.class_sheet_img, (155,0))
            self.clear_button(163, 85, 545, 123, BUTTON_TRANSP, BUTTON_TRANSP_HOVER, "A") 
            if ch_select == True:
               Open = False
            self.clear_button(163, 219, 545, 123, BUTTON_TRANSP, BUTTON_TRANSP_HOVER, "B")
            if ch_select == True:
               Open = False
            self.clear_button(163, 353, 545, 123, BUTTON_TRANSP, BUTTON_TRANSP_HOVER, "C")
            if ch_select == True:
               Open = False
            pg.display.flip()
            self.clock.tick(FPS)

    def show_tof_screen(self,playerclass,playerluck,enemyclass,enemyluck):
        x1= 65
        x2 = 600
        y1= 45
        y2 = 27
        y3 = 290
        y4 = 270
        fontsize = 23
        self.screen.blit(self.tof_sheet_img, (15,10))
        if playerclass == FIRST_CLASS:
            if playerluck == "upward":
                self.screen.blit(self.card_images["highpriestess"], (x2,y2))
                self.read_abilities("thehighpriestessU",fontsize,x1,y1)
            elif playerluck == "downward":
                self.card_images["highpriestess"] = pg.transform.flip(self.card_images["highpriestess"],False,True)
                self.screen.blit(self.card_images["highpriestess"], (x2,y2))
                self.read_abilities("thehighpriestessD",fontsize,x1,y1)
                self.card_images["highpriestess"] = pg.transform.flip(self.card_images["highpriestess"],False,True)
        elif playerclass == SECOND_CLASS:
            if playerluck == "upward":
                self.screen.blit(self.card_images["strength"], (x2,y2))
                self.read_abilities("strengthU",fontsize,x1,y1)
            elif playerluck == "downward":
                self.card_images["strength"] = pg.transform.flip(self.card_images["strength"],False,True)
                self.screen.blit(self.card_images["strength"], (x2,y2))
                self.read_abilities("strengthD",fontsize,x1,y1)
                self.card_images["strength"] = pg.transform.flip(self.card_images["strength"],False,True)
        elif playerclass == THIRD_CLASS:
            if playerluck == "upward":
                self.screen.blit(self.card_images["justice"], (x2,y2))
                self.read_abilities("justiceU",fontsize,x1,y1)
            elif playerluck == "downward":
                self.card_images["justice"] = pg.transform.flip(self.card_images["justice"],False,True)
                self.screen.blit(self.card_images["justice"], (x2,y2))
                self.read_abilities("justiceD",fontsize,x1,y1)
                self.card_images["justice"] = pg.transform.flip(self.card_images["justice"],False,True)

        if enemyclass == "The Fool":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["fool"], (x2,y4))
                self.read_abilities("thefoolU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["fool"] = pg.transform.flip(self.card_images["fool"],False,True)
                self.screen.blit(self.card_images["fool"], (x2,y4))
                self.read_abilities("thefoolD",fontsize,x1,y3)
                self.card_images["fool"] = pg.transform.flip(self.card_images["fool"],False,True)
        elif enemyclass == "The Hanged Man":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["hangedman"], (x2,y4))
                self.read_abilities("thehangedmanU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["hangedman"] = pg.transform.flip(self.card_images["hangedman"],False,True)
                self.screen.blit(self.card_images["hangedman"], (x2,y4))
                self.read_abilities("thehangedmanD",fontsize,x1,y3)
                self.card_images["hangedman"] = pg.transform.flip(self.card_images["hangedman"],False,True)
        elif enemyclass == "The Empress":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["empress"], (x2,y4))
                self.read_abilities("theempressU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["empress"] = pg.transform.flip(self.card_images["empress"],False,True)
                self.screen.blit(self.card_images["empress"], (x2,y4))
                self.read_abilities("theempressD",fontsize,x1,y3)
                self.card_images["empress"] = pg.transform.flip(self.card_images["empress"],False,True)
        elif enemyclass == "The Emperor":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["emperor"], (x2,y4))
                self.read_abilities("theemperorU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["emperor"] = pg.transform.flip(self.card_images["emperor"],False,True)
                self.screen.blit(self.card_images["emperor"], (x2,y4))
                self.read_abilities("theemperorD",fontsize,x1,y3)
                self.card_images["emperor"] = pg.transform.flip(self.card_images["emperor"],False,True)
        elif enemyclass == "The Hermit":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["hermit"], (x2,y4))
                self.read_abilities("thehermitU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["hermit"] = pg.transform.flip(self.card_images["hermit"],False,True)
                self.screen.blit(self.card_images["hermit"], (x2,y4))
                self.read_abilities("thehermitD",fontsize,x1,y3)
                self.card_images["hermit"] = pg.transform.flip(self.card_images["hermit"],False,True)
        elif enemyclass == "The Magician":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["magician"], (x2,y4))
                self.read_abilities("themagicianU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["magician"] = pg.transform.flip(self.card_images["magician"],False,True)
                self.screen.blit(self.card_images["magician"], (x2,y4))
                self.read_abilities("themagicianD",fontsize,x1,y3)
                self.card_images["magician"] = pg.transform.flip(self.card_images["magician"],False,True)
        elif enemyclass == "The Devil":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["devil"], (x2,y4))
                self.read_abilities("thedevilU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["devil"] = pg.transform.flip(self.card_images["devil"],False,True)
                self.screen.blit(self.card_images["devil"], (x2,y4))
                self.read_abilities("thedevilD",fontsize,x1,y3)
                self.card_images["devil"] = pg.transform.flip(self.card_images["devil"],False,True)
        elif enemyclass == "Death":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["death"], (x2,y4))
                self.read_abilities("deathU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["death"] = pg.transform.flip(self.card_images["death"],False,True)
                self.screen.blit(self.card_images["death"], (x2,y4))
                self.read_abilities("deathD",fontsize,x1,y3)
                self.card_images["death"] = pg.transform.flip(self.card_images["death"],False,True)
        elif enemyclass == "The World":
            if enemyluck == "upward":
                self.screen.blit(self.card_images["world"], (x2,y4))
                self.read_abilities("theworldU",fontsize,x1,y3)
            elif enemyluck == "downward":
                self.card_images["world"] = pg.transform.flip(self.card_images["world"],False,True)
                self.screen.blit(self.card_images["world"], (x2,y4))
                self.read_abilities("theworldD",fontsize,x1,y3)
                self.card_images["world"] = pg.transform.flip(self.card_images["world"],False,True)
        self.clock.tick(FPS)
        pg.display.update()

    def show_battle_screen(self):
        self.playerBattleMatter = self.characterMatter
        self.playerBattleSpirit = self.characterSpirit
        self.enemyBattleMatter, self.enemyBattleSpirit = self.enemy.enemyStats()
        self.playerBattleMatter, self.playerBattleSpirit, self.enemyBattleMatter, self.enemyBattleSpirit =\
        self.classTOF(self.characterClass,self.characterMatter,self.characterSpirit, self.enemyBattleMatter, self.enemyBattleSpirit)

        self.playerBattleMatter, self.playerBattleSpirit, self.enemyBattleMatter, self.enemyBattleSpirit, self.enemyAttackType =\
        self.opponentTOF(self.enemy.type,self.playerBattleMatter, self.playerBattleSpirit, self.enemyBattleMatter,\
        self.enemyBattleSpirit, enemyAttackType = "")
        self.tof_sound.play()
        pause(3900)
        display = True
        while display:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_SPACE:
                        display = False
            self.show_tof_screen(self.characterClass,playerTOF,self.enemy.type,enemyTOF)
        edf = False
        Open = True
        color = None
        while Open:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.screen.blit(self.battle_img, (0,0))
            if playerTOF == "upward":
                color = MIDNIGHTBLUE
            elif playerTOF == "downward":
                color = RED
            self.draw_text(self.inventory_font_name, self.characterClass, 26, BLACK, 530, 377,"c")
            self.draw_text(self.inventory_font_name,"Card position: " + playerTOF, 21, color, 535, 402,"c")
            self.draw_text(self.inventory_font_name,"Matter:  " + str(self.playerBattleMatter), 21, BLACK, 530, 423,"c")
            self.draw_text(self.inventory_font_name,"Spirit:  " + str(self.playerBattleSpirit), 21, BLACK, 530, 443,"c")
            self.draw_text(self.inventory_font_name, PTOFresult, 21, BLACK, 530, 467,"c")
            self.draw_text(self.inventory_font_name, self.enemy.type, 26, BLACK, 145, 377,"c")
            self.draw_text(self.inventory_font_name,"Card position: " + enemyTOF, 21, BLACK, 150, 402,"c")
            self.draw_text(self.inventory_font_name,"Matter:  " + str(self.enemyBattleMatter), 21, BLACK, 145, 423,"c")
            self.draw_text(self.inventory_font_name,"Spirit:  " + str(self.enemyBattleSpirit), 21, BLACK, 145, 443,"c")
            self.draw_text(self.inventory_font_name,ETOFresult, 21, BLACK, 145, 463,"c")
            self.draw_text(self.inventory_font_name, "Turn Count", 26, CRIMSON, 350, 377,"c")
            if self.enemy.type == "The World" or self.enemy.type == "Death" or self.enemy.type == "The Devil":
                self.battle_imgs(50,155,"e",self.enemy.type,"right")
            else:
                self.battle_imgs(50,190,"e",self.enemy.type,"right")
            self.battle_imgs(783,200,"c",self.characterClass,"left")
            self.clock.tick(FPS)
            pg.display.flip()
            self.battleSim(self.characterClass,self.enemy.type,self.playerBattleMatter, self.playerBattleSpirit,\
            self.enemyBattleMatter, self.enemyBattleSpirit, self.enemyAttackType)
            if enemyDeathFlag == True:
                self.graveyard.append(self.enemy.type)
                if self.enemyAttackType == "matter":
                    self.characterMatter +=1
                elif self.enemyAttackType == "spirit":
                    self.characterSpirit +=1
                #pause(4000)
                self.wait_for_key()
                self.enemy.kill()
                Open = False
            if enemyFleeFlag == True:
                self.fleeyard.append(self.enemy.type)
                if self.enemyAttackType == "matter":
                    self.characterMatter +=1
                elif self.enemyAttackType == "spirit":
                    self.characterSpirit +=1
                #pause(4000)
                self.wait_for_key()
                self.enemy.kill()
                Open = False
                self.all_sprites.add(self.item)
                self.items.add(self.item)
            if playerDeathFlag == True:
                #pause(4000)
                self.wait_for_key()
                open = False
                self.show_go_screen()  

    def show_go_screen(self):
        # game over/continue
        pg.mixer.music.stop()
        self.dark_ambience.play()
        self.screen.fill(BLACK)
        self.screen.blit(self.menu_images["gameover"],(0,0))
        pg.display.flip()
        self.wait_for_key()
        self.current_level = 0
        self.hermit_counter = 0
        self.graveyard = []
        self.fleeyard = []
        self.itemlist = []
        self.inventorydic={}
        g.show_start_screen()
        self.dark_ambience.stop()
        g.show_name_entry_screen()
        g.show_class_screen()
        while True:
            g.new()
            g.run()

    def show_ending_screen(self):
        pg.mixer.music.stop()
        self.screen.fill(BLACK)
        self.screen.blit(self.menu_images["ending"],(0,0))
        pg.display.flip()
        self.wait_for_key()
        self.current_level = 0
        self.hermit_counter = 0
        self.graveyard = []
        self.fleeyard = []
        self.itemlist = []
        self.inventorydic={}
        g.show_start_screen()
        g.show_name_entry_screen()
        g.show_class_screen()
        while True:
            g.new()
            g.run()
################# Utility methods ####################
    def wait_for_key(self): #put where the user can only continue if they press a button
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False

    def draw_text(self, yourfont, text, size, color, x, y, loc): #a utility method to render text 
        font = pg.font.Font(yourfont, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if loc == "c":
            text_rect.midtop = (x, y)
        elif loc == "l":
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def clear_button(self, x, y, w, h, transp, hover_transp, action = None): #a button method for class selection 
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        global ch_select 
        ch_select = False
        self.button = pg.Surface((w,h), pg.SRCALPHA, 32)
        if x + w > mouse[0] > x and  y + h > mouse[1] > y:
            self.button.fill((235, 180, 140, hover_transp)) # the less the last number the more clear the button
            self.screen.blit(self.button, (x,y))
            if click[0] == 1 and action != None:
                if action == "A":
                    self.characterClass = FIRST_CLASS
                    self.character_stats(FIRST_CLASS)
                    self.name_bonus()
                    ch_select = True
                elif action == "B":
                    self.characterClass = SECOND_CLASS
                    self.character_stats(SECOND_CLASS)
                    self.name_bonus()
                    ch_select = True
                elif action == "C":
                    self.characterClass = THIRD_CLASS
                    self.character_stats(THIRD_CLASS)
                    self.name_bonus()
                    ch_select = True

        else:
            self.button.fill((235, 180, 140, transp))
            self.screen.blit(self.button, (x,y))

    def menu_button(self, x, y, w, h, transp, hover_transp, action = None): #a button method for menu selection 
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        global newgame_select
        global other_select
        newgame_select = False
        other_select = False
        self.button = pg.Surface((w,h), pg.SRCALPHA, 32)
        if x + w > mouse[0] > x and  y + h > mouse[1] > y:
            self.button.fill((235, 180, 140, hover_transp)) # the less the last number the more clear the button
            self.screen.blit(self.button, (x,y))
            if click[0] == 1 and action != None:
                if action == "A":
                    newgame_select = True
                elif action == "B":
                    display = True
                    while display:
                        self.screen.blit(self.menu_images["howtoplay"],(0,0))
                        pg.display.flip()
                        for event in pg.event.get():
                            if event.type==pg.QUIT:
                                pg.quit()
                                sys.exit()
                            if event.type == pg.MOUSEBUTTONDOWN:
                               display = False
                    other_select = True
                elif action == "C":
                    display = True
                    while display:
                        self.screen.blit(self.menu_images["controls"],(0,0))
                        pg.display.flip()
                        for event in pg.event.get():
                            if event.type==pg.QUIT:
                                pg.quit()
                                sys.exit()
                            if event.type == pg.MOUSEBUTTONDOWN:
                               display = False
                    other_select = True
                elif action == "D":
                    display = True
                    while display:
                        self.screen.blit(self.menu_images["credits"],(0,0))
                        pg.display.flip()
                        for event in pg.event.get():
                            if event.type==pg.QUIT:
                                pg.quit()
                                sys.exit()
                            if event.type == pg.MOUSEBUTTONDOWN:
                               display = False
                    other_select = True
                elif action == "E":
                    self.quit()
                    other_select = True
        else:
            self.button.fill((235, 180, 140, transp))
            self.screen.blit(self.button, (x,y))

    def read_dialogue(self, filename):
        with open(self.dialogue_data[filename],"r") as my_dialogue :
            counter = 0
            self.render_message_box(self.dialogue_box_img,100,0)
            line_gen = islice(my_dialogue, 0,9)
            for line in line_gen:
                self.draw_text(self.dialogue_font_name,line.rstrip(),23,BLACK,130,15 + counter,"l")
                counter = counter + 30

    def render_message_box(self, boximage, x, y):
        self.screen.blit(boximage, (x,y))

    def battle_imgs(self, x, y, imageclass, type, imgdirection):

        if imgdirection == "left" and imageclass == "e":
            image = self.enemy_images[type].get_image(52,187,34,56)
            image = pg.transform.scale(image,(38,56))
        elif imgdirection == "right" and imageclass == "e":
            if type == "The Hanged Man":
                image =self.enemy_images[type].get_image(168,13,77,128,"yes")
            elif type == "The Devil":
                image =self.enemy_images[type].get_image(144,6,136,135,"devil")
            elif type == "Death":
                image =self.enemy_images[type].get_image(175,11,90,124,"devil")
            elif type == "The World":
                image =self.enemy_images[type].get_image(149,2,131,140,"devil2")
            else:
                image =self.enemy_images[type].get_image(51,64,33,60)
                image = pg.transform.scale(image,(38,56))
        elif imgdirection == "left" and imageclass == "c":
            image = self.manifistation_images[type].get_image(52,187,34,56)
            image = pg.transform.scale(image,(38,56))
        elif imgdirection == "right" and imageclass == "c":
            image =self.manifistation_images[type].get_image(51,64,33,60)
            image = pg.transform.scale(image,(38,56))
        image.set_colorkey(BLACK)
        self.screen.blit(image, (x,y))
                       
    def read_abilities(self, filename , size , x,y):
        with open(self.ability_data[filename],"r") as my_ability:
            counter = 0
            line_gen = islice(my_ability, 0,6)
            for line in line_gen:
                self.draw_text(self.dialogue_font_name,line.rstrip(),size,BLACK,x,y + counter,"l")
                counter = counter + 30
##########################################################
    def character_stats(self,manifestation): # stats of each class
        if manifestation == FIRST_CLASS:
           self.characterMatter = 2
           self.characterSpirit = 5
           self.characterFortune = 2     
        elif manifestation == SECOND_CLASS:
            self.characterMatter = 4
            self.characterSpirit = 1
            self.characterFortune = 4              
        elif manifestation == THIRD_CLASS:
            self.characterMatter = 3
            self.characterSpirit = 3
            self.characterFortune = 3   

    def name_bonus(self): # Tyoing in specifc secret ames grants you different bonuses
        if self.characterName == "Classified :D":
             self.characterSpirit = self.characterSpirit + 1
        elif self.characterName == "Classified :D":
             self.characterFortune = self.characterFortune + 1
        elif self.characterName == "Classified :D" or self.characterName == "Classified :D":
             self.characterMatter = self.characterMatter + 1
             self.characterSpirit = self.characterSpirit + 1
        elif self.characterName == "Classified :D":
             self.characterMatter = self.characterMatter + 2
        elif self.characterName == "Classified :D":
             self.characterMatter = self.characterMatter + 1
             self.characterSpirit = self.characterSpirit + 1
             self.characterFortune = self.characterFortune + 1
        elif self.characterName == "Classified :D" or self.characterName == "Classified :D":
             self.characterSpirit = self.characterSpirit + 2
        elif self.characterName == "Jafar" or self.characterName == "Ja'far":
             self.characterMatter = self.characterMatter + 3
             self.characterSpirit = self.characterSpirit + 3
        elif self.characterName == "Classified :D" or self.characterName == "Classified :D"or self.characterName == "Classified :D":
             self.characterMatter = 0
             self.characterSpirit = 0
             self.characterFortune = 0
        elif self.characterName == "Classified :D" or self.characterName == "Classified :D"\
             or self.characterName == "Classified :D":
             self.characterMatter = self.characterMatter + 4
             self.characterSpirit = self.characterSpirit + 4
        else:
             self.characterMatter = self.characterMatter + 0
             self.characterSpirit = self.characterSpirit + 0
             self.characterFortune = self.characterFortune + 0

 
################### Battle stuff #############################

    def flip(self,pl):
        return "upward" if random.random() < pl else "downward"

    def classTOF(self,yourClass,yourMatter,yourSpirit,foeMatter,foeSpirit):
        global playerTOF
        global PTOFresult
        if "Cup of Ace" in self.itemlist:
            playerTOF = self.flip(0.5 + (0.0675 * self.characterFortune))
        else:
            playerTOF = self.flip(0.5 + (0.0550 * self.characterFortune))
        if yourClass == FIRST_CLASS:
            if playerTOF == "upward":
                foeMatter = 1
                PTOFresult = "The enemy matter has dropped to 1"
            elif playerTOF == "downward":
                yourMatter = 1
                PTOFresult = "your matter dropped to 1"
        elif yourClass == SECOND_CLASS:
            if playerTOF == "upward":
                yourSpirit = yourSpirit + 2
                PTOFresult = "Your spirit has increased by 2"
            elif playerTOF == "downward":
                foeMatter = foeMatter + 2
                PTOFresult = "The enemy matter has increased by 2"
        elif yourClass == THIRD_CLASS:
            if playerTOF == "upward":
                yourMatter +=1
                yourSpirit +=1
                PTOFresult = "Your stats are increased by 1"
            elif playerTOF == "downward":
                foeMatter +=1
                foeSpirit +=1
                PTOFresult = "The enemy stats increased by 1"
        return yourMatter,yourSpirit,foeMatter,foeSpirit

    def opponentTOF(self, enemyType, yourMatter, yourSpirit, enemyMatter, enemySpirit, enemyAttackType):
        global enemyTOF
        global ETOFresult
        enemyTOF = self.flip(0.5)
        if enemyType == "The Fool":
            if enemyTOF == "upward":
                enemyAttackType = "matter"
                ETOFresult = "The Fool will use matter based attacks"
            elif enemyTOF == "downward":
                enemyAttackType = "spirit"
                ETOFresult = "The Fool will use spirit based attacks"

        elif enemyType == "The Hanged Man":
            enemyAttackType = "matter"
            if enemyTOF == "upward":
                if yourMatter > self.characterMatter:
                    enemyMatter = enemyMatter - (yourMatter - self.characterMatter)
                    ETOFresult = "Death seeker"
                if yourSpirit > self.characterSpirit:
                    enemySpirit = enemySpirit - (yourSpirit - self.characterSpirit)
                    ETOFresult = "Death seeker"
                else:
                    ETOFresult = "Indecision"
            elif enemyTOF == "downward":
                if yourMatter > self.characterMatter:
                    enemyMatter = enemyMatter + (yourMatter - self.characterMatter)
                    ETOFresult = "Death Jailor"
                if yourSpirit > self.characterSpirit:
                    enemySpirit = enemySpirit + (yourSpirit - self.characterSpirit)
                    ETOFresult = "Death Jailor"
                else:
                    ETOFresult = "Indecision"

        elif enemyType == "The Empress":
            enemyAttackType = "spirit"
            if enemyTOF == "upward":
                if enemyMatter == 1:
                    enemyMatter = 1
                    yourSpirit = yourSpirit * 2
                else:
                    enemyMatter = enemyMatter // 2
                    yourSpirit = yourSpirit * 2
                ETOFresult = "The Empress's Grace"
            elif enemyTOF == "downward":
                enemySpirit = enemySpirit + abs(yourMatter-yourSpirit)
                ETOFresult = "Abuse of Power"

        elif enemyType == "The Emperor":
            enemyAttackType = "matter"
            if enemyTOF == "upward":
                if enemySpirit == 1:
                    enemySpirit = 1
                    yourMatter = yourMatter * 2
                else:
                    enemySpirit = enemySpirit // 2
                    yourMatter = yourMatter * 2
                ETOFresult = "The Emperor's Justice"
            elif enemyTOF == "downward":
                enemyMatter = enemyMatter + abs(yourMatter-yourSpirit)
                ETOFresult = "Abuse of Power"

        elif enemyType == "The Magician":
            enemyAttackType = "spirit"
            if enemyTOF == "upward":
                enemyMatter = enemyMatter + self.characterFortune
                enemySpirit = enemySpirit + self.characterFortune                
                ETOFresult = "Accumulated Fortune"
            elif enemyTOF == "downward":
                enemyMatter = self.characterMatter
                enemySpirit = self.characterSpirit
                ETOFresult = "Copycat"

        elif enemyType == "The Hermit":
            enemyAttackType = "matter"
            if enemyTOF == "upward":
                enemyMatter = self.characterMatter + 1         
                ETOFresult = "Introspection"
            elif enemyTOF == "downward":
                enemyMatter = self.characterMatter - 1
                ETOFresult = "Soul Release"

        elif enemyType == "The Devil":
            if enemyTOF == "upward":        
                ETOFresult = "Devil Disaster"
            elif enemyTOF == "downward":
                ETOFresult = "Eternal Suffering"

        elif enemyType == "Death":
            enemyAttackType = "spirit"
            if enemyTOF == "upward":   
                yourSpirit = yourSpirit + len(self.graveyard)
                yourMatter = yourMatter + len(self.graveyard)
                ETOFresult = "Necro Sacrifice"
            elif enemyTOF == "downward":
                ETOFresult = "Tour of Doom"

        elif enemyType == "The World":
            if enemyTOF == "upward":   
                ETOFresult = "Over-Catastrophe"
            elif enemyTOF == "downward":
                ETOFresult = "Slither of Hope"
                enemyMatter +=2
                enemySpirit +=2
                yourMatter = yourMatter + (len(self.fleeyard)) 
                yourSpirit = yourSpirit + (len(self.fleeyard)) 
        return yourMatter, yourSpirit, enemyMatter,enemySpirit,enemyAttackType

    def battleSim(self,yourClass,enemyClass,playerMatter,playerSpirit,enemyMatter,enemySpirit,enemyAttackType):
        global enemyDeathFlag
        global playerDeathFlag
        global enemyFleeFlag
        playerDeathFlag = False
        enemyDeathFlag = False
        enemyFleeFlag = False
        fontsize = 20
        pmatterCounter = 0
        pspiritCounter = 0
        turnCounter = 1
        passCounter = 0
        xcoorp = 485
        xcoore = 60
        ycoor = 15
        ycoorfinish = 35
        while (playerDeathFlag == False) and (enemyDeathFlag == False) and (enemyFleeFlag == False):

            if playerDeathFlag == False:
                userpress = True
                playerAttackType = ''
                while userpress:
                    for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_m:
                                    playerAttackType = playerAttackType + "m"
                                    userpress = False
                                if event.key == pygame.K_s:
                                    playerAttackType = playerAttackType + "s"
                                    userpress = False
                                if event.key == pygame.K_p:
                                    playerAttackType = playerAttackType+ "p"
                                    userpress = False
            
                if enemyClass == "The World" and enemyTOF == "upward" and (turnCounter%2 != 0):
                    playerAttackType = "p"
                    self.draw_text(self.inventory_font_name,enemyClass +" forced you to skip your turn!"\
                    ,fontsize,FIREBRICK,xcoorp ,ycoorfinish,"l")

                if playerAttackType == "m":
                    self.matter_sound.play()
                    self.screen.blit(self.upper_right_square_img, (xcoorp,ycoor))
                    pmatterCounter +=1
                    if playerMatter > enemyMatter:
                        if "King of Wands" in self.itemlist:
                            dmg = ("You inflicted {0:d} damage to your enemy's matter.".format((playerMatter+1) - enemyMatter))
                            self.draw_text(self.inventory_font_name,dmg,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                            enemyMatter = enemyMatter - ((playerMatter+1) - enemyMatter)
                            if enemyClass == "Death" and enemyTOF =="downward":
                                self.draw_text(self.inventory_font_name,"Attacking " +enemyClass +" physically is darining your life!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                playerSpirit = playerSpirit - ((playerMatter+1) - enemyMatter)
                        else:
                            dmg = ("You inflicted {0:d} damage to your enemy's matter.".format(playerMatter - enemyMatter))
                            self.draw_text(self.inventory_font_name,dmg,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                            enemyMatter = enemyMatter - (playerMatter - enemyMatter)
                            if enemyClass == "Death" and enemyTOF =="downward":
                                self.draw_text(self.inventory_font_name,"Attacking " +enemyClass +" physically is darining your life!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                playerSpirit = playerSpirit - ((playerMatter) - enemyMatter)
                        if enemyMatter <= 0:
                             self.draw_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoorfinish ,"l")
                             enemyDeathFlag = True
                             self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                 ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")

                    elif playerMatter == enemyMatter:
                         if "King of Wands" in self.itemlist:
                             self.draw_text(self.inventory_font_name,"You inflicted 2 damage to your enemy's matter."\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                             enemyMatter = enemyMatter -2
                             if enemyClass == "Death" and enemyTOF =="downward":
                                 self.draw_text(self.inventory_font_name,"Attacking " +enemyClass +" physically is darining your life!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                 playerSpirit = playerSpirit - 2
                         else:
                             self.draw_text(self.inventory_font_name,"You inflicted 1 damage to your enemy's matter."\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                             enemyMatter = enemyMatter -1
                             if enemyClass == "Death" and enemyTOF =="downward":
                                 self.draw_text(self.inventory_font_name,"Attacking " +enemyClass +" physically is darining your life!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                 playerSpirit = playerSpirit - 1
                         if enemyMatter <= 0:
                             self.draw_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoorfinish,"l")
                             enemyDeathFlag = True
                             self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                 ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")

                    elif playerMatter < enemyMatter:
                         self.draw_text(self.inventory_font_name,"Your attack did nothing.",\
                             fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")

                elif playerAttackType == "s":
                    self.spirit_sound.play()
                    self.screen.blit(self.upper_right_square_img, (xcoorp,ycoor))
                    pspiritCounter +=1
                    if playerSpirit > enemySpirit:
                       if "Queen of Wands" in self.itemlist:
                           dmg = ("You inflicted {0:d} damage to your enemy's spirit.".format((playerSpirit+1) - enemySpirit))
                           self.draw_text(self.inventory_font_name,dmg,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                           enemySpirit = enemySpirit - ((playerSpirit+1) - enemySpirit)
                       else:
                           dmg = ("You inflicted {0:d} damage to your enemy's spirit.".format(playerSpirit - enemySpirit))
                           self.draw_text(self.inventory_font_name,dmg,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                           enemySpirit = enemySpirit - (playerSpirit - enemySpirit)
                       if enemySpirit <= 0:
                            self.draw_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoorfinish,"l")
                            enemyDeathFlag = True
                            self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                 ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")

                    elif playerSpirit == enemySpirit:
                         if "Queen of Wands" in self.itemlist:
                             self.draw_text(self.inventory_font_name,"You inflicted 2 damage to your enemy's spirit."\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                             enemySpirit = enemySpirit -2
                         else:
                             self.draw_text(self.inventory_font_name,"You inflicted 1 damage to your enemy's spirit."\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")
                             enemySpirit = enemySpirit -1
                         if enemySpirit <= 0:
                            self.draw_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp ,ycoorfinish, "l")
                            enemyDeathFlag = True
                            self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                 ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")

                    elif playerSpirit < enemySpirit:
                         self.draw_text(self.inventory_font_name,"Your attack did nothing.",\
                             fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")

                elif playerAttackType == "p":
                     self.screen.blit(self.upper_right_square_img, (xcoorp,ycoor))
                     passCounter +=1
                     if "Pentacle of Ace" in self.itemlist and self.characterClass == FIRST_CLASS and enemyClass == "The Devil":
                         self.draw_text(self.inventory_font_name,"You used the sacred item to banish "+enemyClass+"!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoorfinish,"l")
                         enemyDeathFlag = True
                     elif "Pentacle of Ace" in self.itemlist and self.characterClass == SECOND_CLASS and enemyClass == "The World":
                         self.draw_text(self.inventory_font_name,"You used the sacred item to end "+enemyClass+"!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoorfinish,"l")
                         enemyDeathFlag = True
                     elif "Pentacle of Ace" in self.itemlist and self.characterClass == THIRD_CLASS and enemyClass == "Death":
                         self.draw_text(self.inventory_font_name,"You used the sacred item to kill "+enemyClass+" it self!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoorp,ycoorfinish,"l")
                         enemyDeathFlag = True
                     else:
                         self.draw_text(self.inventory_font_name,"You passed your turn!"\
                             ,fontsize,MIDNIGHTBLUE,xcoorp,ycoor,"l")

                         if enemyClass == "The World" and enemyTOF == "upward" and (turnCounter%2 != 0):
                            self.draw_text(self.inventory_font_name,enemyClass +" forced you to skip your turn!"\
                            ,fontsize,FIREBRICK,xcoorp ,ycoorfinish,"l")

                         elif enemyClass == "The Hermit" and enemySpirit == 1 and pspiritCounter > 0:
                            self.screen.blit(self.upper_left_square_img, (xcoore,ycoor))
                            self.draw_text(self.inventory_font_name,'"I...I feel better now, Thank you '+ self.characterClass + '"'\
                                    ,fontsize,FIREBRICK,xcoore ,ycoor,"l")
                            enemyFleeFlag = True
                            self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                    ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")


            self.screen.blit(self.small_blue_square_img, (165,423))
            self.draw_text(self.inventory_font_name," " +str(enemyMatter), 21, BLACK, 171, 423,"c")
            self.screen.blit(self.small_blue_square_img, (163,444))
            self.draw_text(self.inventory_font_name, " " +str(enemySpirit), 21, BLACK, 166, 443,"c")
                
            if enemyDeathFlag == False:

                if passCounter == 5:
                    if enemyClass == "The Fool":
                        self.screen.blit(self.upper_left_square_img, (xcoore,ycoor))
                        self.draw_text(self.inventory_font_name,'"Stop making me feel stupid, aaaaaaaaah"'\
                                ,fontsize,FIREBRICK,xcoore ,ycoor,"l")
                        enemyFleeFlag = True
                        self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")

                if pmatterCounter == 5:
                    if enemyClass == "The Empress":
                        self.screen.blit(self.upper_left_square_img, (xcoore,ycoor))
                        self.draw_text(self.inventory_font_name,'"You did not try to kill me!"'\
                            ,fontsize,FIREBRICK,xcoore ,ycoor,"l")
                        self.draw_text(self.inventory_font_name,'"Maybe I was wrong about you, take this gift."'
                            ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                        self.draw_text(self.inventory_font_name,'"This will help you crush the spirits of your enemies"'\
                            ,fontsize,FIREBRICK,xcoore ,ycoorfinish+20,"l")
                        enemyFleeFlag = True
                        self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")

                if pspiritCounter == 5:
                    if enemyClass == "The Emperor":
                        self.screen.blit(self.upper_left_square_img, (xcoore,ycoor))
                        self.draw_text(self.inventory_font_name,'"You really are a noble one! If only the others knew..."'\
                            ,fontsize,FIREBRICK,xcoore ,ycoor,"l")
                        self.draw_text(self.inventory_font_name,'"Here, with this everyone shall shatter before you!"'\
                            ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                        enemyFleeFlag = True
                        self.draw_text(self.inventory_font_name,"You gain + 1 to " +enemyAttackType\
                                ,fontsize,FORESTGREEN,xcoorp,ycoorfinish+20,"l")

            if enemyFleeFlag == False and enemyDeathFlag == False:

                if enemyClass == "The Devil":
                    enemyAttackType = random.choice(self.devilbook)

                elif enemyClass == "The World":
                    if enemyMatter >= playerMatter:
                        enemyAttackType = "matter"
                    elif enemySpirit >= playerSpirit:
                        enemyAttackType = "spirit"
                    else:
                        enemyAttackType = random.choice(self.devilbook)
                pg.display.update()
                pause(1500)
                if enemyAttackType == "matter":
                    self.matter_sound.play()
                    self.screen.blit(self.upper_left_square_img, (xcoore,ycoor))
                    if enemyMatter > playerMatter:
                        dmg =  (enemyClass +" has inflicted {0:d} damage to your matter.".format(enemyMatter - playerMatter))
                        self.draw_text(self.inventory_font_name,dmg,fontsize,FIREBRICK,xcoore ,ycoor,"l")
                        playerMatter = playerMatter - ( enemyMatter - playerMatter)

                        if enemyClass == "The Devil":
                            if enemyTOF == "upward":
                                playerSpirit = playerSpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is tormenting you!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                            elif enemyTOF == "downward":
                                playerSpirit = playerSpirit - 1
                                enemyMatter = enemyMatter - 1
                                enemySpirit = enemySpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is losing his powers!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                if enemySpirit<=0 or enemyMatter<=0 :
                                    enemyDeathFlag = True                                    

                        if playerMatter <= 0:
                            self.draw_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoore,ycoorfinish+20,"l")
                            playerDeathFlag = True

                    elif enemyMatter == playerMatter:
                         self.draw_text(self.inventory_font_name,enemyClass +" has inflicted 1 damage to your matter."\
                             ,fontsize,FIREBRICK,xcoore ,ycoor,"l")
                         playerMatter = playerMatter -1

                         if enemyClass == "The Devil":
                            if enemyTOF == "upward":
                                playerSpirit = playerSpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is tormenting you!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                            elif enemyTOF == "downward":
                                playerSpirit = playerSpirit - 1
                                enemyMatter = enemyMatter - 1
                                enemySpirit = enemySpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is losing his powers!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                if enemySpirit<=0 or enemyMatter<=0 :
                                    enemyDeathFlag = True

                         if playerMatter <= 0:
                            self.draw_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoore ,ycoorfinish+20,"l")
                            playerDeathFlag = True

                    elif enemyMatter < playerMatter:
                         self.draw_text(self.inventory_font_name,enemyClass +"'s attack did nothing."\
                             ,fontsize,FIREBRICK,xcoore,ycoor,"l")

                         if enemyClass == "The Devil":
                            if enemyTOF == "upward":
                                playerSpirit = playerSpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is tormenting you!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                            elif enemyTOF == "downward":
                                playerSpirit = playerSpirit - 1
                                enemyMatter = enemyMatter - 1
                                enemySpirit = enemySpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is losing his powers!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                if enemySpirit<=0 or enemyMatter<=0 :
                                    enemyDeathFlag = True
                            if playerMatter <= 0:
                                self.draw_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                     ,fontsize,FIREBRICK,xcoore ,ycoorfinish+20,"l")
                                playerDeathFlag = True

                elif enemyAttackType == "spirit":
                    self.spirit_sound.play()
                    self.screen.blit(self.upper_left_square_img, (xcoore,ycoor))
                    if enemySpirit > playerSpirit:
                        dmg = ( enemyClass +" has inflicted {0:d} damage to your spirit.".format(enemySpirit - playerSpirit))
                        self.draw_text(self.inventory_font_name,dmg,fontsize,FIREBRICK,xcoore,ycoor ,"l")
                        playerSpirit = playerSpirit - (enemySpirit - playerSpirit)

                        if enemyClass == "The Devil":
                            if enemyTOF == "upward":
                                playerMatter = playerMatter - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is tormenting you!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                            elif enemyTOF == "downward":
                                playerMatter = playerMatter - 1
                                enemyMatter = enemyMatter - 1
                                enemySpirit = enemySpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is losing his powers!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                if enemySpirit<=0 or enemyMatter<=0 :
                                    enemyDeathFlag = True

                        if playerSpirit <= 0:
                            self.draw_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoore ,ycoorfinish+20,"l")
                            playerDeathFlag = True

                    elif enemySpirit == playerSpirit:
                         self.draw_text(self.inventory_font_name,enemyClass +" has inflicted 1 damage to your spirit."\
                             ,fontsize,FIREBRICK,xcoore,ycoor,"l")
                         playerSpirit = playerSpirit -1

                         if enemyClass == "The Devil":
                            if enemyTOF == "upward":
                                playerMatter = playerMatter - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is tormenting you!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                            elif enemyTOF == "downward":
                                playerMatter = playerMatter - 1
                                enemyMatter = enemyMatter - 1
                                enemySpirit = enemySpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is losing his powers!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                if enemySpirit<=0 or enemyMatter<=0 :
                                    enemyDeathFlag = True

                         if playerSpirit <= 0:
                             self.draw_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoore,ycoorfinish+20,"l")
                             playerDeathFlag = True

                    elif enemySpirit < playerSpirit:
                         self.draw_text(self.inventory_font_name,enemyClass +"'s attack did nothing."\
                             ,fontsize,FIREBRICK,xcoore,ycoor,"l")
                         if enemyClass == "The Devil":
                            if enemyTOF == "upward":
                                playerMatter = playerMatter - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is tormenting you!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                            elif enemyTOF == "downward":
                                playerMatter = playerMatter - 1
                                enemyMatter = enemyMatter - 1
                                enemySpirit = enemySpirit - 1
                                self.draw_text(self.inventory_font_name,enemyClass +" is losing his powers!"\
                                ,fontsize,FIREBRICK,xcoore ,ycoorfinish,"l")
                                if enemySpirit<=0 or enemyMatter<=0 :
                                    enemyDeathFlag = True
                            if playerSpirit <= 0:
                                 self.draw_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                     ,fontsize,FIREBRICK,xcoore,ycoorfinish+20,"l")
                                 playerDeathFlag = True

                if enemyClass == "The Hermit":
                    enemySpirit = enemySpirit - 1
                    self.draw_text(self.inventory_font_name,enemyClass +" is losing his will to live..."\
                             ,fontsize,FIREBRICK,xcoore,ycoorfinish,"l")
                    if enemySpirit <= 0:
                        enemyDeathFlag =True

            self.screen.blit(self.small_blue_square_img, (554,423))
            self.draw_text(self.inventory_font_name," " +str(playerMatter), 21, BLACK, 556, 423,"c")
            self.screen.blit(self.small_blue_square_img, (549,446))
            self.draw_text(self.inventory_font_name, " " +str(playerSpirit), 21, BLACK, 553, 443,"c")
            self.screen.blit(self.small_blue_square_img, (340,405))
            self.draw_text(self.inventory_font_name, " " +str(turnCounter), 25, CRIMSON, 350, 401,"c")
            turnCounter +=1
            pg.display.update()
        return

          
###################### Inventory stuff ###############

    def inventoryMenu(self): #the inventory menu itself
        playerInv = self.player.get_inventory()  
        invKeys = []
        if playerInv == {}:
            self.emptyInvMessage()
        else:
            for key in playerInv.keys():
                invKeys.append(key)
            if len(invKeys) <= 8:
                self.smallInvMenu(playerInv, invKeys)    
            
    def emptyInvMessage(self): #this will display if you have no items in your inventory
        inventoryFont = pg.font.Font(self.inventory_font_name, 28)
        HeaderText = inventoryFont.render(self.characterName + "'s Inventory ", True, BLACK)
        EmptyText = inventoryFont.render('The Inventory is Empty!', True, BLACK)
        xcoord = 90 #text coordinate
        ycoord = 55 #text coordiante
        Open = True
        while Open:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_e:
                        Open = False
            self.screen.blit(self.inventory_img, (self.inventory_imgX, self.inventory_imgY))
            if self.characterClass == FIRST_CLASS:
                 self.screen.blit(self.first_class_img, (655,25))
            elif self.characterClass == SECOND_CLASS:
                 self.screen.blit(self.second_class_img, (655,25))
            elif self.characterClass == THIRD_CLASS:
                 self.screen.blit(self.third_class_img, (655,25))
            self.draw_text(self.inventory_font_name, self.characterClass, 30, BLACK, 717,ycoord+105,"c")
            self.draw_text(self.inventory_font_name, "Matter: " + str(self.characterMatter), 30, BLACK, 717,ycoord+133,"c")
            self.draw_text(self.inventory_font_name, "Spirit: " + str(self.characterSpirit), 30, BLACK, 717,ycoord+163,"c")
            self.draw_text(self.inventory_font_name, "Fortune: " + str(self.characterFortune), 30, BLACK, 717,ycoord+193,"c")
            self.screen.blit(HeaderText, (xcoord,ycoord))
            self.screen.blit(EmptyText, (xcoord,ycoord+50))
            self.clock.tick(FPS)
            pg.display.update()

    def smallInvMenu(self, playerInv, invKeys): #this will display if you colleceted an item
        inventoryFont = pg.font.Font(self.inventory_font_name, 28)
        selectFont = pg.font.Font(self.inventory_font_name, 22)
        selectFont.set_underline(True)
        HeaderText = inventoryFont.render(self.characterName + "'s Inventory ", True, BLACK)
        xcoord = 90
        Open = True
        selectNum = 0
        while Open:
            ycoord = 55
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_e:
                        Open = False
                    if event.key==pg.K_w:
                        if selectNum > 0:
                            selectNum -= 1
                        else:
                            selectNum = len(invKeys)-1
                    if event.key==pg.K_s:
                        if selectNum < len(invKeys)-1:
                            selectNum += 1
                        else:
                            selectNum = 0
            self.screen.blit(self.inventory_img, (self.inventory_imgX,self.inventory_imgY))
            self.screen.blit(HeaderText, (xcoord,ycoord))
            if self.characterClass == FIRST_CLASS:
                 self.screen.blit(self.first_class_img, (655,25))
            elif self.characterClass == SECOND_CLASS:
                 self.screen.blit(self.second_class_img, (655,25))
            elif self.characterClass == THIRD_CLASS:
                 self.screen.blit(self.third_class_img, (655,25))
            self.draw_text(self.inventory_font_name, self.characterClass, 30, BLACK, 717,ycoord+105,"c")
            self.draw_text(self.inventory_font_name, "Matter: " + str(self.characterMatter), 30, BLACK, 717,ycoord+133,"c")
            self.draw_text(self.inventory_font_name, "Spirit: " + str(self.characterSpirit), 30, BLACK, 717,ycoord+163,"c")
            self.draw_text(self.inventory_font_name, "Fortune: " + str(self.characterFortune), 30, BLACK, 717,ycoord+193,"c")
            ycoord += 50
            for key in invKeys:
                if invKeys[selectNum] == key:
                    itemtext = selectFont.render("* " + key + ' - ' + str(playerInv[key]),
                                                 True, BLACK)
                else:
                    itemtext = inventoryFont.render("* " + key + ' - ' + str(playerInv[key]),
                                                    True, BLACK)
                self.screen.blit(itemtext, (xcoord,ycoord))
                ycoord += 40

            self.clock.tick(FPS)
            pg.display.update()

##################################

########### Dialogue #############
    def implement_dialogue(self):
        dialogueCheck = self.player.get_dialogue()
        playerPosition = self.player.get_pos()
        enemyPosition = self.enemy.get_pos()
        npcPosition = self.npc.get_pos()
        bonusname = random.choice(self.bonusnamelist)
        if (abs(playerPosition.x - enemyPosition.x) < 30 and abs(playerPosition.y - enemyPosition.y) < 48):
            if "The Fool" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    self.read_dialogue('thefooltext')
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
            elif "The Empress" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    self.read_dialogue('theempresstext' )
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
            elif "The Emperor" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    if "The Empress" in self.graveyard:
                        self.read_dialogue('theemperortext1' )
                    else:
                        self.read_dialogue('theemperortext2' )
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
            elif "The Magician" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    self.read_dialogue('themagiciantext' )
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
            elif "The Hermit" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                self.hermit_counter +=1
                                battle = False
                    self.read_dialogue('thehermittext1')
                    if self.hermit_counter == 8:
                        self.read_dialogue('thehermittext2')
                    if self.hermit_counter == 9:
                        battle = True
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
        elif (abs(playerPosition.x - enemyPosition.x) < 52 and abs(playerPosition.y - enemyPosition.y) < 96):
            if "The Hanged Man" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    self.read_dialogue('thehangedmantext')
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
        elif (abs(playerPosition.x - enemyPosition.x) < 112 and abs(playerPosition.y - enemyPosition.y) < 152):
            if "The World" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    self.read_dialogue('theworldtext')
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
            elif "Death" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    self.read_dialogue('deathtext')
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
            elif "The Devil" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                battle = True
                    self.read_dialogue('thedeviltext')
                    if battle == True:
                        self.show_battle_screen()
                    self.clock.tick(FPS)
                    pg.display.update()
        elif (abs(playerPosition.x - npcPosition.x) < 36 and abs(playerPosition.y - npcPosition.y) < 80):
            if "Grave" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                                self.show_ending_screen()
                    self.render_message_box(self.dialogue_box_img,100,0)
                    self.draw_text(self.dialogue_font_name,"Here lies "+ bonusname +" - also known as "+self.characterName+" -"\
                        ,23,BLACK,424,15,"c")
                    self.draw_text(self.dialogue_font_name,"the second and last ruler of the fallen kingdom of Fortuna"\
                        ,23,BLACK,424,60,"c")
                    self.draw_text(self.dialogue_font_name,"Conducted the forbidden ritual to defend the kingdom from the Rose Crusaders"\
                        ,23,BLACK,424,90,"c")
                    self.draw_text(self.dialogue_font_name,"Found dead in a mysterious structure just outside the castle"\
                        ,23,BLACK,424,120,"c")
                    self.draw_text(self.dialogue_font_name,"The dedication for protecting the kingdom and its people was never matched"\
                        ,23,BLACK,424,150,"c")
                    self.draw_text(self.dialogue_font_name,"1445 - 1480"\
                        ,23,BLACK,424,195,"c")
                    self.clock.tick(FPS)
                    pg.display.update()
            elif "Zara" in dialogueCheck:
                battle = False
                Open = True
                while Open:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type==pg.KEYDOWN:
                            if event.key==pg.K_SPACE:
                                Open = False
                    self.read_dialogue('zaratext')
                    self.clock.tick(FPS)
                    pg.display.update()
##################################
# create the game object
g = Game()
g.show_start_screen()
g.show_name_entry_screen()
g.show_class_screen()
while True:
    g.new()
    g.run()
