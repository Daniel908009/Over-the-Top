import pygame
import random
import threading
import json
from classes import *
from pygame import mixer

pygame.init()
width, height = 1400, 700
pygame.display.set_caption("Over the Top")
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
clock = pygame.time.Clock()
level_width = None
base_size = int(width/28) # is used for scalability of the window
print(base_size)
# important variables
types_of_units = 4
types_of_special_actions = 2
x_offset = 0
money = None
enemy_money = None
show_main_menu = True
shift = False
right_click_menu = False
menu_pos = (0, 0)
selected_units = []
prices = [5, 10, 20, 50, 150,200] # maybe this will be loaded from a json file later

# loading the data from the json file
def load_data_json(type, nation):
    global money, level_width, positions_of_trenches, alied, enemy, enemy_money, current_nation, current_level
    #print(type)
    if type == "endless":
        with open("levels/endless.json", "r") as file:
            data = json.load(file)
            money = data["money"]
            enemy_money = data["enemy_money"]
            level_width = data["level_width"]
            positions_of_trenches = data["positions_of_trenches"] # later I will try to create a build menu for the game, for now this is enough though
            alied = data["allied"]
            enemy = data["enemy"]
        file.close()
    else:
        #print("levels/level_" + str(type) + ".json")
        with open("levels/"+str(nation)+"/level_" + str(type) + ".json", "r") as file:
            data = json.load(file)
            money = data["money"]
            enemy_money = data["enemy_money"]
            level_width = data["level_width"]
            positions_of_trenches = data["positions_of_trenches"]
            alied = data["allied"]
            enemy = data["enemy"]
        file.close()
    # these are usefull in resetting the game
    current_nation = nation
    current_level = type

# function that loads the selected images and sets up the level, for now only flags
def setup_level():
    global alied_flag, enemy_flag, object_group, flags, positions_of_trenches, number_of_trenches, level_width, unit_images_running_allies, unit_images_firing_allies, tank_images_allies, unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies, base_size
    # loading the images, this will later be done based on who is fighting who, you can see this in the json file
    if alied == "default":
        alied_flag = Flag("alied", pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/default_flag1.png"), (base_size*2, base_size*2)), True, False), level_width, height)
        flags.add(alied_flag)
        unit_images_running_allies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_1.png"), (base_size, base_size)), pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_2.png"), (50, 50))] # later more running images will be made
        unit_images_firing_allies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1.png"), (base_size, base_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_2.png"), (base_size, base_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_3.png"), (base_size, base_size))] # the firing images are the ones used in the trenches, maybe this will change later
        tank_images_allies = [pygame.transform.scale(pygame.image.load("assets/tank.png"), (base_size*2, base_size*2))]
    elif alied == "british":
        pass
    elif alied == "germans":
        pass
    elif alied == "french":
        pass
    elif alied == "russians":
        pass
    elif alied == "austro-hungarians":
        pass
    elif alied == "ottomans":
        pass
    elif alied == "bulgarians":
        pass
    elif alied == "serbians":
        pass
    elif alied == "greeks":
        pass
    elif alied == "italians":
        pass
    elif alied == "americans":
        pass

    if enemy == "default":
        enemy_flag = Flag("enemy", pygame.transform.scale(pygame.image.load("assets/default_flag2.png"), (base_size*2, base_size*2)), level_width, height)
        flags.add(enemy_flag)
        unit_images_running_enemies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_1.png"), (base_size, base_size)), pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_2.png"), (50, 50))]
        unit_images_firing_enemies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1.png"), (base_size, base_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_2.png"), (base_size, base_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_3.png"), (base_size, base_size))] # the firing image is the one used in the trenches, maybe this will change later
        tank_images_enemies = [pygame.transform.scale(pygame.image.load("assets/tank.png"), (base_size*2, base_size*2))]
    elif enemy == "british":
        pass
    elif enemy == "germans":
        pass
    elif enemy == "french":
        pass
    elif enemy == "russians":
        pass
    elif enemy == "austro-hungarians":
        pass
    elif enemy == "ottomans":
        pass
    elif enemy == "bulgarians":
        pass
    elif enemy == "serbians":
        pass
    elif enemy == "greeks":
        pass
    elif enemy == "italians":
        pass
    elif enemy == "americans":
        pass
    
    for i in range(len(positions_of_trenches)):
        trench = Trench(positions_of_trenches[i], number_of_trenches, base_size)
        object_group.add(trench)
        number_of_trenches += 1

# main menu function
def main_menu_loop():
    global show_main_menu, font, running, base_size
    previous_button_position = 0
    difference_in_height = base_size*3
    buttons = pygame.sprite.Group()
    # creating the buttons
    button = Button(1, width/2 - base_size*5, height/2 - base_size*2, base_size*10, base_size*2, None, "Endless", (50, 50, 50))
    buttons.add(button)
    previous_button_position = height/2 - base_size*2
    button = Button(2, width/2 - base_size*5, previous_button_position + difference_in_height, base_size*10, base_size*2, None, "Campaign", (50, 50, 50))
    buttons.add(button)
    previous_button_position += difference_in_height
    button = Button(3, width/2 - base_size*5, previous_button_position +difference_in_height, base_size*10, base_size*2, None, "Exit", (50, 50, 50))
    buttons.add(button)
    previous_button_position += difference_in_height 
    while show_main_menu:
        screen.fill((255, 255, 255))
        # drawing three main buttons and their text
        buttons.draw(screen)
        for button in buttons:
            text = font.render(str(button.aliegance), True, (0, 0, 0))
            screen.blit(text, (button.rect.x + base_size*5 - text.get_width()/2, button.rect.y + base_size - text.get_height()/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                show_main_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # checking if one of the buttons is clicked
                    pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.rect.collidepoint(pos):
                            if button.level == 1:
                                show_main_menu = False
                                load_data_json("endless", None)
                                setup_level()
                                #reset_game("endless", None)
                            if button.level == 2:
                                show_main_menu = False
                                nation_pick_menu()
                            if button.level == 3:
                                running = False
                                show_main_menu = False
        pygame.display.update()

# function for picking the nation in case player wants to play the campaign
def nation_pick_menu():
    global clock, running, return_arrow_image, show_main_menu, base_size
    nation_pick_window = True
    nation_buttons = pygame.sprite.Group()
    # getting the number of nations in the game from the json file
    with open("levels/Info.json", "r") as file:
        data = json.load(file)
        names_of_nations = data["names_of_nations"]
        flags_of_nations = data["flags_of_nations"] # I will need to find the remaining missing flags
    file.close()
    number_of_nations = len(names_of_nations)
    # creating the buttons for each nation
    index = 0
    line_height = base_size*2
    previous_button_position = 0
    for i in range(number_of_nations):
        if index == 5:
            index = 0
            line_height += base_size*6
            previous_button_position = 0
        flag = pygame.transform.scale(pygame.image.load(flags_of_nations[i]), (base_size*4, base_size*2))
        button = Button(i+1, width/20 + previous_button_position+ width/10, line_height, base_size*4, base_size*2, flag, names_of_nations[i], None)
        nation_buttons.add(button)
        previous_button_position = button.rect.x
        index += 1
    while nation_pick_window:
        screen.fill((255, 255, 255))

        nation_buttons.draw(screen)

        #drawing the text on the buttons, later image will propably be enough
        for button in nation_buttons:
            text = font.render(str(button.aliegance), True, (0, 0, 0))
            screen.blit(text, (button.rect.x + base_size*2-text.get_width()/2, button.rect.y + base_size*3-int(base_size/2) - text.get_height()/2))

        #drawing the return arrow
        screen.blit(return_arrow_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                nation_pick_window = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in nation_buttons:
                    if button.rect.collidepoint(pos):
                        nation_pick_window = False
                        nation_buttons.empty()
                        levels_choice_menu(button.aliegance)
                if pos[0] < base_size+int(base_size/2) and pos[1] < base_size+int(base_size/2):
                    nation_pick_window = False
                    show_main_menu = True

        clock.tick(60)
        pygame.display.update()

# function for drawing the levels choices, later they will be organized in a better way, this is just for testing
def levels_choice_menu(aliegance):
    # getting the number of levels
    with open("levels/"+aliegance+"/Info.json", "r") as file:
        data = json.load(file)
        number_of_levels = data["number_of_levels"]
        background_flag = data["background_flag"]
    file.close()
    global font, running, clock, return_arrow_image, base_size
    choice_menu = True
    level_choice_buttons = pygame.sprite.Group() # I chose to use a sprite group, because it will be easier to handle the drawing and clicking of the buttons
            # drawing the level buttons, they are organized in rows of 5, for now
    index = 0
    line_height = base_size*2
    previous_button_position = 0
    for i in range(number_of_levels):
        if index == 5:
            index = 0
            line_height += base_size*6
            previous_button_position = 0
        button = Button(i+1, width/20 + previous_button_position+ width/10, line_height, base_size*2, base_size*2, None, aliegance, None) # here I will later pass in the flag of the nation as an image
        level_choice_buttons.add(button)
        previous_button_position = button.rect.x
        index += 1
    flag = pygame.transform.scale(pygame.image.load(background_flag), (base_size*2, base_size*2))
    while choice_menu:
        screen.fill((255, 255, 255))
        # drawing the buttons
        level_choice_buttons.draw(screen)
        for button in level_choice_buttons:
            # drawing the text on the buttons
            text = font.render(str(button.level), True, (255, 255, 255))
            screen.blit(text, (button.rect.x + base_size-text.get_width()/2, button.rect.y + base_size - text.get_height()/2))

        # drawing the return arrow
        screen.blit(return_arrow_image, (0, 0))
        # drawing the flag
        screen.blit(flag, (width/2 - base_size, height-base_size*2))
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                choice_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in level_choice_buttons:
                    if button.rect.collidepoint(pos):
                        choice_menu = False
                        level_choice_buttons.empty()
                        load_data_json(button.level, button.aliegance)
                        setup_level()
                        #reset_game(button.aliegance, button.level)
                if pos[0] < base_size and pos[1] < base_size:
                    choice_menu = False
                    nation_pick_menu()

        clock.tick(60)
        pygame.display.update()

# function that resets the game
# has to be reworked, because currently there is too many weird things happening if I try to use it
def reset_game(nation, level):
    # clearing the sprite groups
    global object_group, allied_unit_group, enemy_unit_group, bullets, flags, number_of_units, number_of_trenches, right_click_buttons, screen
    object_group.empty()
    allied_unit_group.empty()
    enemy_unit_group.empty()
    right_click_buttons.empty()
    bullets.empty()
    flags.empty()
    number_of_units = 0
    number_of_trenches = 0
    # getting the new size and width of the window, and resizing the base_size and all the images
    global width, height,base_size, back_button_image, down_arrow_image, forward_button_image, return_arrow_image, square_image, menu_button_image
    base_size = int(width/28) # will later have to be adjusted, since currently changing anything about this causes errors
    menu_button_image = pygame.transform.scale(pygame.image.load("assets/menu.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
    forward_button_image = pygame.transform.scale(pygame.image.load("assets/forward.png"), (base_size, base_size))
    back_button_image = pygame.transform.scale(pygame.image.load("assets/back.png"), (base_size, base_size))
    return_arrow_image = pygame.transform.scale(pygame.image.load("assets/back_arrow.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
    down_arrow_image = pygame.transform.scale(pygame.image.load("assets/arrow_down.png"), (base_size, base_size))
    square_image = pygame.transform.scale(pygame.image.load("assets/square.png"), (base_size, base_size))
    # resetting all the menus and screen, important variables
    global show_game_menu, show_main_menu, right_click_menu, x_offset
    right_click_menu = False
    show_game_menu = False
    if nation == None and level == None:
        show_main_menu = True
    x_offset = 0
    # resizing the screen
    #if width != screen.get_width() or height != screen.get_height():
    #    width, height = screen.get_size()
    #    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    # if the reset comes from the game, then reloading the level
    if nation != None and level != None:
        load_data_json(level, nation)
        setup_level()

# enemy control function this is a basic version of the enemy control, will be enhanced later, for now it works as intended
# is currently capable of winning the game
# I will later create different levels and different types of enemy control, this is currently the dummy version
def enemy_con():
    global running, object_group, allied_unit_group, enemy_unit_group, show_game_menu, show_main_menu, base_size
    can_buy = True
    # creating a 2d array that resembles the trench positions and who owns them
    trench_positions = []
    for trench in object_group:
        trench_positions.append([trench.rect.x, trench.current_owner, trench.id, trench.units_in_trench, trench.current_owner])
    # sorting the trench positions based on the id from the biggest to the smallest
    trench_positions = sorted(trench_positions, key=lambda x: x[2], reverse=True)
    while running:
        if show_game_menu == False and show_main_menu == False:
            # checking if the enemy can still buy units, this is done by checking if no allied units are near the enemy flag(this is done, because the battle would not end otherwise)
            for unit in allied_unit_group:
                if unit.rect.x > enemy_flag.rect.x - base_size*4:
                    can_buy = False
                    break
                else:
                    can_buy = True
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
                
                # checking if the enemy has a number advantage compared to the alied trench, if so then sending all units to atack
                if next_trench[1] == "alied" and trench[1] == "enemy" and next_trench[3] < trench[3]:
                    #print("sending units from trench " + str(trench[2]) + " to trench " + str(next_trench[2])+" because the enemy has a number advantage")
                    send_units_forward(trench[2], "enemy", None)

            clock.tick(1)
        clock.tick(1)

# function that updates the offset of the camera
def update_offset():
    global x_offset, running, flags, object_group, bullets
    if running and x_offset != 0: # running has to also be checked, because the game would otherwise end with an error if player exits from the main menu
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
        
        # moving the bullets
        for bullet in bullets:
            bullet.rect.x += x_offset
        
        # moving the flags
        for flag in flags:
            flag.rect.x += x_offset

# function that highlights the selected unit
def highlight_unit(unit):
    # drawing a rectangle around the unit
    pygame.draw.rect(screen, (0, 0, 0), (unit.rect.x - int(base_size/10), unit.rect.y - int(base_size/10), unit.rect.width + int(base_size/5), unit.rect.height + int(base_size/5)), int(base_size/10))

# function that draws the progress bar
def progress_bar():
    global base_size
    # getting the number of trenches and who owns which trench
    number_of_alied_trenches = 0
    number_of_enemy_trenches = 0
    for trench in object_group:
        if trench.current_owner == "alied":
            number_of_alied_trenches += 1
        if trench.current_owner == "enemy":
            number_of_enemy_trenches += 1
    # drawing the progress bar
    progress_bar_width = base_size*6
    piece_width = 0
    if number_of_alied_trenches + number_of_enemy_trenches != 0:
        piece_width = progress_bar_width / (number_of_alied_trenches + number_of_enemy_trenches)
    # drawing the entire progress bar neutral part
    pygame.draw.rect(screen, (100, 100, 100), (width - progress_bar_width, 0, progress_bar_width, base_size))
    if piece_width != 0:
        # drawing the alied part from the left end of the progress bar
        pygame.draw.rect(screen, (0, 0, 255), (width - progress_bar_width, 0, piece_width * number_of_alied_trenches, base_size))
        # drawing the enemy part from the right end of the progress bar
        pygame.draw.rect(screen, (255, 0, 0), (width - progress_bar_width + piece_width * number_of_alied_trenches, 0, piece_width * number_of_enemy_trenches, base_size))

# buy function
def buy(unit_type, owner):
    global money, allied_unit_group, enemy_money, enemy_unit_group, tank_images_allies, enemy_flag, alied_flag, number_of_units, unit_images_running_allies, unit_images_firing_allies, unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies, prices
    number_of_units += 1
    if owner == "alied" and money >= prices[unit_type]:
        if unit_type == 0:
            unit = Unit(0, "alied", unit_images_running_allies, unit_images_firing_allies, enemy_flag, alied_flag, number_of_units, base_size)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
        elif unit_type == 1 and money >= prices[unit_type]:
            unit = Unit(1, "alied", unit_images_running_allies, unit_images_firing_allies, enemy_flag, alied_flag, number_of_units,base_size)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
        elif unit_type == 2 and money >= prices[unit_type]:
            unit = Unit(2, "alied", unit_images_running_allies, unit_images_firing_allies, enemy_flag, alied_flag, number_of_units,base_size)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
        elif unit_type == 3 and money >= prices[unit_type]:
            unit = tank("alied", 3, tank_images_allies, enemy_flag, alied_flag, number_of_units,base_size)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
        elif unit_type == 4 and money >= prices[unit_type]:
            print("gas")
        elif unit_type == 5 and money >= prices[unit_type]:
            print("artillery")
    elif owner == "enemy":
        if unit_type == 0 and enemy_money >= prices[unit_type]:
            unit = Unit(0, "enemy", unit_images_running_enemies, unit_images_firing_enemies, enemy_flag, alied_flag, number_of_units,base_size)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]
        elif unit_type == 1 and enemy_money >= prices[unit_type]:
            unit = Unit(1, "enemy", unit_images_running_enemies, unit_images_firing_enemies, enemy_flag, alied_flag, number_of_units,base_size)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]
        elif unit_type == 2 and enemy_money >= prices[unit_type]:
            unit = Unit(2, "enemy", unit_images_running_enemies, unit_images_firing_enemies, enemy_flag, alied_flag, number_of_units,base_size)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]
        elif unit_type == 3 and enemy_money >= prices[unit_type]:
            unit = tank("enemy", 3, tank_images_enemies, enemy_flag, alied_flag, number_of_units,base_size)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]
        elif unit_type == 4 and enemy_money >= prices[unit_type]:
            print("gas")
        elif unit_type == 5 and enemy_money >= prices[unit_type]:
            print("artillery")

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
                    #unit.image = unit.image_running
        if owner == "enemy":
            for unit in enemy_unit_group:
                if unit.in_trench_id == trench_id:
                    unit.direction = 1
                    unit.in_trench = False
                    unit.in_trench_id = -1
                    unit.left_trench = trench_id
                    #unit.image = unit.image_running
    else:
        # sending units of a specific type forward
        #print("sending units of type " + str(type) + " forward")
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

# same as the send_units_forward function, but for a single specific unit, maybe later I will merge it with the send_units_forward function to save some lines
def send_a_unit_forward(trench_id, owner, unit_id):
    if owner == "alied":
        for unit in allied_unit_group:
            if unit_id == unit.id:
                unit.direction = 1
                unit.in_trench = False
                unit.in_trench_id = -1
                unit.left_trench = trench_id
                unit.image = unit.image_running 
    if owner == "enemy":
        for unit in enemy_unit_group:
            if unit_id == unit.id:
                unit.direction = 1
                unit.in_trench = False
                unit.in_trench_id = -1
                unit.left_trench = trench_id
                unit.image = unit.image_running

# same as the send_units_back function, but for a single specific unit, maybe later I will merge it with the send_units_back function to save some lines
def send_a_unit_back(trench_id, owner, unit_id):
    if owner == "alied":
        for unit in allied_unit_group:
            if unit_id == unit.id:
                unit.direction = -1
                unit.in_trench = False
                unit.in_trench_id = -1
                unit.left_trench = trench_id
                unit.image = pygame.transform.flip(unit.image_running, True, False)
    if owner == "enemy":
        for unit in enemy_unit_group:
            if unit_id == unit.id:
                unit.direction = -1
                unit.in_trench = False
                unit.in_trench_id = -1
                unit.left_trench = trench_id
                unit.image = pygame.transform.flip(unit.image_running, True, False)


# function that shows the trench menu
def show_trench_menu(trench_id, x, types):
    global font, clicking, square_image, unit_images_firing_allies, base_size
    # drawing the buttons for each unit type present
    for i in range(len(types)):
        # drawing the button
        screen.blit(square_image, (x + base_size, base_size*2 + base_size*i))
        # drawing the units image on the button
        if types[i] < 3:
            screen.blit(pygame.transform.scale(unit_images_firing_allies[types[i]], (base_size-int(base_size/10),base_size-int(base_size/10))), (x + base_size*2-base_size, base_size*2 + base_size*i))
        elif types[i] == 3:
            screen.blit(pygame.transform.scale(tank_images_allies[0], (base_size-int(base_size/10), base_size-int(base_size/10))), (x + base_size*2-base_size, base_size*2 + base_size*i))
            
        # drawing the text on the button
        text = font.render(str(types[i]+1), True, (0, 0, 255))
        screen.blit(text, (x + text.get_width()/2+base_size*2-int(base_size/2), base_size*2+int(base_size/2) + base_size*i ))
    # checking if the buttons are clicked
    if pygame.mouse.get_pressed()[0]: # the problem is that when the person clicks a button it will send not only the units of that type, but also the units next in line of types, its the basic button pressing problem, I will have to find a fix for it, but for now I dont have any ideas
        pos = pygame.mouse.get_pos()
        for i in range(len(types)):
            if pos[0] > x + base_size and pos[0] < x + base_size*2 and pos[1] > base_size*2 + base_size*i and pos[1] < base_size*3 + base_size*i and clicking == False:
                send_units_forward(trench_id, "alied", types[i])
                clicking = True
                break
    else:
        clicking = False

# function to show trench commands(originaly this was in the class it self, but I had to redo it here because the drawing cant be done from another file)
def show_trench_commands(trench):
    global show_game_menu, forward_button_image, back_button_image, down_arrow_image, clicking, base_size
    # if there is at least one unit in the trench, control buttons will appear above the trench
    if trench.units_in_trench > 0 and trench.current_owner == "alied":
        screen.blit(forward_button_image, (trench.rect.x, base_size))
        # if the button is clicked, the units will leave the trench
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x and pos[0] < trench.rect.x + base_size and pos[1] > base_size and pos[1] < base_size*2:
                send_units_forward(trench.id, trench.current_owner, None)
        # creating a button, that will send the units back
        screen.blit(back_button_image, (trench.rect.x, 0))
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x and pos[0] < trench.rect.x + base_size and pos[1] > 0 and pos[1] < base_size:
                send_units_back(trench.id, trench.current_owner)
        # drawing a drop down menu icon for showing the unit types in the trench
        if trench.show_menu == False:
            screen.blit(pygame.transform.rotate(down_arrow_image, 180), (trench.rect.x + base_size, base_size))
        else:
            screen.blit(down_arrow_image, (trench.rect.x + base_size, base_size))
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x + base_size and pos[0] < trench.rect.x + base_size*2 and pos[1] > base_size and pos[1] < base_size*2 and clicking == False:
                trench.show_menu = not trench.show_menu
                clicking = True
        else:
            clicking = False
        if trench.show_menu:
            show_trench_menu(trench.id, trench.rect.x, trench.types_in_trench)

    # creating a button, that will auto send all units coming through
    # this has to be outside of the main button loop, because it has to be shown at all times
    if trench.current_owner == "alied":
        # drawing the button
        if trench.auto_send:
            pygame.draw.rect(screen, (0, 255, 0), (trench.rect.x -base_size, base_size, base_size, base_size), base_size*2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (trench.rect.x-base_size, base_size, base_size, base_size), base_size*2)
        # checking if the button is clicked
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x - base_size and pos[0] < trench.rect.x and pos[1] > base_size and pos[1] < base_size*2 and clicking == False:
                trench.auto_send = not trench.auto_send
                clicking = True
        else:
            clicking = False

# function for the end screen after the game is over
def end_screen(winner):
    global running, clock, return_arrow_image, show_main_menu, font, base_size, current_level, current_nation
    end_screen = True
    font2 = pygame.font.Font(None, base_size*2 - int(base_size/2))
    while end_screen:
        screen.fill((255, 255, 255))
        #drawing the winner text
        text = font2.render(winner+" wins!", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()))
        # drawing two arrows, one for returning to the main menu and the other for exiting the game
        screen.blit(return_arrow_image, (width*0.4 - int(base_size/2), height/2))
        text = font.render("Exit to main menu", True, (0, 0, 0))
        screen.blit(text, (width*0.4 - text.get_width()/2, height/2 + base_size*2))
        screen.blit(pygame.transform.flip(return_arrow_image, True, False), (width*0.6 - int(base_size/2), height/2))
        text = font.render("Exit game", True, (0, 0, 0))
        screen.blit(text, (width*0.6 - text.get_width()/2, height/2 + base_size*2))
        # later some statistics about the game will be shown here
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_screen = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    end_screen = False
                    #reset_game(current_nation, current_level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > width*0.4 - int(base_size/2) and pos[0] < width*0.4 + int(base_size/2) and pos[1] > height/2 and pos[1] < height/2 + base_size:
                        current_nation = None
                        current_level = None
                        end_screen = False
                        show_main_menu = True
                    if pos[0] > width*0.6 - int(base_size/2) and pos[0] < width*0.6 + int(base_size/2) and pos[1] > height/2 and pos[1] < height/2 + base_size:
                        running = False
                        end_screen = False
        clock.tick(60)
        pygame.display.update()

# unit groups
allied_unit_group = pygame.sprite.Group()
enemy_unit_group = pygame.sprite.Group()
# unit images, more images will be added later, this is just for testing
unit_images_running_allies = None
unit_images_firing_allies = None
unit_images_running_enemies = None
unit_images_firing_enemies = None
# tank images
tank_images_allies = None
tank_images_enemies = None

# trenches
object_group = pygame.sprite.Group()
number_of_trenches = 1 # works as a unique id for the trenches
positions_of_trenches = []

# bullets
bullets = pygame.sprite.Group()
unit_bullet = pygame.transform.scale(pygame.image.load("assets/bullet.png"), (int(base_size/5), int(base_size/5)))
shot_sound = pygame.mixer.Sound("assets/gun_shot.mp3")

# flags
flags = pygame.sprite.Group()

# allies X enemies
alied = None
enemy = None
number_of_units = 0

# images used in the game and menu
menu_button_image = pygame.transform.scale(pygame.image.load("assets/menu.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
forward_button_image = pygame.transform.scale(pygame.image.load("assets/forward.png"), (base_size, base_size))
back_button_image = pygame.transform.scale(pygame.image.load("assets/back.png"), (base_size, base_size))
return_arrow_image = pygame.transform.scale(pygame.image.load("assets/back_arrow.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
down_arrow_image = pygame.transform.scale(pygame.image.load("assets/arrow_down.png"), (base_size, base_size))
square_image = pygame.transform.scale(pygame.image.load("assets/square.png"), (base_size, base_size))
gas = pygame.transform.scale(pygame.image.load("assets/gas.png"), (base_size, base_size))
bomb = pygame.transform.scale(pygame.image.load("assets/bomb.png"), (base_size, base_size))
actions = [gas, bomb]
special_actions = pygame.sprite.Group()
right_click_buttons = pygame.sprite.Group()
# setting up the enemy spawn thread 
enemy_control = threading.Thread(target=enemy_con)

# main loop
running = True
show_game_menu = False
font = pygame.font.Font(None, int(base_size/2 + base_size/4))
frame_rate = 60
time_to_add_money = 1 * frame_rate
enemy_time_to_add_money = 1 * frame_rate # maybe will be changed later
clicking = False # this is used to prevent buttons from being clicked multiple times in one click, if that makes sense
current_nation = None
current_level = None
while running:

    # showing the main menu
    if show_main_menu:
        main_menu_loop()

    # starting the enemy control thread
    if enemy_control.is_alive() == False:
        enemy_control.start()

    screen.fill((255, 255, 255))
    # drawing a line representing the border between ground and sky
    pygame.draw.line(screen, (0, 255, 0), (0, base_size*2), (width, base_size*2), int(base_size/10))
    # drawing the ground, later it will be image instead of a pygame.draw.rect
    pygame.draw.rect(screen, (20, 20, 50), (0, base_size*2, width, height-base_size*2)) # later will be brown, I have no idea what is its rgb value so I will do it later

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and show_game_menu == False or event.key == pygame.K_LEFT and show_game_menu == False:
                x_offset += int(base_size/2)
            if event.key == pygame.K_d and show_game_menu == False or event.key == pygame.K_RIGHT and show_game_menu == False:
                x_offset -=int( base_size/2)
            if event.key == pygame.K_LSHIFT:
                shift = True
            if event.key == pygame.K_r:
                #reset_game(current_nation, current_level)
                pass
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a  or event.key == pygame.K_d:
                x_offset = 0
            if event.key == pygame.K_LSHIFT:
                shift = False
        # handling the mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                # checking if the player clicked on a unit
                for unit in allied_unit_group:
                    if unit.rect.collidepoint(pos) and show_game_menu == False:
                        if unit in selected_units:
                            selected_units.remove(unit)
                            if shift == False:
                                selected_units.clear()
                        elif shift == False:
                            selected_units.clear()
                            selected_units.append(unit)
                        else:
                            selected_units.append(unit)
                # checking if the player clicked on one of the right click menu buttons
                if right_click_menu and show_game_menu == False:
                    for button in right_click_buttons:
                        if button.rect.collidepoint(pos):
                            if button.aliegance == "Send forward":
                                for unit in selected_units:
                                    send_a_unit_forward(unit.in_trench_id, "alied", unit.id)
                            if button.aliegance == "Send back":
                                for unit in selected_units:
                                    send_a_unit_back(unit.in_trench_id, "alied", unit.id)
                # checking if the player clicked on a buy button
                elif pos[1] > base_size*12 and show_game_menu == False:
                    for i in range(types_of_units):
                        if pos[0] > i * base_size*2 and pos[0] < (i + 1) * base_size*2:
                            buy(i, "alied")
                # checking if the drop down menu button in the top left corner is clicked
                elif pos[0] < base_size*2+int(base_size/2) and pos[1] < base_size*2+int(base_size/2):
                    show_game_menu = True
                # checking if some game menu option is clicked
                elif show_game_menu:
                    if pos[0] > width/2 - base_size*4 and pos[0] < width/2 + base_size*4 and pos[1] > height/2 - base_size and pos[1] < height/2 + base_size:
                        show_game_menu = False
                    if pos[0] > width/2 - base_size*4 and pos[0] < width/2 + base_size*4 and pos[1] > height/2 + base_size and pos[1] < height/2 + base_size*3:
                        show_main_menu = True
                        show_game_menu = False
                # checking if the player clicked on a special action button, will be done through classes and sprites later
                elif pos[0] > width - base_size*2 and pos[1] < base_size*2*types_of_special_actions and show_game_menu == False:
                    for i in range(types_of_special_actions):
                        if pos[1] > height - base_size*2 - (base_size*2)*i and pos[1] < height - base_size*2 - (base_size*2)*(i-1):
                            print("special action " + str(i) + " clicked") # for some reason doesnt work, will have to look into it
                            buy(i+types_of_units, "alied")
            # opening the right click menu
            if event.button == 3 and len(selected_units) > 0:
                if right_click_menu == False:
                    right_click_menu = True
                    # creating the buttons for the right click menu
                    menu_pos = pygame.mouse.get_pos()
                    right_click_buttons.empty()
                    right_click_buttons.add(Button(None,menu_pos[0], menu_pos[1]-base_size/2, base_size, base_size,forward_button_image, "Send forward", None))
                    right_click_buttons.add(Button(None,menu_pos[0]- base_size, menu_pos[1]-base_size/2 , base_size, base_size, back_button_image, "Send back", None))
                else:
                    right_click_menu = False
                    selected_units.clear()

    # updating the offset to applu to all the objects
    update_offset()

    # drawing the alied flag and updating its position, and the same for the enemy flag
    flags.draw(screen)

    # drawing the objects
    object_group.draw(screen)
    for object in object_group:
        object.update(allied_unit_group, enemy_unit_group)
        show_trench_commands(object) # replacement for the old show_trench_commands method in the class

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

    # drawing the bullets
    try:
        bullets.draw(screen)
    except:
        pass
    
    # updating the units images
    if show_game_menu == False:
        for unit in allied_unit_group:
            unit.update()
        for unit in enemy_unit_group:
            unit.update()

    # sorting the units based on their y position to create sort of a 3d effect(pun intended)
    allied_unit_group = pygame.sprite.Group(sorted(allied_unit_group, key=lambda x: x.rect.y))
    enemy_unit_group = pygame.sprite.Group(sorted(enemy_unit_group, key=lambda x: x.rect.y))

                       # UI
    # drawing buttons from the bottom left corner, based on the number of types of units
    if running: # running has to be checked, otherwise the game ends with an error if player tries to exit from the main menu
        for i in range(types_of_units):
            pygame.draw.rect(screen, (50, 50, 50), (i * base_size*2, height-base_size*2, base_size*2, base_size*2))
            screen.blit(pygame.transform.scale(square_image, (base_size*2,base_size*2)), (i * base_size*2, base_size*12)) # later will be a different image, since this one is not really fitting corectly
            # drawing the image of the unit to which the button corresponds
            if i <= 2:
                screen.blit(unit_images_firing_allies[i], (i * base_size*2 + int(base_size/2), base_size*12 + int(base_size/2)))
            elif i == 3:
                screen.blit(tank_images_allies[0], (i * base_size*2, base_size*12 ))
            # drawing the price of the unit on the bottom of the button
            text = font.render(str(prices[i]), True, (200, 0, 200))
            screen.blit(text, (i * base_size*2 + int(base_size/2 + text.get_width()/2), base_size*13 + text.get_height()))

    # drawing a drop down menu icon
    screen.blit(menu_button_image, (0, 0))

    # drawing the special actions menu from the bottom right corner
    for i in range(types_of_special_actions):
        pygame.draw.rect(screen, (50, 50, 50), (width - base_size*2, height - base_size*2 - (base_size*2)*i, base_size*2, base_size*2))
        screen.blit(pygame.transform.scale(square_image, (base_size*2,base_size*2)), (width - base_size*2, height - base_size*2 - (base_size*2)*i))# later will be a different image, since this one is not really fitting corectly
        text = font.render(str(prices[len(prices)-i-1]), True, (200, 0, 200))
        screen.blit(text, (width - base_size*2 + int(base_size/2 + text.get_width()/2), height -base_size - (base_size*2)*i + text.get_height()))
        screen.blit(actions[i], (width - base_size*2 + int(base_size/2), height - base_size*2 - (base_size*2)*i + int(base_size/2)))
        # images will be added later

    # drawing a fill bar in the top right, representing the progress of the battle
    progress_bar()
    
    # drawing the money and making sure it can always be seen
    pygame.draw.rect(screen, (50, 50, 50), (width/2 - base_size*2, 0, base_size*4, base_size/2))
    text = font.render(str(money)+ " money", True, (0, 0, 255))
    screen.blit(text, (width/2- text.get_width()/2, 0))

    # drawing the game menu
    if show_game_menu:
        pygame.draw.rect(screen, (50, 50, 50), (width/2 - base_size*4, height/2 -base_size, base_size*8, base_size*2))
        text = font.render("Resume", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - int(base_size/2-base_size/4 + text.get_height()/2)))
        pygame.draw.rect(screen, (50, 50, 50), (width/2 - base_size*4, height/2 + base_size, base_size*8, base_size*2))
        text = font.render("Exit to main menu", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 + base_size+int(base_size/2 + text.get_height()/2)))

    # moving the units
    if show_game_menu == False:
        for unit in allied_unit_group:
            unit.move()
            unit.fire(enemy_unit_group, allied_unit_group) # currently the firing is like a line of bullets, but later each unit will have its own firing rate
            # checking if the unit is firing, if so than spawning a bullet
            if unit.firing:
                bullet = Bullet("allied",unit_bullet, unit.rect.x, unit.rect.y, unit.fire_range)
                bullets.add(bullet)
            if unit in selected_units:
                highlight_unit(unit)
        for unit in enemy_unit_group:
            unit.move()
            unit.fire(enemy_unit_group, allied_unit_group)
            # checking if the unit is firing, if so than spawning a bullet
            if unit.firing:
                bullet = Bullet("enemy",unit_bullet, unit.rect.x, unit.rect.y, unit.fire_range)
                bullets.add(bullet)
                #shot_sound.play()

    # moving the bullets
    for bullet in bullets:
        try:
            if bullet.direction !=0: # this ensures than only completely spawned bullet objects can move, if this isnt done, than the game has a high chance of error
                bullet.move()
        except:
            pass
        # checking if the bullet is out of its range, if so than removing it
        if bullet.range <= 0:
            bullets.remove(bullet)

    # checking if the units are dead and removing them
    for unit in allied_unit_group:
        if unit.health <= 0:
            allied_unit_group.remove(unit)
            if unit in selected_units:
                selected_units.remove(unit)
    for unit in enemy_unit_group:
        if unit.health <= 0:
            enemy_unit_group.remove(unit)
            if unit in selected_units:
                selected_units.remove(unit)

    # in case the right click menu is open, then showing the menu, will be enhanced later
    if right_click_menu:
        pygame.draw.circle(screen, (50, 50, 50), menu_pos, base_size)
        right_click_buttons.draw(screen)
        
    # checking if at least one unit is selected, if not than there is no point in having the right click menu open
    if len(selected_units) == 0:
        right_click_menu = False
    
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
            end_screen("alied")
            break
    for unit in enemy_unit_group:
        if unit.rect.x < alied_flag.rect.x + unit.rect.width:
            end_screen("enemy")
            break

    # adding the money once per second
    if show_game_menu == False:
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