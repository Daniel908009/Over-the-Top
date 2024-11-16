import pygame
import random
import threading

pygame.init()
width, height = 1400, 700
pygame.display.set_caption("Over the Top")
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(pygame.image.load("helmet.png"))
clock = pygame.time.Clock()
level_width = 2700
# important variables
types_of_units = 3
x_offset = 0
money = 1000
enemy_money = 1000
show_main_menu = True
shift = False
right_click_menu = False
menu_pos = (0, 0)
selected_units = []

# main menu function, will be enhanced later
def main_menu_loop():
    global show_main_menu, font, running
    while show_main_menu:
        screen.fill((255, 255, 255))
        text = font.render("Press any key to start the game", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                show_main_menu = False
            if event.type == pygame.QUIT:
                show_main_menu = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_main_menu = False
        pygame.display.update()

# enemy control function
def enemy_con():
    global running, enemy_money
    while running:

        # this will be much much more complex later, for now I only want to test and create the basic functionality

        if enemy_money >= 10 and random.randint(0, 1) == 1:
            unit = Unit(random.randint(0, 2), "enemy")
            enemy_unit_group.add(unit)
            enemy_money -= 10

        clock.tick(1)

# functions
def update_offset():
    global x_offset
    # checking that the player doesnt move the camera too far
    if alied_flag.rect.x + x_offset > width/2 - alied_flag.rect.width:
        x_offset = 0
    if enemy_flag.rect.x + x_offset < width/2 + enemy_flag.rect.width:
        x_offset = 0

    # moving the objects
    for object in object_group:
        object.rect.x += x_offset
    for unit in allied_unit_group:
        unit.rect.x += x_offset
    for unit in enemy_unit_group:
        unit.rect.x += x_offset
    
    # moving the flags
    for flag in flags:
        flag.rect.x += x_offset


# classes
class Unit(pygame.sprite.Sprite):
    def __init__(self, type, owner):
        global money
        super().__init__()
        self.owner = owner
        self.image = pygame.Surface((50, 50))
        if type == 0:
            self.image.fill((255, 0, 0))
            self.health = 100
            self.damage = 10
            self.fire_range = 100
        if type == 1:
            self.image.fill((0, 255, 0))
            self.health = 200
            self.damage = 20
            self.fire_range = 200
        if type == 2:
            self.image.fill((0, 0, 255))
            self.health = 300
            self.damage = 30
            self.fire_range = 300
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

    def move(self):
        if self.in_trench == False and self.owner == "alied" and not self.firing:
            self.rect.x += self.speed*self.direction
        if self.in_trench == False and self.owner == "enemy":
            self.rect.x -= self.speed*self.direction

    def update(self):
        # if the unit is selected, then drawing a rectangle around it for now
        if self in selected_units:
            pygame.draw.rect(screen, (100, 100, 0), (self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10), 5)

    def fire(self):
        global enemy_unit_group, allied_unit_group
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
    def __init__(self, x):
        global number_of_trenches
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("wall.png"), (50, 500))
        self.rect = self.image.get_rect()
        self.rect.y = 100
        self.rect.x = x 
        self.id = number_of_trenches
        number_of_trenches += 1
        self.units_in_trench = 0
        self.current_owner = "none"
        self.auto_send = False

    def update(self):
        # if auto_send is on, than sending all the units that are from the owner automatically through
        # I will later decide if the enemy should have the option to auto send, or not
        # this will maybe be reused later, once I create more commands
    #    if self.auto_send:
    #        if self.current_owner == "alied":
     #           for unit in allied_unit_group:
      #              if unit.in_trench_id == self.id:
       #                 unit.in_trench = False
        #                unit.in_trench_id = -1
         #               unit.left_trench = self.id
          #  if self.current_owner == "enemy":
           #     for unit in enemy_unit_group:
            #        if unit.in_trench_id == self.id:
             #           unit.in_trench = False
              #          unit.in_trench_id = -1
               #         unit.left_trench = self.id

        # checking if a unit is colliding with the trench, if yes, then the unit will stop moving
        for unit in allied_unit_group:
            if self.rect.colliderect(unit.rect) and unit.left_trench != self.id and self.auto_send == False:
                unit.in_trench = True
                unit.in_trench_id = self.id
                unit.direction = 1
                if self.current_owner == "none":
                    pass
                elif self.current_owner == "enemy":
                    self.auto_send = False
                self.current_owner = "alied"
                # will propably be changed, once i have the actual trench image
                unit.rect.x = self.rect.x - unit.rect.width/2
        for unit in enemy_unit_group:
            if self.rect.colliderect(unit.rect) and unit.left_trench != self.id and self.auto_send == False:
                unit.in_trench = True
                unit.in_trench_id = self.id
                unit.direction = -1
                if self.current_owner == "none":
                    pass
                elif self.current_owner == "alied":
                    self.auto_send = False
                self.current_owner = "enemy"
                self.auto_send = False
                # will propably be changed, once I have the actual trench image
                unit.rect.x = self.rect.x + unit.rect.width/2
        # getting the number of units in the trench
        self.units_in_trench = 0
        for unit in allied_unit_group:
            if unit.in_trench_id == self.id:
                self.units_in_trench += 1

    def commands(self):
        # if there is at least one unit in the trench, control buttons will appear above the trench
        if self.units_in_trench > 0 :
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, 50, 50, 50))
            # if the button is clicked, the units will leave the trench
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x and pos[0] < self.rect.x + 50 and pos[1] > 50 and pos[1] < 100:
                    for unit in allied_unit_group:
                        if unit.in_trench_id == self.id:
                            unit.in_trench = False
                            unit.in_trench_id = -1
                            unit.left_trench = self.id
            # creating a button, that will send the units back
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, 0, 50, 50))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x and pos[0] < self.rect.x + 50 and pos[1] > 0 and pos[1] < 50:
                    for unit in allied_unit_group:
                        if unit.in_trench_id == self.id:
                            unit.direction = -1
                            unit.in_trench = False
                            unit.in_trench_id = -1
                            unit.left_trench = self.id
            # creating a drop down menu button, that will show all the unit types in the trench
            pass

        # creating a button, that will auto send all units coming through
        # this has to be outside of the main button loop, because it has to be shown at all times
        pygame.draw.rect(screen, (50, 50, 50), (self.rect.x - 50, 50, 50, 50))
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.rect.x - 50 and pos[0] < self.rect.x and pos[1] > 50 and pos[1] < 100:
                self.auto_send = True
                print("auto send")
                # I WILL HAVE TO FIX THIS, BECAUSE FOR SOME REASON THIS SPECIFIC PART OF THE CODE RUNS MULTIPLE TIMES AND EACH TIME IT IS A DIFFERENT AMMOUNT OF TIMES

# alied flag
class Flag(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((150, 150, 150))
        self.rect = self.image.get_rect()
        self.owner = owner
        if owner == "alied":
            self.rect.x = 0
        if owner == "enemy":
            self.rect.x = level_width 
        self.rect.y = height/2 - self.rect.height/2

# unit groups
allied_unit_group = pygame.sprite.Group()
enemy_unit_group = pygame.sprite.Group()
# test trenches
object_group = pygame.sprite.Group()
number_of_trenches = 1 # works as a unique id for the trenches
for i in range(int(1500/250)):
    trench = Trench(i*400+300)
    object_group.add(trench)

# flags
flags = pygame.sprite.Group()
# spawning the alied flag
alied_flag = Flag("alied")
flags.add(alied_flag)
# spawning the enemy flag
enemy_flag = Flag("enemy")
flags.add(enemy_flag)

# setting up the enemy spawn thread 
enemy_control = threading.Thread(target=enemy_con)

# main loop
running = True
font = pygame.font.Font(None, 36)
frame_rate = 60
time_to_add_money = 1 * frame_rate
while running:

    # showing the main menu
    if show_main_menu:
        main_menu_loop()

    # starting the enemy control thread
    if enemy_control.is_alive() == False:
        enemy_control.start()

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_offset += 25
            if event.key == pygame.K_d:
                x_offset -= 25
            if event.key == pygame.K_LSHIFT:
                shift = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                x_offset = 0
            if event.key == pygame.K_LSHIFT:
                shift = False
        # handling the mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                # checking if the player clicked on a buy button
                if pos[1] > 600:
                    for i in range(types_of_units):
                        if pos[0] > i * 100 and pos[0] < (i + 1) * 100:
                            # later maybe this will be changed to something better
                            if money < i * 10:
                                pass
                            else:
                                unit = Unit(i, "alied")
                                allied_unit_group.add(unit)
                # checking if the player clicked on a unit
                for unit in allied_unit_group:
                    if unit.rect.collidepoint(pos):
                        if unit in selected_units:
                            selected_units.remove(unit)
                            if shift == False:
                                selected_units.clear()
                        elif shift == False:
                            selected_units.clear()
                            selected_units.append(unit)
                        else:
                            selected_units.append(unit)
            # opening the right click menu
            if event.button == 3 and len(selected_units) > 0:
                if right_click_menu == False:
                    right_click_menu = True
                else:
                    right_click_menu = False
                    selected_units.clear()
                menu_pos = pygame.mouse.get_pos()

    # drawing a line representing the ground
    pygame.draw.line(screen, (0, 255, 0), (0, 100), (1400, 100), 5)

    # updating the offset to applu to all the objects
    update_offset()

    # drawing the alied flag and updating its position, and the same for the enemy flag
    flags.draw(screen)

    # drawing the objects
    object_group.draw(screen)
    for object in object_group:
        object.update()
        object.commands()

    # drawing the units
    allied_unit_group.draw(screen)
    enemy_unit_group.draw(screen)

                       # UI
    # drawing buttons from the bottom left corner, based on the number of types of units
    for i in range(types_of_units):
        pygame.draw.rect(screen, (50, 50, 50), (i * 100, 600, 100, 100))

    # drawing a drop down menu icon, for now a square
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, 100, 100))

    # drawing the selection menu in the bottom right corner, for now also only a square
    pygame.draw.rect(screen, (50, 50, 50), (1300, 600, 100, 100))

    # drawing a fill bar in the top right, representing the progress of the battle
    pygame.draw.rect(screen, (0, 0, 0), (width - 200, 0, 200, 50))
    
    # drawing the money
    text = font.render(str(money)+ " money", True, (0, 0, 0))
    screen.blit(text, (width/2- text.get_width()/2, 0))

    # moving the units
    for unit in allied_unit_group:
        unit.move()
        unit.fire()
        unit.update()
    for unit in enemy_unit_group:
        unit.move()
        unit.fire()

    # checking if the units are dead and removing them
    for unit in allied_unit_group:
        if unit.health <= 0:
            allied_unit_group.remove(unit)
    for unit in enemy_unit_group:
        if unit.health <= 0:
            enemy_unit_group.remove(unit)

    # in case the right click menu is open, then showing the menu, will be enhanced later
    if right_click_menu:
        pygame.draw.circle(screen, (50, 50, 50), menu_pos, 50)

    # checking that players units dont leave the screen
    for unit in allied_unit_group:
        if unit.rect.x < alied_flag.rect.x:
            unit.direction = 1
            unit.left_trench = -1

    # checking if one side has won
    for unit in allied_unit_group:
        if unit.rect.x > enemy_flag.rect.x - unit.rect.width:
            print("you won")
            running = False
    for unit in enemy_unit_group:
        if unit.rect.x < alied_flag.rect.x + unit.rect.width:
            print("enemy won")
            running = False

    # adding the money once per second
    time_to_add_money -= 1
    if time_to_add_money == 0:
        money += 10
        time_to_add_money = 1 * frame_rate
    
    clock.tick(frame_rate)
    pygame.display.update()

pygame.quit()