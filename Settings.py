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
DIALOGUE_FONT= "Lucida Bright" 
INVENTORY_FONT = 'Gabriola'
TITLE = "Fortuna! (Demo)"
BGCOLOR = FIREBRICK

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE #27 squeared
GRIDHEIGHT = HEIGHT / TILESIZE #16 squares

#UI settings
DIALOGUE_BOX_IMG = "Dialogue_box.png"
DIALOGUE_ARROW_IMG = "fancyarrow.png"
NAME_SCROLL_IMG = "scroll.png"
CLASS_SHEET_IMG = "Class Selection.png"
INVENTORY_BOX = "inventory_box.png"
BATTLE_UI_IMG = "BattleUi.png"
BUTTON_TRANSP = 0
BUTTON_TRANSP_HOVER = 50
DIALOGUE_FILES = {'thefooltext' : 'thefooldialogue.txt',
                  'dumbtext' : 'placeholderdialogue.txt'}

#Enviroment Settings
WALL_IMG = "wall_image.png"

#Items Settings
ITEM_IMGS = {'Cup of Ace': 'cupoface.png'}

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


#Enemy Settings
IDLE_FRAME_SPEED = 850
ENEMY_SPRITESHEETS = {"The Fool": "thefoolSpriteSheet.png"}

#NPC Settings
IDLE_FRAME_SPEED = 850
NPC_SPRITESHEETS = {"Zara": "Zaraspritesheet.png"}


