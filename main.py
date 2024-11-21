import pygame
import random
import threading

pygame.init()
width, height = 1400, 700
pygame.display.set_caption("Over the Top")
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))# yes I know its from ww2, but it looks cool, maybe I will change it later
clock = pygame.time.Clock()
level_width = 2700
base_size = width/10 # will later be used for scaleability of the window
# important variables
types_of_units = 4
x_offset = 0
money = 1000 # for testing, later will be balanced
enemy_money = 200 # we will see if I manage to make good enough opponents to keep this balanced
show_main_menu = True
shift = False
right_click_menu = False
menu_pos = (0, 0)
selected_units = []

# main menu function
def main_menu_loop():
    global show_main_menu, font, running
    while show_main_menu:
        screen.fill((255, 255, 255))
        # drawing three main buttons
        pygame.draw.rect(screen, (50, 50, 50), (width/2 - 250, height/2 - 50, 500, 100))
        pygame.draw.rect(screen, (50, 50, 50), (width/2 - 250, height/2 + 100, 500, 100))
        pygame.draw.rect(screen, (50, 50, 50), (width/2 - 250, height/2 + 250, 500, 100))
        # drawing the text on the buttons
        text = font.render("Endless", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - 50 + text.get_height()/2))
        text = font.render("Levels", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 + 100 + text.get_height()/2))
        text = font.render("Exit", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 + 250 + text.get_height()/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                show_main_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # checking if one of the buttons is clicked
                pos = pygame.mouse.get_pos()
                if pos[0] > width/2 - 250 and pos[0] < width/2 + 250:
                    if pos[1] > height/2 - 50 and pos[1] < height/2 + 50:
                        show_main_menu = False
                    if pos[1] > height/2 + 100 and pos[1] < height/2 + 200:
                        show_main_menu = False
                    if pos[1] > height/2 + 250 and pos[1] < height/2 + 350:
                        running = False
                        show_main_menu = False
        pygame.display.update()

# enemy control function this is a basic version of the enemy control, will be enhanced later, for now it works as intended
def enemy_con():
    global running, object_group, allied_unit_group, enemy_unit_group
    can_buy = True
    # creating a 2d array that resembles the trench positions and who owns them
    trench_positions = []
    for trench in object_group:
        trench_positions.append([trench.rect.x, trench.current_owner, trench.id, trench.units_in_trench, trench.current_owner])
    # sorting the trench positions based on the id from the biggest to the smallest
    trench_positions = sorted(trench_positions, key=lambda x: x[2], reverse=True)
    while running:
        # checking if the enemy can still buy units, this is done by checking if no allied units are near the enemy flag(this is done, because the battle would not end otherwise)
        #for unit in allied_unit_group:
        #    if unit.rect.x > enemy_flag.rect.x - 200:
        #        can_buy = False
        #        break                              # I think this is causing some problems to the units movement, but I will have to test it more to be sure
        #    else:
        #        can_buy = True
        # updating the trench positions
        for trench in object_group:
            for pos in trench_positions:
                if pos[2] == trench.id:
                    pos[1] = trench.current_owner
                    pos[3] = trench.units_in_trench
                    pos[4] = trench.current_owner
                    break
        # sorting the trench positions based on the id from the biggest to the smallest
        trench_positions = sorted(trench_positions, key=lambda x: x[2], reverse=True)
            # main logic here
        # buying units
        if can_buy:
            buy(random.randint(0,3), "enemy")
        # sending out orders, for now only basic ones
        for trench in trench_positions:
            # getting the next trench in line using the trench_positions array and the current trench id
            for pos in trench_positions:
                if pos[2] == trench[2] - 1:
                    next_trench = pos
                    break
            # checking if the next trench in line is owned by no one, using the trench_positions array, if so then sending the units from the closest enemy owned trench
            if next_trench[1] == "none" and trench[1] == "enemy":
                #print("sending units from trench " + str(trench[2]) + " to trench " + str(next_trench[2])+" because its empty")
                send_units_forward(trench[2], "enemy", None)
                        
            
            # checking if there is at least ten units in the enemy owned trenches, if not then sending all the units from the closest enemy owned trench
            if next_trench[1] == "enemy" and trench[1] == "enemy" and next_trench[3] < 10:
                #print("sending units from trench " + str(trench[2]) + " to trench " + str(next_trench[2])+" because there are only " + str(next_trench[3]) + " units in the trench")
                send_units_forward(trench[2], "enemy", None)
        #print(trench_positions)
        clock.tick(1)

# function that updates the offset of the camera
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

# function that draws the progress bar
def progress_bar():
    # getting the number of trenches and who owns which trench
    number_of_alied_trenches = 0
    number_of_enemy_trenches = 0
    for trench in object_group:
        if trench.current_owner == "alied":
            number_of_alied_trenches += 1
        if trench.current_owner == "enemy":
            number_of_enemy_trenches += 1
    # drawing the progress bar
    progress_bar_width = 300
    piece_width = 0
    if number_of_alied_trenches + number_of_enemy_trenches != 0:
        piece_width = progress_bar_width / (number_of_alied_trenches + number_of_enemy_trenches)
    # drawing the entire progress bar neutral part
    pygame.draw.rect(screen, (100, 100, 100), (width - progress_bar_width, 0, progress_bar_width, 50))
    if piece_width != 0:
        # drawing the alied part from the left end of the progress bar
        pygame.draw.rect(screen, (0, 0, 255), (width - progress_bar_width, 0, piece_width * number_of_alied_trenches, 50))
        # drawing the enemy part from the right end of the progress bar
        pygame.draw.rect(screen, (255, 0, 0), (width - progress_bar_width + piece_width * number_of_alied_trenches, 0, piece_width * number_of_enemy_trenches, 50))

# buy function
def buy(unit_type, owner):
    global money, allied_unit_group, enemy_money
    if owner == "alied" and money >= 5:
        if unit_type == 0:
            unit = Unit(0, "alied")
            allied_unit_group.add(unit)
            money -= 5
        if unit_type == 1 and money >= 10:
            unit = Unit(1, "alied")
            allied_unit_group.add(unit)
            money -= 10
        if unit_type == 2 and money >= 20:
            unit = Unit(2, "alied")
            allied_unit_group.add(unit)
            money -= 20
        if unit_type == 3 and money >= 50:
            unit = tank("alied", 3)
            allied_unit_group.add(unit)
            money -= 50
    elif owner == "enemy":
        if unit_type == 0 and enemy_money >= 5:
            unit = Unit(0, "enemy")
            enemy_unit_group.add(unit)
            enemy_money -= 5
        if unit_type == 1 and enemy_money >= 10:
            unit = Unit(1, "enemy")
            enemy_unit_group.add(unit)
            enemy_money -= 10
        if unit_type == 2 and enemy_money >= 20:
            unit = Unit(2, "enemy")
            enemy_unit_group.add(unit)
            enemy_money -= 20
        if unit_type == 3 and enemy_money >= 50:
            unit = tank("enemy", 3)
            enemy_unit_group.add(unit)
            enemy_money -= 50

# function that sends the units back once a button is clicked or the enemy decides to send the units back
def send_units_back(trench_id, owner):
    global allied_unit_group, enemy_unit_group
    if owner == "alied":
        for unit in allied_unit_group:
            if unit.in_trench_id == trench_id:
                unit.direction = -1
                unit.in_trench = False
                unit.in_trench_id = -1
                unit.left_trench = trench_id
                unit.image = pygame.transform.flip(unit.image_running, True, False)
    if owner == "enemy":
        for unit in enemy_unit_group:
            if unit.in_trench_id == trench_id:
                unit.direction = -1
                unit.in_trench = False
                unit.in_trench_id = -1
                unit.left_trench = trench_id
                unit.image = pygame.transform.flip(unit.image_running, True, False)

# function that sends the units forward once a button is clicked or the enemy decides to send the units forward
def send_units_forward(trench_id, owner, type):
    global allied_unit_group, enemy_unit_group
    if type == None:
        # sending all the units in a trench forward
        if owner == "alied":
            for unit in allied_unit_group:
                if unit.in_trench_id == trench_id:
                    unit.direction = 1
                    unit.in_trench = False
                    unit.in_trench_id = -1
                    unit.left_trench = trench_id
                    unit.image = unit.image_running
        if owner == "enemy":
            for unit in enemy_unit_group:
                if unit.in_trench_id == trench_id:
                    unit.direction = 1
                    unit.in_trench = False
                    unit.in_trench_id = -1
                    unit.left_trench = trench_id
                    unit.image = unit.image_running
    else:
        # sending units of a specific type forward
        print("sending units of type " + str(type) + " forward")
        if owner == "alied":
            for unit in allied_unit_group:
                if unit.in_trench_id == trench_id and unit.type == type:
                    unit.direction = 1
                    unit.in_trench = False
                    unit.in_trench_id = -1
                    unit.left_trench = trench_id
                    unit.image = unit.image_running
        if owner == "enemy":
            for unit in enemy_unit_group:
                if unit.in_trench_id == trench_id and unit.type == type:
                    unit.direction = 1
                    unit.in_trench = False
                    unit.in_trench_id = -1
                    unit.left_trench = trench_id
                    unit.image = unit.image_running


# function that shows the trench menu
def show_trench_menu(trench_id, x, types):
                    # this is the old version of the menu, but I coulnt get it to work, and I figured up that its better if I just do the 
                    # types in the update function of the trench class
    #print("showing menu for trench " + str(trench_id))
    # getting the number of different types of units in the trench
    #types = []
    # setting up the types array
#    for i in object_group:
 #       types.append([])
  #  print(types)
   # for unit in allied_unit_group:
    #    for t in types[trench_id]:
 #           if t == unit.type:
 #               break
  #      else:
 #           types[trench_id].append(unit.type)
 #   print(types)
 #   print(str(types[trench_id]) +"in trench " + str(trench_id))
    # reordering the types from smallest to biggest for each trench
   # for t in types:
   #     t.sort()
  #  print(types)
    # drawing the buttons for each unit type present
    for i in range(len(types)):
        pygame.draw.rect(screen, (50, 50, 50), (x + 50, 100 + 50*i, 50, 50))
        text = font.render(str(types[i]), True, (0, 0, 255))
        screen.blit(text, (x + text.get_width()/2+50, 100 + 50*i + text.get_height()/2))
    # checking if the buttons are clicked
    if pygame.mouse.get_pressed()[0]: # the problem is that when the person clicks a button it will send not only the units of that type, but also the units next in line of types, its the basic button pressing problem, I will have to find a fix for it, but for now I dont have any ideas
        pos = pygame.mouse.get_pos()
        for i in range(len(types)):
            if pos[0] > x + 50 and pos[0] < x + 100 and pos[1] > 100 + 50*i and pos[1] < 150 + 50*i:
                print(types[i])
                send_units_forward(trench_id, "alied", types[i])
                break
    #types.clear()
# classes
class tank(pygame.sprite.Sprite):
    def __init__(self, owner, type):
        super().__init__()
        self.owner = owner
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
    def update(self):
        # if the tank is selected, then drawing a rectangle around it for now
        if self in selected_units:
            pygame.draw.rect(screen, (100, 100, 0), (self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10), 5)

class Unit(pygame.sprite.Sprite):
    def __init__(self, type, owner):
        super().__init__()
        self.owner = owner
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
            self.damage = 15
            self.fire_range = 600
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
        self.image = pygame.transform.scale(pygame.image.load("assets/wall.png"), (50, 500))
        self.rect = self.image.get_rect()
        self.rect.y = 100
        self.rect.x = x 
        self.id = number_of_trenches
        number_of_trenches += 1
        self.units_in_trench = 0
        self.current_owner = "none"
        self.auto_send = False
        self.show_menu = False
        self.types_in_trench = []

    def update(self):
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

    def commands(self):
        # if there is at least one unit in the trench, control buttons will appear above the trench
        if self.units_in_trench > 0 and self.current_owner == "alied":
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, 50, 50, 50))
            # if the button is clicked, the units will leave the trench
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x and pos[0] < self.rect.x + 50 and pos[1] > 50 and pos[1] < 100:
                    send_units_forward(self.id, self.current_owner, None)
            # creating a button, that will send the units back
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, 0, 50, 50))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x and pos[0] < self.rect.x + 50 and pos[1] > 0 and pos[1] < 50:
                    send_units_back(self.id, self.current_owner)
            # creating a drop down menu button, that will show all the unit types in the trench
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, 50, 100, 50))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x and pos[0] < self.rect.x + 100 and pos[1] > 50 and pos[1] < 100:
                    self.show_menu = True
            if self.show_menu:
                show_trench_menu(self.id, self.rect.x, self.types_in_trench)

        # creating a button, that will auto send all units coming through
        # this has to be outside of the main button loop, because it has to be shown at all times
        if self.current_owner == "alied":
            # drawing the buttons
            # if autosend is false than lowering the visibility of the button
            if self.auto_send:
                pygame.draw.rect(screen, (0, 255, 0), (self.rect.x -50, 50, 50, 50), 100)
            else:
                pygame.draw.rect(screen, (0, 150, 0), (self.rect.x-50, 50, 50, 50), 100)
            # checking if the button is clicked
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x - 50 and pos[0] < self.rect.x and pos[1] > 50 and pos[1] < 100:
                    self.auto_send = True
            # drawing the stop button
            # if autosend is true than lowering the visibility of the button
            if self.auto_send:
                pygame.draw.rect(screen, (150, 0, 0), (self.rect.x-100, 50, 50, 50), 100)
            else:
                pygame.draw.rect(screen, (255, 0, 0), (self.rect.x-100, 50, 50, 50))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x - 100 and pos[0] < self.rect.x - 50 and pos[1] > 50 and pos[1] < 100:
                    self.auto_send = False

# alied flag
class Flag(pygame.sprite.Sprite):
    def __init__(self, owner, image):
        super().__init__()
        self.image = image
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
# unit images, more images will be added later, this is just for testing
unit_images_running = [pygame.transform.scale(pygame.image.load("assets/soldier.png"), (50, 50))]
unit_images_firing = [pygame.transform.scale(pygame.image.load("assets/unit.png"), (50, 50))] # the firing image is the one used in the trenches, maybe this will change later
# tank images
tank_images = [pygame.transform.scale(pygame.image.load("assets/tank.png"), (100, 100))]

# test trenches
object_group = pygame.sprite.Group()
number_of_trenches = 1 # works as a unique id for the trenches
for i in range(int(1500/250)):
    trench = Trench(i*400+300)
    object_group.add(trench)

# flags
flags = pygame.sprite.Group()
# spawning the alied flag
alied_flag_img = pygame.transform.scale(pygame.image.load("assets/default_flag1.png"), (100, 100))
alied_flag = Flag("alied", alied_flag_img)
flags.add(alied_flag)
# spawning the enemy flag
enemy_flag_img = pygame.transform.scale(pygame.image.load("assets/default_flag2.png"), (100, 100))
enemy_flag = Flag("enemy", enemy_flag_img)
flags.add(enemy_flag)

# setting up the enemy spawn thread 
enemy_control = threading.Thread(target=enemy_con)

# main loop
running = True
font = pygame.font.Font(None, 36)
frame_rate = 60
time_to_add_money = 1 * frame_rate
enemy_time_to_add_money = 1 * frame_rate # maybe will be changed later
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
                            buy(i, "alied")
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
    # this has to be in try except blocks, because of a blit failed error, I have encountered this error in one of my earlier projects, but I dont remember how I fixed it, but I will look into it soon
    try:
        allied_unit_group.draw(screen)
    except:
        pass
    try:
        enemy_unit_group.draw(screen)
    except:
        pass
    # sorting the units based on their y position to create sort of a 3d effect(pun intended)
    allied_unit_group = pygame.sprite.Group(sorted(allied_unit_group, key=lambda x: x.rect.y))
    enemy_unit_group = pygame.sprite.Group(sorted(enemy_unit_group, key=lambda x: x.rect.y))

                       # UI
    # drawing buttons from the bottom left corner, based on the number of types of units
    for i in range(types_of_units):
        pygame.draw.rect(screen, (50, 50, 50), (i * 100, 600, 100, 100))
        # drawing the type num on the button, later it will be the actual image of the unit with its price
        text = font.render(str(i), True, (0, 0, 0))
        screen.blit(text, (i * 100 + 50 - text.get_width()/2, 600 + 50 - text.get_height()/2))

    # drawing a drop down menu icon, for now a square
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, 100, 100))

    # drawing the selection menu in the bottom right corner, for now also only a square
    pygame.draw.rect(screen, (50, 50, 50), (1300, 600, 100, 100))

    # drawing a fill bar in the top right, representing the progress of the battle
    progress_bar()
    
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
        # drawing the health of the selected unit if its only one
        if len(selected_units) == 1:
            text = font.render(str(selected_units[0].health), True, (0, 0, 0))
            screen.blit(text, (menu_pos[0] - text.get_width()/2, menu_pos[1] - text.get_height()/2))

    # checking that players units dont leave the screen
    for unit in allied_unit_group:
        if unit.rect.x < alied_flag.rect.x:
            unit.direction = 1
            unit.left_trench = -1
            unit.image = unit.image_running
    
    # doing the same for the enemy units(this is not neccesary, but its good for testing)
    for unit in enemy_unit_group:
        if unit.rect.x > enemy_flag.rect.x:
            unit.direction = 1
            unit.left_trench = -1
            unit.image = unit.image_running

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
        money += 3
        time_to_add_money = 1 * frame_rate
    enemy_time_to_add_money -= 1
    if enemy_time_to_add_money == 0:
        enemy_money += 3
        enemy_time_to_add_money = 1 * frame_rate
    
    clock.tick(frame_rate)
    pygame.display.update()

pygame.quit()