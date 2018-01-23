"""
Lemon Kingdom Quest: The Sorceror Arises
- Developed by: The Citrus Project
- Story: Nakamura Daiki, Yukimura Nobuko
- Main Programmer: Ethan Fyre of NaetherTech
- Citrish and Pholeth: Karl Schneider, Nikita Chekhov
- Sprite Design: Nikita Chekhov,  Kobayashi Koji
- Concept Art: N/A
- Game Testing: Gregor Mikhailova
- Music: Frank Lawson, Kobayashi Koji
- NPC Text: Almyra Nayelie, Daniel Hunter
- Special Thanks: James Jamison
"""
import os.path

import pygame
from pygame.locals import *
from pytmx import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

import time as tm
from random import randint
from math import sqrt,pow,fabs


# define configuration variables here
RESOURCES_DIR = 'data'

WIN_WIDTH = 800
WIN_HEIGHT = 600
#            R    G    B
BLACK  = (   0,   0,   0)      #self explanatory: RGB for black
WHITE  = ( 255, 255, 255)      #self explanatory: RGB for white
BLUE   = (   0,   0, 255)      #self explanatory: RGB for blue
GREEN  = (   0, 255,   0)      #self explanatory: RGB for green
RED    = ( 255,   0,   0)      #self explanatory: RGB for red
PURPLE = ( 255,   0, 255)      #self explanatory: RGB for purple
AQUA   = (   0, 255, 255)      #self explanatory: RGB for aqua  
YELLOW = ( 255, 255,   0)      #self explanatory: RGB for yellow


# ------------------------------------ FUNCTIONS ------------------------------------------------------------------
def texx(text,x,y,screen,color,font):
    myfont = pygame.font.SysFont("timesnewroman", font)
    myfont.set_bold(True)
    label = myfont.render(text, 1, color)
    screen.blit(label, (x,y))
def damaged(attacker, defender, move):
    weapon = attacker.weapon
    armour = defender.armour
    speed_dif_A = attacker.stats['speed']/defender.stats['speed']
    speed_dif_D = defender.stats['speed']/attacker.stats['speed']
    evasion =  1
    if (randint(0, 100) < (speed_dif_D*(5+(defender.stats['luck']/10)))):
        evasion = 0
    crit = 1
    if (randint(0, 100)<(5+(attacker.stats['luck']/10))):
        crit = 1.5
    double = 1
    if speed_dif_A > 2.5:
        double = 2
    modifier = (attacker.level/defender.level)*attacker.level*crit*evasion*double
    magical_damage = ((attacker.stats['magic'] )/(defender.stats['spirit']))*(weapon.stats['magic']/armour.stats['spirit']) * move[2] / 100
    physical_damage = ((attacker.stats['power'] )/(defender.stats['resiliance']))*(weapon.stats['power']/armour.stats['resiliance']) * move[1] / 100
    damage = (magical_damage + physical_damage)*modifier
    return (damage)
    
def display_money(screen,citrons):
    money = pygame.image.load("data/images/Citron.gif").convert()
    screen.blit(money, (715, 10))
    myfont = pygame.font.SysFont("iomanoid", 30)
    myfont.set_bold(False)
    label = myfont.render(citrons, 1, PURPLE)
    label2 = myfont.render(citrons, 1, BLACK)
    screen.blit(label2, (739, 4))
    screen.blit(label2, (739, 6))
    screen.blit(label2, (741, 4))
    screen.blit(label2, (741, 6))
    screen.blit(label, (740, 5))
          
def display_text(screen,w,h,text):
    pygame.draw.rect(screen, BLUE, (10, h - 90, w - 20, 80))
    pygame.draw.rect(screen, WHITE, (15, h - 85, w - 30, 70))
    myfont = pygame.font.SysFont("iomanoid", 15)
    myfont.set_bold(True)
    label = myfont.render(text, 1, BLACK)
    screen.blit(label, (20,h-80))
def battle_text(screen, text1, text2, text3, text4):
    pygame.draw.rect(screen, BLUE, (10, 400, 780, 190))
    pygame.draw.rect(screen, WHITE, (15, 405, 770, 180))
    myfont = pygame.font.SysFont("castellar", 25)
    myfont.set_bold(False)
    label1 = myfont.render(text1, 1, BLACK)
    label2 = myfont.render(text2, 1, BLACK)
    label3 = myfont.render(text3, 1, BLACK)
    label4 = myfont.render(text4, 1, BLACK)
    screen.blit(label1, (20,410))
    screen.blit(label2, (20,455))
    screen.blit(label3, (20,500))
    screen.blit(label4, (20,545))
def text_queue(text1, text2, text3, text4, d1, d2, d3, d4, text):
    if text1 == "":
        return text, text2, text3, text4, "", d2, d3, d4
    elif text2 == "":
        return text1, text, text3, text4, d1, "", d3, d4
    elif text3 == "":
        return text1, text2, text, text4, d1, d2, "", d4
    elif text4 == "":
        return text1, text2, text3, text, d1, d2, d3, ""
    else:
        return text1, text2, text3, text4, d1, d2, d3, d4

def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen

# make loading maps a little easier
def get_map(filename):
    return os.path.join(RESOURCES_DIR, filename)


# make loading images a little easier
def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))

#LOAD SPRITES FROM A FILE
def get_sprites(self, file, width, height, D, U, R, L):
    pygame.sprite.Sprite.__init__(self)
    sheet = SpriteSheet(file)
    image = sheet.pic(0,0,width,height)
    D.append(image)
    image = sheet.pic(0,height,width,height)
    D.append(image)
    image = sheet.pic(0,height*2,width,height)
    D.append(image)
    image = sheet.pic(0,height*3,width,height)
    D.append(image)

    image = sheet.pic(width*2,0,width,height)
    U.append(image)
    image = sheet.pic(width*2,height,width,height)
    U.append(image)
    image = sheet.pic(width*2,height*2,width,height)
    U.append(image)
    image = sheet.pic(width*2,height*3,width,height)
    U.append(image)

    image = sheet.pic(width*3,0,width,height)
    R.append(image)
    image = sheet.pic(width*3,height,width,height)
    R.append(image)
    image = sheet.pic(width*3,height*2,width,height)
    R.append(image)
    image = sheet.pic(width*3,height*3,width,height)
    R.append(image)
      
    image = sheet.pic(width,0,width,height)
    L.append(image)
    image = sheet.pic(width,height,width,height)
    L.append(image)
    image = sheet.pic(width,height*2,width,height)
    L.append(image)
    image = sheet.pic(width,height*3,width,height)
    L.append(image)

#----------------------------------------------------------CLASSES-----------------------------------------------------------------
class SpriteSheet(object):
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name)


    def pic(self, x, y, width, height):

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        image.set_colorkey(AQUA)

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Return the image
        return image
#class used to define a chest
class Chest(pygame.sprite.Sprite):
    contact = False
    items = []
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    def take_items(self,player):
        for i in self.items:
            if i[1] == "c":
                player.money += int(i[3:-1])
        self.items = []
        
#class used to define an npc
class NPC(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    Rwalkpics = []
    Lwalkpics = []
    Uwalkpics = []
    Dwalkpics = []
    
    text = ""
    above = False         #Is the player above the npc?
    below = False         #Is the player below the npc?
    left = False          #Is the player left of the npc?
    right = False         #Is the player right of the npc?
    speed = 2
    player = None
    direction = "down"

    def __init__(self,x,y,sheet,bl,br,bt,bb,width, height):
        get_sprites(self, sheet, width, height, self.Dwalkpics, self.Uwalkpics, self.Rwalkpics, self.Lwalkpics)       
        
        self.image = self.Dwalkpics[0]
        self.rect = self.image.get_bounding_rect()
        self.rect.y = y * 64
        self.old_y = y * 64
        self.rect.x = x * 64
        self.old_x = x * 64
        self.feet = pygame.Rect(0,0, self.rect.width, self.rect.height * .5)
        self.top_bound = bt * 64
        self.bottom_bound = bb * 64
        self.left_bound = bl * 64
        self.right_bound = br * 64
    def update(self,dist,time,text_displayed):
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        self.rect.x += self.change_x
        posh = self.rect.x
        self.rect.y += self.change_y
        posv = self.rect.y
        self.feet.midbottom = self.rect.midbottom
        if self.direction == "right":
            frame = (posh // dist) % len(self.Rwalkpics)
            self.image = self.Rwalkpics[int(frame)]
        elif self.direction == 'left':
            frame = (posh // dist) % len(self.Lwalkpics)
            self.image = self.Lwalkpics[int(frame)]
        elif self.direction == 'up':
            frame = (posv // dist) % len(self.Uwalkpics)
            self.image = self.Uwalkpics[int(frame)]
        elif self.direction == 'down':
            frame = (posv // dist) % len(self.Dwalkpics)
            self.image = self.Dwalkpics[int(frame)]

        if posh < self.left_bound or posh > self.right_bound:
            self.change_x *= -1
            if self.direction == "right":
                self.direction = "left"
            if self.direction == "left":
                self.direction = "right"
        if posv < self.top_bound or posv > self.bottom_bound:
            self.change_y *= -1
            if self.direction == "up":
                self.direction = "down"
            if self.direction == "down":
                self.direction = "up"
        if text_displayed == False:
            if time % 30 == 0 :
                ter = randint(0,5)
                if ter == 0:
                    self.change_x = 0
                    self.change_y = self.speed
                    self.direction = "down"
                elif ter == 1:
                    self.change_x = 0
                    self.change_y = -self.speed
                    self.direction = "up" 
                elif ter == 2:
                    self.change_x = self.speed
                    self.change_y = 0
                    self.direction = "right" 
                elif ter == 3:
                    self.change_x = -self.speed
                    self.change_y = 0
                    self.direction = "left" 
                elif ter >= 4:
                    if self.direction == "left":
                        self.image = self.Lwalkpics[0]
                    elif self.direction == "up":
                        self.image = self.Uwalkpics[0]
                    elif self.direction == "down":
                        self.image = self.Dwalkpics[0]
                    elif self.direction == "right":
                        self.image = self.Rwalkpics[0]
                    self.change_x = 0
                    self.change_y = 0
        elif text_displayed == True:
            self.change_x = 0
            self.change_y = 0
            if self.left == True:
                self.direction = "left" 
                self.image = self.Lwalkpics[0]
            if self.right == True:
                self.direction = "right" 
                self.image = self.Rwalkpics[0]
            if self.above == True:
                self.direction = "down" 
                self.image = self.Dwalkpics[0]
            if self.below == True:
                self.direction = "up" 
                self.image = self.Uwalkpics[0]
            self.left = False
            self.right = False
            self.above = False
            self.below = False
                        
    def move_back(self):
        self.rect.x = self.old_x
        self.rect.y = self.old_y
        self.feet.midbottom = self.rect.midbottom
        
class Enemy(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    Rwalkpics = []
    Lwalkpics = []
    Uwalkpics = []
    Dwalkpics = []
    speed = 2
    above = False         #Is the player above the enemy?
    below = False         #Is the player below the enemy?
    left = False          #Is the player left of the enemy?
    right = False         #Is the player right of the enemy?
    targeting = False     #Is the enemy currently targeting the player?
    target = True         #Will the enemy target the player?

    direction = "down"

    def __init__(self,x,y,sheet,bl,br,bt,bb,width, height, tg):
        get_sprites(self, sheet, width, height, self.Dwalkpics, self.Uwalkpics, self.Rwalkpics, self.Lwalkpics)
        self.image = self.Dwalkpics[0]
        self.rect = self.image.get_bounding_rect()
        self.rect.y = y * 64
        self.old_y = y * 64
        self.rect.x = x * 64
        self.old_x = x * 64
        self.feet = pygame.Rect(0,0, self.rect.width, self.rect.height * .5)
        self.top_bound = bt
        self.bottom_bound = bb
        self.left_bound = bl
        self.right_bound = br
        self.target_dist = tg
        self.group = []
    def update(self,dist,time,text_displayed,player):
        self.player = player
        self.dist_x = fabs(self.player.rect.x - self.rect.x)
        self.dist_y = fabs(self.player.rect.y - self.rect.y)
        if self.player.rect.y > self.rect.y:
            self.below = True
            self.above = False
        elif self.player.rect.y < self.rect.y:
            self.above = True
            self.below = False
        if self.player.rect.x > self.rect.x:
            self.right = True
            self.left = False
        elif self.player.rect.x < self.rect.x:
            self.left = True
            self.right = False
        if self.target == False:
            self.targetting = False
        elif sqrt((self.dist_x ** 2) + (self.dist_y ** 2)) < self.target_dist:
            self.targeting = True
        else:
            self.targeting = False
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        self.rect.x += self.change_x
        posh = self.rect.x
        self.rect.y += self.change_y
        posv = self.rect.y
        self.feet.midbottom = self.rect.midbottom
        if self.direction == "right":
            frame = (posh // dist) % len(self.Rwalkpics)
            self.image = self.Rwalkpics[int(frame)]
        elif self.direction == 'left':
            frame = (posh // dist) % len(self.Lwalkpics)
            self.image = self.Lwalkpics[int(frame)]
        elif self.direction == 'up':
            frame = (posv // dist) % len(self.Uwalkpics)
            self.image = self.Uwalkpics[int(frame)]
        elif self.direction == 'down':
            frame = (posv // dist) % len(self.Dwalkpics)
            self.image = self.Dwalkpics[int(frame)]

        if posh < self.left_bound or posh > self.right_bound:
            self.change_x *= -1
            if self.direction == "right":
                self.direction = "left"
            if self.direction == "left":
                self.direction = "right"
        if posv < self.top_bound or posv > self.bottom_bound:
            self.change_y *= -1
            if self.direction == "up":
                self.direction = "down"
            if self.direction == "down":
                self.direction = "up"
        if text_displayed == False:
            if self.targeting == False:
                if time % 30 == 0 :
                    ter = randint(0,5)
                    if ter == 0:
                        self.change_x = 0
                        self.change_y = self.speed
                        self.direction = "down"
                    elif ter == 1:
                        self.change_x = 0
                        self.change_y = -self.speed
                        self.direction = "up" 
                    elif ter == 2:
                        self.change_x = self.speed
                        self.change_y = 0
                        self.direction = "right" 
                    elif ter == 3:
                        self.change_x = -self.speed
                        self.change_y = 0
                        self.direction = "left" 
                    elif ter >= 4:
                        if self.direction == "left":
                            self.image = self.Lwalkpics[0]
                        elif self.direction == "up":
                            self.image = self.Uwalkpics[0]
                        elif self.direction == "down":
                            self.image = self.Dwalkpics[0]
                        elif self.direction == "right":
                            self.image = self.Rwalkpics[0]
                        self.change_x = 0
                        self.change_y = 0
            elif self.targeting == True:
                if self.dist_x > self.dist_y:
                    if self.right == True:
                        self.change_x = self.speed
                        self.direction = "right"
                    elif self.left == True:
                        self.change_x = -self.speed
                        self.direction = "left"
                    self.change_y = 0
                elif self.dist_x < self.dist_y:
                    if self.below == True:
                        self.change_y = self.speed
                        self.direction = "down"
                    elif self.above == True:
                        self.change_y = -self.speed
                        self.direction = "up"
                    self.change_x = 0
        elif text_displayed == True:
            self.change_x = 0
            self.change_y = 0
    def move_back(self):
        self.rect.x = self.old_x
        self.rect.y = self.old_y
        self.feet.midbottom = self.rect.midbottom
# ------------------------------------------------------------------------BATTLE CLASSES---------------------------------------------------
class Weapon(object):
    def __init__(self,  name, power, magic, power_bonus, magic_bonus, weight,  luck_bonus, hp_bonus):
        self.stats = {}           
        self.stats['power'] = power                            #0-200
        self.stats['magic'] = magic                            #0-200
        self.stats['weight'] = weight                         #0-50       
        self.stats['power_bonus'] = power_bonus     #0-20 
        self.stats['magic_bonus'] = magic_bonus     #0-20 
        self.stats['luck_bonus'] = luck_bonus          #0-20 
        self.stats['hp_bonus'] = hp_bonus                #0-5000  
class Glaive(Weapon):
    def __init__(self):
        Weapon.__init__(self, "Glaive",  60, 60, 0, 0, 0, 0, 0)
class Slayer(Weapon):
    def __init__(self):
        Weapon.__init__(self, "Slayer",  140, 20, 5, 0, 0,  0, 0)
        
class Armour(object):
    stats = {'resiliance': 1,'spirit': 1, 'resiliance_bonus': 0, 'spirit_bonus': 0, 'weight': 0, 'luck_bonus': 0, 'hp_bonus': 0}
    def __init__(self, name):
         self.name = name

class Ruby_vest(Armour):
    def __init__(self, resiliance, weight):
        Armour.__init__(self, "glaive")
        self.stats['resiliance'] = resiliance
        self.stats['weight'] = weight
        
class Battle_Enemy(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    Rwalkpics = []
    Lwalkpics = []
    Uwalkpics = []
    Dwalkpics = []
    Rswordpics = []
    direction = 'down'
    def __init__(self,x, y, name, power, magic, resiliance, spirit, speed, luck, hp):
        get_sprites(self, "data/images/octorock.gif",40,40, self.Dwalkpics, self.Uwalkpics, self.Rwalkpics, self.Lwalkpics)
    
        #Set the default position and image
        self.image = self.Dwalkpics[0]
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (x,y)
        self.old_y = y
        self.old_x = x
        self.feet = pygame.Rect(0,0, self.rect.width, self.rect.height * .5)
        self.stats = {}
        self.base_stats = {}
        self.weapon = None
        self.armour = None
        self.level = 1
        self.name = name
        self.base_stats['power'] = power
        self.base_stats['magic'] = magic
        self.base_stats['resiliance'] = resiliance
        self.base_stats['spirit'] = spirit
        self.base_stats['speed'] = speed
        self.base_stats['luck'] = luck
        self.base_stats['hp'] = hp
        self.stats['hp'] = (self.base_stats['hp'] * self.level / 100)
        self.tick = 0
        self.gauge = 0
        self.bias = None
        self.aggro = [5, 5, 5]
        self.moves = None
        self.status = 'alive'
    def update(self):
        self.stats['power'] = (self.base_stats['power'] * self.level / 100) + self.weapon.stats['power_bonus']
        self.stats['magic'] = (self.base_stats['magic'] * self.level / 100) + self.weapon.stats['magic_bonus']
        self.stats['resiliance'] = (self.base_stats['resiliance'] * self.level / 100) + self.armour.stats['resiliance_bonus']
        self.stats['spirit'] = (self.base_stats['spirit'] * self.level / 100) + self.armour.stats['spirit_bonus']
        self.stats['speed'] = (self.base_stats['speed'] * self.level / 100) - self.armour.stats['weight'] - self.weapon.stats['weight']
        self.stats['luck'] = (self.base_stats['luck']) + self.armour.stats['luck_bonus'] + self.weapon.stats['luck_bonus']
        self.stats['hp_max'] = (self.base_stats['hp'] * self.level / 100) + self.armour.stats['hp_bonus'] + self.weapon.stats['hp_bonus']   
    def drawh(self, screen):
        COLOR = GREEN
        if self.stats['hp'] >= self.stats['hp_max'] / 2:
            COLOR = GREEN
        elif self.stats['hp'] <= self.stats['hp_max'] / 4:
            COLOR = RED
        else:
            COLOR = YELLOW
        pygame.draw.rect(screen, BLACK, (self.rect.x - 1, self.rect.y - 11, 42, 7))
        pygame.draw.rect(screen, COLOR, (self.rect.x, self.rect.y - 10, (self.stats['hp'] / self.stats['hp_max'] * 40), 5))
        pygame.draw.rect(screen, BLACK, (self.rect.x - 1, self.rect.y - 19, 42, 5))
        pygame.draw.rect(screen, BLUE, (self.rect.x, self.rect.y - 18, self.gauge / 100 * 40, 3))
    def moveb(self, walls, dist, t):        
        self.old_x = self.rect.centerx
        self.old_y = self.rect.centery
        self.rect.centerx += float(self.change_x)
        self.rect.centery += float(self.change_y) + 3
        self.feet.midbottom = self.rect.midbottom 
    def move_back(self):
        self.rect.centerx = self.old_x
        self.rect.centery = self.old_y
        self.feet.midbottom = self.rect.midbottom
    def AI(self, target):
        power = []
        for move in self.moves:
            power.append(damaged(self, target, move))
        return (self.moves[power.index(max(power))])
    
class Jumper(Battle_Enemy):
    def __init__(self, x, y):
        Battle_Enemy.__init__(self, x, y, "Jumper", 400, 400, 100, 100, 100, 0,100000)
        self.weapon = Glaive()
        self.armour = Ruby_vest(1, 0)
        self.moves = [["Slash",  30, 0], ["Magislash",  20,  50]]
        self.bias = 'archer'

class Slammer(Battle_Enemy):
    def __init__(self, x, y):
        Battle_Enemy.__init__(self, x, y, "Slammer", 160, 160, 160, 160, 160, 0, 100000)
        self.weapon = Glaive()
        self.armour = Ruby_vest(1, 0)
        self.moves = [["Slash",  30, 0], ["Magislash",  20,  50]]
        self.bias = 'tank'   

class Hero(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    Rwalkpics = []
    Lwalkpics = []
    Uwalkpics = []
    Dwalkpics = []
    Rswordpics = []
    direction = 'down'
    money = 10
    battle_trigger = None
    
    def __init__(self,x,y, name, power, magic, resiliance, spirit, speed, luck, hp, level):
        get_sprites(self, "data/images/holder.png",60,60, self.Dwalkpics, self.Uwalkpics, self.Rwalkpics, self.Lwalkpics)
    
        #Set the default position and image
        self.image = self.Dwalkpics[0]
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (x,y)
        self.old_y = y
        self.old_x = x
        self.feet = pygame.Rect(0,0, self.rect.width, self.rect.height * .5)
        self.base_stats = {}
        self.stats = {}
        print ("yeah")
        self.weapon = None
        self.armour = None
        self.level = level
        self.name = name
        self.base_stats['power'] = power
        self.base_stats['magic'] = magic
        self.base_stats['resiliance'] = resiliance
        self.base_stats['spirit'] = spirit
        self.base_stats['speed'] = speed
        self.base_stats['luck'] = luck
        self.base_stats['hp'] = hp
        self.stats['hp'] = (self.base_stats['hp'] * self.level / 100)
        self.type = "none"
        self.tick = 0
        self.gauge = 0
        self.moves = [["Killer",  90, 0], ["Ripper",  60,  100]]
        self.status = 'alive'
        
        

    def changespeed(self, x, y,direc):
        self.change_x += x
        self.change_y += y
        if direc == "non":
            self.direction = self.direction
        else:
            self.direction = direc

    def update(self):
        self.stats['power'] = (self.base_stats['power'] * self.level / 100) + self.weapon.stats['power_bonus']
        self.stats['magic'] = (self.base_stats['magic'] * self.level / 100) + self.weapon.stats['magic_bonus']
        self.stats['resiliance'] = (self.base_stats['resiliance'] * self.level / 100) + self.armour.stats['resiliance_bonus']
        self.stats['spirit'] = (self.base_stats['spirit'] * self.level / 100) + self.armour.stats['spirit_bonus']
        self.stats['speed'] = (self.base_stats['speed'] * self.level / 100) - self.armour.stats['weight'] - self.weapon.stats['weight']
        self.stats['luck'] = (self.base_stats['luck']) + self.armour.stats['luck_bonus'] + self.weapon.stats['luck_bonus']
        self.stats['hp_max'] = (self.base_stats['hp'] * self.level / 100) + self.armour.stats['hp_bonus'] + self.weapon.stats['hp_bonus']
    def drawh(self, screen):
        COLOR = GREEN
        if self.stats['hp'] >= self.stats['hp_max'] / 2:
            COLOR = GREEN
        elif self.stats['hp'] <= self.stats['hp_max'] / 4:
            COLOR = RED
        else:
            COLOR = YELLOW
        pygame.draw.rect(screen, BLACK, (self.rect.x - 1, self.rect.y - 11, 62, 7))
        pygame.draw.rect(screen, COLOR, (self.rect.x, self.rect.y - 10, (self.stats['hp'] / self.stats['hp_max'] * 60), 5))
        pygame.draw.rect(screen, BLACK, (self.rect.x - 1, self.rect.y - 19, 62, 5))
        pygame.draw.rect(screen, BLUE, (self.rect.x, self.rect.y - 18, self.gauge / 100 * 60, 3))
    def moveb(self, walls, dist, t):        
        self.old_x = self.rect.centerx
        self.old_y = self.rect.centery
        self.rect.centerx += float(self.change_x)
        self.rect.centery += float(self.change_y) + 3
        self.feet.midbottom = self.rect.midbottom       
        
    def move(self, walls,enemies,npcs,chests,room,dist,t):
        """ Find a new position for the player """
 
        # Move left/right
        self.old_x = self.rect.centerx
        self.old_y = self.rect.centery
        self.rect.centerx += float(self.change_x)
        posh = float(self.rect.centerx)
        self.rect.centery += float(self.change_y)
        posv = float(self.rect.centery)
        self.feet.midbottom = self.rect.midbottom
        
        #'animate' the character by switching sprites
        if self.direction == "right":
            if self.change_x == 0 and self.change_y == 0:
                    self.image = self.Rwalkpics[0]
            else:
                frame = (posh // dist) % len(self.Rwalkpics)
                self.image = self.Rwalkpics[int(frame)]
        elif self.direction == 'left':           
            if self.change_x == 0 and self.change_y == 0:
                self.image = self.Lwalkpics[0]
            else:
                frame = (posh // dist) % len(self.Lwalkpics)
                self.image = self.Lwalkpics[int(frame)]            
        elif self.direction == 'up':
            if self.change_x == 0 and self.change_y == 0:
                self.image = self.Uwalkpics[0]
            else:
                frame = (posv // dist) % len(self.Uwalkpics)
                self.image = self.Uwalkpics[int(frame)]
        elif self.direction == 'down':
            if self.change_x == 0 and self.change_y == 0:
                self.image = self.Dwalkpics[0]
            else:
                frame = (posv // dist) % len(self.Dwalkpics)
                self.image = self.Dwalkpics[int(frame)]

        # See if the player hit/was hit by an enemy and act accordingly
        enemy_hit_list = pygame.sprite.spritecollide(self, enemies, False)
        for block in enemy_hit_list:
            if pygame.sprite.collide_rect(self, block):
                self.battle_trigger = block
#            else:
#                self.battle_trigger = None
        #See if the player hits a chest
        chest_hit_list = chests
        for chest in chest_hit_list:
            if pygame.sprite.collide_rect(self, chest):
                chest.contact = True
            else:
                chest.contact = False
        # See if the player hit/was hit by an npc and act accordingly
        npc_hit_list = npcs
        for block in npc_hit_list:
            if pygame.sprite.collide_rect(self, block):
                if self.change_x > 0:                   # walking right
                    self.move_back()
                    block.left = True
                elif self.change_x < 0:                 # walking left
                    self.move_back()
                    block.right = True
                elif self.change_y > 0:                 # walking down
                    self.move_back()
                    block.below = True
                elif self.change_y < 0:                 # walking up
                    self.move_back()
                    block.above = True
                if block.change_x > 0:                  # npc walking right
                    block.move_back()
                    block.left = True
                elif block.change_x < 0:                # npc walking left
                    block.move_back()
                    block.right = True
                elif block.change_y > 0:                # npc walking down
                    block.move_back()
                    block.below = True
                elif block.change_y < 0:                # npc walking up
                    block.move_back()
                    block.above = True
#            else:
#                block.above = False
#                block.below = False
#                block.left = False
#                block.right = False
        
    def move_back(self):
        self.rect.centerx = self.old_x
        self.rect.centery = self.old_y
        self.feet.midbottom = self.rect.midbottom

#CLASS TO HANDLE DIFFERENT LEVELS (ROOMS)
class Room(object):
    def __init__(self, player, filename, screen, sound_file):
        self.player = player
        self.filename = filename
        self.screen = screen
        self.file = get_map(self.filename)
        self.tmx_data = load_pygame(self.file)
        self.wall_list = list()
        self.chest_list = list()
        self.enemy_sprites = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.moves = list()
        self.moves_names = list()
        self.music = sound_file
        print (self.tmx_data.properties)
        for object in self.tmx_data.objects:
            if object.name == 'wall':
                self.wall_list.append(pygame.Rect(object.x,object.y,object.width,object.height))
            elif object.name[0:6] == "chest:":
                chest = Chest(object.x,object.y,object.width,object.height)
                chest.items = (object.name[6:].split("."))
                self.chest_list.append(chest)
                self.wall_list.append(pygame.Rect(object.x+6,object.y+6,object.width-12,object.height-12))
            else:
                self.moves.append(pygame.Rect(object.x,object.y,object.width,object.height))
                self.moves_names.append(object.name)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 1
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.group.add(self.player)
        for i in self.chest_list:
            print (i.items)
    def draw(self, screen):
        screen.fill(BLACK)
        self.enemy_sprites.draw(screen)
        self.npcs.draw(screen)
        self.group.center(self.player.rect.center)
        self.group.draw(screen)
    def update(self,dist,time,condition):
        self.enemy_sprites.update(dist/2,time,condition,self.player)
        self.npcs.update(dist,time,condition)
        for enemy in self.enemy_sprites:
            if enemy.feet.collidelist(self.wall_list) > -1:
                enemy.move_back()            
            self.group.add(enemy)
        for npc in self.npcs:
            if npc.feet.collidelist(self.wall_list) > -1:
                npc.move_back()            
            self.group.add(npc)
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.wall_list) > -1:
                sprite.move_back()
            
class Battle_Room(object):
    def __init__(self, players, filename, screen, sound_file):
        self.players = players
        self.filename = filename
        self.screen = screen
        self.file = get_map(self.filename)
        self.tmx_data = load_pygame(self.file)
        self.wall_list = list()
        self.enemy_sprites = pygame.sprite.Group()
        self.music = sound_file
        print (self.tmx_data.properties)
        for object in self.tmx_data.objects:
            self.wall_list.append(pygame.Rect(object.x,object.y,object.width,object.height))
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 1
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        for man in self.players:
            self.group.add(man)
    def draw(self, screen):
        screen.fill(BLACK)
        self.enemy_sprites.draw(screen)
        self.group.center((400, 300))
        self.group.draw(screen)
        for man in self.group:
            man.drawh(screen)
    def update(self,dist,time,condition):
        for enemy in self.enemy_sprites:
            if enemy.feet.collidelist(self.wall_list) > -1:
                enemy.move_back()            
            self.group.add(enemy)
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.wall_list) > -1:
                sprite.move_back()
#BATTLE TEST LEVEL
class Battle_Test(Battle_Room):
    def __init__(self,players,screen):
        Battle_Room.__init__(self,players,'levels/battle.tmx',screen,"data/music/battle.wav")
#FIRST TEST LEVEL           
class grass_test(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/grasslands.tmx',screen,"data/music/cake.ogg")
        npc = NPC(1100/64,800/64,"data/images/cape_redhead.gif",1000/64,1300/64,700/64,900/64,60,60)
        npc.text = "Greetings to the grasslands!"
        npc.change_y = 2
        self.npcs.add(npc)
        enemy = Enemy(900,800,"data/images/octorock.gif",0,3000/64,0,3000/64,40,40,50)
        enemy.change_y = 2
        enemy.target = False
        enemy.health = 1
        self.enemy_sprites.add(enemy)
    def new_room(self, place):
        if place == "grass_test2":
            return (900, 740)

#SECOND TEST LEVEL
class grass_test2(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/grasslands_small.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "grass_test":
            return (250,100)
class COSthroneroom(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSthroneroom.tmx',screen,"data/music/Songtest.ogg")
        enemy_1 = Jumper(100, 200)
        enemy_1.name = "E1"
        enemy_1.level = 50
        enemy_1.update()
        enemy_1.stats['hp'] = enemy_1.stats['hp_max']
        
        enemy_2 = Slammer(170, 250)
        enemy_2.name = "E2"
        enemy_2.level = 55
        enemy_2.update()
        enemy_2.stats['hp'] = enemy_2.stats['hp_max']
        
        enemy_3 = Slammer(240, 150)
        enemy_3.name = "E3"
        enemy_3.level = 54
        enemy_3.update()
        enemy_3.stats['hp'] = enemy_3.stats['hp_max']
        
        enemy = Enemy(3, 9,'data/images/octorock.gif',30,600,0,600,40, 40, 300)
        enemy.group = [enemy_1, enemy_2, enemy_3]
        enemy.target = False
        self.enemy_sprites.add(enemy)
        
    def new_room(self, place):
        if place == "COSchestTR":
            return (11*64, 3.5*64, "left")
        elif place == "COSchestLR":
            return (11*64, 10.5*64, "left")
        elif place == "COSchestTL":
            return (0*64, 3.5*64, "right")
        elif place == "COSchestLL":
            return (0*64, 10.5*64, "right")
        elif place == "COSfoyer":
            return (6*64, 15*64, "up")
class COSchestTR(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSchestTR.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSthroneroom":
            return (0*64, 2.5*64, "right")
class COSchestLR(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSchestLR.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSthroneroom":
            return (0*64, 2.5*64, "right")
class COSchestTL(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSchestTL.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSthroneroom":
            return (8*64, 2.5*64, "left")
class COSchestLL(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSchestLL.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSthroneroom":
            return (8*64, 2.5*64, "left")
class COSfoyer(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSfoyer.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSthroneroom":
            return (5*64, 0*64, "down")
        elif place == "COSstairL":
            return (0*64, 2.5*64, "right")
        elif place == "COSstairR":
            return (10*64, 2.5*64, "left")
        elif place == "COSTstair1":
            return (10*64, 2.5*64, "left")
class COSstairR(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSstairR.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSfoyer":
            return (0*64, 2.5*64, "right")
        elif place == "COSTstair":
            return (4*64, 1*64, "down")
class COSstairL(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSstairL.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSfoyer":
            return (8*64, 2.5*64, "left")
        elif place == "COSBstair0":
            return (4*64, 1*64, "down")
class COSTstair(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSTstair.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSstairR":
            return (4*64, 1*64, "down")
        elif place == "COSThallway":
            return (0*64, 2.5*64, "right")
class COSThallway(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSThallway.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSTstair":
            return (7*64, 18.5*64, "left")
        elif place == "COSTscribe":
            return (0*64, 6.5*64, "right")
        elif place == "COSTlounge":
            return (0*64, 17.5*64, "right")
        elif place == "COSTarmoury":
            return (4*64, 6.5*64, "left")
class COSTscribe(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSTscribe.tmx',screen,"data/music/Songtest.ogg")
        npc = NPC(1,2,"data/images/cape_redhead.gif",0,3,0,6,60,60)
        npc.text = "I've been hearing strange rumors about the people of the seven main cities. News takes a long time to get over the barrier mountains, so I can only guess though."
        npc.change_y = 2
        self.npcs.add(npc)
        npc = NPC(9,3,"data/images/cape_redhead.gif",7,12,0,9,60,60)
        npc.text = "... Perhaps I left it over there? ... OH! Hello, I did not see you. ... Now where was it again? ..."
        npc.change_y = 2
        self.npcs.add(npc)
    def new_room(self, place):
        if place == "COSThallway":
            return (13*64, 6.5*64, "left")
class COSTlounge(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSTlounge.tmx',screen,"data/music/Songtest.ogg")
        npc = NPC(1,5,"data/images/cape_redhead.gif",1000/64,1300/64,700/64,900/64,60,60)
        npc.text = "Ahh, Finally I can relax for a bit!"
        npc.change_y = 2
        self.npcs.add(npc)
        npc = NPC(5,3,"data/images/cape_redhead.gif",1000/64,1300/64,700/64,900/64,60,60)
        npc.text = "There's an old wives tale about a blue orb or something. Also something about a water temple."
        npc.change_y = 2
        self.npcs.add(npc)
    def new_room(self, place):
        if place == "COSThallway":
            return (13*64, 6.5*64, "left")
class COSTarmoury(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSTarmoury.tmx',screen,"data/music/Songtest.ogg")
        npc = NPC(3,6,"data/images/cape_redhead.gif",1000/64,1300/64,700/64,900/64,60,60)
        npc.text = "Feel free to take one of each."
        npc.change_y = 2
        self.npcs.add(npc)
    def new_room(self, place):
        if place == "COSThallway":
            return (0*64, 6.5*64, "right")
class COSBstair0(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSBstair0.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSstairL":
            return (4*64, 1*64, "down")
        elif place == "COSBdining":
            return (8*64, 2.5*64, "left")
        elif place == "COSBstair1":
            return (5*64, 1*64, "down")
class COSBstair1(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSBstair1.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSBstair0":
            return (4*64, 1*64, "down")
class COSBdining(Room):
    def __init__(self,player,screen):
        Room.__init__(self,player,'levels/COSBdining.tmx',screen,"data/music/Songtest.ogg")
    def new_room(self, place):
        if place == "COSBstair0":
            return (0*64, 14.5*64, "right")

'''def battle(players, enemies):
    Battle = True
    battle_tick = 10
    fast_player = players[0]
    deadplayers = [0, 0]
    deadenemies = [0, 0]
    for enemy in enemies:
        enemy.tick = battle_tick * enemy.stats['speed']/fast_player.stats['speed']
        print (enemy.name, enemy.stats['hp'])
        for player in players:
            if player.type == enemy.bias:
                enemy.aggro[players.index(player)] = 1000
    for player in players:
        player.tick = battle_tick * player.stats['speed']/fast_player.stats['speed']
        print (player.name, player.stats['hp'])
    while Battle:
        for enemy in enemies:
            if enemy.status == 'dead':
                enemy.gauge = 0
                enemy.stats['hp'] = 0
                enemy.aggro = [0, 0, 0]
                deadenemies[enemies.index(enemy)] = 1
            else:
                if enemy.gauge >= 100:
                    target = players[enemy.aggro.index(max(enemy.aggro))]
                    move = enemy.AI(target)
                    damage = damaged(enemy, target, move)
                    target.stats['hp']  -= damage
                    print (enemy.aggro)
                    print ("%s dealt %f damage to %s using %s." %(enemy.name, damage,  target.name,  move[0]) )
                    enemy.gauge = 0
                    if target.stats['hp'] <= 0:
                        enemy.aggro[players.index(target)] = 0
                        print ("%s fainted!" %(target.name))
                        target.status = 'dead'
                        print (enemy.aggro)
                enemy.gauge += enemy.tick
                #print ("%s: %f" %(enemy.name,  enemy.gauge))
                
            
            
        for player in players:
            if player.status == 'dead':
                player.stats['hp'] = 0
                player.gauge = 0
                deadplayers[players.index(player)] = 1
            else:
                if player.gauge >= 100:
                    targ = randint(0, len(enemies) - 1)
                    target = enemies[targ]
                    move = player.moves[0]
                    damage = damaged(player, target, move)
                    target.stats['hp']  -= damage
                    print ("%s dealt %f damage to %s using %s." %(player.name, damage,  target.name,  move[0]))
                    target.aggro[players.index(player)] += damage
                    player.gauge = 0
                    if target.stats['hp'] <= 0:
                        print ("%s fainted!" %(target.name))
                        target.status = 'dead'

                player.gauge += player.tick               
                #print ("%s: %f" %(player.name,  player.gauge))
        if all(deadplayers):
           winners = enemies
           Battle = False
        if all(deadenemies):
           winners = players
           Battle = False
        #sleep(.5)
        #print ('\n')
    return (winners)
    
def hp_calc(level):
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    screen = init_screen(WIN_WIDTH, WIN_HEIGHT)
    pygame.display.init()
    pygame.display.set_caption('Lemon Kingdom Quest: The Sorceror Arises')
    man_1 = Hero(5,5,"Archy", 150, 150, 150, 150, 150, 0, 100000)
    man_1.level = level
    man_1.weapon = Glaive()
    man_1.armour = Ruby_vest(1, 0)
    man_1.type = 'archer'
    man_1.update()   
    man_1.stats['hp'] = man_1.stats['hp_max']
    
    man_2 = Hero(5,5,"Tanky", 150, 150, 150, 150, 140, 0, 100000)
    man_2.level = level
    man_2.weapon = Glaive()
    man_2.armour = Ruby_vest(1, 0)
    man_2.type = 'tank'
    man_2.update()
    man_2.stats['hp'] = man_2.stats['hp_max']
    
    enemy_1 = Jumper()
    enemy_1.name = "archler"
    enemy_1.level = level
    enemy_1.update()
    enemy_1.stats['hp'] = enemy_1.stats['hp_max']
    
    enemy_2 = Slammer()
    enemy_2.name = "tankler"
    enemy_2.level = level
    enemy_2.update()
    enemy_2.stats['hp'] = enemy_2.stats['hp_max']
    
    return (battle([man_1,  man_2], [enemy_1,  enemy_2]))
    
for i in hp_calc(75):
    print ("%s: %f"  %(i.name,  i.stats['hp']))
'''
    
