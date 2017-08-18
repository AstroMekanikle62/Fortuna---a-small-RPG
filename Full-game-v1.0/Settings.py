#!/usr/bin/env python
#Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
SILVER = (192,192,192)

GREEN = (0,128,0)
FORESTGREEN = (34,139,34)

RED = (255,0,0)
FIREBRICK = (178, 34, 34)
SADDLEBROWN = (139, 69, 19)
CRIMSON = (235,0,75)

PURPLE = (128,0,128)

BLUE = (0,0,255)
MIDNIGHTBLUE = (25, 25, 112)
PALEBLUE = (224,224,255)
LIGHTBLUE = (0,255,255)
TEAL = (0,128,128)

ORANGE = (255,140,0)
YELLOW = (255,255,0)
GOLD = (255,225,0)
OILY = (153,153,0)

# game settings
WIDTH = 864  # 16 * 54 or 32 * 27 
HEIGHT = 512  #  32 * 16 or 64 * 8
FPS = 60
START_FONT= "Lucida Calligraphy"
DIALOGUE_FONT= "Gabriola" 
INVENTORY_FONT = 'Gabriola'
NORMAL_FONT = 'Times New Roman'
TITLE = "Fortuna! by Jafar Al Hussain"
BGCOLOR = FIREBRICK
LEVELS = ["level1.tmx","level2.tmx","level3.tmx","level4.tmx","level5.tmx","level6.tmx","level7.tmx","level8.tmx",
                       "level9.tmx","level10.tmx","Regret.tmx"]

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE #27 squeared
GRIDHEIGHT = HEIGHT / TILESIZE #16 squares

#UI settings
DIALOGUE_BOX_IMG = "Dialogue_box.png"
#DIALOGUE_ARROW_IMG = "arrowpointing.png"
NAME_SCROLL_IMG = "scroll.png"
CLASS_SHEET_IMG = "Class Selection.png"
INVENTORY_BOX = "inventory_box.png"
BATTLE_UI_IMG = "BattleUi.png"
BUTTON_TRANSP = 0
BUTTON_TRANSP_HOVER = 50

MENU_IMAGES = {'start' : 'startscreen-main.png',
               'howtoplay' : 'startscreen-htp.png',
               'controls' : 'startscreen-controls.png',
               'credits' : 'startscreen-credits.png',
               'gameover' : 'gameoverscreen.png',
               'ending' : 'endscreen.png',
               'background' : 'Background-verydim.png'}

CARD_IMAGES = {'fool' : '00_fool.png',
               'magician' : '01_magician.png',
               'highpriestess' : '02_high_priestess.png',
               'empress' : '03_empress.png',
               'emperor' : '04_emperor.png',
               'justice' : '08_justice.png',
               'hermit' : '09_hermit.png',
               'strength' : '11_strength.png',
               'hangedman' : '12_hanged_man.png',
               'death' : '13_death.png',
               'devil' : '15_devil.png',
               'world' : '21_world.png'}

DIALOGUE_FILES = {'thefooltext' : 'thefooldialogue.txt',
                  'zaratext' : 'zaradialogue.txt',
                  'thehangedmantext' : 'thehangedmandialogue.txt',
                  'theempresstext' : 'theempressdialogue.txt',
                  'theemperortext1' : 'theemperordialogue1.txt',
                  'theemperortext2' : 'theemperordialogue2.txt',
                  'theemperortext2' : 'theemperordialogue2.txt',
                  'themagiciantext' : 'themagiciandialogue.txt',
                  'thehermittext1' : 'thehermitdialogue1.txt',
                  'thehermittext2' : 'thehermitdialogue2.txt',
                  'thedeviltext' : 'thedevildialogue.txt',
                  'deathtext' : 'deathdialogue.txt',
                  'theworldtext' : 'theworlddialogue.txt'}

ABILITY_FILES = {'thehighpriestessU': "thehighpriestess-U.txt",
                 'thehighpriestessD': "thehighpriestess-D.txt",
                 'strengthU': "strength-U.txt",
                 'strengthD': "strength-D.txt",
                 'justiceU': "justice-U.txt",
                 'justiceD': "justice-D.txt",
                 'thefoolU': "0-thefool-U.txt",
                 'thefoolD': "0-thefool-D.txt",
                 'themagicianU': "1-themagician-U.txt",
                 'themagicianD': "1-themagician-D.txt",
                 'theempressU': "3-theempress-U.txt",
                 'theempressD': "3-theempress-D.txt",
                 'theemperorU': "4-theemperor-U.txt",
                 'theemperorD': "4-theemperor-D.txt",
                 'thehermitU': "9-thehermit-U.txt",
                 'thehermitD': "9-thehermit-D.txt",
                 'thehangedmanU': "12-thehangedman-U.txt",
                 'thehangedmanD': "12-thehangedman-D.txt",
                 'deathU': "13-death-U.txt",
                 'deathD': "13-death-D.txt",
                 'thedevilU': "15-thedevil-U.txt",
                 'thedevilD': "15-thedevil-D.txt",
                 'theworldU': "21-theworld-U.txt",
                 'theworldD': "21-theworld-D.txt"}

#Enviroment Settings
WALL_IMG = "wall_image.png"

#Items Settings
ITEM_IMGS = {'Cup of Ace': 'cupoface.png',
             'Queen of Wands': 'queenofwands.png',
             'King of Wands': 'kingofwands.png',
             'Pentacle of Ace': 'pentacleoface.png'}

#Player Settings
PLAYER_SPEED = 175
PLAYER_SPRITESHEET = "playerSpriteSheet.png"
WALKING_FRAME_SPEED = 250

#Class Settings
FIRST_CLASS = "The High Priestess"
SECOND_CLASS = "Strength"
THIRD_CLASS = "Justice"
FIRST_CLASS_PORTRAIT = "TheHighPriestessPOR.png"
SECOND_CLASS_PORTRAIT = "StrengthPOR.png"
THIRD_CLASS_PORTRAIT = "JusticePOR.png"
CLASS_SPRITESHEETS= {"The High Priestess": "TheHIghPriestessspritesheet.png",
                     "Strength": "Strengthspritesheet.png", "Justice": "Justicespritesheet.png"}

#Enemy Settings
IDLE_FRAME_SPEED = 1500
ENEMY_SPRITESHEETS = {"The Dummy": "thedummySpriteSheet.png",
                      "The Fool": "thefoolSpriteSheet.png",
                      "The Hanged Man":'thehangedmanSpriteSheet.png',
                      "The Empress":'theempressSpriteSheet.png',
                      "The Emperor":'theemperorSpriteSheet.png',
                      "The Magician":'themagicianSpriteSheet.png',
                      "The Hermit":'thehermitSpriteSheet.png',
                      "The Devil":'thedevilSpriteSheet.png',
                      "Death":'deathSpriteSheet.png',
                      "The World":'theworldSpriteSheet.png'}

#NPC Settings
NPC_SPRITESHEETS = {"Zara": "Zaraspritesheet.png",
                    "Grave": "Stillstuff1spritesheet.png"}




