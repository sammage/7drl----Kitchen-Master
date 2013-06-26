***
ATTENTION: the game runs of python 2.7.2 32 BIT!
You can get this at
http://www.python.org/getit/releases/2.7/ 
http://www.python.org/ftp/python/2.7/python-2.7.msi
This needs to be installed for the game to run, then run 'kitchenmaster.py'!
***


KITCHENMASTER:

Kitchenmaster is a roguelike, a randomly generated dungeon full of terrible, food-based monsters! You have to battle through the floors of the dungeon and finally slay the boss, the terrible Critic! Be careful - in this game, death is permanent, so you must use all of your wits and cooking skills to get you out of tight spots. 

-Is a monster just too powerful to deal with? Quickly cook some noodles to entangle them with!
-Lots of monsters closing in? Bake some shortbread throwing stars!
-Feel like your spatula isn't doing enough damage? Pour some hot sauce on that sucker!

Destroying enemies gives you essential ingredients to cook your delicious recipes. It's a limited resource, so choose what you make with care, and try to use a healthy balance of all the ingredients for maximum chance of survival!


This game was made for the 7DRL competition 2012. In the 7DRL you have to make a roguelike in just 7 seven days - so if you find any bugs, that's what's to blame, honest! It was made by Sammage. His favorite animal is cats and his favorite colour is 'also cats'. 

The game runs on python, and uses the libtcod library by Doryen. The base of the game was a libtcod roguelike tutorial written by Jotaf.

If you have any bugs or suggestions for improvements, email them to zarquonmk2@gmail.com!

KEYS
----

The game supports both Vi keys and Numpad keys

Vi keys:

y k u
 \|/
h-.-l
 /|\
b j n

Numpad keys:

7 8 9
 \|/
4-5-6
 /|\
1 2 3

ADDITIONAL KEYS
---------------
Picking up items: 'g' or ',' or numpad 0
Inventory: 'i'
Drop item: 'd'
Recipe menu: 'z'
Ascend/descend stairs: '>' or '<'
Review Messages: 'm'
Character stats: 'c'
Toggle fullscreen: alt + enter
This help menu: '?' or '/'








BUG I HAVE NO IDEA HOW TO FIX:
if you close the game with the cross at the top, YOUR GAME WILL NOT BE SAVED!
Be wary of closing the game like that!













SOME OFFICIAL CHANGELOGLIKE
---------------------------


----------
Day6
--------
-Added all recipes, and recipe descriptions
-Added all hats and spatulas(hereby known as sphatulas)

STUFF I WANT TO DO TOMORROW
---------------------------
everything else

-------------
Day5
--------

ADDED
-----
-all functionality (but not balance/drops) for monsters barring the end boss
(the talking pepper is the only one with any real personality unfortunately)
(lots untested, will very likely crash on the higher levels)
-hats and spatulas droplist and wearability, but lacking description
-all recipes, sans functionality, cost and description >.>

CHANGED
------
-really simplified the ingredients list, it should be a lot more manageable now!
 now there are 4 basic ingredients and 2 advanced ingredients


REMOVED
-------
-saying goodbye to the idea of a friendly pasta monster, it would require
cleaner combat code


STUFF I WANT TO DO TOMORROW
---------------------------

You know what, i'm gonna just save the colour scheme for the last day
tomorrow i want to add functionality for every spell. if I don't, i will be
BEHIND SCHEDULE.
then either start working on descriptions, balance or the end boss, though
that will probably all be final day stuff
------------
Day4
----------

ADDED
-----
-A special handmade dungeon for the last zone
-all the monsters(special abilities, ais, deaths and drops not coded yet)
-monster levelled list

CHANGED
-------
replaced the basic ai with a good one that can actually pathfind
combat system is now a lot more random(it's also retarded, but who cares)
the font is larger
walking into walls no longer takes a turn
stairs can no longer spawn on top of other stairs

REMOVED
-------
grand schemes of hats and spatulas have shrunk down to a very simple thing


STUFF I WANT TO DO TOMORROW
---------------------------
THE COLOUR SCHEME LOLOLOL
design doc - recipes
add all the recipes without functionality
add in the functionality for monsters
put spatulas and chefhats in droplists
rare drops of recipes, and recipes from levelling

------------
Day3
-----------

ADDED
-----
message log (the m key)
recipe framework
crappy testrecipe to test recipe framework
help menu (the ? key)
recipe menu (the z key)
character stats(the c key)

STUFF I WANT TO DO TOMORROW
---------------------------
-levelled lists and colour schemes, you've heard it all before
but this time i've actually start a design doc!
-picking up new weapons and hats
-finish design doc
-combat system revamp
-sTART ADDING CONTENT OH GOD


-------------
Day2
---------

ADDED
-----
saving and loading
weapons and !!hats!!
framework for ingredients
a really crappy test monster and ai, who drops ingredients on death
levelling(numbers to be tweeked when i look at combat stuff)


CHANGED
-------
tweaked the gui some
changed how ingredients are stored
changed how turns are processed, now every unit has a 'speed' that determines when they get their turns
that allows for fast and slow monsters and speed/slow buffs!

FIXED
-----
Small menu bug, game refusing to quit

REMOVED
-------
Screw doing a highscores page, the save/load page shows when a character is *DEAD* and it makes a nice morgue list for a 7 day game

STUFF I WANT TO DO TOMORROW
---------------------------
-levelled lists
-colour scheme, for real this time
-recipe list, and a tester recipe
-recipe description folder for the recipe list
-picking up new weapons and hats
-'character' menu, detailing some interesting stats
-'help' menu (though that might be tough, might be extremely basic!)
-dungeon levelled list?
everything after that will be PURE CONTENT BABY oh god

-------------
Day1
---------

ADDED
-----
-Gui
-Multiple dungeon floors
-Menu
-Ingredients
-Player name/experience/level
-Title string and floor string for cool titles and unique dungeons
(for unique dungeons i still need to add unique tile colouring for each floor)

STUFF I WANT TO DO TOMORROW
---------------------------

Make a test monster with cruddy ai
Figure out the colour scheme
Get saving and loading working based on player names
??Highscores?? based on exp (if i have time, going out tomorrow)