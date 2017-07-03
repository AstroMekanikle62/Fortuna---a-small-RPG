__author__ = "Jafar alhussain , alias: Astro_Mekanikle"
__license__ = "Feel free to benifit from and/or use this program"
__version__ = "0.5"

import pygame as pg
import sys
from os import path
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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #Size of the display screen
        pg.display.set_caption(TITLE) #Title of the game that appears on top of the screen
        self.clock = pg.time.Clock() #pygame clock
        pg.key.set_repeat(500, 100) #keep doing the key action when the user is holding a key
        self.load_data() #external data (images and other files) that must be loaded
        self.start_font_name = pg.font.match_font(START_FONT) #font of the startup screen
        self.inventory_font_name = pg.font.match_font(INVENTORY_FONT) #font used by the inventory
        self.dialogue_font_name = pg.font.match_font(DIALOGUE_FONT)


    def load_data(self):
        game_folder = path.dirname(__file__) #game file directory
        img_folder = path.join(game_folder, "img") #img file directory
        map_folder = path.join(game_folder, "maps")
        player_folder = path.join(img_folder, "player")
        enemies_folder = path.join(img_folder, "enemies")
        npcs_folder = path.join(img_folder, "npc")
        item_folder = path.join(img_folder, "items")
        placeholder_folder = path.join(img_folder, "placeholders")
        ui_folder = path.join(img_folder, "UI")
        class_folder = path.join(img_folder, "class")
        dialogue_folder = path.join(game_folder, "dialogue")
        self.map = Tiledmap(path.join(map_folder,"level1.tmx")) #loading the tiled map used by "Tiled" software
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
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
        #load item images
        self.item_images={}
        for item in ITEM_IMGS:
            self.item_images[item] = pg.image.load(path.join(item_folder, ITEM_IMGS[item])).convert_alpha()
            self.item_images[item] = pg.transform.scale(self.item_images[item], (18, 36))
        #load wall images
        #self.wall_img = pg.image.load(path.join(placeholder_folder, WALL_IMG)).convert_alpha()
        #self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        #load UI images
        self.dialoguearrow_img= pg.image.load(path.join(ui_folder, DIALOGUE_ARROW_IMG)).convert_alpha()
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
        #load character class images
        self.class_sheet_img = pg.image.load(path.join(class_folder, CLASS_SHEET_IMG)).convert_alpha()
        self.first_class_img = pg.image.load(path.join(class_folder, FIRST_CLASS_PORTRAIT)).convert_alpha()
        self.second_class_img = pg.image.load(path.join(class_folder, SECOND_CLASS_PORTRAIT)).convert_alpha()
        self.third_class_img = pg.image.load(path.join(class_folder, THIRD_CLASS_PORTRAIT)).convert_alpha()
        #load dialogue data
        self.dialogue_data = {}
        for file in DIALOGUE_FILES:
            self.dialogue_data[file] = path.join(dialogue_folder,DIALOGUE_FILES[file])
            #print(self.dialouge_data['thefooltext'])
        #self.read_dialogue('thefooltext') #testing the read_dialogue function

    def new(self): 
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group() #group that contains all sprites
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.talking_sprites = pg.sprite.Group()
        self.items = pg.sprite.Group()
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
            if tile_object.name == 'The Fool':
                self.enemy = Enemy(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name == 'Zara':
                self.npc = NPC(self, obj_center.x, obj_center.y, tile_object.name)
            if tile_object.name == 'Cup of Ace':
                self.item = Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False # we will use it to check the hit box of everything on the map by pressing h                                  

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
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_e:
                    self.inventoryMenu()
                if event.key == pg.K_SPACE:
                    self.implement_dialogue()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(FORESTGREEN)
        self.draw_text(self.start_font_name,TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 7)
        self.draw_text(self.start_font_name,"A game created by Jafar Al-hussain aka Astro_Mekanikle", 22, WHITE, WIDTH / 2, HEIGHT / 3.5)
        self.draw_text(self.start_font_name,"Arrows to move, Space to interact, e to open the inventory", 22, WHITE, WIDTH / 2, HEIGHT / 1.8)
        self.draw_text(self.start_font_name,"During the battle, press M or S or P to conduct the corresponding attack", 22, WHITE, WIDTH / 2, HEIGHT / 1.6)
        self.draw_text(self.start_font_name,"Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_name_entry_screen(self):
        #The name entry screen utilize the input box function from pygame_functions
        self.screen.fill(GREEN)
        self.screen.blit(self.name_scroll_img, (27, 0))
        self.name_box = makeTextBox(310, 110 , 250 , 1, "    Type then press enter" , 24 , 24)
        showTextBox(self.name_box)
        self.characterName = textBoxInput(self.name_box).capitalize()
        if self.characterName == "Aloy":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, ORANGE, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"A formidable tribal warrior known across the land", 28, ORANGE, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"as Aloy you gain +1 to Spirit", 28, ORANGE, WIDTH / 2, 330)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385)
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Misty":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, PURPLE, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"Famous for her charm in the town of Liberty", 28, PURPLE, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"as Misty you gain +1 to Fortune", 28, PURPLE, WIDTH / 2, 330)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385)
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Akiza" or self.characterName == "Aki":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, CRIMSON, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"As the bearer of the black rose and the mark of the crimson dragon",\
                         28, CRIMSON, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"you gain +1 to Matter and Spirit", 28, CRIMSON, WIDTH / 2, 330)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385)
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Athena":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, RED, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"Slayed an entire army, with a single sword!", 28, RED, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"as Athena you gain +2 to Matter", 28, RED, WIDTH / 2, 330)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385)
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Vivec":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, OILY, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"Some say he was immortal", 28, PALEBLUE, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"as Vivec you gain +1 to all stats", 28, OILY, WIDTH / 2, 330)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385)
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Jafar" or self.characterName == "Ja'far":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, GREEN, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"The creator grants you +3 to Matter and Spirit", 28, GREEN, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385)
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Hart" or self.characterName == "Cortez":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS!", 35, DARKGREY, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"Defeating the timesplitters granted you + 2 to Spirit", 28, DARKGREY, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, DARKGREY, WIDTH / 2, 385)
           pg.display.flip()
           self.wait_for_key()
        elif self.characterName == "Ea" or self.characterName == "Activision" or self.characterName == "CUbisoft":
           self.draw_text(self.inventory_font_name,"SPECIAL NAME BONUS LOCKED!", 35, BLACK, WIDTH / 2, 250)
           self.draw_text(self.inventory_font_name,"To unlock this bonus you must pay 9.99$", 28, BLACK, WIDTH / 2, 300)
           self.draw_text(self.inventory_font_name,"Until you pay your stats are set to 0", 28, BLACK, WIDTH / 2, 330)
           self.draw_text(self.inventory_font_name,"(Press any key to continue)", 24, BLACK, WIDTH / 2, 385)
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

            self.screen.fill(FORESTGREEN)
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

    def show_battle_screen(self):
        self.playerBattleMatter = self.characterMatter
        self.playerBattleSpirit = self.characterSpirit
        self.enemyBattleMatter, self.enemyBattleSpirit = self.enemy.enemyStats()
        self.playerBattleMatter, self.playerBattleSpirit, self.enemyBattleMatter, self.enemyBattleSpirit =\
        self.classTOF(self.characterClass,self.characterMatter,self.characterSpirit, self.enemyBattleMatter, self.enemyBattleSpirit)

        self.playerBattleMatter, self.playerBattleSpirit, self.enemyBattleMatter, self.enemyBattleSpirit, self.enemyAttackType =\
        self.opponentTOF(self.enemy.type,self.playerBattleMatter, self.playerBattleSpirit, self.enemyBattleMatter,\
        self.enemyBattleSpirit, enemyAttackType = "")
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
            self.draw_text(self.inventory_font_name, self.characterClass, 26, BLACK, 530, 377)
            self.draw_text(self.inventory_font_name,"Card position: " + playerTOF, 21, color, 535, 402)
            self.draw_text(self.inventory_font_name,"Matter: " + str(self.playerBattleMatter), 21, BLACK, 530, 423)
            self.draw_text(self.inventory_font_name,"Spirit: " + str(self.playerBattleSpirit), 21, BLACK, 530, 443)
            self.draw_text(self.inventory_font_name, PTOFresult, 21, BLACK, 530, 467)
            self.draw_text(self.inventory_font_name, self.enemy.type, 26, BLACK, 145, 377)
            self.draw_text(self.inventory_font_name,"Card position: " + enemyTOF, 21, BLACK, 150, 402)
            self.draw_text(self.inventory_font_name,"Matter: " + str(self.enemyBattleMatter), 21, BLACK, 145, 423)
            self.draw_text(self.inventory_font_name,"Spirit: " + str(self.enemyBattleSpirit), 21, BLACK, 145, 443)
            self.draw_text(self.inventory_font_name,ETOFresult, 21, BLACK, 145, 463)
            self.clock.tick(FPS)
            pg.display.flip()
            self.battleSim(self.characterClass,self.enemy.type,self.playerBattleMatter, self.playerBattleSpirit,\
            self.enemyBattleMatter, self.enemyBattleSpirit, self.enemyAttackType)
            if enemyDeathFlag == True:
                pause(4000)
                self.enemy.kill()
                Open = False
                #self.all_sprites.add(self.item)
            if enemyFleeFlag == True:
                pause(4000)
                self.enemy.kill()
                Open = False
                self.all_sprites.add(self.item)
                self.items.add(self.item)
            if playerDeathFlag == True:
                pause(4000)
                open = False
                self.show_go_screen()  

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(FORESTGREEN)
        self.draw_text(self.start_font_name,"GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.start_font_name,"Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        g.show_start_screen()
        g.show_name_entry_screen()
        g.show_class_screen()
        while True:
            g.new()
            g.run()

################# Utility methods ####################
    def wait_for_key(self): #put where the user can only continute if he presses a button
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False

    def draw_text(self, yourfont, text, size, color, x, y): #a utility method to render text 
        font = pg.font.Font(yourfont, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_normal_text(self, yourfont, text, size, color, x, y): 
        font = pg.font.Font(yourfont, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
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

    def read_dialogue(self, filename):
        with open(self.dialogue_data[filename],"r") as my_dialogue :
            counter = 0
            self.render_message_box(self.dialogue_box_img,100,0)
            line_gen = islice(my_dialogue, 0,5)
            for line in line_gen:
                self.draw_normal_text(self.dialogue_font_name,line.rstrip(),20,BLACK,130,15 + counter)
                counter = counter + 30

    def render_message_box(self, boximage, x, y):
        self.screen.blit(boximage, (x,y))
        
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
        if self.characterName == "Aloy":
             self.characterSpirit = self.characterSpirit + 1
        elif self.characterName == "Misty":
             self.characterFortune = self.characterFortune + 1
        elif self.characterName == "Akiza" or self.characterName == "Aki":
             self.characterMatter = self.characterMatter + 1
             self.characterSpirit = self.characterSpirit + 1
        elif self.characterName == "Athena":
             self.characterMatter = self.characterMatter + 2
        elif self.characterName == "Vivec":
             self.characterMatter = self.characterMatter + 1
             self.characterSpirit = self.characterSpirit + 1
             characterFortune = characterFortune + 1
        elif self.characterName == "Hart" or self.characterName == "Cortez":
             self.characterSpirit = self.characterSpirit + 2
        elif self.characterName == "Jafar" or self.characterName == "Ja'far":
             self.characterMatter = self.characterMatter + 3
             self.characterSpirit = self.characterSpirit + 3
        elif self.characterName == "Ea" or self.characterName == "Activision"or self.characterName == "Ubisoft":
             self.characterMatter = 0
             self.characterSpirit = 0
             self.characterFortune = 0
        else:
             self.characterMatter = self.characterMatter + 0
             self.characterSpirit = self.characterSpirit + 0
             self.characterFortune = self.characterFortune + 0

    def item_bonus(self, itemName):
        invCheck = self.player.get_inventory()
        if itemName in invCheck:
           return True
        else:
           return False
 
################### Battle stuff #############################

    def flip(self,pl):
        return "upward" if random.random() < pl else "downward"

    def classTOF(self,yourClass,yourMatter,yourSpirit,foeMatter,foeSpirit):
        global playerTOF
        global PTOFresult
        cup = self.item_bonus("Cup of Ace")
        if cup == True:
            #print("CUP")
            playerTOF = self.flip(0.5 + (0.0625 * self.characterFortune))
        else:
            #print("NOT")
            playerTOF = self.flip(0.5 + (0.0575 * self.characterFortune))
        #print(playerTOF)
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
                yourMatter = yourMatter + 1
                yourSpirit = yourSpirit + 1
                PTOFresult = "Your stats are increased by 1"
            elif playerTOF == "downward":
                foeMatter = foeMatter + 1
                foeSpirit = foeSpirit + 1
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
        return yourMatter, yourSpirit, enemyMatter,enemySpirit,enemyAttackType

    def battleSim(self,yourClass,enemyClass,playerMatter,playerSpirit,enemyMatter,enemySpirit,enemyAttackType):
        global enemyDeathFlag
        global playerDeathFlag
        global enemyFleeFlag
        playerDeathFlag = False
        enemyDeathFlag = False
        enemyFleeFlag = False
        fontsize = 20
        verCounter = 0
        horCounter = 0
        lineCounter = 0
        xcoor = 40
        ycoor = 110
        ycoorfinish = 130
        passCounter = 0
        while (playerDeathFlag == False) and (enemyDeathFlag == False) and (enemyFleeFlag == False):

            if playerDeathFlag == False:
                userpress = True
                playerAttackType = ''
                while userpress:
                    for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_m:
                                    playerAttackType = playerAttackType + "m"
                                    print(playerAttackType)
                                    userpress = False
                                if event.key == pygame.K_s:
                                    playerAttackType = playerAttackType + "s"
                                    userpress = False
                                if event.key == pygame.K_p:
                                    playerAttackType = playerAttackType+ "p"
                                    userpress = False
            
                if playerAttackType == "m":

                    if playerMatter > enemyMatter:
                        dmg = ("You inflicted {0:d} damage to your enemy's matter.".format(playerMatter - enemyMatter))
                        self.draw_normal_text(self.inventory_font_name,dmg,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoor + verCounter)
                        enemyMatter = enemyMatter - (playerMatter - enemyMatter)
                        if enemyMatter <= 0:
                             self.draw_normal_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoorfinish + verCounter)
                             enemyDeathFlag = True

                    elif playerMatter == enemyMatter:
                         self.draw_normal_text(self.inventory_font_name,"You inflicted 1 damage to your enemy's matter."\
                             ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoor + verCounter)
                         enemyMatter = enemyMatter -1
                         if enemyMatter <= 0:
                             self.draw_normal_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoorfinish + verCounter)
                             enemyDeathFlag = True

                    elif playerMatter < enemyMatter:
                         self.draw_normal_text(self.inventory_font_name,"Your attack did nothing."\
                             ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoor + verCounter)

                elif playerAttackType == "s":

                    if playerSpirit > enemySpirit:
                       dmg = ("You inflicted {0:d} damage to your enemy's spirit.".format(playerSpirit - enemySpirit))
                       self.draw_normal_text(self.inventory_font_name,dmg,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoor + verCounter)
                       enemySpirit = enemySpirit - (playerSpirit - enemySpirit)
                       if enemySpirit <= 0:
                            self.draw_normal_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoorfinish + verCounter)
                            enemyDeathFlag = True


                    elif playerSpirit == enemySpirit:
                         self.draw_normal_text(self.inventory_font_name,"You inflicted 1 damage to your enemy's spirit."\
                             ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoor + verCounter)
                         enemySpirit = enemySpirit -1
                         if enemySpirit <= 0:
                            self.draw_normal_text(self.inventory_font_name,"You have prevailed! "+enemyClass+" is defeated!"\
                                 ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoorfinish + verCounter)
                            enemyDeathFlag = True

                    elif playerSpirit < enemySpirit:
                         self.draw_normal_text(self.inventory_font_name,"Your attack did nothing.",\
                             fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoor + verCounter)

                elif  playerAttackType == "p":
                     passCounter = passCounter + 1
                     self.draw_normal_text(self.inventory_font_name,"You passed your turn!"\
                         ,fontsize,MIDNIGHTBLUE,xcoor + horCounter,ycoor + verCounter)

            self.screen.blit(self.small_blue_square_img, (164,423))
            self.draw_text(self.inventory_font_name," " +str(enemyMatter), 21, BLACK, 169, 423)
            self.screen.blit(self.small_blue_square_img, (163,446))
            self.draw_text(self.inventory_font_name, " " +str(enemySpirit), 21, BLACK, 163, 443)
            lineCounter = lineCounter + 1
            verCounter = verCounter + 25
            if lineCounter == 10:
               lineCounter = 0
               verCounter = 0
               horCounter = horCounter + 220
                
            if enemyDeathFlag == False:

                if passCounter == 5:
                    if enemyClass == "The Fool":
                            self.draw_normal_text(self.inventory_font_name,'"Why are you doing nothing! This is driving me insane!!"'\
                                ,fontsize,FIREBRICK,xcoor + horCounter,ycoor + verCounter)
                            enemyFleeFlag = True

                elif enemyAttackType == "matter":
                    if enemyMatter > playerMatter:
                        dmg =  (enemyClass +" has inflicted {0:d} damage to your matter.".format(enemyMatter - playerMatter))
                        self.draw_normal_text(self.inventory_font_name,dmg,fontsize,FIREBRICK,xcoor + horCounter,ycoor + verCounter)
                        playerMatter = playerMatter - ( enemyMatter - playerMatter)
                        if playerMatter <= 0:
                            self.draw_normal_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoor + horCounter,ycoorfinish + verCounter)
                            playerDeathFlag = True

                    elif enemyMatter == playerMatter:
                         self.draw_normal_text(self.inventory_font_name,enemyClass +" has inflicted 1 damage to your matter."\
                             ,fontsize,FIREBRICK,xcoor + horCounter,ycoor + verCounter)
                         playerMatter = playerMatter -1
                         if playerMatter <= 0:
                            self.draw_normal_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoor + horCounter,ycoorfinish + verCounter)
                            playerDeathFlag = True

                    elif enemyMatter < playerMatter:
                         self.draw_normal_text(self.inventory_font_name,enemyClass +"'s attack did nothing.",\
                             fontsize,FIREBRICK,xcoor + horCounter,ycoor + verCounter)

                elif enemyAttackType == "spirit":
                    if enemySpirit > playerSpirit:
                        dmg = ( enemyClass +" has inflicted {0:d} damage to your spirit.".format(enemySpirit - playerSpirit))
                        self.draw_normal_text(self.inventory_font_name,dmg,fontsize,FIREBRICK,xcoor + horCounter,ycoor + verCounter)
                        playerSpirit = playerSpirit - (enemySpirit - playerSpirit)
                        if playerSpirit <= 0:
                            self.draw_normal_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoor + horCounter,ycoorfinish + verCounter)
                            playerDeathFlag = True

                    elif enemySpirit == playerSpirit:
                         self.draw_normal_text(self.inventory_font_name,enemyClass +" has inflicted 1 damage to your spirit."\
                             ,fontsize,FIREBRICK,xcoor + horCounter,ycoor + verCounter)
                         playerSpirit = playerSpirit -1
                         if playerSpirit <= 0:
                             self.draw_normal_text(self.inventory_font_name,"You have failed and doomed the entire world."\
                                 ,fontsize,FIREBRICK,xcoor + horCounter,ycoorfinish + verCounter)
                             playerDeathFlag = True

                    elif enemySpirit < playerSpirit:

                         self.draw_normal_text(self.inventory_font_name,enemyClass +"'s attack did nothing."\
                             ,fontsize,FIREBRICK,xcoor + horCounter,ycoor + verCounter)

            self.screen.blit(self.small_blue_square_img, (552,423))
            self.draw_text(self.inventory_font_name," " +str(playerMatter), 21, BLACK, 552, 423)
            self.screen.blit(self.small_blue_square_img, (548,446))
            self.draw_text(self.inventory_font_name, " " +str(playerSpirit), 21, BLACK, 548, 443)
            lineCounter = lineCounter + 1
            verCounter = verCounter + 25
            if lineCounter == 10:
               lineCounter = 0
               verCounter = 0
               horCounter = horCounter + 220
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
            self.draw_text(self.inventory_font_name, self.characterClass, 30, BLACK, 717,ycoord+105)
            self.draw_text(self.inventory_font_name, "Matter: " + str(self.characterMatter), 30, BLACK, 717,ycoord+133)
            self.draw_text(self.inventory_font_name, "Spirit: " + str(self.characterSpirit), 30, BLACK, 717,ycoord+163)
            self.draw_text(self.inventory_font_name, "Fortune: " + str(self.characterFortune), 30, BLACK, 717,ycoord+193)
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
            self.draw_text(self.inventory_font_name, self.characterClass, 30, BLACK, 717,ycoord+105)
            self.draw_text(self.inventory_font_name, "Matter: " + str(self.characterMatter), 30, BLACK, 717,ycoord+133)
            self.draw_text(self.inventory_font_name, "Spirit: " + str(self.characterSpirit), 30, BLACK, 717,ycoord+163)
            self.draw_text(self.inventory_font_name, "Fortune: " + str(self.characterFortune), 30, BLACK, 717,ycoord+193)
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
        if (playerPosition.x - enemyPosition.x < abs(30) and playerPosition.y - enemyPosition.y < abs(48))\
            and (enemyPosition.x - playerPosition.x < abs(30) and enemyPosition.y - playerPosition.y < abs(48)):
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

##################################
# create the game object
g = Game()
g.show_start_screen()
g.show_name_entry_screen()
g.show_class_screen()
while True:
    g.new()
    g.run()
