import libtcodpy as libtcod
import math
import textwrap
import shelve
import os.path
import glob
import logging


###########################
#CONSTANTS
###########################

FONT_PATH = 'data/fonts/arial12x12.png'#Change this if you wish to change the font!
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 58
MAP_HEIGHT = 48

BAR_WIDTH = 20
PANEL_HEIGHT = 2
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
SIDEPANEL_WIDTH = 22
SIDEPANEL_X = SCREEN_WIDTH - SIDEPANEL_WIDTH

MSG_X = 1
MSG_WIDTH = SIDEPANEL_WIDTH - 2
MSG_HEIGHT = 9
MSG_Y = MAP_HEIGHT - MSG_HEIGHT - 2

BIG_MSG_WIDTH = 60
BIG_MSG_HEIGHT = 40
BIG_MSG_Y = SCREEN_HEIGHT / 2 - (BIG_MSG_HEIGHT + 6) / 2
BIG_MSG_X = SCREEN_WIDTH / 2 - (BIG_MSG_WIDTH + 4) / 2

CHARACTER_MENU_WIDTH = 60
CHARACTER_MENU_HEIGHT = 40
CHARACTER_MENU_Y = SCREEN_HEIGHT / 2 - (CHARACTER_MENU_HEIGHT + 6) / 2
CHARACTER_MENU_X = SCREEN_WIDTH / 2 - (CHARACTER_MENU_WIDTH + 4) / 2
CHARACTER_MENU_COLUMN1_X = 2
CHARACTER_MENU_COLUMN1_Y = 5
CHARACTER_MENU_COLUMN_DIVIDER_X = (CHARACTER_MENU_WIDTH + 4) / 2
CHARACTER_MENU_COLUMN_DIVIDER_LENGTH = CHARACTER_MENU_HEIGHT
CHARACTER_MENU_COLUMN2_X = CHARACTER_MENU_COLUMN_DIVIDER_X + 2
CHARACTER_MENU_COLUMN2_Y = 5

RECIPE_MENU_WIDTH = 60
RECIPE_MENU_HEIGHT = 40
RECIPE_MENU_Y = SCREEN_HEIGHT / 2 - (RECIPE_MENU_HEIGHT + 6) / 2
RECIPE_MENU_X = SCREEN_WIDTH / 2 - (RECIPE_MENU_WIDTH + 4) / 2
RECIPE_MENU_COLUMN_DIVIDER_X = (RECIPE_MENU_WIDTH + 4) / 2


HELP_MENU_OPTIONS = 4
HELP_MENU_1 = "About Kitchenmaster"
HELP_MENU_2 = "Keys"
HELP_MENU_3 = "Storyline"
HELP_MENU_4 = "Credits"
HELP_MENU_1_PATH = 'data/helpfiles/about kitchenmaster.txt'
HELP_MENU_2_PATH = 'data/helpfiles/keys.txt'
HELP_MENU_3_PATH = 'data/helpfiles/storyline.txt'
HELP_MENU_4_PATH = 'data/helpfiles/credits.txt'



HEAL_AMOUNT = 4

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

STAIRS_PER_FLOOR = 3
FLOOR_MAX = 10
SPECIAL_FLOOR = 666

SMAP = ['##########################################################',
        '##########################################################',
        '###################                     ##################',
        '##################                       #################',
        '#################        ###   ###        ################',
        '################        #   M  M  #        ###############',
        '###############        #           #        ##############',
        '##############        #             #        #############',
        '#############        #    M      M   #        ############',
        '############        #                 #        ###########',
        '########### M   M  #                   #  M   M ##########',
        '###########        #                   #        ##########',
        '###########        #      #     #      #        ##########',
        '###########        #       M   M       #        ##########',
        '###########        #   #           #   #        ##########',
        '###########        #         X         #        ##########',
        '###########        #   #           #   #        ##########',
        '###########        #       M   M       #        ##########',
        '###########        #      #     #      #        ##########',
        '########### M   M  #                   #  M   M ##########',
        '###########        #                   #        ##########',
        '############        #                 #        ###########',
        '#############        #               #        ############',
        '##############        #             #        #############',
        '###############        #           #        ##############',
        '################        #         #        ###############',
        '#################        #########        ################',
        '##################                       #################',
        '###################        M   M        ##################',
        '###########################     ##########################',
        '###########################     ##########################',
        '#####                    ##     ##                   #####',
        '##### ################## ##     ## ################# #####',
        '##### ################## ##     ## ################# #####',
        '##### ##        #        ##     ##      M#        ## #####',
        '##### ##   M    #        ##     ##      M#        ## #####',
        '##### ##  M        M M   ##     ##      M    M  M ## #####',
        '##### ##  M     # M M    ##     ##      M#M       ## #####',
        '##### ##   M    #        ##     ##       #    M   ## #####',
        '##### ## ##################     ################# ## #####',
        '##### ## ##################     ################# ## #####',
        '##### ##     M  #        ##     ##       #     M  ## #####',
        '##### ##    M   #    +   ##     ##  =    #    M   ## #####',
        '##### ##   M             ##     ##           M    ## #####',
        '##### ##  M     #        ##     ##       #  M     ## #####',
        '##### #####################     #################### #####',
        '#####                        <                       #####',
        '##########################################################',
        '##########################################################']

INVENTORY_WIDTH = 50

INGREDIENT_MEAT = 0
INGREDIENT_FLOUR = 1
INGREDIENT_MILK = 2
INGREDIENT_VEGGIES = 3

INGREDIENT_CHOCOLATE = 5
INGREDIENT_SPICES = 4


INGREDIENT_MEAT_COLOUR = libtcod.Color(130,0,0)
INGREDIENT_FLOUR_COLOUR = libtcod.Color(191,151,96)
INGREDIENT_MILK_COLOUR = libtcod.Color(255,255,255)
INGREDIENT_VEGGIES_COLOUR = libtcod.Color(0,191,0)

INGREDIENT_SPICES_COLOUR = libtcod.Color(255,0,100)
INGREDIENT_CHOCOLATE_COLOUR = libtcod.Color(229,191,0)

INGREDIENT_CODE = 0
INGREDIENT_NAME = 1
INGREDIENT_AMOUNT = 2
INGREDIENT_COLOUR = 3

RECIPE_TESTRECIPE = 0
RECIPE_ENTANGLING_NOODLES = 1
RECIPE_HOT_SAUCE = 2
RECIPE_SHORTBREAD_THROWING_STARS = 3
RECIPE_EXTRA_THICK_GRAVY = 4
RECIPE_CHOCOLATE_FONDUE_VOLCANO = 5
RECIPE_CHICKEN_JALFREEZY = 6
RECIPE_ICE_CUBES = 7
RECIPE_EGG_CUSTARD_TART = 8
RECIPE_SMELLY_PARMESAN = 9
RECIPE_CHOCOLATE_SWAN = 10
RECIPE_HUNDREDS_AND_THOUSANDS = 11
RECIPE_RHUBARB_SAUCE = 12
RECIPE_RUNNER_BEANS = 13
RECIPE_FROZEN_PIZZA = 14
RECIPE_SPINACH = 15
RECIPE_SPONGECAKE = 16
RECIPE_CHOP_SUEY = 17
RECIPE_TOAD_IN_THE_HOLE = 18
RECIPE_CHICKEN_TIKKA = 19
RECIPE_SAUSAGE_ROLL = 20
RECIPE_CHOCOLATE_LOG = 21
RECIPE_MINCE_MEAT = 22
RECIPE_TREACLE_TART = 23
RECIPE_JALAPENO_PEPPERS = 24
RECIPE_BANANA_SPLIT = 25
RECIPE_VANILLA_ICECREAM = 26
RECIPE_STRAWBERRY_ICECREAM = 27
RECIPE_CHOCOLATE_ICECREAM = 28
RECIPE_KNICKERBOCKER_GLORY = 29
RECIPE_MESSY_BOLOGNESE_SPLASH = 30
RECIPES = 30

MONSTER_TESTMONSTER = 0
MONSTER_GINGERBREADMAN = 1
MONSTER_BATTERFLY = 2
MONSTER_PEA_SHOOTER = 3
MONSTER_BROCCOLLI = 4
MONSTER_CUSTOMER = 5
MONSTER_GREEN_JELLY = 6
MONSTER_ICE_SCREAM = 7
MONSTER_HAGGIS = 8
MONSTER_MEAT_BALLER = 9
MONSTER_CHEESE_ROLLER = 10
MONSTER_GRUBBY_FORK = 11
MONSTER_VENDING_MACHINE = 12
MONSTER_NOT_SO_SWEETIE = 13
MONSTER_HARD_CANDY = 14
MONSTER_UNION_ONION = 15
MONSTER_RED_JELLY = 16 
MONSTER_TALKATIVE_PEPPER = 17
MONSTER_THE_CRITIC = 18#to do - ai, death, winning game etc

#wordwraps at 30 characters!

RECIPE_TESTRECIPE_DESC = """Test Recipe:
Cost: 5 meat

What better way to test if recipes work, than with a test recipe? This recipe will do 5 damage to the nearest  enemy.

123456789012345678901234567890"""

RECIPE_ENTANGLING_NOODLES_DESC = """Entangling Noodes:

Have you ever made noodles so thick and full of life that they wrap around the fork, crawl up your wrist, then slowly tighten around your whole body until you can't move? You have now.  

Entangles a monster for 3-6 turns"""

RECIPE_HOT_SAUCE_DESC = """Hot Sauce:

Hot Sauce! Using a secret blend of Tabasco, diesel and saucey romance novels, you can create a sauce so hot that few can withstand its effects! Just pour it on your spatula and see your damage increase until it dries up!

Buff: 10 more power for 100 turns  """

RECIPE_SHORTBREAD_THROWING_STARS_DESC = """Shortbread Throwing Stars:

God, these things are so.. OW.. so tasty.. OUCH! They're really sharp! And surprisingly aerodynamic. You'd better throw the rest of this batch at random people! For science!

Deals 5 globs of 5 damage to random nearby enemies, remaining stars get eaten for 3 health"""

RECIPE_EXTRA_THICK_GRAVY_DESC = """Extra-Thick Gravy:

Some people like their gravy thick. Some people like gravy so thick that it can help deflect attacks. This is the latter.

Buff: 10 more defense for 100 turns  """

RECIPE_CHOCOLATE_FONDUE_VOLCANO_DESC = """Chocolate Fondue Volcano

It takes a true master of confectionery to produce this swansong of a chocolate. Beautiful, delicious, and most importantly, capable of spitting deadly molten chocolate over large distances. A must have for any party!

Occasionally lobs chocolate at random enemies for 5 damage a time """

RECIPE_CHICKEN_JALFREEZY_DESC = """Chicken Jalfreezy:

Chicken Jalfrezi is a popular, if rather spicy, Indian dish. Less well known and much colder is its sister dish, chicken jalfreezy! 

Slows and damages for 5 all enemies in the area """

RECIPE_ICE_CUBES_DESC = """Ice Cubes:
You summon a giant ice cube* and throw it at your foe.
*Not Ice Cube, the hip-hop artist, actor, writer, director and producer of the same name.

Damages target enemy for 5 and slows """

RECIPE_EGG_CUSTARD_TART_DESC = """Egg-Custard Tart:

The most important rule about making an egg-custard tart is the 1:3 ratio between egg and custard. You remember this ratio from Kitchen University, but you never learned how to apply the nutmeg coefficient. Sadly, this means all these tarts are good for is throwing.

Debuff: Reduces attack and defence by 6 for 10 turns """

RECIPE_SMELLY_PARMESAN_DESC = """Smelly Parmesan:

'Wow, this Parmesan STINKS! How old is this?! I'm not eating this! Get that thing away from me!'
      -Your enemy

Debuff: reduces defense by 20 for 10 turns """

RECIPE_CHOCOLATE_SWAN_DESC = """Chocolate Swan:

Chef combat guide:
1: Cook an immaculate chocolate swan (This is the easy bit. Frankly you're a bit bored of making perfect swans by now)
2: Give the swan to a monster so they have their hands full.
3: Hit the monster until it dies.

Debuff: Reduces attack by 20 for 10 turns """

RECIPE_HUNDREDS_AND_THOUSANDS_DESC = """Hundreds and Thousands:

Hundreds and thousands, commonly known as sprinkles, are hand painted grains of sugar, cooked until hard in miniature ovens, or 'sprinklifiers'. It takes approximately 3 months to craft one batch of sprinkles, which are then sorted according to government-measured deliciousness charts. Only grade C+ and up sprinkles actually make it to the shelves. THE MORE YOU KNOW!

Confuses the target monster for 5 turns """

RECIPE_RHUBARB_SAUCE_DESC = """Rhubarb Sauce:

You invented rhubarb sauce during one of your 'experimental' phases. Everyone around you agreed it was so nice that you should never make it again, in case it 'ruined the memory'. Regardless, you have been tinkering around with it in your spare time, and have managed to make it extra 'barb'y. Wait until people try this out!

Buff: Reflects damage done for 100 turns"""

RECIPE_RUNNER_BEANS_DESC = """Runner Beans:

As well as being an excellent chef, you have dabbled in a little bit of gardening in your spare time. You have managed to grow a runner bean plant so lively that it seems to move around in the ground! No-one believes you, but you'll show them. You'll show them all.

Buff: Adds 100 speed for 100 turns"""

RECIPE_FROZEN_PIZZA_DESC = """Frozen Pizza: 

Being a chef is fun and all, but sometimes when you get back home and you've been cooking all day, and then you have to cook for yourself in the evening.. it just feels like work, you know?
For this very reason you spend 2 hours every day cooking and freezing pizzas, to unfreeze when you get back home. Sure, it's a little more work. But that's the price you pay for convenience!

Damages target for 20 damage and slows
"""

RECIPE_SPINACH_DESC = """Spinach:

With a little splash of olive oyl, maybe some hamgravy, perhaps a few Swee'Peas, this stuff will turn you from a Wimpy to a Popeye. And it's strong to the finach!

I'm sorry.

(Fun true fact: Spinach sales in America went up 33 percent between 1931-1936, largely attributed to Popeye!)

Buff: Gives you 100 more health for 100 turns """

RECIPE_SPONGECAKE_DESC = """Spongecake:

Your spongecake is famous for its use of actual sponge rock, to give it that distinct 'bludgeon you over the head' flavour!

Damages target for 15 damage and heals you 15 life """

RECIPE_CHOP_SUEY_DESC = """Chop Suey:

Your special chop suey recipe has three distinct flavours: Pain, anger, and mixed vegetables. It is particularly effective against those pesky Union Onions!

Damages target 3 times for 5 damage each
 """

RECIPE_TOAD_IN_THE_HOLE_DESC = """Toad in the Hole:

Toad in the hole is a traditional British dish where sausages (the toads) are placed in a Yorkshire pudding (the hole). The recipe can be described as "English cooked-again stewed meat". It's a little bit too silly for this game, so this variation of the recipe causes a giant toad (the toad) to fall on someone (the hole).

Damages a random monster for 50 damage
 """

RECIPE_CHICKEN_TIKKA_DESC = """Chicken Tikka:

Sorry, you're thinking of chicken TIKKA, the popular curry. This is actually chicken TICKER, a chicken stuffed with a ticking time bomb. You would be amazed how many monsters have made that mistake!

Damages target monster for 35 damage
 """

RECIPE_SAUSAGE_ROLL_DESC = """Sausage Roll:

This one used to really crack people up at the resturant! You used to take a sausage, and roll it along the table, yelling 'sausage roll! Get it? sausage roll!'. You zany person!

Damages in a line for 5-11 damage
 """

RECIPE_CHOCOLATE_LOG_DESC = """Chocolate Log:

A fine chocolatier will tell you that minimalism is the best quality you can have in confections. Simple, distinct flavours.

A MASTER chocolatier will tell you that that is rubbish, then hit you with a colossal chocolate log.

Damages in a line for 20-51 damage
 """

RECIPE_MINCE_MEAT_DESC = """Mince Meat:

Why are so many of your recipes based around hurting people? Why do you push people away? Is it that, deep down, what you really fear isn't being killed by giant brocollis; It's being rejected by giant brocollis.

Just a theory. Anyway, back to the game: This hurts monsters real bad.

Damages target monster for 15 damage
 """

RECIPE_TREACLE_TART_DESC = """Treacle Tart:

I guess the main question with this recipe is: Where did you get the treacle from? In fact, where does anyone get treacle from? What even IS treacle?

Damages target monster for 15 damage and slows
"""

RECIPE_JALAPENO_PEPPERS_DESC = """Jalapeno Peppers:

Be extra careful making this recipe - this is your top secret weapon. Just a 'pepper' of this will kill nearly anything in the game. Use this power wisely, it's an expensive one!

Damages target monster for 100 damage plus an extra 100 damage over time
"""

RECIPE_BANANA_SPLIT_DESC = """Banana Split:

Being a cook, you've probably heard them all. But what about THIS one:

Q.Why do bananas do so well on the dating scene?
A.Because they have Appeal!


A PEEL get it do you get it DO YOU GET IT

Heals you 1 life a turn for 40 turns
 """

RECIPE_VANILLA_ICECREAM_DESC = """Vanilla Icecream:

In this game, vanilla icecream gives the least healing of all the ice creams. Wheras in reality, vanilla ice cream is objectively the best ice cream (PROVE ME WRONG). Life is funny that way!

Heals you 10 life
  """

RECIPE_STRAWBERRY_ICECREAM_DESC = """Strawberry Icecream:

You carefully whip up a big batch of strawberry icecream, and quickly eat it all yourself. No, monsters, you can't have any. Stop asking.

Heals you 20 life
  """

RECIPE_CHOCOLATE_ICECREAM_DESC = """Chocolate Icecream:

Chocolate icecream is the executive rank of icecream in this game, combining the healing qualities of ice cream with the raw power of chocolate. Tasty!

Heals you 50 life
 """

RECIPE_KNICKERBOCKER_GLORY_DESC = """Knickerbocker Glory:

The ultimate heal, this heaven-sent confection will not only turn the tide of a battle, but also keep you fighting-fit for many turns to come!
Also it has the word 'knicker' in it. Hee, knicker.

Heals you 100 life plus 10 life a turn for 15 turns
 """

RECIPE_MESSY_BOLOGNESE_SPLASH_DESC = """Messy Bolognese Splash:

Ah, spaghetti bolognese, just like your mother used to make it! In a quantity large enough to drown everything around it in tasty bolognese sauce!

Deals 10 damage in a 3x3 grid around tile
 """


#a quick hack to blot the description in the recipe menu
RECIPE_CLEARSTRING = """Mouse over a recipe to see its description.                           
                                                     
                                                   
                                           
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              """
RECIPE_BLANKSTRING = """                                                                                                            
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              

                              
                              
                              
                              
                              
                              
                              
                              
                              """
                              

MAX_ROOM_MONSTERS = 3

LIMIT_FPS = 20

FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True
DEFAULT_SIGHT_RANGE = 10


color_dark_wall = libtcod.Color(125, 20, 20)
color_light_wall = libtcod.Color(250, 40, 40)
color_dark_ground = libtcod.Color(100, 75, 75)
color_light_ground = libtcod.Color(200, 150, 150)

#for future reference: \n

###########################
#CLASSES
###########################

class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color, explorable=False, explored=False, 
                 blocks=False, fighter=None, ai=None, item=None, stairs=None,
                 experience=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.fighter = fighter
        self.stairs = stairs
        self.explorable = explorable
        self.explored = explored
        self.experience = experience
        if self.fighter:  #let the fighter component know who owns it
            self.fighter.owner = self
        self.ai = ai
        if self.ai:  #let the AI component know who owns it
            self.ai.owner = self
        self.item = item
        if self.item:  #let the Item component know who owns it
            self.item.owner = self
        if self.stairs:
            self.stairs.owner = self
        if self.experience:
            self.experience.owner = self
 
    def move(self, dx, dy):
        #move by the given amount
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
 
    def draw(self):
        #set the color and then draw the character that represents this object at its position
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_foreground_color(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
 
    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return round(math.sqrt(dx ** 2 + dy ** 2))
        
    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_towards(self, target_x, target_y):
        path = libtcod.path_new_using_map(fov_map, 1.0)
        libtcod.path_compute(path, self.x, self.y, target_x, target_y)
        dx, dy = libtcod.path_get(path, 0)
        self.move(dx - self.x, dy - self.y)
        libtcod.path_delete(path)

    def send_to_back(self):
        #make this object be drawn first, so all others appear above it if they're in the same tile.
        global objects
        objects.remove(self)
        objects.insert(0, self)

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
 
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
        
class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

        
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
     
class Stairs:

    
    def __init__(self, direction, pairedwith=None):
        self.pairedwith = pairedwith
        self.direction = direction
        
    def use(self):
        global floor, objects, fov_recompute, player
        change_floor(floor, (floor + self.direction))
        if self.pairedwith != None:
            player.x = self.pairedwith.x
            player.y = self.pairedwith.y
        else:
            #adopt an up stair
            found = False
            while found == False:
                for object in objects:
                    if object.stairs != None:
                        if object.stairs.pairedwith == None:
                            if object.stairs.direction == 0 - self.direction:
                                self.pairedwith = object
                                object.stairs.pairedwith = self.owner
                                player.x = self.pairedwith.x
                                player.y = self.pairedwith.y
                                found = True
                                break
        initialize_fov()
        render_all()
                
class Hat:
    def __init__(self, shortname, longname, colour=libtcod.Color(255,255,255), level=0):
        self.shortname = shortname
        self.longname = longname
        self.colour = colour
        self.level = level
        self.buffedname = self.longname
        
        
    def wear(self):
        message('You place the ' + self.shortname + ' majestically on your head.', self.colour)
        if player.fighter.hat.level > self.level:
            message('This hat is worse than your old one!', libtcod.Color(255,115,115))
        if player.fighter.hat.level == self.level:
            message('This hat is equal to your old one.', libtcod.Color(255,255,255))
        if player.fighter.hat.level < self.level and player.fighter.hat.longname != 'Nothing':
            message('This hat is better than your old one!', libtcod.Color(115,255,115))
        player.fighter.defense -= player.fighter.hat.level
        player.fighter.max_hp -= (player.fighter.hat.level * 2)
        player.fighter.defense += self.level
        player.fighter.max_hp += (self.level * 2)
        if player.fighter.hp > player.fighter.max_hp:
            player.fighter.hp = player.fighter.max_hp
        player.fighter.hat=self
        player_action()
        
class Weapon:
    def __init__(self, shortname, longname, colour=libtcod.Color(255,255,255), level=0):
        self.shortname = shortname
        self.longname = longname
        self.colour = colour
        self.level = level
        self.buffedname = self.longname
        

    def wear(self):
        message('You grip the ' + self.shortname + ' triumphantly in your hands.', self.colour)
        if player.fighter.weapon.level > self.level:
            message('This ' + self.shortname + ' is worse than your old weapon!', libtcod.Color(255,115,115))
        if player.fighter.weapon.level == self.level:
            message('This ' + self.shortname + ' is equal to your old weapon.', libtcod.Color(255,255,255))
        if player.fighter.weapon.level < self.level and player.fighter.weapon.longname != 'Nothing':
            message('This ' + self.shortname + ' is better than your old weapon!', libtcod.Color(115,255,115))
        player.fighter.minpower -= player.fighter.weapon.level
        player.fighter.power -= (player.fighter.weapon.level * 2)
        player.fighter.minpower += self.level
        player.fighter.power += (self.level * 2)
        player.fighter.weapon = self
        player_action()
        
class BasicMonster:
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    monster.move_towards(player.x, player.y)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)   
  
class OnionMonster:
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        self.layers = 3
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    monster.move_towards(player.x, player.y)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)   

    def take_damage(self, damage, attacker):
        if damage > 0:
            self.layers -= 1
            if self.layers == 0:
                #kill onion
                function = self.owner.fighter.death_function
                if function is not None:
                    function(self.owner)    
            else:
                #shed a layer
                message('Your attack cuts a layer off the onion, but it has ' + str(self.layers) + ' more!')
        else:
            if attacker == player:
                message('Your attack on the onion bounces off its many layers!')
                 
                        
class HaggisMonster:
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    monster.move_towards(player.x, player.y)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)   
                        
    def take_damage(self, damage, attacker):
        if attacker == player:
            message("You can't bring yourself to even touch the haggis with your " + player.fighter.weapon.shortname + "!", libtcod.Color(255,0,0))

  
class PeaShooterMonster:   
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                pass
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    if monster.distance_to(player) < 6:
                        choice = libtcod.random_get_int(0, 0, 1)
                        if choice == 1 and player.fighter.hp > 0:
                            message('The pea shooter spits a pea at you!', libtcod.Color(0,255,0))
                            monster.fighter.attack(player)
                        else:
                            pass
                    else:
                        pass
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        pass
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player) 

class IceScreamMonster:   
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        self.screamed = 0
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                if self.screamed == 0:
                    if monster.distance_to(player) < 4:
                        message('Your blood chills as the ice scream lets out a banshee wail!', libtcod.Color(115,115,255))
                        self.screamed = 1
                        for object in objects:
                            if monster.distance_to(object) < 5 and object.fighter and object is not self.owner:
                                chilldebuff = Chill_Debuff(66, 6)
                                chilldebuff.apply_debuff(object)
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    monster.move_towards(player.x, player.y)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player) 

class CheeseRollerMonster:   
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    #either wander around or huck a cheese
                    choice = libtcod.random_get_int(0,0,100)
                    if choice > 50 and player.fighter.hp > 0:
                        #huck!
                        message('The cheese roller winds up and hucks a destructive cheese wheel at you!', libtcod.Color(255,255,0))
                        path = libtcod.path_new_using_map(fov_map, 1.0)
                        libtcod.path_compute(path, monster.x, monster.y, player.x, player.y)
                        dx, dy = libtcod.path_get(path, 0)
                        for i in range(0, libtcod.path_size(path)):
                            dx, dy = libtcod.path_get(path, i)
                            for object in objects:
                                if object.fighter and object.x == dx and object.y == dy:
                                    message(object.name.capitalize() + ' is hit by the cheese wheel!', libtcod.Color(255,255,0))
                                    damage = libtcod.random_get_int(0,5, 11)
                                    object.fighter.take_damage(damage)
                        libtcod.path_delete(path)
                    else:
                        dx = libtcod.random_get_int(0, -1, 1)
                        dy = libtcod.random_get_int(0, -1, 1)
                        monster.move(dx, dy)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player) 
 
class VendingMachineMonster:  
    #AI for a basic monster.
    
    def __init__(self, ai_state='vending', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        self.max_candies = 3
        self.current_candies = []
        self.turns_until_vending = 0
        self.time_to_vend = 10
        
        
    def take_turn(self):
        monster = self.owner
        #erry day i'm vendering
        self.ai_state = 'vending'
        self.turns_until_vending -= 1
        if self.turns_until_vending < 1 and len(self.current_candies) < self.max_candies:
            self.createcandy()
            self.turns_until_vending = self.time_to_vend
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                message('With a mighty grunt of effort, the vending machine pops out a not-so-sweetie!')
        
    def createcandy(self):
        candy = createmonster(MONSTER_NOT_SO_SWEETIE)
        #put it next to the vending machine
        validsquarex, validsquarey = 0, 0
        for x in range(self.owner.x - 1, self.owner.x+2):
            for y in range(self.owner.y - 1, self.owner.y+2):
                if is_blocked(x, y) == False:
                    validsquarex = x
                    validsquarey = y
        if validsquarex != 0:
            candy.x = validsquarex
            candy.y = validsquarey
            candy.vender = self
            self.current_candies.append(candy)
            objects.append(candy)
                       

class CriticMonster:   
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        self.turns_per_shout = 3
        self.turns_until_shout = 0
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 100:
                    #shout to wake up close by monsters
                    message("The Critic claps his hands in delight and squeals, 'I remember you... " + player.name + ", isn't it? I do believe I got your resturant shut down. Ah, memories... so. Have you come here for more punishment? Marvelous! Let the fun begin!'", libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            choice = libtcod.random_get_int(0,0,100)
            #can either move, attack if he is in range or do nothing, or (on a timer) shout
            if choice < 33:
                #attack/move
                if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)    
            elif choice < 33 + 33:
                #stay still/attack
                if monster.distance_to(player) > 1:
                    pass
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player) 
            else:
                #shout/attack/move
                if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                    if self.turns_until_shout < 1:
                        #shoutcodehere
                        #executive decision: shouts will be: cold, heal, summon monsters, deal damage
                        shout = libtcod.random_get_int(0,0,100)
                        if shout < 25:
                            message("The Critic bellows: 'This meal is too COLD!' A shiver goes up your spine as you start to freeze!", libtcod.red)
                            chilldebuff = Chill_Debuff(30, 6)
                            chilldebuff.apply_debuff(player)
                        elif shout < 50:
                            #heal
                            message("The Critic bellows: 'This meal is too dry, I want to be REFRESHED!' The critic is bathed in green light, and looks in better shape than before!", libtcod.red)
                            self.owner.fighter.heal(35)
                        elif shout < 75:
                            #summon
                            message("The critic looks down at his place, and bellows: 'This meal needs more ONIONS!'", libtcod.red)
                            self.createonions()
                            self.createonions()
                        else:
                            #damage
                            message("Throws his meal at you in disgust: 'This meal PAINS me!' Ouch, that hurt!", libtcod.red)
                            player.fighter.take_damage(libtcod.random_get_int(0,1,35))
                        self.turns_until_shout = self.turns_per_shout
                    else:
                        if monster.distance_to(player) > 1:
                            monster.move_towards(player.x, player.y)
                        #close enough, attack! (if the player is still alive.)
                        elif player.fighter.hp > 0:
                            monster.fighter.attack(player) 
            self.turns_until_shout -= 1
    
    def take_damage(self, damage, attacker):
        #he'll yell at you for hitting him, things like 'good, not great' or 'poor swing, needs work, very dry' etc
        attacker.fighter.normalattack(self.owner.fighter, damage)
        try:
            if self.owner.fighter.hp > 0:
                choice = libtcod.random_get_int(0,0,100)
                if choice > 20:
                    message("The Critic drones at you, 'A mediocre swing, with a pitiful follow-through. 3/10.'", libtcod.red)
                if choice > 40:
                    message("The critic picks up a tape recorder and intones: 'I'm not sure what is worse, his food or his appalling combat stance.'", libtcod.red)
                if choice > 60:
                    message("The critic looks at you and sighs, 'Is THAT really the BEST you can do?'", libtcod.red)
                if choice > 80:
                    message("The critic looks at his watch impatiently and whines: 'Look, is this going to take a while? I have other resturants to close down!'", libtcod.red )           
        except:
            pass
            
    def createonions(self):
        onion = createmonster(MONSTER_UNION_ONION)
        #put it next to the critic
        validsquarex, validsquarey = 0, 0
        for x in range(self.owner.x - 1, self.owner.x+2):
            for y in range(self.owner.y - 1, self.owner.y+2):
                if is_blocked(x, y) == False:
                    validsquarex = x
                    validsquarey = y
        if validsquarex != 0:
            onion.x = validsquarex
            onion.y = validsquarey
            objects.append(onion)
            message('A Union Onion appears!')
class PepperMonster:   
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #say something hilarious!
                choice = libtcod.random_get_int(0,0,100)
                if choice > 50:
                    message(self.pepper_say(), libtcod.Color(191,95,0))
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    monster.move_towards(player.x, player.y)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)
                        
    def pepper_say(self):
        choice = libtcod.random_get_int(0,0,5)
        if choice == 0:
            return "'It's gettin' hot in here!', the Pepper yells."
        if choice == 1:
            return "The talkative pepper leers at you and says, 'Hot stuff, coming through!'"
        if choice == 2:
            return "The pepper grins and screams 'I'm gonna be jalapeno business!'. He quickly looks around to see if anyone 'got it'."
        if choice == 3:
            return "'Stay back!', yells the talkative pepper, 'I've got a firey temper!'"
        if choice == 4:
            return "The pepper gibbers 'Man, I am on FIRE today!'"
        if choice == 5:
            return "The pepper drones 'The spice must flow!'"
           
class ForkMonster:   
    #AI for a basic monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #move towards player if far away
                if monster.distance_to(player) > 2:
                    monster.move_towards(player.x, player.y)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    message('The horrible fork lunges at you with its terrible three-pronged head!', libtcod.Color(255,115,115))
                    monster.fighter.attack(player)  
                    monster.fighter.attack(player)
                    monster.fighter.attack(player)
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player) 
 
 
class BerserkerMonster:
    #AI for a berserker monster.
    
    def __init__(self, ai_state='resting', turns_since_seen=0):
        self.ai_state = ai_state
        self.turns_since_seen = turns_since_seen
        self.berserker = 0
        
        
    def take_turn(self):
        monster = self.owner
        if self.ai_state == 'resting':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
                rand = libtcod.random_get_int(0, 0, 100)
                if rand < 20:
                    #shout to wake up close by monsters
                    message(monster.name.capitalize() + ' sees you and yells!', libtcod.Color(255,0,0))
                    for object in objects:
                        if object.ai and object.distance_to(monster) < 15:
                            object.ai.ai_state = 'aggressive'
                            object.ai.turns_since_seen = -5
        if self.ai_state == 'wandering':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                self.ai_state = 'aggressive'
            else:
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                monster.move(dx, dy)
        if self.ai_state == 'aggressive':
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
                #move towards player if far away
                if monster.distance_to(player) > 1:
                    monster.move_towards(player.x, player.y)
                #close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0:
                    monster.fighter.attack(player)    
            else:
                self.turns_since_seen += 1
                if self.turns_since_seen >= 5:
                    self.ai_state = 'wandering'
                    self.turns_since_seen = 0
                else:
                    #move towards player if far away
                    if monster.distance_to(player) > 1:
                        monster.move_towards(player.x, player.y)
                    #close enough, attack! (if the player is still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)
                        
    def take_damage(self, damage, attacker):
        if self.berserker == 0:
            message('Upon being hit, ' + self.owner.name.capitalize() + ' flies into a berserk rage!');
            self.owner.color = libtcod.Color(255,100,100)
            self.owner.fighter.power *= 2
            self.owner.fighter.minpower *= 2
            self.owner.fighter.speed *= 2
            self.berserker = 1
        #apply damage if possible
        if damage > 0:
            self.owner.fighter.hp -= damage
            if self.owner.fighter.hp <= 0:
                function = self.owner.fighter.death_function
                if function is not None:
                    function(self.owner)

class EntangledMonster:
    #AI for a temporarily confused monster (reverts to previous AI after a while).
    def __init__(self, old_ai, num_turns=10):
        self.old_ai = old_ai
        self.num_turns = num_turns
 
    def take_turn(self):
        if self.num_turns > 0:  #still confused...
            #move in a random direction, and decrease the number of turns confused
            if libtcod.random_get_int(0,0,100) > 50:
                message('The ' + self.owner.name + ' struggles in the entangling noodles.', libtcod.Color(255,255,0))
            self.num_turns -= 1
 
        else:  #restore the previous AI (this one will be deleted because it's not referenced anymore)
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer entangled!', libtcod.Color(255,0,0))
                    
class ConfusedMonster:
    #AI for a temporarily confused monster (reverts to previous AI after a while).
    def __init__(self, old_ai, num_turns=10):
        self.old_ai = old_ai
        self.num_turns = num_turns
 
    def take_turn(self):
        if self.num_turns > 0:  #still confused...
            #move in a random direction, and decrease the number of turns confused
            if libtcod.random_get_int(0,0,100) > 50:
                message('The ' + self.owner.name + ' giggles and chases after the sprinkles!', libtcod.Color(255,255,0))
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
 
        else:  #restore the previous AI (this one will be deleted because it's not referenced anymore)
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer distracted by the sugary confetti!', libtcod.Color(255,0,0))
   

 
#done - berserker, peashooter, fork, icecream, vendingmachine, cheese, onion, haggis
#todo CRITIC
 
class Recipe:
    def __init__(self, name, description, cast_function, cost):
        self.cast_function = cast_function
        self.cost = cost
        self.name = name
        self.description = description
        
    def learn(self):
        global known_recipes
        #adds the recipe to your recipe list
        #check the recipe list to see if you know it
        #if not, add it to the list
        found = False
        for i in known_recipes:
            if self.name == i.name:
                found = True
                break
        if found == False:
            known_recipes.append(self)
            message('You learn the recipe ' + self.name + '.', libtcod.Color(115,115,255))
            return True
        else:
            message('You already know ' + self.name.capitalize() + '!', libtcod.Color(255,0,0))
            
    def known(self):
        found = False
        for i in known_recipes:
            if self.name == i.name:
                found = True
                break
        if found == True:
            return True
        else:
            return False
        return False
    
    def cast(self):
        global recipes_used
        if check_ingredients(self.cost):
            if self.cast_function():
                use_ingredients(self.cost)
                recipes_used += 1
                player_action()
        else:
            message('You do not have enough ingredients!', libtcod.Color(159,159,159))
           
            
     
class Item:

    def __init__(self, chefhat=None, spatula=None, use_function=None):
        self.use_function = use_function
        self.chefhat = chefhat
        self.spatula = spatula
        if self.chefhat:  #let the chefhat component know who owns it
            self.chefhat.owner = self
        if self.spatula:  #let the spatula component know who owns it
            self.spatula.owner = self
        
    #an item that can be picked up and used.
    def pick_up(self):
        #add to the player's inventory and remove from the map
        if len(inventory) >= 26:
            message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.Color(255,0,0))
        else:
            if self.chefhat or self.spatula:
                if self.chefhat:
                    if self.chefhat.compare():
                        self.chefhat.wear()
                if self.spatula:
                    if self.spatula.compare():
                        self.spatula.wear()
            else:
                inventory.append(self.owner)
                objects.remove(self.owner)
                message('You picked up a ' + self.owner.name + '.', libtcod.Color(0,255,0))
            
    def drop(self):
        #add to the map and remove from the player's inventory. also, place it at the player's coordinates
        objects.append(self.owner)
        inventory.remove(self.owner)
        self.owner.x = player.x
        self.owner.y = player.y
        message('You dropped a ' + self.owner.name + '.', libtcod.Color(255,255,0))
            
    def use(self):
        #just call the "use_function" if it is defined
        if self.use_function is None:
            message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function(self.owner) != 'cancelled':
                pass
      
class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power, minpower, speed=100, weapon=None, hat=None, death_function=None, mnum=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.minpower = minpower
        self.speed = speed
        self.tusaved = 0
        self.weapon = weapon
        self.hat = hat
        self.mnum = mnum
        if self.weapon:
            self.weapon.owner = self
        if self.hat:
            self.hat.owner = self
        self.death_function = death_function
        self.debuffs = []
        self.rhubarb = False

    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            message(self.owner.name.capitalize() + ' takes ' + str(damage) + ' damage.')
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner)

    def attack(self, target):
        global total_spatula_damage, total_damage_blocked
        powerd = libtcod.random_get_int(0,self.minpower,self.power)
        defenced = libtcod.random_get_int(0,0,target.fighter.defense)
        if self.owner == player:
            #add to spatula damage
            total_spatula_damage += powerd
        if target == player:
            #add to damage defended
            total_damage_blocked += defenced
        #a simple formula for attack damage
        damage = powerd - defenced
        try:
            target.ai.take_damage(damage, self.owner)
        except:
            self.normalattack(target, damage)
        try:
            if target.fighter.rhubarb == True:
                message(self.owner.name.capitalize() + ' is hit back by the sharp barbs in the rhubarb sauce!', libtcod.Color(255,115,115))
                self.take_damage(damage)
        except:
            pass
            
    def normalattack(self, target, damage):
        if damage > 0:
            #make the target take some damage
            message(self.owner.name.capitalize() + ' attacks ' + target.name + '.')
            target.fighter.take_damage(damage)
        else:
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
         
    def specialattack(self, amount, target, blocked=True):
        #now defunct: you can just use take_damage() duh
        powerd = amount
        if blocked == True:
            defenced = libtcod.random_get_int(0,0,target.fighter.defense)
        else:
            defenced = 0
        
        #a simple formula for attack damage
        damage = powerd - defenced
        
        if damage > 0:
            target.fighter.take_damage(damage)
            return True
        else:
            return False
   
         
    def heal(self, amount):
        global total_hp_healed
        #stats for the stats god
        if amount + self.hp > self.max_hp:
            total_hp_healed += self.max_hp - self.hp
        else:
            total_hp_healed += amount
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
            
    def debuffs_tick(self):
        if len(self.debuffs) > 0:
            for debuff in self.debuffs:
                debuff.tick(self.owner)
            

class Chill_Debuff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        self.todecrease =  0
        
    
    def apply_debuff(self, target):
        if target == player:
            message ('You feel much colder! You start to slow down.', libtcod.Color(115,115,255))
        else:
            message(target.name.capitalize() + ' slows down.', libtcod.Color(115,115,255))
        spd = float(target.fighter.speed)
        amnt = float(self.amount)
        self.todecrease = target.fighter.speed - int(spd / 100.0 * amnt)
        target.fighter.speed -= self.todecrease
        target.fighter.debuffs.append(self)
    
    def tick(self, target):
        self.turns -= 1
        if self.turns == 0:
            #debuff out
            if target == player:
                message ('You feel like your normal speed again.', libtcod.Color(255,127,0))
            else:
                message(target.name.capitalize() + ' is moving at normal speed again.', libtcod.Color(115,115,255))
            target.fighter.speed += self.todecrease
            target.fighter.debuffs.remove(self)

class Hot_Sauce_Buff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        if target == player:
            message ('You pour hot sauce over your ' + target.fighter.weapon.shortname + '! Now it will be extra damaging for a while.', libtcod.Color(255,115,115))
        target.fighter.power += self.amount
        target.fighter.minpower += (self.amount / 2)
        self.updateweaponname(target)
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        self.updateweaponname(target)
        if self.turns == 0:
            #debuff out
            if target == player:
                message ('The hot sauce on your ' + target.fighter.weapon.shortname + ' dries up.', libtcod.Color(255,115,115))
            target.fighter.weapon.buffedname = target.fighter.weapon.longname
            target.fighter.power -= self.amount
            target.fighter.minpower -= (self.amount / 2)
            target.fighter.debuffs.remove(self)
    
    def updateweaponname(self, target):
        target.fighter.weapon.buffedname = target.fighter.weapon.longname + '(Hot sauce: ' + str(self.turns) + ' turns)'
    
class Extra_Thick_Gravy_Buff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        if target == player:
            message ('You dollop extra thick gravy over your ' + target.fighter.hat.shortname + '. It acts as a protective shield from attacks and getting dates.', libtcod.Color(255,115,115))
        target.fighter.defense += self.amount
        self.updatehatname(target)
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        self.updatehatname(target)
        if self.turns == 0:
            #debuff out
            if target == player:
                message ('The gravy on your ' + target.fighter.hat.shortname + ' dries up. You probably still need a shower before meeting new people though.', libtcod.Color(255,115,115))
            target.fighter.hat.buffedname = target.fighter.hat.longname
            target.fighter.defense -= self.amount
            target.fighter.debuffs.remove(self)
    
    def updatehatname(self, target):
        target.fighter.hat.buffedname = target.fighter.hat.longname + '(Thick gravy: ' + str(self.turns) + ' turns)'
       
class Chocolate_Fondue_Buff():

    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        if target == player:
            message ('You craftilly craft a large chocolate fondue volcano. Careful, this stuff is hot!', libtcod.Color(255,127,0))
        target.fighter.debuffs.append(self)

    def tick(self, target):
        monster = target_random_monster()
        if monster != None:
            if libtcod.random_get_int(0,0,100) > 66:
                #spit
                message('Your volcano erupts a glob of molten chocolate at ' + monster.name + '! It burns!', libtcod.Color(255,127,0))
                monster.fighter.take_damage(5)
                self.turns -= 1
        if self.turns == 0:
            #debuff out
            if target == player:
                message ('Your chocolate fondue volcano is all dried up. You throw it to the curb, where it safely dissolves.', libtcod.Color(255,115,115))
            target.fighter.debuffs.remove(self)
    
class Egg_Custard_Tart_Debuff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        message(target.name.capitalize() + ' is covered in custard! EGG-custard! The shame is hampering its fighting prowess!', libtcod.Color(255,255,0))
        target.fighter.power -= self.amount
        target.fighter.minpower -= (self.amount / 2)
        target.fighter.defense -= self.amount
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        if self.turns == 0:
            #debuff out
            message(target.name.capitalize() + ' wipes all the custard out its eyes and is back to full fighting strength!', libtcod.Color(255,255,0))
            target.fighter.power += self.amount
            target.fighter.minpower += (self.amount / 2)
            target.fighter.defense += self.amount
            target.fighter.debuffs.remove(self)
  
class Chocolate_Swan_Debuff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        message('You carelessly toss an immaculate chocoalte swan at ' + target.name + '. It cradles the swan close to its chest, greatly reducing its ability to attack!', libtcod.Color(255,115,115))
        target.fighter.power -= self.amount
        target.fighter.minpower -= (self.amount / 2)
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        if self.turns == 0:
            #debuff out
            message(target.name.capitalize() + ' clumsily drops the chocolate swan! After wiping a tear from its eye, it is back to full fighting strength.', libtcod.Color(255,115,115))
            target.fighter.power += self.amount
            target.fighter.minpower += (self.amount / 2)
            target.fighter.debuffs.remove(self)
 
class Smelly_Parmesan_Debuff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        message(target.name.capitalize() + ' is distracted by the smell of parmesan! It is too distracted to defend itself!', libtcod.Color(255,255,0))
        target.fighter.defense -= self.amount
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        if self.turns == 0:
            #debuff out
            message(target.name.capitalize() + ' has accepted the smell of parmesan in its life, and is back to full fighting strength!', libtcod.Color(255,255,0))
            target.fighter.defense += self.amount
            target.fighter.debuffs.remove(self)
 
class Rhubarb_Sauce_Buff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        if target == player:
            message ('You whip up a batch of rhubarb sauce and delicately layer it onto your ' +target.fighter.hat.shortname + ', making sure all the barbs point the right way.', libtcod.Color(255,115,115))
        target.fighter.rhubarb = True
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        if self.turns == 0:
            #debuff out
            if target == player:
                message ('Your rhubarb sauce has gone gross and icky, and you scrap it off.', libtcod.Color(255,115,115))
            target.fighter.rhubarb = False
            target.fighter.debuffs.remove(self)
    

class Runner_Beans_Buff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        message('As you nom down on the runner beans, you start to feel quick on your feet!', libtcod.Color(115,255,115))
        target.fighter.speed += self.amount
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        if self.turns == 0:
            #debuff out
            message("Your runner beans have 'run' out. Get it?", libtcod.Color(115,255,115))
            target.fighter.speed -= self.amount
            target.fighter.debuffs.remove(self)
            if target.fighter.speed < 1:
                message("Ah, you seem to be having a spot of speed trouble! Let us add some time to this buff, so you don't explode.")
                self.turns = 20
                self.apply_debuff(target)
            
class Spinach_Buff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        message('You crush a can of spinach, which explodes and sends spinach flying into your mouth! You feel tougher.', libtcod.Color(115,255,115))
        target.fighter.max_hp += self.amount
        target.fighter.hp += self.amount
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        if self.turns == 0:
            #debuff out
            message("You start to feel like your weeny self again.", libtcod.Color(115,255,115))
            target.fighter.max_hp -= self.amount
            if target.fighter.max_hp < target.fighter.hp:
                target.fighter.hp = target.fighter.max_hp
            target.fighter.debuffs.remove(self)
 
class Jalapeno_Peppers_Debuff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        message(target.name.capitalize() + ' is set on fire by the sheer hotness!', libtcod.Color(255,0,0))
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        message(target.name.capitalize() + ' burns!', libtcod.Color(255,0,0))
        target.fighter.take_damage(self.amount)
        if self.turns == 0:
            #debuff out
            message(target.name.capitalize() + ' cools down.', libtcod.Color(115,255,115))
            target.fighter.debuffs.remove(self)

class Heal_Over_Time_Buff():
    def __init__(self, amount, turns):
        self.amount = amount
        self.turns = turns
        
    
    def apply_debuff(self, target):
        message(target.name.capitalize() + ' is bathed in dairy goodness!', libtcod.Color(115,255,115))
        target.fighter.debuffs.append(self)

    
    def tick(self, target):
        self.turns -= 1
        target.fighter.heal(self.amount)
        if libtcod.random_get_int(0,0,100) > 66:
            message('So refreshing!', libtcod.Color(115,255,115))
        if self.turns == 0:
            #debuff out
            message('You are no longer being refreshed.', libtcod.Color(115,255,115))
            target.fighter.debuffs.remove(self)

            
class Experience:
    #Experience goes here!
    def __init__(self, level, experience):
        self.level = level
        self.experience = experience
        
    def gainexp(self, exp):
        self.experience = self.experience + exp
        if self.experience >= self.expfornextlevel():
            self.levelup()
            self.experience = 0
    
    def expfornextlevel(self):
        #just pulling numbers out the air
        return self.level * 100
    
    def levelup(self):
        #woohoo!
        self.level = self.level + 1
        message('Congratulations! You have been reached level ' + str(self.level) +' and have been promoted to ' + getTitleString(self.level) +'!', libtcod.Color(255,255,0))
        self.owner.fighter.max_hp = self.owner.fighter.max_hp + 5 
        self.owner.fighter.hp = self.owner.fighter.max_hp
        self.owner.fighter.minpower += 1
        self.owner.fighter.power += 2
        self.owner.fighter.defense += 1
        if self.level <= 10:
            recipechoices = []
            reps = 0
            while len(recipechoices) != 3:
                recipe = createrecipe(libtcod.random_get_int(0, 1, 30))
                alreadyin = False
                if len(recipechoices) != 0:
                    for i in recipechoices:
                        if recipe.name == i.name:
                            alreadyin = True
                if recipe.known() == False and alreadyin == False:
                    recipechoices.append(recipe)
                else:
                    reps +=1
                    if reps == 50:
                        break
            recipestrings = []
            for recipe in recipechoices:
                recipestrings.append(recipe.name)
            chosen = False
            while chosen == False:
                choice = menu('Choose a new recipe to learn!', recipestrings, 40)
                if choice == None:
                    secondchoice = confirmbox("Are you sure? You won't learn anything! Y/N")
                    if secondchoice == True:
                        chosen = True
                else:
                    recipechoices[choice].learn()
                    chosen = True
            
    
###########################
#METHODS
###########################
def main_menu():
    """contains everything about the main menu.
    should contain: new game, load game, highscores, about, quit"""
    while not libtcod.console_is_window_closed():
        #prepare the screen
        libtcod.console_set_background_color(0, libtcod.Color(0,0,0))
        libtcod.console_clear(0)
        libtcod.console_set_window_title('Kitchen Master')
        #show the game's title
        libtcod.console_set_foreground_color(0, libtcod.light_yellow)
        libtcod.console_print_center(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, 'KITCHEN MASTER')

        #show options and wait for the player's choice
        choice = menu('', ['Play a new game', 'Load game', 'Quit'], 24)
        
        
        if choice == 0:  #new game
            playername = inputbox('What name do you wish to be called?', width=35)
            if playername != '':
                new_game(playername)
                play_game()
        elif choice == 1: #load game
            load_game()
        elif choice == 2:  #quit
            break

def new_game(playername):
    global player, inventory, game_msgs, game_state, floors, floor, ingredients, savepath, big_game_msgs, known_recipes
    global monsters_killed, totalturns, tiles_explored, recipes_used, ingredients_earned
    global total_hp_healed, total_spatula_damage, total_damage_blocked
    #create object representing the player
    hat_component = Hat('head', 'Nothing', libtcod.Color(255,255,255), 0)
    weapon_component = Weapon('fists', 'Nothing', libtcod.Color(255,255,255), 0)
    fighter_component = Fighter(hp=30, defense=2, power= 5, minpower=1, speed=100, death_function=player_death,
                                weapon=weapon_component, hat=hat_component)
    experience_component = Experience(1,0)
    player = Object(0, 0, '@', playername, libtcod.Color(255,255,255), blocks=True, fighter=fighter_component,
                    experience=experience_component)
    floor = 1
    floors = []
    tiles_explored = 0
    #generate map (at this point it's not drawn to the screen)
    make_map()
    initialize_fov()
    #the path to the save if there is one
    savepath = ''
    game_state = 'playing'
    inventory = []
    known_recipes = []
    #set all stats to 0:
    monsters_killed = 0
    totalturns = 0
    recipes_used = 0
    ingredients_earned = 0
    total_hp_healed = 0
    total_spatula_damage = 0
    total_damage_blocked = 0
    #the ingredients pouch!
    ingredients = []
    meat = 0, 'Meat', libtcod.random_get_int(0, 0, 20), INGREDIENT_MEAT_COLOUR
    flour = 1, 'Flour', libtcod.random_get_int(0, 0, 20), INGREDIENT_FLOUR_COLOUR
    milk = 2, 'Milk', libtcod.random_get_int(0, 0, 20), INGREDIENT_MILK_COLOUR
    veggies = 3, 'Veggies', libtcod.random_get_int(0, 0, 20), INGREDIENT_VEGGIES_COLOUR
    spices = 4, 'Spices', libtcod.random_get_int(0, 0, 20), INGREDIENT_SPICES_COLOUR
    chocolate =5, 'Chocolate', libtcod.random_get_int(0, 0, 20), INGREDIENT_CHOCOLATE_COLOUR

    ingredients.append(meat)
    ingredients.append(flour)
    ingredients.append(milk)
    ingredients.append(veggies)
    ingredients.append(spices)
    ingredients.append(chocolate)


                   
    
    #create the list of game messages and their colors, starts empty
    game_msgs = []
    big_game_msgs = []
    #fill in floors so save doesn't crash
    change_floor(1,1)
    #a warm welcoming message!
    message('Welcome to Kitchen Master, ' + player.name + '! You stumble into the dungeon of the Critic, armed only with a handful of ingredients and your trusty spatula.', libtcod.gold)
    #change this later!
    recipesatstart = 0
    while recipesatstart != 3:
        recipe = createrecipe(libtcod.random_get_int(0,1,30))
        if recipe.known() == False:
            recipe.learn()
            recipesatstart += 1
    message("Press '?' for help!")

def play_game():
    player_action = None
 
    while not libtcod.console_is_window_closed():
        #render the screen
        render_all()
        libtcod.console_set_window_title(player.name + ' - Kitchen Master')
 
        libtcod.console_flush()
 
        #erase all objects at their old locations, before they move
        for object in objects:
            object.clear()

 
        #handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break
            
def render_all():
    global color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_map, fov_recompute
    global player, ingredients, floor, tiles_explored
    
    if fov_recompute:
        #recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, DEFAULT_SIGHT_RANGE, FOV_LIGHT_WALLS, FOV_ALGO)

        #go through all tiles, and set their background color
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight
                if not visible:
                    #if it's not visible right now, the player can only see it if it's explored
                    if map[x][y].explored:
                        if wall:
                            libtcod.console_set_back(con, x, y, get_dark_wall(), libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_back(con, x, y, get_dark_ground(), libtcod.BKGND_SET)
                else:
                    #it's visible
                    if wall:
                        libtcod.console_set_back(con, x, y, get_light_wall(), libtcod.BKGND_SET )
                    else:
                        libtcod.console_set_back(con, x, y, get_light_ground(), libtcod.BKGND_SET )
                    if map[x][y].explored == False:
                        tiles_explored += 1
                    map[x][y].explored = True
    
    #draw all objects in the list
    for object in objects:
        if object != player:
            object.draw()
    #draw the explored but not seen stationary objects
    for object in objects:
        if object.explorable == True:
            visible = libtcod.map_is_in_fov(fov_map, object.x, object.y)
            if visible:
                object.explored = True
            else:
                if object.explored == True:
                    libtcod.console_set_foreground_color(con, object.color)
                    libtcod.console_put_char(con, object.x, object.y, object.char, libtcod.BKGND_NONE)
                    
    player.draw()

    #finally blit the main screen
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)

    #prepare to render the GUI panel
    libtcod.console_set_background_color(sidepanel, libtcod.Color(0,0,0))
    libtcod.console_clear(sidepanel)
	
	#print the game messages, one line at a time
    y = 1
    libtcod.console_set_background_color(sidepanel, libtcod.darker_gray)
    libtcod.console_rect(sidepanel, MSG_X, MSG_Y+1, MSG_WIDTH, MSG_HEIGHT, False)
    for (line, color) in game_msgs:
        libtcod.console_set_foreground_color(sidepanel, color)
        libtcod.console_print_left(sidepanel, MSG_X, MSG_Y+y, libtcod.BKGND_NONE, line)
        y += 1
 
    #show the player's name and title at the top
    libtcod.console_set_background_color(sidepanel, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(sidepanel, libtcod.Color(255,255,255))
    namex = SIDEPANEL_WIDTH / 2 - len(player.name) / 2
    titlex = SIDEPANEL_WIDTH / 2 - len(getTitleString(player.experience.level)) / 2
    leveltext = '(Level ' + str(player.experience.level) + ')'
    levelx = SIDEPANEL_WIDTH / 2 - len(leveltext) / 2
    libtcod.console_print_left(sidepanel, namex, 1, libtcod.BKGND_NONE, player.name)
    libtcod.console_print_left(sidepanel, titlex, 2, libtcod.BKGND_NONE, getTitleString(player.experience.level))
    libtcod.console_print_left(sidepanel, levelx, 3, libtcod.BKGND_NONE, leveltext)

    
 
 
    #show the player's stats
    render_bar(1, 5, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp,
        libtcod.Color(255,115,115), libtcod.darker_red)
    #show the player's experience
    render_bar(1, 6, BAR_WIDTH, 'EXP', player.experience.experience, player.experience.expfornextlevel(),
        libtcod.Color(115,115,255), libtcod.darker_blue)
 
 
    #Show the ingredients and count
    libtcod.console_set_background_color(sidepanel, libtcod.Color(0,0,0))
    for y in range(0, len(ingredients)):
        ing = ingredients[y][0]
        libtcod.console_set_foreground_color(sidepanel, ingredients[y][3])
        libtcod.console_print_left(sidepanel, 2, 10+ing, libtcod.BKGND_NONE, ingredients[y][1] + ':')
        libtcod.console_set_foreground_color(sidepanel, ingredients[y][3])
        libtcod.console_print_right(sidepanel, SIDEPANEL_WIDTH - 3, 10+ing, libtcod.BKGND_NONE, str(ingredients[y][2]))
    

    #your spatula and hat go here
    libtcod.console_set_background_color(sidepanel, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(sidepanel, libtcod.Color(255,255,255))
    libtcod.console_print_left(sidepanel, 2, 25, libtcod.BKGND_NONE, 'Wielding:')
    libtcod.console_set_foreground_color(sidepanel, player.fighter.weapon.colour)
    #calculate total height for the weapon (after auto-wrap)
    weapon_text_height = libtcod.console_height_left_rect(sidepanel, 2, 26, SIDEPANEL_WIDTH - 3, SCREEN_HEIGHT, 
                                                          player.fighter.weapon.buffedname)
    libtcod.console_print_left_rect(sidepanel, 2, 26, SIDEPANEL_WIDTH-3, weapon_text_height, libtcod.BKGND_NONE, 
                                    player.fighter.weapon.buffedname)
    libtcod.console_set_foreground_color(sidepanel, libtcod.Color(255,255,255))
    libtcod.console_print_left(sidepanel, 2, 26 + weapon_text_height, libtcod.BKGND_NONE, 'Wearing:')
    libtcod.console_set_foreground_color(sidepanel, player.fighter.hat.colour)
    hat_text_height = libtcod.console_height_left_rect(sidepanel, 2, 26 + weapon_text_height, SIDEPANEL_WIDTH - 3, 
                                                       SCREEN_HEIGHT, player.fighter.hat.buffedname)
    libtcod.console_print_left_rect(sidepanel, 2, 27 + weapon_text_height, SIDEPANEL_WIDTH-3, 
                                    hat_text_height, libtcod.BKGND_NONE, player.fighter.hat.buffedname)
    """
    #speed goes here
    libtcod.console_set_background_color(sidepanel, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(sidepanel, libtcod.Color(255,255,255))
    libtcod.console_print_left(sidepanel, 2, 30, libtcod.BKGND_NONE, 'Speed:')
    libtcod.console_print_right(sidepanel, SIDEPANEL_WIDTH - 3, 30, libtcod.BKGND_NONE, str(player.fighter.speed))
    """
    #the floor you're on goes here
    libtcod.console_set_background_color(sidepanel, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(sidepanel, libtcod.Color(255,255,255)) 
    floor_text_height = libtcod.console_height_left_rect(sidepanel, 2, 34, SIDEPANEL_WIDTH - 2, SCREEN_HEIGHT, 
                                                          getFloorString(floor))
    libtcod.console_print_left_rect(sidepanel, 2, 34, SIDEPANEL_WIDTH-2, floor_text_height, libtcod.BKGND_NONE, 
                                    getFloorString(floor))
    
    #blit the contents of "sidepanel" to the root console
    libtcod.console_blit(sidepanel, 0, 0, SIDEPANEL_WIDTH, MAP_HEIGHT, 0, SIDEPANEL_X, 0)
    
    #now for bottompanel
    
    #prepare to render the GUI panel
    libtcod.console_set_background_color(bottompanel, libtcod.Color(0,0,0))
    libtcod.console_clear(bottompanel)
    
    #display names of objects under the mouse
    libtcod.console_set_foreground_color(bottompanel, libtcod.Color(159,159,159))
    libtcod.console_print_left(bottompanel, 1, 0, libtcod.BKGND_NONE, get_names_under_mouse())
    #display speed if it's been enhanced or reduced
    if player.fighter.speed != 100:
        libtcod.console_set_foreground_color(bottompanel, libtcod.gray)
        libtcod.console_print_left(bottompanel, 1, 1, libtcod.BKGND_NONE, 
                                   'Current speed: ' + str(player.fighter.speed) + ' percent of normal')
    #that's all for now, blit it
    libtcod.console_blit(bottompanel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

def change_floor(fromfloor, tofloor):
    global map, objects, floor, floors
    #save the current map
    if floors != []:
        for x in range(0,len(floors)):
            if floors[x][0] == fromfloor:
                del floors[x]
                break
    thisfloor = tuple()
    thisfloor = fromfloor, map, objects
    floors.append(thisfloor)
    #set next floor level
    floor = tofloor
    #check to see if new floor is found
    found = False
    foundon = 0
    if floors != []:
        for x in range(0,len(floors)):
            if floors[x][0] == tofloor:
                found = True
                foundon = x
    if found == True:
        #load that map and objects
        map = floors[foundon][1]
        objects = floors[foundon][2]
    else:
        #create a new map and add it to the floors list
        #quick hack
        if floor != SPECIAL_FLOOR:
            make_map()
        else:
            make_special_map()
        thisfloor = tuple()
        thisfloor = tofloor, map, objects
        floors.append(thisfloor)
    initialize_fov()
  

def make_map():
    global map, objects

    #the list of objects with just the player
    objects = [player]
    #fill map with "unblocked" tiles
    map = [[ Tile(True)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
    
    rooms = []
    num_rooms = 0
    for r in range(MAX_ROOMS):
        #random width and height
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        #random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

        #"Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)
 
        #run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        if not failed:
            #this means there are no intersections, so this room is valid
 
            #"paint" it to the map's tiles
            create_room(new_room)
            
            #add some contents to this room, such as monsters
            place_objects(new_room)

 
            #center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()
 
            if num_rooms == 0:
                #this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                #all rooms after the first:
                
                #connect it to the previous room with a tunnel
 
                #center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms-1].center()
 
                #draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
 
            #finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1
    #finally place the stairs and equipment
    place_stairs()
    place_equipment()
     
def make_special_map():
    global map, objects
    #the list of objects with just the player
    objects = [player]
    #fill map with "unblocked" tiles
    map = [[ Tile(True)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
    #make the custom map 'SMAP'
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if SMAP[y][x] == '#':
                map[x][y].blocked = True
                map[x][y].block_sight = True
            else:
                map[x][y].blocked = False
                map[x][y].block_sight = False
    place_special_objects()
    
def place_special_objects():
    global map, objects, floor
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if SMAP[y][x] == '<':
                stairs_component = Stairs(direction=-656)
                stairs = Object(x, y, '<', 'Hellish-looking stairs', libtcod.Color(255,0,0),
                                blocks=False, explorable=True, stairs=stairs_component)
                objects.append(stairs)
                stairs.send_to_back()
            if SMAP[y][x] == 'M':
                monster = choosemonster()
                monster.x = x
                monster.y = y
                objects.append(monster)
            if SMAP[y][x] == 'X':
                monster = createmonster(MONSTER_THE_CRITIC)
                monster.x = x
                monster.y = y
                objects.append(monster)
            if SMAP[y][x] == '+':
                #spatula
                spat = createspatula(floor)
                spat.x = x
                spat.y = y
                objects.append(spat)
                spat.send_to_back()
            if SMAP[y][x] == '=':
                #hat
                hat = createhat(floor)
                hat.x = x
                hat.y = y
                objects.append(hat)
                hat.send_to_back()

    
def create_room(room):
    global map
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    global map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global map
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    #render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)
 
    #render the background first
    libtcod.console_set_background_color(sidepanel, back_color)
    libtcod.console_rect(sidepanel, x, y, total_width, 1, False)
 
    #now render the bar on top
    libtcod.console_set_background_color(sidepanel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(sidepanel, x, y, bar_width, 1, False)
	#finally, some centered text with the values
    libtcod.console_set_foreground_color(sidepanel, libtcod.Color(255,255,255))
    libtcod.console_print_center(sidepanel, x + total_width / 2, y, libtcod.BKGND_NONE,
        name + ': ' + str(value) + '/' + str(maximum))
    
def initialize_fov():
    global fov_recompute, fov_map
    fov_recompute = True
    libtcod.console_clear(con)  #unexplored areas start black (which is the default background color)
    #create the FOV map, according to the generated map
    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)       
	
def get_names_under_mouse():
    #return a string with the names of all objects under the mouse
    mouse = libtcod.mouse_get_status()
    (x, y) = (mouse.cx, mouse.cy)
	#create a list with the names of all objects at the mouse's coordinates and in FOV
    names = [obj.name for obj in objects if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]
    names = ', '.join(names)  #join the names, separated by commas
    return names.capitalize()  

def place_objects(room):
    #choose random number of monsters
    num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
    
    for i in range(num_monsters):
        #choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        #only place it if the tile is not blocked
        if not is_blocked(x, y):
            #let's put down the test duder
            monster = choosemonster()
            walking = libtcod.random_get_int(0, 0, 1)
            if walking == 1:
                monster.ai.ai_state == 'wandering'
            monster.x = x
            monster.y = y
            objects.append(monster)
    
def place_stairs():
    global floor, objects
    if floor > 1 and floor <= FLOOR_MAX:
        #place up stairs
        toplace = STAIRS_PER_FLOOR
        while toplace != 0:
            x = libtcod.random_get_int(0, 0, MAP_WIDTH - 1)
            y = libtcod.random_get_int(0, 0, MAP_HEIGHT - 1)
            #only place it if the tile is not blocked
            objecthere = False
            for object in objects:
                if object.x == x and object.y == y and object != player:
                    objecthere = True
            if not is_blocked(x, y) and objecthere == False:
                stairs_component = Stairs(direction=-1)
                stairs = Object(x, y, '<', 'Stairs leading up', libtcod.Color(255,255,255),
                                blocks=False, explorable=True, stairs=stairs_component)
                objects.append(stairs)
                stairs.send_to_back()
                toplace = toplace-1                                 
    if floor < FLOOR_MAX:
        #place down stairs
        toplace = STAIRS_PER_FLOOR
        while toplace != 0:
            x = libtcod.random_get_int(0, 0, MAP_WIDTH -1)
            y = libtcod.random_get_int(0, 0, MAP_HEIGHT -1)
            #only place it if the tile is not blocked
            objecthere = False
            for object in objects:
                if object.x == x and object.y == y and object != player:
                    objecthere = True
            if not is_blocked(x, y) and objecthere == False:
                stairs_component = Stairs(direction=1)
                stairs = Object(x, y, '>', 'Stairs leading down', libtcod.Color(255,255,255),
                                blocks=False, explorable=True, stairs=stairs_component)
                objects.append(stairs)
                stairs.send_to_back()
                toplace = toplace-1 
    if floor == FLOOR_MAX:
        #place special stair to boss zone!
        placed = False
        while placed == False:
            x = libtcod.random_get_int(0, 0, MAP_WIDTH -1)
            y = libtcod.random_get_int(0, 0, MAP_HEIGHT -1)
            #only place it if the tile is not blocked
            objecthere = False
            for object in objects:
                if object.x == x and object.y == y and object != player:
                    objecthere = True
            if not is_blocked(x, y) and objecthere == False:
                stairs_component = Stairs(direction=656)
                stairs = Object(x, y, '>', 'Hellish-looking stairs', libtcod.Color(255,0,0),
                                blocks=False, explorable=True, stairs=stairs_component)
                objects.append(stairs)
                stairs.send_to_back()
                placed = True
    return None
    
def place_equipment():
    global map, objects, floor
    spatulas_to_place = True
    hats_to_place = True
    while spatulas_to_place == True:
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT  - 1)
        
        #only place it if the tile is not blocked
        if not is_blocked(x, y):
            spatula = createspatula(floor)
            spatula.x = x
            spatula.y = y
            objects.append(spatula)
            spatula.send_to_back()
            spatulas_to_place = False
            
    while hats_to_place == True:
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - 1)
        
        #only place it if the tile is not blocked
        if not is_blocked(x, y):
            hat = createhat(floor)
            hat.x = x
            hat.y = y
            objects.append(hat)
            hat.send_to_back()
            hats_to_place = False
   
def is_blocked(x, y):
    #first test the map tile
    if map[x][y].blocked:
        return True
 
    #now check for any blocking objects
    for object in objects:
        if object.blocks and object.x == x and object.y == y:
            return True
 
    return False

def message(new_msg, color = libtcod.Color(255,255,255)):
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)
    big_msg_lines = textwrap.wrap(new_msg, BIG_MSG_WIDTH)
 
    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room for the new one
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]
        #add the new line as a tuple, with the text and the color
        game_msgs.append( (line, color) )
    for line in big_msg_lines:
        if len(big_game_msgs) == BIG_MSG_HEIGHT:
            del big_game_msgs[0]
        big_game_msgs.append( (line, color) )
 

		
def inputbox(header, width=50, maxlength=30):
    """to allow people to type their name in and so on"""
    timer = 0
    command = ""
    x = 0
    header_height = libtcod.console_height_left_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    inputboxheight = 3
    height = header_height + inputboxheight
    window = libtcod.console_new(width, height)
    writingheight = header_height + (inputboxheight / 2)
    while not libtcod.console_is_window_closed():

        key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)

        timer += 1
        if timer % (LIMIT_FPS // 4) == 0:
            if timer % (LIMIT_FPS // 2) == 0:
                timer = 0
                libtcod.console_set_char(window, x,  writingheight, "_")
                libtcod.console_set_fore(window, x, writingheight, libtcod.Color(255,255,255))
            else:
                libtcod.console_set_char(window, x,  writingheight, " ")
                libtcod.console_set_fore(window, x, writingheight, libtcod.Color(255,255,255))
    
        if key.vk == libtcod.KEY_BACKSPACE and x > 0:
            libtcod.console_set_char(window, x,  writingheight, " ")
            libtcod.console_set_fore(window, x, writingheight, libtcod.Color(255,255,255))
            command = command[:-1]
            x -= 1
        elif key.vk == libtcod.KEY_ENTER:
            return command
            break
        elif key.vk == libtcod.KEY_ESCAPE:
            return ""
        elif key.c > 0 and len(command) <= maxlength:
            letter = chr(key.c)
            libtcod.console_set_char(window, x, writingheight, letter)  #print new character at appropriate position on screen
            libtcod.console_set_fore(window, x, writingheight, libtcod.Color(255,255,255))  #make it white or something
            command += letter  #add to the string
            x += 1
        #print the header, with auto-wrap
        libtcod.console_set_foreground_color(window, libtcod.Color(255,255,0))
        libtcod.console_print_left_rect(window, 0, 0, width, height, libtcod.BKGND_NONE, header)
        #blit the final window
        windowx = SCREEN_WIDTH/2 - width/2
        windowy = SCREEN_HEIGHT/2 - height/2
        libtcod.console_blit(window, 0, 0, width, height, 0, windowx, windowy, 1.0, 0.7)
        libtcod.console_flush()
        
def confirmbox(header, width=50):
    header_height = libtcod.console_height_left_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    height = header_height + 2
    window = libtcod.console_new(width, height)
    libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
    libtcod.console_print_left_rect(window, 0, 1, width, height, libtcod.BKGND_NONE, header)
    #blit the contents of "window" to the root console
    x = SCREEN_WIDTH/2 - width/2
    y = SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
    key_char = chr(key.c)
    if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    if key_char == 'y':
        return True
    if key_char == 'n':
        return False

def msgbox(text, width=50):
    menu(text, [], width)  #use menu() as a sort of "message box"
   
def menu(header, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
    #calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_height_left_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    totalheight = header_height
    for option in options:
        totalheight += libtcod.console_height_left_rect(con, 4, 0, width-4, SCREEN_HEIGHT, option)
        
    height = totalheight
    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
 
    #print the header, with auto-wrap
    libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
    libtcod.console_print_left_rect(window, 0, 0, width, height, libtcod.BKGND_NONE, header)
    #print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        prefix = '(' + chr(letter_index) + ') '
        libtcod.console_print_left(window, 0, y, libtcod.BKGND_NONE, prefix)
        text_height = libtcod.console_height_left_rect(con, 4, y, width-4, SCREEN_HEIGHT, option_text)
        libtcod.console_print_left_rect(window, 4, y, width-4, height, libtcod.BKGND_NONE, option_text)
        #text = '(' + chr(letter_index) + ') ' + option_text
        #libtcod.console_print_left(window, 0, y, libtcod.BKGND_NONE, text)
        y += text_height
        letter_index += 1
    #blit the contents of "window" to the root console
    x = SCREEN_WIDTH/2 - width/2
    y = SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    #convert the ASCII code to an index; if it corresponds to an option, return it
    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    return None

def inventory_menu(header):
    #show a menu with each item of the inventory as an option
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory]
 
    index = menu(header, options, INVENTORY_WIDTH)
    #if an item was chosen, return it
    if index is None or len(inventory) == 0: return None
    return inventory[index].item

def player_move_or_attack(dx, dy):
    global fov_recompute
 
    #the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy
 
    #try to find an attackable object there
    target = None
    for object in objects:
        if object.fighter and object.x == x and object.y == y:
            target = object
            break
 
    #attack if target found, move otherwise
    if target is not None and target is not player:
        player.fighter.attack(target)
        player_action()
    else:
        if map[x][y].blocked == False:
            player.move(dx, dy)
            fov_recompute = True
            player_action()
        
     
def handle_keys():
    global fov_recompute
 
    #key = libtcod.console_check_for_keypress()  #real-time
    #key = libtcod.console_wait_for_keypress(True)  #turn-based
    key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)

    #actions you can do at any time including while dead
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        exit = confirmbox('Are you sure you wish to save and quit? y/n')
        if exit:
            return 'exit'
            
    elif chr(key.c) == 'm':
        big_message_screen()
            
    elif chr(key.c) == '/' or chr(key.c) == '?':
        help_menu()
    elif chr(key.c) == 'c':
        character_stats_screen()

    
    if game_state == 'playing':
        #movement keys
        if key.vk ==libtcod.KEY_UP:
            player_move_or_attack(0, -1)
 
        elif key.vk == libtcod.KEY_DOWN:
            player_move_or_attack(0, 1)
 
        elif key.vk == libtcod.KEY_LEFT:
            player_move_or_attack(-1, 0)
 
        elif key.vk == libtcod.KEY_RIGHT:
            player_move_or_attack(1, 0)
            
        elif key.vk ==libtcod.KEY_KP1:
            player_move_or_attack(-1, 1)
        
        elif key.vk ==libtcod.KEY_KP2:
            player_move_or_attack(0, 1)
            
        elif key.vk ==libtcod.KEY_KP3:
            player_move_or_attack(1, 1)
            
        elif key.vk ==libtcod.KEY_KP4:
            player_move_or_attack(-1, 0)
            
        elif key.vk ==libtcod.KEY_KP5:
            player_move_or_attack(0, 0)
            
        elif key.vk ==libtcod.KEY_KP6:
            player_move_or_attack(1, 0)
            
        elif key.vk ==libtcod.KEY_KP7:
            player_move_or_attack(-1, -1)
            
        elif key.vk ==libtcod.KEY_KP8:
            player_move_or_attack(0, -1)
            
        elif key.vk ==libtcod.KEY_KP9:
            player_move_or_attack(1, -1)
            
        key_char = chr(key.c)    
        if key_char == 'b':
            player_move_or_attack(-1, 1)
            
        elif key_char == 'j':
            player_move_or_attack(0, 1)
            
        elif key_char == 'n':
            player_move_or_attack(1, 1)
            
        elif key_char == 'h':
            player_move_or_attack(-1, 0)
            
        elif key_char == '.':
            player_move_or_attack(0, 0)
            
        elif key_char == 'l':
            player_move_or_attack(1, 0)
            
        elif key_char == 'y':
            player_move_or_attack(-1, -1)
            
        elif key_char == 'k':
            player_move_or_attack(0, -1)
            
        elif key_char == 'u':
            player_move_or_attack(1, -1)
            


            
        else:
            #actions other than movement
            if key_char == 'g' or key_char == ',' or key.vk ==libtcod.KEY_KP0:
                #pick up an item
                for object in objects:  #look for an item in the player's tile
                    if object.x == player.x and object.y == player.y and object.item:
                        object.item.pick_up()
                        break
            if key_char == '>' or key_char == '<':
                use_stairs()
            if key_char == 'i':
                #show the inventory; if an item is selected, use it
                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()
            if key_char == 'd':
                #show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()
            if key_char == 'z':
                cast_spell()
            return 'didnt-take-turn'

def player_death(player):
    #the game ended!
    global game_state
    message('You died!', libtcod.Color(255,0,0))
    game_state = 'dead'
 
    #for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = libtcod.dark_red
             
def use_stairs():
    found = False
    #I just realised looking at this that you totally don't need the while statement
    #also derp derp flerp
    while found == False:
        for object in objects:
            if object.x == player.x and object.y == player.y:
                if object.stairs != None:
                    if object.stairs.direction == 1:
                        message('You descend the staircase.', libtcod.Color(255,127,0))
                    elif object.stairs.direction == -1:
                        message('You ascend the staircase.', libtcod.light_orange)
                    elif object.stairs.direction == 656:
                        message("You boldly enter the Critic's domain.", libtcod.Color(255,115,115))
                    elif object.stairs.direction == -656:
                        message("Your cowardice gets the better of you and you flee the Critic's domain.", libtcod.Color(255,115,115))
                    object.stairs.use()
                    found = True
                    player_action()
                    initialize_fov()
                    render_all()
                    break
        break
    if found == False:
        message('No stairs found!')
        
def getTitleString(lvl):
    #returns a string depending on the level given
    if lvl == 1: return 'Dishwasher 2nd Class'
    if lvl == 2: return 'Head Dishwasher'
    if lvl == 3: return 'Executive Peeler'
    if lvl == 4: return 'Grillsman'
    if lvl == 5: return 'Fillet Fiend'
    if lvl == 6: return 'Recipe Hoarder'
    if lvl == 7: return 'Sauceror'
    if lvl == 8: return 'Pastrymancer'
    if lvl == 9: return 'Dances with Sporks'
    if lvl == 10: return 'Chefulhu'
    else:
        return 'Chef Dude'
    
def getFloorString(floor):
    #returns a string depending on the floor given
    prefix = 'Floor ' + str(floor) + ': '
    suffix = ''
    if floor == 1:
        suffix = 'The Foyer of your Demise'
    elif floor == 2:
        suffix = 'Coat Room Nightmares'
    elif floor == 3:
        suffix = 'Enter the Kitchenmaster'
    elif floor == 4:
        suffix = 'The Skullery'
    elif floor == 5:
        suffix = 'A Frosty Reception'
    elif floor == 6:
        suffix = "Today's Special is Pain"
    elif floor == 7:
        suffix = 'High Noon Buffet'
    elif floor == 8:
        suffix = 'The Dining Halls of the Damned'
    elif floor == 9:
        suffix = 'The Broiling Room'
    elif floor == 10:
        suffix = 'Out of the Frying Pan..'
    elif floor == 666:
        suffix = "The Critic's Domain"
    return prefix + suffix
    
def save_game():
    global savepath
    if savepath != '':
        #open and overwrite the existing shelve
        file = shelve.open((savepath), 'n')
        file['map'] = map
        file['objects'] = objects
        file['player_index'] = objects.index(player)  #index of player in objects list
        file['inventory'] = inventory
        file['game_msgs'] = game_msgs
        file['big_game_msgs'] = big_game_msgs
        file['game_state'] = game_state
        file['floor'] = floor
        file['floors'] = floors
        file['ingredients'] = ingredients
        file['known_recipes'] = known_recipes
        file['monsters_killed'] = monsters_killed
        file['totalturns'] = totalturns
        file['tiles_explored'] = tiles_explored
        file['recipes_used'] = recipes_used
        file['ingredients_earned'] = ingredients_earned
        file['total_hp_healed'] = total_hp_healed
        file['total_spatula_damage'] = total_spatula_damage
        file['total_damage_blocked'] = total_damage_blocked
        file['savepath'] = savepath
        file.close()

    else:   
    #open a new empty shelve to write the game data
        saved = False
        x = 0
        while saved == False:
            f = os.path.isfile('saves/' + player.name + str(x) + '.sav')
            if f == False:
                savepath = 'saves/' + player.name + str(x) + '.sav'
                file = shelve.open('saves/' + player.name + str(x) + '.sav', 'n')
                file['map'] = map
                file['objects'] = objects
                file['player_index'] = objects.index(player)  #index of player in objects list
                file['inventory'] = inventory
                file['game_msgs'] = game_msgs
                file['big_game_msgs'] = big_game_msgs
                file['game_state'] = game_state
                file['floor'] = floor
                file['floors'] = floors
                file['ingredients'] = ingredients
                file['known_recipes'] = known_recipes
                file['monsters_killed'] = monsters_killed
                file['totalturns'] = totalturns
                file['tiles_explored'] = tiles_explored
                file['recipes_used'] = recipes_used
                file['ingredients_earned'] = ingredients_earned
                file['total_hp_healed'] = total_hp_healed
                file['total_spatula_damage'] = total_spatula_damage
                file['total_damage_blocked'] = total_damage_blocked
                file['savepath'] = savepath
                file.close()
                saved = True
            else:
                x = x+1
    
def load_game():
    global map, objects, player, inventory, game_msgs, game_state, floor 
    global floors, ingredients, savepath, big_game_msgs, known_recipes
    global monsters_killed, totalturns, tiles_explored, recipes_used, ingredients_earned
    global total_hp_healed, total_spatula_damage, total_damage_blocked
    savefiles = []
    savechoice = []
    path = 'saves/'
    listing = os.listdir(path)
    a = 0
    for x in listing:
        if x.find('.sav', 0, len(x)) != -1:
            try:
                file = shelve.open(path + x, 'r')
                sname = file['objects'][file['player_index']].name
                stitle = getTitleString(file['objects'][file['player_index']].experience.level)
                sfloor = getFloorString(file['floor'])
                dead = ''
                if file['game_state'] == 'dead':
                    dead = ' *DEAD*'
                if file['game_state'] == 'won':
                    dead = ' *WON*'
                savefiles.append(sname + ' the ' + stitle + ', ' + sfloor + dead)
                savetuple = a,x
                savechoice.append(savetuple)
                a = a+1#this links the save to the name for loading
                file.close()
            except:
                pass
    if savefiles != []:
        #prepare the screen
        libtcod.console_set_background_color(0, libtcod.Color(0,0,0))
        libtcod.console_clear(0)
        choice = menu('Choose a save game to load:', savefiles, 60)
        if choice == None:
            pass
        else:
            try:
                file = shelve.open(path + savechoice[choice][1], 'r')
                #open the previously saved shelve and load the game data
                map = file['map']
                objects = file['objects']
                player = objects[file['player_index']]  #get index of player in objects list and access it
                inventory = file['inventory']
                game_msgs = file['game_msgs']
                big_game_msgs = file['big_game_msgs']
                game_state = file['game_state']
                floor = file['floor']
                floors = file['floors']
                ingredients = file['ingredients']
                known_recipes = file['known_recipes']
                monsters_killed = file['monsters_killed']
                totalturns = file['totalturns']
                tiles_explored = file['tiles_explored']
                recipes_used = file['recipes_used']
                ingredients_earned = file['ingredients_earned']
                total_hp_healed = file['total_hp_healed']
                total_spatula_damage = file['total_spatula_damage']
                total_damage_blocked = file['total_damage_blocked']
                savepath = path + savechoice[choice][1] # just in case someone renames the save
                file.close()
                initialize_fov()
                play_game()
            except:
                msgbox('\n Something strange happened! Your saves might be corrupted :(\n Please send the errorlog.txt to zarquonmk2@gmail.com !', 40)
                logging.exception("Oops:")

            
    else:
        msgbox('\n No saved games found. \n', 24)

def win_game():
    global game_state
    libtcod.console_clear(0)
    msgbox("The Critic suddenly staggers, and blinks, his focus gone. 'What the-'")
    libtcod.console_clear(0)
    msgbox("The Critic falls to his knees. 'How can this.. happen..'")
    libtcod.console_clear(0)
    msgbox("The Critic starts to shrivel up and shrink. 'I'm... meeeeeeeltiiiinnnng'")
    libtcod.console_clear(0)
    msgbox("The Critic's clothes fall to the floor, and squeaking sound is heard amongst them! A rat is revealed!")
    libtcod.console_clear(0)
    msgbox("'At last, you have revealed my true form! Now prepare to suffer the - oh..'. You step over the rat-critic with a spatula.")
    libtcod.console_clear(0)
    msgbox("The Rat Critic considers his options. 'Oookay, you've won this time! But you haven't seen the last of me!' and runs away.")
    libtcod.console_clear(0)
    msgbox("Congratulations, you have won the game!")
    render_all()
    message("You have won the game! Congratulations!", libtcod.orange)
    game_state = 'won'
    
        
def player_action():
    global totalturns
    totalturns += 1
    if totalturns % 10 == 0:
        player.fighter.heal(1)
    #tick the buffs/debuffs on the player down
    player.fighter.debuffs_tick()
    #the player has taken a turn!
    #let's see what else can now take a turn and adjust accordingly
    #call this at the end of every action that should take a turn
    if game_state == 'playing':
        for object in objects:
            if object.ai and object.fighter:
                if object.fighter.speed + object.fighter.tusaved >= player.fighter.speed:
                    tospend = object.fighter.speed + object.fighter.tusaved
                    while tospend >= player.fighter.speed:
                        object.ai.take_turn()
                        object.fighter.debuffs_tick()
                        tospend = tospend - player.fighter.speed
                        object.fighter.tusaved = tospend
                else:
                    object.fighter.tusaved = object.fighter.tusaved + object.fighter.speed
    initialize_fov()
    render_all()

def monster_death(monster):
    global monsters_killed, objects
    monsters_killed += 1
    drops = False
    goodies = libtcod.random_get_int(0, 0, 100)
    if goodies > 50:
        message(monster.name.capitalize() + ' dropped some goodies!', libtcod.Color(115,115,255))
        drops = True
    #transform it into a nasty corpse! it doesn't block, can't be
    #attacked and doesn't move
    message(monster.name.capitalize() + ' is dead!', libtcod.Color(255,127,0))
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()
    
    if monster.fighter.mnum == MONSTER_GINGERBREADMAN:
        if drops:
            add_ingredients([ [INGREDIENT_FLOUR, 5], [INGREDIENT_MILK, 5] ])
        player.experience.gainexp(10)
    elif monster.fighter.mnum == MONSTER_BATTERFLY:
        if drops:
            add_ingredients([ [INGREDIENT_FLOUR, 5], [INGREDIENT_MEAT, 5] ])
        player.experience.gainexp(5)
    elif monster.fighter.mnum == MONSTER_PEA_SHOOTER:
        if drops:
            add_ingredients([ [INGREDIENT_VEGGIES, 7], ])
        player.experience.gainexp(10)
    elif monster.fighter.mnum == MONSTER_BROCCOLLI:
        if drops:
            add_ingredients([ [INGREDIENT_VEGGIES, 5], [INGREDIENT_MILK, 5] ])
        player.experience.gainexp(20)
    elif monster.fighter.mnum == MONSTER_CUSTOMER:
        if drops:
            add_ingredients([ [INGREDIENT_MEAT, 5], [INGREDIENT_VEGGIES, 5], [INGREDIENT_CHOCOLATE, 1] ])
        player.experience.gainexp(25)
    elif monster.fighter.mnum == MONSTER_GREEN_JELLY:
        try:
            if monster.spawned == True:
                if drops:
                    add_ingredients([ [INGREDIENT_FLOUR, 3], [INGREDIENT_MILK, 3], ])
                player.experience.gainexp(15)
        except:
            if drops:
                add_ingredients([ [INGREDIENT_FLOUR, 5], [INGREDIENT_MILK, 5], [INGREDIENT_SPICES, 1] ])
            player.experience.gainexp(30)
            jelliescreated = 0
            for i in range(0,3):
                jelly=createmonster(MONSTER_GREEN_JELLY)
                validsquarex, validsquarey = 0, 0
                for x in range(monster.x - 1, monster.x+2):
                    for y in range(monster.y - 1, monster.y+2):
                        if is_blocked(x, y) == False:
                            validsquarex = x
                            validsquarey = y
                if validsquarex != 0:
                    jelly.x = validsquarex
                    jelly.y = validsquarey
                    jelly.fighter.max_hp /= 2
                    jelly.fighter.hp /= 2
                    jelly.fighter.minpower /= 2
                    jelly.fighter.power /=2
                    jelly.fighter.defense /= 2
                    jelly.spawned = True
                    objects.append(jelly)
                    jelliescreated += 1
            if jelliescreated != 0:
                message(str(jelliescreated) + ' more jellies pop up in its place!', libtcod.Color(115,255,115))
    elif monster.fighter.mnum == MONSTER_ICE_SCREAM:
        if drops:
            add_ingredients([ [INGREDIENT_MILK, 5], [INGREDIENT_FLOUR, 5], [INGREDIENT_CHOCOLATE, 1] ])
        player.experience.gainexp(35)
    elif monster.fighter.mnum == MONSTER_HAGGIS:
        if drops:
            add_ingredients([ [INGREDIENT_MEAT, 5], [INGREDIENT_VEGGIES, 5], [INGREDIENT_SPICES, 1] ])
        player.experience.gainexp(40)
    elif monster.fighter.mnum == MONSTER_MEAT_BALLER:
        if drops:
            add_ingredients([ [INGREDIENT_MEAT, 5], [INGREDIENT_MILK, 5], [INGREDIENT_SPICES, 2] ])
        player.experience.gainexp(45)
    elif monster.fighter.mnum == MONSTER_CHEESE_ROLLER:
        if drops:
            add_ingredients([ [INGREDIENT_MILK, 5], [INGREDIENT_VEGGIES, 5], [INGREDIENT_CHOCOLATE, 2] ])
        player.experience.gainexp(50)
    elif monster.fighter.mnum == MONSTER_GRUBBY_FORK:
        if drops:
            add_ingredients([ [libtcod.random_get_int(0,0,5), 5], [libtcod.random_get_int(0,0,5), 5]  ])
        player.experience.gainexp(55)
    elif monster.fighter.mnum == MONSTER_VENDING_MACHINE:
        if drops:
            add_ingredients([ [INGREDIENT_MILK, 5], [INGREDIENT_VEGGIES, 5], [INGREDIENT_CHOCOLATE, 5],
                            [INGREDIENT_FLOUR, 5], [INGREDIENT_MEAT, 5], [INGREDIENT_SPICES, 5] ])
        player.experience.gainexp(100)
    elif monster.fighter.mnum == MONSTER_NOT_SO_SWEETIE:
        if drops:
            add_ingredients([ [libtcod.random_get_int(0,0,5), 2], [libtcod.random_get_int(0,0,5), 2]  ])
        player.experience.gainexp(10)
        monster.vender.current_candies.remove(monster)
    elif monster.fighter.mnum == MONSTER_HARD_CANDY:
        if drops:
            add_ingredients([ [INGREDIENT_FLOUR, 5], [INGREDIENT_MILK, 5], [INGREDIENT_CHOCOLATE, 3] ])
        player.experience.gainexp(65)
    elif monster.fighter.mnum == MONSTER_UNION_ONION:
        if drops:
            add_ingredients([ [INGREDIENT_MEAT, 5], [INGREDIENT_VEGGIES, 5], [INGREDIENT_SPICES, 3] ])
        player.experience.gainexp(70)
    elif monster.fighter.mnum == MONSTER_RED_JELLY:
        try:
            if monster.spawned == True:
                if drops:
                    add_ingredients([ [INGREDIENT_MEAT, 5], [INGREDIENT_MILK, 5], [INGREDIENT_CHOCOLATE, 1], [INGREDIENT_SPICES, 1] ])
                player.experience.gainexp(40)
        except:
            if drops:
                    add_ingredients([ [INGREDIENT_MEAT, 10], [INGREDIENT_MILK, 10], [INGREDIENT_CHOCOLATE, 3], [INGREDIENT_SPICES, 3] ])
            player.experience.gainexp(80)
            jelliescreated = 0
            for i in range(0,3):
                jelly=createmonster(MONSTER_RED_JELLY)
                validsquarex, validsquarey = 0, 0
                for x in range(monster.x - 1, monster.x+2):
                    for y in range(monster.y - 1, monster.y+2):
                        if is_blocked(x, y) == False:
                            validsquarex = x
                            validsquarey = y
                if validsquarex != 0:
                    jelly.x = validsquarex
                    jelly.y = validsquarey
                    jelly.fighter.max_hp /= 2
                    jelly.fighter.hp /= 2
                    jelly.fighter.minpower /= 2
                    jelly.fighter.power /=2
                    jelly.fighter.defense /= 2
                    jelly.spawned = True
                    objects.append(jelly)
                    jelliescreated += 1
            if jelliescreated != 0:
                message(str(jelliescreated) + ' more jellies pop up in its place!', libtcod.Color(255,115,115))
    elif monster.fighter.mnum == MONSTER_TALKATIVE_PEPPER:
        if drops:
            add_ingredients([ [INGREDIENT_SPICES, 10],  ])
        player.experience.gainexp(85)
        pass
    elif monster.fighter.mnum == MONSTER_THE_CRITIC:
        win_game()
    else:
        pass
    #then wipe its brain    
    monster.fighter = None
    monster.ai = None

    #things that have effects on death
    #critic - wins game
    #jellies - split into 2 smaller jellies once
    #not so sweeties - frees up a candy for the spawner


def big_message_screen():
    #create an off-screen console that represents the menu's window
    libtcod.console_set_background_color(0, libtcod.Color(0,0,0))
    libtcod.console_clear(0)
    window = libtcod.console_new(BIG_MSG_WIDTH + 4, BIG_MSG_HEIGHT + 6)
    libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
    title = 'Message Log'
    libtcod.console_set_background_color(window, libtcod.dark_gray)
    libtcod.console_rect(window, 0, 0, BIG_MSG_WIDTH + 4, 3, False)
    libtcod.console_print_left(window, (BIG_MSG_WIDTH + 4) / 2 - len(title) / 2, 1, 
                               libtcod.BKGND_NONE, title)
    libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
    y = 0
    for (line, color) in big_game_msgs:
        libtcod.console_set_foreground_color(window, color)
        libtcod.console_print_left(window, 2, 4+y, libtcod.BKGND_NONE, line)
        y += 1
    #blit the contents of "window" to the root console
    libtcod.console_blit(window, 0, 0, BIG_MSG_WIDTH +4, BIG_MSG_HEIGHT + 6, 0, BIG_MSG_X, BIG_MSG_Y, 1.0, 1.0)
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    
def character_stats_screen():
    global monsters_killed, totalturns, tiles_explored, recipes_used, ingredients_earned
    global total_hp_healed, total_spatula_damage, total_damage_blocked
    #things that i want to display here
    #turns spent
    #tiles explored
    #monsters killed
    #recipes used
    #total ingredients earned
    #current speed
    #total hp healed
    #damage dealt with spatulas
    #damage protected by hat
    #create an off-screen console that represents the menu's window
    libtcod.console_set_background_color(0, libtcod.Color(0,0,0))
    libtcod.console_clear(0)
    window = libtcod.console_new(CHARACTER_MENU_WIDTH + 4, CHARACTER_MENU_HEIGHT + 6)
    libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
    title = player.name.capitalize() + ' - Stats'
    libtcod.console_set_background_color(window, libtcod.dark_gray)
    libtcod.console_rect(window, 0, 0, CHARACTER_MENU_WIDTH + 4, 3, False)
    libtcod.console_print_left(window, (CHARACTER_MENU_WIDTH + 4) / 2 - len(title) / 2, 1, 
                               libtcod.BKGND_NONE, title)
    libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
    #the things i wish to show in a list
    stats = []
    stats.append( ('Turns taken:', totalturns) )
    stats.append( ('Monsters killed:', monsters_killed) )
    stats.append( ('Tiles explored:', tiles_explored) )
    stats.append( ('Recipes made:', recipes_used) )
    stats.append( ('Ingredients earned:', ingredients_earned) )
    stats.append( ('Current speed:', player.fighter.speed) )
    stats.append( ('Total HP healed:', total_hp_healed) )
    stats.append( ('Total spatula damage:', total_spatula_damage) )
    stats.append( ('Damage reduced by hat:', total_damage_blocked) )
    #now to show the stats
    index = 1
    y = 0
    for (text, stat) in stats:
        if index % 2 == 1:
            #column 1
            libtcod.console_print_left(window, 4, 5 + y, libtcod.BKGND_NONE, text)
            libtcod.console_print_right(window, CHARACTER_MENU_COLUMN_DIVIDER_X - 2, 
                                        5 + y, libtcod.BKGND_NONE, str(stat))
        else:     
            #column 2
            libtcod.console_print_left(window, CHARACTER_MENU_COLUMN_DIVIDER_X + 2, 
                                    5 + y, libtcod.BKGND_NONE, text)
            libtcod.console_print_right(window, CHARACTER_MENU_WIDTH - 2, 
                                        5 + y, libtcod.BKGND_NONE, str(stat))
            y += 2
        index += 1
    #blit the contents of "window" to the root console
    libtcod.console_blit(window, 0, 0, CHARACTER_MENU_WIDTH +4, CHARACTER_MENU_HEIGHT + 6, 0, CHARACTER_MENU_X, CHARACTER_MENU_Y, 1.0, 1.0)
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    
def help_menu():
    file_list = []
    file_list.append(HELP_MENU_1)
    file_list.append(HELP_MENU_2)
    file_list.append(HELP_MENU_3)
    file_list.append(HELP_MENU_4)
    choice = menu('Help Menu', file_list, 24)
    if choice != None:
        if choice == 0:
            path = HELP_MENU_1_PATH
        elif choice == 1:
            path = HELP_MENU_2_PATH
        elif choice == 2:
            path = HELP_MENU_3_PATH
        elif choice == 3:
            path = HELP_MENU_4_PATH
        else:
            path = ''
        if path != '':
            #now you have the path
            #do everything else
            f = open(path, 'r')
            helptext= ''
            flines = f.readlines()
            for line in flines:
                helptext = helptext + line
            #going to be hacky and assume that
            #the helpfile is written with good
            #textwrap
            #create an off-screen console that represents the menu's window
            libtcod.console_set_background_color(0, libtcod.Color(0,0,0))
            libtcod.console_clear(0)
            window = libtcod.console_new(BIG_MSG_WIDTH + 4, BIG_MSG_HEIGHT + 6)
            libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
            libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
            title = 'Help Menu'
            libtcod.console_set_background_color(window, libtcod.dark_gray)
            libtcod.console_rect(window, 0, 0, BIG_MSG_WIDTH + 4, 3, False)
            libtcod.console_print_left(window, (BIG_MSG_WIDTH + 4) / 2 - len(title) / 2, 1, 
                                       libtcod.BKGND_NONE, title)
            libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
            libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
            #also going to assume it fits in the space >.< bad writing could sink it
            libtcod.console_print_left_rect(window, 2, 4, BIG_MSG_WIDTH  + 2, BIG_MSG_HEIGHT, libtcod.BKGND_NONE, helptext)
            #blit the contents of "window" to the root console
            libtcod.console_blit(window, 0, 0, BIG_MSG_WIDTH +4, BIG_MSG_HEIGHT + 6, 0, BIG_MSG_X, BIG_MSG_Y, 1.0, 1.0)
            #present the root console to the player and wait for a key-press
            libtcod.console_flush()
            key = libtcod.console_wait_for_keypress(True)
            if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
            
        
    
    pass
    
def recipe_menu():
    #create an off-screen console that represents the menu's window
    libtcod.console_set_background_color(0, libtcod.Color(0,0,0))
    libtcod.console_clear(0)
    window = libtcod.console_new(RECIPE_MENU_WIDTH + 4, RECIPE_MENU_HEIGHT + 6)
    libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
    title = 'Recipes'
    libtcod.console_set_background_color(window, libtcod.dark_gray)
    libtcod.console_rect(window, 0, 0, RECIPE_MENU_WIDTH + 4, 3, False)
    libtcod.console_print_left(window, (RECIPE_MENU_WIDTH + 4) / 2 - len(title) / 2, 1, 
                               libtcod.BKGND_NONE, title)
    #print out the recipes
    rectangles = []
    libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
    libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
    letter_index = ord('a')
    y = 0
    for recipe in known_recipes:
        libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
        libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
        text = '(' + chr(letter_index) + ') ' + recipe.name.capitalize()
        rectstartx = 10
        rectstarty = 7+y
        libtcod.console_print_left(window, 2, 5 + y, libtcod.BKGND_NONE, text)
        #then print ingredients
        ing = recipe.cost
        x = 0
        y += 1
        for (type, amount) in ing:
            col = libtcod.Color(255,255,255)
            for (a,b,c,d) in ingredients:
                if type == a:
                    col = d
                    text = b + ': ' + str(amount)
            if x >= RECIPE_MENU_COLUMN_DIVIDER_X - len(text) - 2:
                y += 1
                x = 0
            libtcod.console_set_foreground_color(window, col)
            libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
            libtcod.console_print_left(window, 2 + x, 5 + y, libtcod.BKGND_NONE, text)
            x += len(text) + 2
        rectendx = RECIPE_MENU_COLUMN_DIVIDER_X + 8
        rectendy = 7 + y
        rectangles.append((letter_index, rectstartx, rectstarty, rectendx, rectendy))
        y += 1
        letter_index += 1
    while not libtcod.console_is_window_closed():
        mouse = libtcod.mouse_get_status()
        key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
        libtcod.console_clear(0)
        #now the description side
        libtcod.console_set_background_color(window, libtcod.Color(0,0,0))
        libtcod.console_set_foreground_color(window, libtcod.Color(255,255,255))
        libtcod.console_print_left_rect(window, RECIPE_MENU_COLUMN_DIVIDER_X + 2, 5, 
                                        RECIPE_MENU_COLUMN_DIVIDER_X - 2,  
                                        RECIPE_MENU_HEIGHT -3, libtcod.BKGND_NONE, 
                                        RECIPE_BLANKSTRING)
        libtcod.console_print_left_rect(window, RECIPE_MENU_COLUMN_DIVIDER_X + 2, 5, 
                                        RECIPE_MENU_COLUMN_DIVIDER_X - 2,  
                                        RECIPE_MENU_HEIGHT -3, libtcod.BKGND_NONE, 
                                        get_recipe_under_mouse(rectangles, mouse.cx, mouse.cy))
        #blit
        libtcod.console_blit(window, 0, 0, RECIPE_MENU_WIDTH +4, RECIPE_MENU_HEIGHT + 6, 0, RECIPE_MENU_X, RECIPE_MENU_Y, 1.0, 1.0)
        libtcod.console_flush()
        if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        #convert the ASCII code to an index; if it corresponds to an option, return it
        index = key.c - ord('a')
        if index >= 0 and index < len(known_recipes): 
            return index
            break
        if index >= len(known_recipes) or index <= 0 and key.pressed != False :
            return None
            break
        

def get_recipe_under_mouse(rectangles, x, y):
    #return a string with the names of all objects under the mouse
    for (index, startx, starty, endx, endy) in rectangles:
        if x >= startx and x <= endx and y >= starty and y <= endy:
            return known_recipes[index - ord('a')].description
    return RECIPE_CLEARSTRING

    
def check_ingredients(ing):
    #returns true if able, false if not
    global ingredients
    #first check to see if you can
    able = True
    for x in range(0, len(ing)):
        #find the ingredient you're checking in ingredients
        a = -1
        for y in range(0, len(ingredients)):
            if ing[x][0] == ingredients[y][0]:
                a = y
                break
        if a == -1:
            able = False#i coded it wrong or someone typo'd an ingredient
            break
        else:
            if ingredients[a][2] < ing[x][1]:
                able = False
    return able
  
def use_ingredients(ing):
    #returns true if used, false if not
    global ingredients
    if check_ingredients(ing):
        #find the ingredients again lol
        for x in range(0, len(ing)):
            for y in range(0, len(ingredients)):
                if ing[x][0] == ingredients[y][0]:
                    newtuple = ingredients[y][0], ingredients[y][1], ingredients[y][2] - ing[x][1], ingredients[y][3]
                    del ingredients[y]
                    ingredients.append(newtuple)
                    break
        return True
    else:
        return False
                    

def createrecipe(rnum):
    global known_recipes
    #this method will take a number, and return a full blown Recipe
    #complete with cast_function and everything. all the recipes in
    #the game will be kept in here and it's a giant switch function
    #to select the proper one!
    #name, description, cast_function, cost
    if rnum == RECIPE_TESTRECIPE:
        rcast_function = cast_testrecipe
        rname = 'test recipe'
        rcost = [ (INGREDIENT_MEAT, 5), ]
        rdesc = RECIPE_TESTRECIPE_DESC
    if rnum == RECIPE_ENTANGLING_NOODLES:
        rcast_function = cast_entangling_noodles
        rname = 'Entangling Noodles'
        rcost = [ (INGREDIENT_MEAT, 8), (INGREDIENT_FLOUR, 8), (INGREDIENT_SPICES, 1) ]
        rdesc = RECIPE_ENTANGLING_NOODLES_DESC
    if rnum == RECIPE_HOT_SAUCE:
        rcast_function = cast_hot_sauce
        rname = 'Hot Sauce'
        rcost = [ (INGREDIENT_MEAT, 7), (INGREDIENT_MILK, 5), (INGREDIENT_SPICES, 1) ]
        rdesc = RECIPE_HOT_SAUCE_DESC
    if rnum == RECIPE_SHORTBREAD_THROWING_STARS:
        rcast_function = cast_shortbread_throwing_stars
        rname = 'Shortbread Throwing Stars'
        rcost = [ (INGREDIENT_FLOUR, 5), (INGREDIENT_MILK, 5) ]
        rdesc = RECIPE_SHORTBREAD_THROWING_STARS_DESC
    if rnum == RECIPE_EXTRA_THICK_GRAVY:
        rcast_function = cast_extra_thick_gravy
        rname = 'Extra-thick Gravy'
        rcost = [ (INGREDIENT_MEAT, 10), (INGREDIENT_FLOUR, 10) ]
        rdesc = RECIPE_EXTRA_THICK_GRAVY_DESC
    if rnum == RECIPE_CHOCOLATE_FONDUE_VOLCANO:
        rcast_function = cast_chocolate_fondue_volcano
        rname = 'Chocolate Fondue Volcano'
        rcost = [ (INGREDIENT_MILK, 7), (INGREDIENT_FLOUR, 7), (INGREDIENT_SPICES, 3), (INGREDIENT_CHOCOLATE, 3) ]
        rdesc = RECIPE_CHOCOLATE_FONDUE_VOLCANO_DESC
    if rnum == RECIPE_CHICKEN_JALFREEZY:
        rcast_function = cast_chicken_jalfreezy
        rname = 'Chicken Jalfreezy'
        rcost = [ (INGREDIENT_MEAT, 5), (INGREDIENT_VEGGIES, 5), (INGREDIENT_SPICES, 1)]
        rdesc = RECIPE_CHICKEN_JALFREEZY_DESC
    if rnum == RECIPE_ICE_CUBES:
        rcast_function = cast_ice_cubes
        rname = 'Ice Cubes'
        rcost = [ (INGREDIENT_MILK, 4), (INGREDIENT_FLOUR, 4)]
        rdesc = RECIPE_ICE_CUBES_DESC
    if rnum == RECIPE_EGG_CUSTARD_TART:
        rcast_function = cast_egg_custard_tart
        rname = 'Egg-Custard Tart'
        rcost = [ (INGREDIENT_MILK, 5), (INGREDIENT_FLOUR, 5) ]
        rdesc = RECIPE_EGG_CUSTARD_TART_DESC
    if rnum == RECIPE_SMELLY_PARMESAN:
        rcast_function = cast_smelly_parmesan
        rname = 'Smelly Parmesan'
        rcost = [ (INGREDIENT_MILK, 10), (INGREDIENT_VEGGIES, 5), (INGREDIENT_SPICES, 2) ]
        rdesc = RECIPE_SMELLY_PARMESAN_DESC
    if rnum == RECIPE_CHOCOLATE_SWAN:
        rcast_function = cast_chocolate_swan
        rname = 'Chocolate Swan'
        rcost = [ (INGREDIENT_MILK, 10), (INGREDIENT_FLOUR, 5), (INGREDIENT_CHOCOLATE, 2) ]
        rdesc = RECIPE_CHOCOLATE_SWAN_DESC
    if rnum == RECIPE_HUNDREDS_AND_THOUSANDS:
        rcast_function = cast_hundreds_and_thousands
        rname = 'Hundreds and Thousands'
        rcost = [ (INGREDIENT_FLOUR, 5), (INGREDIENT_MILK, 5), (INGREDIENT_CHOCOLATE, 1) ]
        rdesc = RECIPE_HUNDREDS_AND_THOUSANDS_DESC
    if rnum == RECIPE_RHUBARB_SAUCE:
        rcast_function = cast_rhubarb_sauce
        rname = 'Rhubarb Sauce'
        rcost = [ (INGREDIENT_VEGGIES, 10), (INGREDIENT_FLOUR, 10), (INGREDIENT_SPICES, 1) ]
        rdesc = RECIPE_RHUBARB_SAUCE_DESC
    if rnum == RECIPE_TOAD_IN_THE_HOLE:
        rcast_function = cast_toad_in_the_hole
        rname = 'Toad in the Hole'
        rcost = [ (INGREDIENT_MEAT, 10), (INGREDIENT_FLOUR, 10), (INGREDIENT_SPICES, 1) ]
        rdesc = RECIPE_TOAD_IN_THE_HOLE_DESC
    if rnum == RECIPE_CHOCOLATE_LOG:
        rcast_function = cast_chocolate_log
        rname = 'Chocolate Log'
        rcost = [ (INGREDIENT_MILK, 10), (INGREDIENT_FLOUR, 8), (INGREDIENT_CHOCOLATE, 1) ]
        rdesc = RECIPE_CHOCOLATE_LOG_DESC
    if rnum == RECIPE_SAUSAGE_ROLL:
        rcast_function = cast_sausage_roll
        rname = 'Sausage Roll'
        rcost = [ (INGREDIENT_MEAT, 6), (INGREDIENT_FLOUR, 5) ]
        rdesc = RECIPE_SAUSAGE_ROLL_DESC
    if rnum == RECIPE_CHICKEN_TIKKA:
        rcast_function = cast_chicken_tikka
        rname = 'Chicken Tikka'
        rcost = [ (INGREDIENT_MEAT, 10), (INGREDIENT_VEGGIES, 5), (INGREDIENT_SPICES, 1) ]
        rdesc = RECIPE_CHICKEN_TIKKA_DESC
    if rnum == RECIPE_CHOP_SUEY:
        rcast_function = cast_chop_suey
        rname = 'Chop Suey'
        rcost = [ (INGREDIENT_MEAT, 8), (INGREDIENT_VEGGIES, 8)]
        rdesc = RECIPE_CHOP_SUEY_DESC
    if rnum == RECIPE_SPINACH:
        rcast_function = cast_spinach
        rname = 'Spinach'
        rcost = [ (INGREDIENT_VEGGIES, 10), (INGREDIENT_SPICES, 1)]
        rdesc = RECIPE_SPINACH_DESC
    if rnum == RECIPE_SPONGECAKE:
        rcast_function = cast_spongecake
        rname = 'Spongecake'
        rcost = [ (INGREDIENT_MEAT, 6), (INGREDIENT_FLOUR, 6), (INGREDIENT_MILK, 6) ]
        rdesc = RECIPE_SPONGECAKE_DESC
    if rnum == RECIPE_FROZEN_PIZZA:
        rcast_function = cast_frozen_pizza
        rname = 'Frozen Pizza'
        rcost = [ (INGREDIENT_MEAT, 5), (INGREDIENT_FLOUR, 10), (INGREDIENT_VEGGIES, 5) ]
        rdesc = RECIPE_FROZEN_PIZZA_DESC
    if rnum == RECIPE_RUNNER_BEANS:
        rcast_function = cast_runner_beans
        rname = 'Runner Beans'
        rcost = [ (INGREDIENT_VEGGIES, 15), (INGREDIENT_SPICES, 1) ]
        rdesc = RECIPE_RUNNER_BEANS_DESC
    if rnum == RECIPE_MINCE_MEAT:
        rcast_function = cast_mince_meat
        rname = 'Mince Meat'
        rcost = [ (INGREDIENT_MEAT, 8), ]
        rdesc = RECIPE_MINCE_MEAT_DESC
    if rnum == RECIPE_TREACLE_TART:
        rcast_function = cast_treacle_tart
        rname = 'Treacle Tart'
        rcost = [ (INGREDIENT_FLOUR, 4), (INGREDIENT_MILK, 4), (INGREDIENT_VEGGIES, 4), (INGREDIENT_MEAT, 4) ]
        rdesc = RECIPE_TREACLE_TART_DESC
    if rnum == RECIPE_JALAPENO_PEPPERS:
        rcast_function = cast_jalapeno_peppers
        rname = 'Jalapeno Peppers'
        rcost = [ (INGREDIENT_VEGGIES, 15), (INGREDIENT_SPICES, 10) ]
        rdesc = RECIPE_JALAPENO_PEPPERS_DESC
    if rnum == RECIPE_BANANA_SPLIT:
        rcast_function = cast_banana_split
        rname = 'Banana Split'
        rcost = [ (INGREDIENT_VEGGIES, 5), (INGREDIENT_MILK, 5)]
        rdesc = RECIPE_BANANA_SPLIT_DESC
    if rnum == RECIPE_VANILLA_ICECREAM:
        rcast_function = cast_vanilla_icecream
        rname = 'Vanilla Icecream'
        rcost = [ (INGREDIENT_MILK, 5), ]
        rdesc = RECIPE_VANILLA_ICECREAM_DESC
    if rnum == RECIPE_STRAWBERRY_ICECREAM:
        rcast_function = cast_strawberry_icecream
        rname = 'Strawberry Icecream'
        rcost = [ (INGREDIENT_MILK, 6), (INGREDIENT_VEGGIES, 3) ]
        rdesc = RECIPE_STRAWBERRY_ICECREAM_DESC
    if rnum == RECIPE_CHOCOLATE_ICECREAM:
        rcast_function = cast_chocolate_icecream
        rname = 'Chocolate Icecream'
        rcost = [ (INGREDIENT_MILK, 10), (INGREDIENT_CHOCOLATE, 2)]
        rdesc = RECIPE_CHOCOLATE_ICECREAM_DESC
    if rnum == RECIPE_KNICKERBOCKER_GLORY:
        rcast_function = cast_knickerbocker_glory
        rname = 'Knickerbocker Glory'
        rcost = [ (INGREDIENT_MILK, 10), (INGREDIENT_FLOUR, 10), (INGREDIENT_CHOCOLATE, 5) ]
        rdesc = RECIPE_KNICKERBOCKER_GLORY_DESC
    if rnum == RECIPE_MESSY_BOLOGNESE_SPLASH:
        rcast_function = cast_messy_bolognese_splash
        rname = 'Messy Bolognese Splash'
        rcost = [ (INGREDIENT_MEAT, 5), (INGREDIENT_FLOUR, 5), (INGREDIENT_SPICES, 1) ]
        rdesc = RECIPE_MESSY_BOLOGNESE_SPLASH_DESC
    #then ship the recipe
    rec = Recipe(rname, rdesc, rcast_function, rcost)
    return rec
    

    
def createmonster(mnum):
    #this method will take an index number, and return the full
    #monster
    fighter_component = None
    ai_component = None
    if mnum == MONSTER_TESTMONSTER:
        fighter_component = Fighter(hp=10, defense=0, power=3, minpower=0, 
                                    death_function=monster_death, mnum=MONSTER_TESTMONSTER)
        ai_component = BasicMonster()
        symbol = 'o'
        colour = libtcod.Color(64,128,64)
        mblocks = True
        name = 'tmonster'
    elif mnum == MONSTER_GINGERBREADMAN:
        fighter_component = Fighter(hp=6, defense=0, power=3, minpower=0, 
                                    death_function=monster_death, mnum=MONSTER_GINGERBREADMAN)
        ai_component = BasicMonster()
        symbol = 'g'
        colour = libtcod.Color(85,45,0)
        mblocks = True
        name = 'ginger bread man'
    elif mnum == MONSTER_BATTERFLY:
        fighter_component = Fighter(hp=3, defense=0, power=2, minpower=0, speed=200, 
                                    death_function=monster_death, mnum=MONSTER_BATTERFLY)
        ai_component = BasicMonster()
        symbol = 'b'
        colour = libtcod.Color(64,96,128)
        mblocks = True
        name = 'batterfly'
    elif mnum == MONSTER_PEA_SHOOTER:
        fighter_component = Fighter(hp=5, defense=0, power=4, minpower=1, speed=90, 
                                    death_function=monster_death, mnum=MONSTER_PEA_SHOOTER)
        ai_component = PeaShooterMonster()
        symbol = 'p'
        colour = libtcod.Color(32,64,32)
        mblocks = True
        name = 'pea shooter'
    elif mnum == MONSTER_BROCCOLLI:
        fighter_component = Fighter(hp=15, defense=2, power=8, minpower=2, speed=60, 
                                    death_function=monster_death, mnum=MONSTER_BROCCOLLI)
        ai_component = BasicMonster()
        symbol = 'B'
        colour = libtcod.Color(32,64,32)
        mblocks = True
        name = 'giant broccolli'
    elif mnum == MONSTER_CUSTOMER:
        fighter_component = Fighter(hp=10, defense=2, power=6, minpower=2, speed=100, 
                                    death_function=monster_death, mnum=MONSTER_CUSTOMER)
        ai_component = BerserkerMonster()
        symbol = 'c'
        colour = libtcod.Color(191,143,0)
        mblocks = True
        name = 'irate customer'
    elif mnum == MONSTER_GREEN_JELLY:
        fighter_component = Fighter(hp=16, defense=4, power=10, minpower=4, speed=100, 
                                    death_function=monster_death, mnum=MONSTER_GREEN_JELLY)
        ai_component = BasicMonster()
        symbol = 'J'
        colour = libtcod.Color(0,64,0)
        mblocks = True
        name = 'green jelly'
    elif mnum == MONSTER_ICE_SCREAM:
        fighter_component = Fighter(hp=20, defense=3, power=7, minpower=2, speed=100, 
                                    death_function=monster_death, mnum=MONSTER_ICE_SCREAM)
        ai_component = IceScreamMonster()
        symbol = 'i'
        colour = libtcod.Color(0,64,128)
        mblocks = True
        name = 'ice scream'
    elif mnum == MONSTER_HAGGIS:
        fighter_component = Fighter(hp=3, defense=1, power=10, minpower=4, speed=100, 
                                    death_function=monster_death, mnum=MONSTER_HAGGIS)
        ai_component = HaggisMonster()
        symbol = 'h'
        colour = libtcod.Color(128,0,0)
        mblocks = True
        name = 'haggis abomination'
    elif mnum == MONSTER_MEAT_BALLER:
        fighter_component = Fighter(hp=25, defense=1, power=14, minpower=6, speed=100, 
                                    death_function=monster_death, mnum=MONSTER_MEAT_BALLER)
        ai_component = BasicMonster()
        symbol = 'b'
        colour = libtcod.Color(128,0,0)
        mblocks = True
        name = 'meat baller'
    elif mnum == MONSTER_CHEESE_ROLLER:
        fighter_component = Fighter(hp=15, defense=4, power=10, minpower=1, speed=90, 
                                    death_function=monster_death, mnum=MONSTER_CHEESE_ROLLER)
        ai_component = CheeseRollerMonster()
        symbol = 'C'
        colour = libtcod.Color(128,128,0)
        mblocks = True
        name = 'cheese roller'
    elif mnum == MONSTER_GRUBBY_FORK:
        fighter_component = Fighter(hp=14, defense=3, power=10, minpower=5, speed=120, 
                                    death_function=monster_death, mnum=MONSTER_GRUBBY_FORK)
        ai_component = ForkMonster()
        symbol = 'F'
        colour = libtcod.Color(208,208,208)
        mblocks = True
        name = 'grubby fork'
    elif mnum == MONSTER_VENDING_MACHINE:
        fighter_component = Fighter(hp=50, defense=1, power=1, minpower=0, speed=50, 
                                    death_function=monster_death, mnum=MONSTER_VENDING_MACHINE)
        ai_component = VendingMachineMonster()
        symbol = 'V'
        colour = libtcod.Color(64,0,128)
        mblocks = True
        name = 'vending machine'
    elif mnum == MONSTER_NOT_SO_SWEETIE:
        fighter_component = Fighter(hp=15, defense=1, power=15, minpower=5, speed=150, 
                                    death_function=monster_death, mnum=MONSTER_NOT_SO_SWEETIE)
        ai_component = BasicMonster()
        symbol = 's'
        colour = libtcod.Color(64,0,128)
        mblocks = True
        name = 'not-so-sweetie'
    elif mnum == MONSTER_HARD_CANDY:
        fighter_component = Fighter(hp=25, defense=15, power=18, minpower=10, speed=150, 
                                    death_function=monster_death, mnum=MONSTER_HARD_CANDY)
        ai_component = BasicMonster()
        symbol = 'C'
        colour = libtcod.Color(64,0,128)
        mblocks = True
        name = 'hard candy'
    elif mnum == MONSTER_UNION_ONION:
        fighter_component = Fighter(hp=30, defense=5, power=26, minpower=15, speed=150, 
                                    death_function=monster_death, mnum=MONSTER_UNION_ONION)
        ai_component = OnionMonster()
        symbol = 'O'
        colour = libtcod.Color(185,115,255)
        mblocks = True
        name = 'union onion'
    elif mnum == MONSTER_RED_JELLY:
        fighter_component = Fighter(hp=40, defense=14, power=30, minpower=20, speed=150, 
                                    death_function=monster_death, mnum=MONSTER_RED_JELLY)
        ai_component = BasicMonster()
        symbol = 'J'
        colour = libtcod.Color(255,100,100)
        mblocks = True
        name = 'red jelly'
    elif mnum == MONSTER_TALKATIVE_PEPPER:
        fighter_component = Fighter(hp=40, defense=15, power=40, minpower=10, speed=100, 
                                    death_function=monster_death, mnum=MONSTER_TALKATIVE_PEPPER)
        ai_component = PepperMonster()
        symbol = 'P'
        colour = libtcod.Color(255,100,100)
        mblocks = True
        name = 'talkative pepper'
    elif mnum == MONSTER_THE_CRITIC:
        fighter_component = Fighter(hp=200, defense=20, power=40, minpower=30, speed=50, 
                                    death_function=monster_death, mnum=MONSTER_THE_CRITIC)
        ai_component = CriticMonster()
        symbol = 'X'
        colour = libtcod.Color(255,0,0)
        mblocks = True
        name = 'the Critic'
    #then create him!
    #note: the other end sorts out x/y coords
    monster = Object(0,0, symbol, name, colour, blocks=mblocks,
                     fighter=fighter_component, ai=ai_component)
    return monster

def createhat(floor):
    item_component = Item(use_function=wear_hat)
    if floor == 1:
        hatcol = libtcod.Color(255,255,255)
        hatshort = 'cap'
        hatlong =  'A Dunce Cap'
    if floor == 2:
        hatcol = libtcod.Color(255,255,255)
        hatshort = 'cap'
        hatlong =  'A White Cap'
    if floor == 3:
        hatcol = libtcod.Color(223,223,223)
        hatshort = "milkman's hat"
        hatlong =  "A Milkman's Hat"
    if floor == 4:
        hatcol = libtcod.Color(188,166,255)
        hatshort = 'hairnet'
        hatlong =  'Kitchen Hairnet'
    if floor == 5:
        hatcol = libtcod.Color(255,100,100)
        hatshort = 'cap'
        hatlong =  'Red Baseball Cap'
    if floor == 6:
        hatcol = libtcod.Color(100,255,100)
        hatshort = 'skullcap'
        hatlong =  'A Green Skullcap'
    if floor == 7:
        hatcol = libtcod.Color(150,150,150)
        hatshort = 'chef hat'
        hatlong =  "Deflated Chef's Hat"
    if floor == 8:
        hatcol = libtcod.Color(255,255,255)
        hatshort = 'trilby'
        hatlong =  'Battle-Trilby'
    if floor == 9:
        hatcol = libtcod.Color(200,200,200)
        hatshort = 'chef hat'
        hatlong =  "Chef's Hat"
    if floor == 10:
        hatcol = libtcod.Color(255,255,255)
        hatshort = 'chef hat'
        hatlong =  "Tall Chef Hat"
    if floor == 666:
        hatcol = libtcod.Color(229,191,0)
        hatshort = 'awesome chef hat'
        hatlong =  "Grand Poofy Chef Hat"
        level = 11
    else:
        level = floor
    item = Object(0, 0, '=', hatshort, libtcod.violet, item=item_component)
    item.long = hatlong
    item.col = hatcol
    item.lvl = level
    item.foundon = floor
    return item
    
    
def createspatula(floor):
    item_component = Item(use_function=wield_spatula)
    if floor == 1:
        hatcol = libtcod.Color(233,255,126)
        hatshort = 'spatula'
        hatlong =  'Cheap Plastic Spatula'   
    if floor == 2:
        hatcol = libtcod.Color(255,127,0)
        hatshort = 'spatula'
        hatlong =  'Brown Plastic Spatula' 
    if floor == 3:
        hatcol = libtcod.Color(255,255,255)
        hatshort = 'spatula'
        hatlong =  'Shiny Metal Spatula' 
    if floor == 4:
        hatcol = libtcod.Color(255,149,115)
        hatshort = 'rolling pin'
        hatlong =  'Rolling Pin' 
    if floor == 5:
        hatcol = libtcod.Color(166,255,166)
        hatshort = 'knife'
        hatlong =  'Vegetable Knife' 
    if floor == 6:
        hatcol = libtcod.Color(255,255,115)
        hatshort = 'cheese grater'
        hatlong =  'Cheese Grater' 
    if floor == 7:
        hatcol = libtcod.Color(166,210,255)
        hatshort = 'meat cleaver'
        hatlong =  'Meat Cleaver' 
    if floor == 8:
        hatcol = libtcod.Color(111,64,128)
        hatshort = 'battle-wok'
        hatlong =  'Battle-wok' 
    if floor == 9:
        hatcol = libtcod.Color(140,140,140)
        hatshort = 'hammer'
        hatlong =  'Steel Meat Tenderiser' 
    if floor == 10:
        hatcol = libtcod.Color(203,203,203)
        hatshort = 'spatula'
        hatlong =  'Platinum Spatula' 
    if floor == 666:
        hatcol = libtcod.Color(229,191,0)
        hatshort = 'spatulus'
        hatlong =  'Diamond-Encrusted Spatulus' 
        level = 11
    else:
        level = floor
    item = Object(0, 0, '+', hatshort, libtcod.violet, item=item_component)
    item.long = hatlong
    item.col = hatcol
    item.lvl = level
    return item
    
def wield_spatula(item):
    weapon = Weapon(item.name, item.long, item.col, item.lvl)
    try:
        tempitem = player.fighter.weapon.invitem
        weapon.invitem = item
        weapon.wear()
        inventory.remove(item)
        inventory.append(tempitem)
    except:
        weapon.invitem = item
        weapon.wear()
        inventory.remove(item)
    
def wear_hat(item):
    hat = Hat(item.name, item.long, item.col, level=item.lvl)
    try:
        tempitem = player.fighter.hat.invitem
        hat.invitem = item
        hat.wear()
        inventory.remove(item)
        inventory.append(tempitem)
    except:
        hat.invitem = item
        hat.wear()
        inventory.remove(item)

def choosemonster():
    global floor
    #choose a monster for that particular floor and places it there
    #this allows for different rarities!
    choice = libtcod.random_get_int(0, 0, 100)
    if floor == 1:
        #gingerbreadman = 60
        #bat = 40
        if choice < 40:
            return createmonster(MONSTER_BATTERFLY)
        else:
            return createmonster(MONSTER_GINGERBREADMAN)
    if floor == 2:
        if choice < 20:
            return createmonster(MONSTER_BROCCOLLI)
        elif choice < 20+40:
            return createmonster(MONSTER_BATTERFLY)
        else:
            return createmonster(MONSTER_GINGERBREADMAN)
        #gingerbreadman=40
        #bat=40
        #broccolli=20
    if floor == 3:
        #broccolli= 35
        #gingerbreadman=20
        #bat=25
        #peashooter=30
        if choice < 25:
            return createmonster(MONSTER_BATTERFLY)
        elif choice < 25+30:
            return createmonster(MONSTER_PEA_SHOOTER)
        elif choice < 25+30+20:
            return createmonster(MONSTER_GINGERBREADMAN)
        else:
            return createmonster(MONSTER_BROCCOLLI)
    if floor == 4:
        #broccolli=35
        #peashooter=35
        #customer=30
        if choice < 30:
            return createmonster(MONSTER_CUSTOMER)
        elif choice < 30+35:
            return createmonster(MONSTER_PEA_SHOOTER)
        else:
            return createmonster(MONSTER_BROCCOLLI)
    if floor == 5:
        #greenjelly=10
        #customer=50
        #peashooter=20
        #icescream=20
        if choice < 20:
            return createmonster(MONSTER_ICE_SCREAM)
        elif choice < 20+20:
            return createmonster(MONSTER_PEA_SHOOTER)
        elif choice < 20+20+50:
            return createmonster(MONSTER_CUSTOMER)
        else:
            return createmonster(MONSTER_GREEN_JELLY)
    if floor == 6:
        #icescream=30
        #greenjelly=20
        #customer=30
        #haggis=20
        if choice < 20:
            return createmonster(MONSTER_HAGGIS)
        elif choice < 20+30:
            return createmonster(MONSTER_CUSTOMER)
        elif choice < 20+30+20:
            return createmonster(MONSTER_GREEN_JELLY)
        else:
            return createmonster(MONSTER_ICE_SCREAM)
    if floor == 7:
        #meatballer=40
        #greenjelly=20
        #fork=10
        #haggis=20
        #pepper=10
        if choice < 10:
            return createmonster(MONSTER_TALKATIVE_PEPPER)
        elif choice < 10+20:
            return createmonster(MONSTER_HAGGIS)
        elif choice < 10+20+10:
            return createmonster(MONSTER_GRUBBY_FORK)
        elif choice < 10+20+10+20:
            return createmonster(MONSTER_GREEN_JELLY)
        else:
            return createmonster(MONSTER_MEAT_BALLER)
    if floor == 8:
        #meatballer=35
        #roller=30
        #fork=20
        #pepper=15
        #vending=10
        if choice < 10:
            return createmonster(MONSTER_VENDING_MACHINE)
        elif choice < 10+15:
            return createmonster(MONSTER_TALKATIVE_PEPPER)
        elif choice < 10+15+20:
            return createmonster(MONSTER_GRUBBY_FORK)
        elif choice < 10+15+20+30:
            return createmonster(MONSTER_CHEESE_ROLLER)
        else:
            return createmonster(MONSTER_MEAT_BALLER)
    if floor == 9:
        #candy=20
        #roller=20
        #fork=20
        #vending=20
        #pepper=20
        if choice < 20:
            return createmonster(MONSTER_TALKATIVE_PEPPER)
        elif choice < 20+20:
            return createmonster(MONSTER_VENDING_MACHINE)
        elif choice < 20+20+20:
            return createmonster(MONSTER_GRUBBY_FORK)
        elif choice < 20+20+20+20:
            return createmonster(MONSTER_CHEESE_ROLLER)
        else:
            return createmonster(MONSTER_HARD_CANDY)
    if floor == 10:
        #onion=20
        #candy=20
        #vending=20
        #redjelly=20
        #cheese=20
        if choice < 20:
            return createmonster(MONSTER_CHEESE_ROLLER)
        elif choice < 20+20:
            return createmonster(MONSTER_RED_JELLY)
        elif choice < 20+20+20:
            return createmonster(MONSTER_VENDING_MACHINE)
        elif choice < 20+20+20+20:
            return createmonster(MONSTER_HARD_CANDY)
        else:
            return createmonster(MONSTER_UNION_ONION)
    if floor == 666:
        #onion=25
        #candy=25
        #roller=25
        #redjelly=25
        if choice < 25:
            return createmonster(MONSTER_RED_JELLY)
        elif choice < 25+25:
            return createmonster(MONSTER_CHEESE_ROLLER)
        elif choice < 25+25+25:
            return createmonster(MONSTER_HARD_CANDY)
        else:
            return createmonster(MONSTER_UNION_ONION)

def cast_spell():
    choice = recipe_menu()
    if choice != None:
        if known_recipes[choice].cast() == True:
            player_action()
            
def cast_testrecipe():
    #find closest enemy (inside a maximum range) and damage it
    monster = closest_monster(10)
    if monster is None:  #no enemy found within maximum range
        message('No enemy is close enough to strike.', libtcod.Color(255,0,0))
        return False
 
    #zap it!
    message('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
        + str(5) + ' hit points.', libtcod.Color(115,115,255))
    monster.fighter.take_damage(5)
    return True
 
def cast_entangling_noodles():
    #ask the player for a target to confuse
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster is None: return False
    #replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    old_ai = monster.ai
    monster.ai = EntangledMonster(old_ai, libtcod.random_get_int(0,3,6))
    monster.ai.owner = monster  #tell the new component who owns it
    message('You whip up a big batch of noodles and throw them at ' + monster.name + '! They knot tightly around it, binding it in place!', libtcod.Color(115,255,115))
    return True
    
def cast_hot_sauce():
    #target:self
    hotsaucebuff = Hot_Sauce_Buff(10, 100)
    hotsaucebuff.apply_debuff(player)
    return True
    
def cast_shortbread_throwing_stars():
    #target: all possible targets in range
    starsleft = 5
    targetsleft = True
    if target_random_monster == None:
        message('There are no targets to hit!')
        return False
    else:
        message('You whip up a tasty batch of deadly shortbread throwing stars, and start flinging them at random!', libtcod.Color(115,255,115))
        while starsleft > 0 and targetsleft == True:
            monster = target_random_monster()
            if monster == None:
                targetsleft = False
                message('Running out of targets, you eat the rest of the throwing stars. Mmm, pointy!')
                player.fighter.heal(starsleft * 3)
            else:
                #throw a star at that monster
                message('You throw a star at ' + monster.name + '!', libtcod.Color(255,255,255))
                monster.fighter.take_damage(5)
                starsleft -= 1
        return True

def cast_extra_thick_gravy():
    #target:self
    gravybuff = Extra_Thick_Gravy_Buff(10, 100)
    gravybuff.apply_debuff(player)
    return True
    
def cast_chocolate_fondue_volcano():
    #target: self
    fonduebuff = Chocolate_Fondue_Buff(10, 30)
    fonduebuff.apply_debuff(player)
    return True

def cast_chicken_jalfreezy():
    #target: all in area
    victims = target_all_in_area()
    if len(victims) == 0:
        message("There's no-one here that would be affected!", libtcod.Color(159,159,159))
        return False
    else:
        message('You start to create a chicken jalfrezi, but change the recipe at the end to a chicken jal FREEZIE!', libtcod.Color(115,115,255))
        for object in victims:
            chilldebuff = Chill_Debuff(30, 6)
            chilldebuff.apply_debuff(object)
            object.fighter.take_damage(5)
        return True
    
def cast_ice_cubes():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('Your ice cubes hit ' + monster.name + ', chilling them.', libtcod.Color(115,115,255))
        chilldebuff = Chill_Debuff(75, 6)
        chilldebuff.apply_debuff(monster)
        monster.fighter.take_damage(5)
        return True
     
def cast_egg_custard_tart():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        custardtartdebuff = Egg_Custard_Tart_Debuff(6, 10)
        custardtartdebuff.apply_debuff(monster)
        monster.fighter.take_damage(3)
        return True
    
def cast_smelly_parmesan():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        parmesandebuff = Smelly_Parmesan_Debuff(20, 10)
        parmesandebuff.apply_debuff(monster)
        return True
    
def cast_chocolate_swan():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        chocolateswandebuff = Chocolate_Swan_Debuff(20, 10)
        chocolateswandebuff.apply_debuff(monster)
        return True
    
def cast_hundreds_and_thousands():
    #target: closest monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        #replace the monster's AI with a "confused" one; after some turns it will restore the old AI
        old_ai = monster.ai
        monster.ai = ConfusedMonster(old_ai, 5)
        monster.ai.owner = monster  #tell the new component who owns it
        return True
      
def cast_rhubarb_sauce():
    #target:self
    rhubarbbuff = Rhubarb_Sauce_Buff(10, 100)
    rhubarbbuff.apply_debuff(player)
    return True
      
def cast_runner_beans():
    #target:self
    runnerbuff = Runner_Beans_Buff(100, 100)
    runnerbuff.apply_debuff(player)
    return True
    
def cast_frozen_pizza():
    #target: single monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('Mama mia! Your frozen-a pizza hits ' + monster.name + ' right in the eye-a!', libtcod.Color(115,115,255))
        chilldebuff = Chill_Debuff(30, 8)
        chilldebuff.apply_debuff(monster)
        monster.fighter.take_damage(20)
        return True
    
def cast_spinach():
    #target: self
    spinachbuff = Spinach_Buff(100, 100)
    spinachbuff.apply_debuff(player)
    return True
    
def cast_spongecake():
    #target: monster
    #deals damage and gives to you as health
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('Your spongecake absorbs some of the tastiness from ' + monster.name + ' and gives it to you.', libtcod.Color(115,115,255))
        monster.fighter.take_damage(15)
        player.fighter.heal(15)
        return True

def cast_chop_suey():
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('Your chop suey chops into ' + monster.name + ' three times, for spicy justice!', libtcod.Color(255,115,115))
        for i in range(0,3):
            if monster.fighter != None:
                monster.fighter.take_damage(5)
        return True
    
def cast_toad_in_the_hole():
    monster = target_random_monster()
    if monster == None:
        message('There are no targets nearby to hit!')
        return False
    else:
        message("You yell 'Toad in the hooole!', and wait for the sounds of booming and ribbits.")
        message(monster.name.capitalize() + ' was hit by a giant toad! Totally worth it!', libtcod.Color(255,0,0))
        monster.fighter.take_damage(50)
        return True
 
 
def cast_chicken_tikka():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('You make a delicious chicken tikka and give it to ' + monster.name + '.', libtcod.Color(255,115,115))
        message('A chicken tikka with a BOMB INSIDE! AHAHAHA-', libtcod.Color(255,0,0))
        monster.fighter.take_damage(35)
        return True

    
def cast_sausage_roll():
    #target: line tile
    message('Left-click a tile to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    dx,dy = target_tile()
    if dx == None: 
        return False
    message('You wind up your bowling arm and roll a sausage!', libtcod.Color(255,115,115))
    if libtcod.random_get_int(0,0,100) > 50:
        message("(There isn't really much 'cooking' in this game, is there?)")
    path = libtcod.path_new_using_map(fov_map, 1.0)
    libtcod.path_compute(path, player.x, player.y, dx, dy)
    for i in range(0, libtcod.path_size(path)):
        tx, ty = libtcod.path_get(path, i)
        for object in objects:
            if object.fighter and object.x == tx and object.y == ty:
                message(object.name.capitalize() + ' is hit by the sausage roll!', libtcod.Color(255,115,115))
                damage = libtcod.random_get_int(0,5, 11)
                object.fighter.take_damage(damage)
    libtcod.path_delete(path)
    return True
    
def cast_chocolate_log():
    #target: line tile
    #target: line tile
    message('Left-click a tile to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    dx,dy = target_tile()
    if dx == None: 
        return False
    message('You wind up your bowling arm and roll an impressive chocolate log!', libtcod.Color(255,115,115))
    path = libtcod.path_new_using_map(fov_map, 1.0)
    libtcod.path_compute(path, player.x, player.y, dx, dy)
    for i in range(0, libtcod.path_size(path)):
        tx, ty = libtcod.path_get(path, i)
        for object in objects:
            if object.fighter and object.x == tx and object.y == ty:
                message(object.name.capitalize() + ' is hit by the chocolate log!', libtcod.Color(255,115,115))
                damage = libtcod.random_get_int(0,20, 51)
                object.fighter.take_damage(damage)
    libtcod.path_delete(path)
    
def cast_mince_meat():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('You make mince meat out of ' + monster.name + '!', libtcod.Color(255,115,115))
        if libtcod.random_get_int(0,0,100) > 50:
            message('(...get it? mince meat?)', libtcod.Color(255,115,115))
        monster.fighter.take_damage(15)
        return True

    
def cast_treacle_tart():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('You hurl a sticky treacle tart at ' + monster.name + ', making them all sticky.', libtcod.Color(115,115,255))
        chilldebuff = Chill_Debuff(30, 6)
        chilldebuff.apply_debuff(monster)
        monster.fighter.take_damage(15)
        return True
    
def cast_jalapeno_peppers():
    #target: monster
    message('Left-click an enemy to target it, or right-click to cancel.', libtcod.Color(115,255,255))
    monster = target_monster()
    if monster == None:
        message('No monster selected.')
        return False
    else:
        message('None can withstand the raw power of the jalapeno pepper! Not even you, ' + monster.name + '!', libtcod.Color(255,0,0))
        pepperdebuff = Jalapeno_Peppers_Debuff(10, 10)
        pepperdebuff.apply_debuff(monster)
        message(monster.name.capitalize() + ' is set on fire by the sheer hotness!', libtcod.Color(255,0,0))
        monster.fighter.take_damage(100)
        return True

def cast_banana_split():
    #target:self
    message('You eat the banana split. Tasty and refreshing, throughout the day!', libtcod.Color(115,255,115))
    buff = Heal_Over_Time_Buff(1, 40)
    buff.apply_debuff(player)
    return True
    
def cast_vanilla_icecream():
    #target:self
    message('You eat the vanilla icecream. Frosty! You feel a bit better.', libtcod.Color(115,115,255))
    player.fighter.heal(10)
    return True
    
def cast_strawberry_icecream():
    #target:self
    message('You eat the strawberry icecream. Fruity! You feel better.', libtcod.Color(115,115,255))
    player.fighter.heal(20)
    return True
    
def cast_chocolate_icecream():
    #target:self
    message('You eat the chocolate icecream. TASTY! You feel much better.', libtcod.Color(115,115,255))
    player.fighter.heal(50)
    return True

def cast_knickerbocker_glory():
    #target:self
    message('You eat the knickerbocker glory. If heaven was a place, it would be your mouth right now.', libtcod.Color(115,115,255))
    player.fighter.heal(100)
    buff = Heal_Over_Time_Buff(10, 15)
    buff.apply_debuff(player)
    return True

def cast_messy_bolognese_splash():
    #target: aoe tile
    dx, dy = target_tile()
    if dx == None:
        return False
    else:
        message('You hurl a messy italian meal straight upwards, and cross your fingers.', libtcod.Color(255,115,115))
        for object in objects:
            if object.distance(dx, dy) <= 2 and object.fighter:
                message(object.name.capitalize() + ' is covered in bolognese!', libtcod.Color(255,115,115))
                object.fighter.take_damage(10)
        return True
 
 
 
def closest_monster(max_range):
    #find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range
 
    for object in objects:
        if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
            #calculate distance between this object and the player
            dist = player.distance_to(object)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = object
                closest_dist = dist
    return closest_enemy

def target_tile(max_range=None):
    #return the position of a tile left-clicked in player's FOV (optionally in a range), or (None,None) if right-clicked.
    while True:
        #render the screen. this erases the inventory and shows the names of objects under the mouse.
        render_all()
        libtcod.console_flush()
 
        key = libtcod.console_check_for_keypress()
        mouse = libtcod.mouse_get_status()  #get mouse position and click status
        (x, y) = (mouse.cx, mouse.cy)
 
        if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and
            (max_range is None or player.distance(x, y) <= max_range)):
            return (x, y)
        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return (None, None)  #cancel if the player right-clicked or pressed Escape
    
def target_monster(max_range=None):
    #returns a clicked monster inside FOV up to a range, or None if right-clicked
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  #player cancelled
            return None
 
        #return the first clicked monster, otherwise continue looping
        for obj in objects:
            if obj.x == x and obj.y == y and obj.fighter and obj != player:
                return obj


def target_random_monster(max_range=None):
    #chooses a random monster in player's FOV
    #never using a max range, hater's gon hate
    enemies = []
    for object in objects:
        if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
            enemies.append(object)
    if len(enemies) == 0:
        return None
    else:
        return enemies[libtcod.random_get_int(0, 0, len(enemies) - 1)]
     
def target_all_in_area(max_range=None):
    #dunno why i'm even including a max range
    #FIGHT DA POWAH
    victims = []
    for object in objects:
        if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
            victims.append(object)
    return victims
    
    
def add_ingredients(ing):
    #for adding bulk ingredients at once
    global ingredients, ingredients_earned
    for x in range(0, len(ing)):
        for y in range(0, len(ingredients)):
            if ing[x][0] == ingredients[y][0]:
                ingredients_earned += ing[x][1]
                total = ingredients[y][2] + ing[x][1]
                newtuple = ingredients[y][0], ingredients[y][1], total, ingredients[y][3]
                del ingredients[y]
                ingredients.append(newtuple)
                break
    
def get_dark_wall():
    global floor
    if floor >= 1 and floor <= 3:
        return libtcod.Color(75, 75, 50)
    if floor >= 4 and floor <= 6:
        return libtcod.Color(0, 0, 100)
    if floor >= 7 and floor <= 9:
        return libtcod.Color(75, 75, 75)
    if floor == 10:
        return libtcod.Color(90, 70, 40)
    if floor == 666:
        return libtcod.Color(125, 20, 20)
   

def get_light_wall():
    global floor
    if floor >= 1 and floor <= 3:
        return libtcod.Color(150, 150, 100)
    if floor >= 4 and floor <= 6:
        return libtcod.Color(50, 110, 130)
    if floor >= 7 and floor <= 9:
        return libtcod.Color(150, 150, 150)
    if floor == 10:
        return libtcod.Color(130, 110, 80)
    if floor == 666:
        return libtcod.Color(250,40,40)
   
   
   
def get_dark_ground():
    global floor
    if floor >= 1 and floor <= 3:
        return libtcod.Color(50, 50, 40)
    if floor >= 4 and floor <= 6:
        return libtcod.Color(50, 50, 150)
    if floor >= 7 and floor <= 9:
        return libtcod.Color(50, 50, 50)
    if floor == 10:
        return libtcod.Color(100, 90, 25)
    if floor == 666:
        return libtcod.Color(100, 75, 75)
   
def get_light_ground():
    global floor
    if floor >= 1 and floor <= 3:
        return libtcod.Color(100, 100, 80)
    if floor >= 4 and floor <= 6:
        return libtcod.Color(50, 180, 200)
    if floor >= 7 and floor <= 9:
        return libtcod.Color(100, 100, 100)
    if floor == 10:
        return libtcod.Color(200, 180, 50)
    if floor == 666:
        return libtcod.Color(200, 150, 150)
   

    
    
###########################
#INITIALISATION
###########################
libtcod.console_set_custom_font(FONT_PATH, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Kitchen Master', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
bottompanel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
sidepanel = libtcod.console_new(SIDEPANEL_WIDTH, MAP_HEIGHT)
logging.basicConfig(level=logging.DEBUG, filename='errorlog.log')
logging.basicConfig(level=logging.ERROR, filename='errorlog.log')
try:
    main_menu()
except:
    try:
        msgbox('Argh, there was an error! Please send the errorlog.log file to me at zarquonmk2@gmail.com!')
        #try:
        #    #save_game()
        #except:
        #    pass
    except:
        pass
    logging.exception("Oops:")
