import pygame
import random
import math

# classes
class tank(pygame.sprite.Sprite):
    def __init__(self, owner, type, tank_images, enemy_flag, alied_flag, number_of_units, base_size):
        super().__init__()
        self.owner = owner
        self.id = number_of_units + 1
        if owner == "alied":
            self.image_firing = tank_images[0] # the firing image is the same as the running image for now, maybe this will change later
            self.image_running = tank_images[0] # the running image is the same as the firing image for now and also its called running, but technicaly its driving, maybe I will change it later
            self.image = self.image_running
        elif owner == "enemy":
            self.image_firing = pygame.transform.flip(tank_images[0], True, False)
            self.image_running = pygame.transform.flip(tank_images[0], True, False)
            self.image = self.image_running
        self.rect = self.image.get_rect()
        if owner == "enemy":
            self.rect.x = enemy_flag.rect.x
        else:
            self.rect.x = alied_flag.rect.x
        self.rect.y = random.randint(base_size*2, base_size*12 - self.rect.height/2)
        self.speed = 2
        self.health = 500
        self.damage = 5
        self.fire_range = base_size*6
        self.in_trench = False
        self.left_trench = -1
        self.in_trench_id = -1
        self.direction = 1 # for now the tank will be almost like a unit, but later it will be different
        self.firing = False
        self.type = type
    def move(self):
        if self.in_trench == False and self.owner == "alied" and not self.firing:
            self.rect.x += self.speed*self.direction
        if self.in_trench == False and self.owner == "enemy" and not self.firing:
            self.rect.x -= self.speed*self.direction
    def fire(self, enemy_unit_group, allied_unit_group):
        if self.owner == "alied":
            for unit in enemy_unit_group:
                if unit.rect.x - self.rect.x < self.fire_range and unit.rect.x - self.rect.x > 0:
                    unit.health -= self.damage
                    self.firing = True
                    break
                else:
                    self.firing = False
        if self.owner == "enemy":
            for unit in allied_unit_group:
                if self.rect.x - unit.rect.x < self.fire_range and self.rect.x - unit.rect.x > 0:
                    unit.health -= self.damage
                    self.firing = True
                    break
                else:
                    self.firing = False
    def update(self):
        pass
        # changing the image of the unit if its running??? or driving
        #self.index += 0.1
        #self.image_running = self.images_running[int(self.type)]
        #self.image = self.image_running
        #if self.index >= len(self.images_running)-1:
        #    self.index = 0

class Unit(pygame.sprite.Sprite):
    def __init__(self, type, owner, unit_images_running, unit_images_firing, enemy_flag, alied_flag, number_of_units, base_size):
        super().__init__()
        self.owner = owner
        self.id = number_of_units + 1
        self.images_running = unit_images_running
        if type == 0:
            self.health = 100
            self.damage = 5
            self.fire_range = base_size*2
            self.reload_time = 2
            self.speed = 4
            if owner == "alied":
                self.image_running = unit_images_running[0]
                self.image_firing = unit_images_firing[type]
                self.image = self.image_running
            elif owner == "enemy":
                self.image_running = pygame.transform.flip(unit_images_running[0], True, False)
                self.image_firing = pygame.transform.flip(unit_images_firing[type], True, False)
                self.image = self.image_running
        if type == 1:
            self.health = 200
            self.damage = 10
            self.fire_range = base_size*4
            self.reload_time = 1
            self.speed = 3
            if owner == "alied":
                self.image_running = unit_images_running[0]
                self.image_firing = unit_images_firing[type]
                self.image = self.image_running
            elif owner == "enemy":
                self.image_running = pygame.transform.flip(unit_images_running[0], True, False)
                self.image_firing = pygame.transform.flip(unit_images_firing[type], True, False)
                self.image = self.image_running
        if type == 2:
            self.health = 300
            self.damage = 12
            self.fire_range = base_size*8
            self.reload_time = 4
            self.speed = 3
            if owner == "alied":
                self.image_running = unit_images_running[0]
                self.image_firing = unit_images_firing[type]
                self.image = self.image_running
            elif owner == "enemy":
                self.image_running = pygame.transform.flip(unit_images_running[0], True, False)
                self.image_firing = pygame.transform.flip(unit_images_firing[type], True, False)
                self.image = self.image_running
        self.rect = self.image.get_rect()
        # making sure the units all spawn in the same place
        if owner == "enemy":
            self.rect.x = enemy_flag.rect.x
        else:
            self.rect.x = alied_flag.rect.x
        self.rect.y = random.randint(base_size*2, base_size*12 - self.rect.height/2)
        self.in_trench = False
        self.left_trench = -1
        self.in_trench_id = -1
        self.direction = 1
        self.firing = False
        self.type = type
        self.index = 0

    def move(self):
        if self.in_trench == False and self.owner == "alied" and not self.firing:
            self.rect.x += self.speed*self.direction
        if self.in_trench == False and self.owner == "enemy" and not self.firing:
            self.rect.x -= self.speed*self.direction
    
    def update(self):
        # changing the image of the unit if its running
        if self.in_trench == False:
            self.index += 0.1
            self.image_running = self.images_running[math.floor(self.index)] # the current number of running images is pathetic and will need to be changed
            if self.owner == "enemy":
                self.image_running = pygame.transform.flip(self.image_running, True, False)
            else:
                self.image = self.image_running
            if self.direction == -1:
                self.image_running = pygame.transform.flip(self.image_running, True, False)
            self.image = self.image_running
            #print(self.index)
            if self.index >= len(self.images_running)-1:
                self.index = 0

    def fire(self, enemy_unit_group, allied_unit_group):
        if self.owner == "alied":
            for unit in enemy_unit_group:
                if unit.rect.x - self.rect.x < self.fire_range and unit.rect.x - self.rect.x > 0:
                    unit.health -= self.damage
                    self.firing = True
                    break
                else:
                    self.firing = False
        if self.owner == "enemy":
            for unit in allied_unit_group:
                if self.rect.x - unit.rect.x < self.fire_range and self.rect.x - unit.rect.x > 0:
                    unit.health -= self.damage
                    self.firing = True
                    break
                else:
                    self.firing = False

class Trench(pygame.sprite.Sprite):
    def __init__(self, x, number_of_trenches, base_size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/wall.png"), (50, 500))
        self.rect = self.image.get_rect()
        self.rect.y = base_size*2
        self.rect.x = x 
        self.id = number_of_trenches+1
        self.units_in_trench = 0
        self.current_owner = "none"
        self.auto_send = False
        self.show_menu = False
        self.types_in_trench = []

    def update(self , allied_unit_group, enemy_unit_group):
        # checking if a unit is colliding with the trench, if yes, then the unit will stop moving
        for unit in allied_unit_group:
            if self.rect.colliderect(unit.rect) and unit.left_trench != self.id and self.auto_send == False:
                unit.in_trench = True
                unit.in_trench_id = self.id
                if unit.direction == -1:
                    unit.image_running = pygame.transform.flip(unit.image_running, True, False)
                unit.direction = 1
                if self.current_owner != "alied":
                    self.auto_send = False
                self.current_owner = "alied"
                unit.image = unit.image_firing
                # will propably be changed, once i have the actual trench image
                unit.rect.x = self.rect.x - unit.rect.width
        for unit in enemy_unit_group:
            if self.rect.colliderect(unit.rect) and unit.left_trench != self.id and self.auto_send == False:
                unit.in_trench = True
                unit.in_trench_id = self.id
                unit.direction = 1
                if self.current_owner != "enemy":
                    self.auto_send = False
                self.current_owner = "enemy"
                # will propably be changed, once I have the actual trench image
                unit.rect.x = self.rect.x + unit.rect.width/2
                unit.image = unit.image_firing
        # getting the number of units in the trench
        self.units_in_trench = 0
        for unit in allied_unit_group:
            if unit.in_trench_id == self.id:
                self.units_in_trench += 1
                if self.units_in_trench ==0:
                    self.show_menu = False # reseting the menu, if there are no units in the trench, maybe will be later done somewhere else
        for unit in enemy_unit_group:
            if unit.in_trench_id == self.id:
                self.units_in_trench += 1
        # getting the types of units in the trench, this is used in the send specific units drop down menu
        self.types_in_trench.clear()
        if self.current_owner == "alied":
            for unit in allied_unit_group:
                if unit.in_trench_id == self.id:
                    for t in self.types_in_trench:
                        if t == unit.type:
                            break
                    else:
                        self.types_in_trench.append(unit.type)
        if self.current_owner == "enemy":
            for unit in enemy_unit_group:
                if unit.in_trench_id == self.id:
                    for t in self.types_in_trench:
                        if t == unit.type:
                            break
                    else:
                        self.types_in_trench.append(unit.type)
        # reordering the types from smallest to biggest num type
        self.types_in_trench.sort()

# class for the bullets
# later will fire at an angle to create a better effect
class Bullet(pygame.sprite.Sprite):
    def __init__(self, owner, image, x, y, range):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.range = range
        self.owner = owner
        if owner == "allied":
            self.direction = 1
        if owner == "enemy":
            self.direction = -1
    def move(self):
        self.rect.x += self.speed*self.direction
        self.range -= self.speed

# flag class
class Flag(pygame.sprite.Sprite):
    def __init__(self, owner, image, level_width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.owner = owner
        if owner == "alied":
            self.rect.x = 0
        if owner == "enemy":
            self.rect.x = level_width 
        self.rect.y = height/2 - self.rect.height/2

# class for menu buttons
class Button(pygame.sprite.Sprite):
    def __init__(self, level, x, y, width, height, image, aliegance, color):
        super().__init__()
        if image != None:
            self.image = pygame.transform.scale(image, (width, height))
        else:
            self.image = pygame.surface.Surface((width, height))
        if aliegance != None:
            self.aliegance = aliegance
        if color != None:
            self.color = color
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        if level != None:
            self.level = level

# class for the gas clouds
class Gas(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
    def expand(self):
        self.rect.width += 1
        self.rect.height += 1

# class for the artillery bombardment
class Artillery(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.area = []
    def random_hit_area(self):
        pass