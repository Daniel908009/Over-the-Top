import pygame
import random
# classes
class tank(pygame.sprite.Sprite):
    def __init__(self, owner, type, tank_images, enemy_flag, alied_flag, number_of_units):
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
        self.rect.y = random.randint(100, 600 - self.rect.height/2)
        self.speed = 2
        self.health = 500
        self.damage = 5
        self.fire_range = 350
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

class Unit(pygame.sprite.Sprite):
    def __init__(self, type, owner, unit_images_running, unit_images_firing, enemy_flag, alied_flag, number_of_units):
        super().__init__()
        self.owner = owner
        self.id = number_of_units + 1
        if owner == "alied":
            self.image_running = unit_images_running[0]#all the units will have the same image for now
            self.image_firing = unit_images_firing[0]
            self.image = self.image_running
        elif owner == "enemy":
            self.image_running = pygame.transform.flip(unit_images_running[0], True, False)
            self.image_firing = pygame.transform.flip(unit_images_firing[0], True, False)
            self.image = self.image_running
        if type == 0:
            self.health = 100
            self.damage = 5
            self.fire_range = 100
        if type == 1:
            self.health = 200
            self.damage = 10
            self.fire_range = 200
        if type == 2:
            self.health = 300
            self.damage = 12
            self.fire_range = 400
        self.rect = self.image.get_rect()
        # making sure the units all spawn in the same place
        if owner == "enemy":
            self.rect.x = enemy_flag.rect.x
        else:
            self.rect.x = alied_flag.rect.x
        self.rect.y = random.randint(100, 600 - self.rect.height/2)
        self.speed = random.randint(3, 6)
        self.in_trench = False
        self.left_trench = -1
        self.in_trench_id = -1
        self.direction = 1
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

class Trench(pygame.sprite.Sprite):
    def __init__(self, x, number_of_trenches):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/wall.png"), (50, 500))
        self.rect = self.image.get_rect()
        self.rect.y = 100
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
                unit.direction = 1
                if self.current_owner != "alied":
                    self.auto_send = False
                self.current_owner = "alied"
                unit.image = unit.image_firing
                # will propably be changed, once i have the actual trench image
                unit.rect.x = self.rect.x - unit.rect.width/2
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