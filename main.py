import pygame
import random
import threading
import json
from classes import *

pygame.init()
width, height = 1400, 700
pygame.display.set_caption("Over the Top")
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))# yes I know its from ww2, but it looks cool, maybe I will change it later
clock = pygame.time.Clock()
level_width = None
base_size = width/10 # will later be used for scaleability of the window
# important variables
types_of_units = 4
x_offset = 0
money = None
enemy_money = None
show_main_menu = True
shift = False
right_click_menu = False
menu_pos = (0, 0)
selected_units = []
prices = [5, 10, 20, 50] # maybe this will be loaded from a json file later

# loading the data from the json file
def load_data_json(type):
    global money, level_width, positions_of_trenches, alied, enemy, enemy_money
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
        with open("levels/level_" + str(type) + ".json", "r") as file:
            data = json.load(file)
            money = data["money"]
            level_width = data["level_width"]
            positions_of_trenches = data["positions_of_trenches"]
            alied = data["allied"]
            enemy = data["enemy"]
        file.close()

# function that loads the selected images and sets up the level, for now only flags
def setup_level():
    global alied_flag, enemy_flag, object_group, flags, positions_of_trenches, number_of_trenches, level_width, unit_images_running_allies, unit_images_firing_allies, tank_images_allies, unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies
    # loading the images, this will later be done based on who is fighting who, you can see this in the json file
    if alied == "default":
        alied_flag = Flag("alied", pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/default_flag1.png"), (100, 100)), True, False), level_width, height)
        flags.add(alied_flag)
        unit_images_running_allies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_1.png"), (50, 50)), pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_2.png"), (50, 50))] # later more running images will be made
        unit_images_firing_allies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1.png"), (50, 50)),pygame.transform.scale(pygame.image.load("assets/default_unit_2.png"), (50, 50)),pygame.transform.scale(pygame.image.load("assets/default_unit_3.png"), (50, 50))] # the firing images are the ones used in the trenches, maybe this will change later
        tank_images_allies = [pygame.transform.scale(pygame.image.load("assets/tank.png"), (100, 100))]
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
        enemy_flag = Flag("enemy", pygame.transform.scale(pygame.image.load("assets/default_flag2.png"), (100, 100)), level_width, height)
        flags.add(enemy_flag)
        unit_images_running_enemies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_1.png"), (50, 50)), pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_2.png"), (50, 50))]
        unit_images_firing_enemies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1.png"), (50, 50)),pygame.transform.scale(pygame.image.load("assets/default_unit_2.png"), (50, 50)),pygame.transform.scale(pygame.image.load("assets/default_unit_3.png"), (50, 50))] # the firing image is the one used in the trenches, maybe this will change later
        tank_images_enemies = [pygame.transform.scale(pygame.image.load("assets/tank.png"), (100, 100))]
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
        trench = Trench(positions_of_trenches[i], number_of_trenches)
        object_group.add(trench)
        number_of_trenches += 1

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
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - 25  + text.get_height()/2))
        text = font.render("Levels", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 + 125 + text.get_height()/2))
        text = font.render("Exit", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 + 275 + text.get_height()/2))
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
                        load_data_json("endless")
                        setup_level()
                    if pos[1] > height/2 + 100 and pos[1] < height/2 + 200:
                        show_main_menu = False
                        nation_pick_menu()
                    if pos[1] > height/2 + 250 and pos[1] < height/2 + 350:
                        running = False
                        show_main_menu = False
        pygame.display.update()

# function for picking the nation in case player wants to play the campaign
def nation_pick_menu():
    global clock, running
    nation_pick_window = True
    nation_buttons = pygame.sprite.Group()
    # getting the number of nations in the game from the json file
    with open("levels/Info.json", "r") as file:
        data = json.load(file)
        number_of_nations = data["number_of_nations"]
        names_of_nations = data["names_of_nations"]
    file.close()
    # creating the buttons for each nation
    index = 0
    line_height = 100
    previous_button_position = 0
    for i in range(number_of_nations):
        if index == 5:
            index = 0
            line_height += 300
            previous_button_position = 0
        button = Button(i+1, width/20 + previous_button_position+ width/10, line_height, 200, 100, None, names_of_nations[i])
        nation_buttons.add(button)
        previous_button_position = button.rect.x
        index += 1
    while nation_pick_window:
        screen.fill((255, 255, 255))

        nation_buttons.draw(screen)

        #drawing the text on the buttons, later image will propably be enough
        for button in nation_buttons:
            text = font.render(str(button.aliegance), True, (255, 255, 255))
            screen.blit(text, (button.rect.x + 100-text.get_width()/2, button.rect.y + 50 - text.get_height()/2))

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
    global font, running, clock
    choice_menu = True
    #print(number_of_levels)
    level_choice_buttons = pygame.sprite.Group() # I chose to use a sprite group, because it will be easier to handle the drawing and clicking of the buttons
            # drawing the level buttons, they are organized in rows of 5, for now
    index = 0
    line_height = 100
    previous_button_position = 0
    for i in range(number_of_levels):
        if index == 5:
            index = 0
            line_height += 300
            previous_button_position = 0
        button = Button(i+1, width/20 + previous_button_position+ width/10, line_height, 100, 100, None, aliegance) # here I will later pass in the flag of the nation as an image
        level_choice_buttons.add(button)
        previous_button_position = button.rect.x
        index += 1

    while choice_menu:
        screen.fill((255, 255, 255))
        # drawing the buttons
        level_choice_buttons.draw(screen)
        for button in level_choice_buttons:
            # drawing the text on the buttons
            text = font.render(str(button.level), True, (255, 255, 255))
            screen.blit(text, (button.rect.x + 50-text.get_width()/2, button.rect.y + 50 - text.get_height()/2))
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
                        load_data_json(button.level)
                        setup_level()

        clock.tick(60)
        pygame.display.update()

# function that resets the game
def reset_game():
    global allied_unit_group, enemy_unit_group, object_group, money, enemy_money, show_game_menu, show_main_menu, selected_units, right_click_menu
    allied_unit_group.empty()
    enemy_unit_group.empty()
    object_group.empty()
    money = None
    enemy_money = None
    show_game_menu = False
    selected_units.clear()
    right_click_menu = False

# enemy control function this is a basic version of the enemy control, will be enhanced later, for now it works as intended
# is currently capable of winning the game
# I will later create different levels and different types of enemy control, this is currently the dummy version
def enemy_con():
    global running, object_group, allied_unit_group, enemy_unit_group, show_game_menu, show_main_menu
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
                if unit.rect.x > enemy_flag.rect.x - 200:
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

            #print(trench_positions)
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
    pygame.draw.rect(screen, (0, 0, 0), (unit.rect.x - 5, unit.rect.y - 5, unit.rect.width + 10, unit.rect.height + 10), 5)

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
    global money, allied_unit_group, enemy_money, enemy_unit_group, tank_images_allies, enemy_flag, alied_flag, number_of_units, unit_images_running_allies, unit_images_firing_allies, unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies, prices
    number_of_units += 1
    if owner == "alied" and money >= 5:
        if unit_type == 0:
            unit = Unit(0, "alied", unit_images_running_allies, unit_images_firing_allies, enemy_flag, alied_flag, number_of_units)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
        if unit_type == 1 and money >= 10:
            unit = Unit(1, "alied", unit_images_running_allies, unit_images_firing_allies, enemy_flag, alied_flag, number_of_units)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
        if unit_type == 2 and money >= 20:
            unit = Unit(2, "alied", unit_images_running_allies, unit_images_firing_allies, enemy_flag, alied_flag, number_of_units)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
        if unit_type == 3 and money >= 50:
            unit = tank("alied", 3, tank_images_allies, enemy_flag, alied_flag, number_of_units)
            allied_unit_group.add(unit)
            money -= prices[unit_type]
    elif owner == "enemy":
        if unit_type == 0 and enemy_money >= 5:
            unit = Unit(0, "enemy", unit_images_running_enemies, unit_images_firing_enemies, enemy_flag, alied_flag, number_of_units)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]
        if unit_type == 1 and enemy_money >= 10:
            unit = Unit(1, "enemy", unit_images_running_enemies, unit_images_firing_enemies, enemy_flag, alied_flag, number_of_units)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]
        if unit_type == 2 and enemy_money >= 20:
            unit = Unit(2, "enemy", unit_images_running_enemies, unit_images_firing_enemies, enemy_flag, alied_flag, number_of_units)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]
        if unit_type == 3 and enemy_money >= 50:
            unit = tank("enemy", 3, tank_images_enemies, enemy_flag, alied_flag, number_of_units)
            enemy_unit_group.add(unit)
            enemy_money -= prices[unit_type]

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
    global font
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

# function to show trench commands(originaly this was in the class it self, but I had to redo it here because the drawing cant be done from another file)
def show_trench_commands(trench):
    global show_game_menu, forward_button_image, back_button_image
    # if there is at least one unit in the trench, control buttons will appear above the trench
    if trench.units_in_trench > 0 and trench.current_owner == "alied":
        screen.blit(forward_button_image, (trench.rect.x, 50))
        # if the button is clicked, the units will leave the trench
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x and pos[0] < trench.rect.x + 50 and pos[1] > 50 and pos[1] < 100:
                send_units_forward(trench.id, trench.current_owner, None)
        # creating a button, that will send the units back
        screen.blit(back_button_image, (trench.rect.x, 0))
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x and pos[0] < trench.rect.x + 50 and pos[1] > 0 and pos[1] < 50:
                send_units_back(trench.id, trench.current_owner)
        # creating a drop down menu button, that will show all the unit types in the trench
        pygame.draw.rect(screen, (50, 50, 50), (trench.rect.x +50, 50, 50, 50))
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x + 50 and pos[0] < trench.rect.x + 100 and pos[1] > 50 and pos[1] < 100:
                trench.show_menu = True
        if trench.show_menu:
            show_trench_menu(trench.id, trench.rect.x, trench.types_in_trench)

    # creating a button, that will auto send all units coming through
    # this has to be outside of the main button loop, because it has to be shown at all times
    if trench.current_owner == "alied":
        # drawing the buttons
        #if autosend is false than lowering the visibility of the button
        if trench.auto_send:
            pygame.draw.rect(screen, (0, 255, 0), (trench.rect.x -50, 50, 50, 50), 100)
        else:
            pygame.draw.rect(screen, (0, 150, 0), (trench.rect.x-50, 50, 50, 50), 100)
        # checking if the button is clicked
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x - 50 and pos[0] < trench.rect.x and pos[1] > 50 and pos[1] < 100:
                trench.auto_send = True
        #drawing the stop button
        #if autosend is true than lowering the visibility of the button
        if trench.auto_send:
            pygame.draw.rect(screen, (150, 0, 0), (trench.rect.x-100, 50, 50, 50), 100)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (trench.rect.x-100, 50, 50, 50))
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x - 100 and pos[0] < trench.rect.x - 50 and pos[1] > 50 and pos[1] < 100:
                trench.auto_send = False

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
unit_bullet = pygame.transform.scale(pygame.image.load("assets/bullet.png"), (10, 10))

# flags
flags = pygame.sprite.Group()

# allies X enemies
alied = None
enemy = None
number_of_units = 0

# images used in the game and menu
menu_button_image = pygame.transform.scale(pygame.image.load("assets/menu.png"), (75, 75))
forward_button_image = pygame.transform.scale(pygame.image.load("assets/forward.png"), (50, 50))
back_button_image = pygame.transform.scale(pygame.image.load("assets/back.png"), (50, 50))

# setting up the enemy spawn thread 
enemy_control = threading.Thread(target=enemy_con)

# main loop
running = True
show_game_menu = False
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
            if event.key == pygame.K_a and show_game_menu == False or event.key == pygame.K_LEFT and show_game_menu == False:
                x_offset += 25
            if event.key == pygame.K_d and show_game_menu == False or event.key == pygame.K_RIGHT and show_game_menu == False:
                x_offset -= 25
            if event.key == pygame.K_LSHIFT:
                shift = True
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
                    if pos[0] > menu_pos[0] + 15 and pos[0] < menu_pos[0] + 45 and pos[1] > menu_pos[1] - 15 and pos[1] < menu_pos[1] + 15:
                        #print("sending selected units forward")
                        for unit in selected_units:
                            send_a_unit_forward(unit.in_trench_id, "alied", unit.id)
                    if pos[0] > menu_pos[0] - 45 and pos[0] < menu_pos[0] - 15 and pos[1] > menu_pos[1] - 15 and pos[1] < menu_pos[1] + 15:
                        #print("sending selected units back")
                        for unit in selected_units:
                            send_a_unit_back(unit.in_trench_id, "alied", unit.id)
                # checking if the player clicked on a buy button
                elif pos[1] > 600 and show_game_menu == False:
                    for i in range(types_of_units):
                        if pos[0] > i * 100 and pos[0] < (i + 1) * 100:
                            buy(i, "alied")
                # checking if the drop down menu button in the top left corner is clicked
                elif pos[0] < 75 and pos[1] < 75:
                    show_game_menu = True
                # checking if some game menu option is clicked
                elif show_game_menu:
                    if pos[0] > width/2 - 200 and pos[0] < width/2 + 200 and pos[1] > height/2 - 50 and pos[1] < height/2 + 50:
                        show_game_menu = False
                    if pos[0] > width/2 - 200 and pos[0] < width/2 + 200 and pos[1] > height/2 + 50 and pos[1] < height/2 + 150:
                        show_main_menu = True
                        show_game_menu = False
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
            pygame.draw.rect(screen, (50, 50, 50), (i * 100, 600, 100, 100))
            # drawing the image of the unit to which the button corresponds
            #print(i)
            if i <= 2:
                screen.blit(unit_images_firing_allies[i], (i * 100 + 25, 600 + 25))
            elif i == 3:
                screen.blit(tank_images_allies[0], (i * 100, 600 ))
            # drawing the price of the unit on the bottom of the button
            text = font.render(str(prices[i]), True, (200, 0, 200))
            screen.blit(text, (i * 100 + 25 + text.get_width()/2, 650 + text.get_height()))

    # drawing a drop down menu icon
    screen.blit(menu_button_image, (0, 0))

    # drawing the selection menu in the bottom right corner, for now also only a square
    pygame.draw.rect(screen, (50, 50, 50), (1300, 600, 100, 100))

    # drawing a fill bar in the top right, representing the progress of the battle
    progress_bar()
    
    # drawing the money
    text = font.render(str(money)+ " money", True, (0, 0, 0))
    screen.blit(text, (width/2- text.get_width()/2, 0))

    # drawing the game menu
    if show_game_menu:
        pygame.draw.rect(screen, (50, 50, 50), (width/2 - 200, height/2 -50, 400, 100))
        text = font.render("Resume", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - 25 + text.get_height()/2))
        pygame.draw.rect(screen, (50, 50, 50), (width/2 - 200, height/2 + 50, 400, 100))
        text = font.render("Exit to main menu", True, (0, 0, 0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 + 75 + text.get_height()/2))

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
        pygame.draw.circle(screen, (50, 50, 50), menu_pos, 50)
        # drawing a small red rectangle representing a forward button, that will send the selected units forward
        pygame.draw.rect(screen, (255, 0, 0), (menu_pos[0]+15 , menu_pos[1] - 15, 30, 30))
        # drawing a small blue rectangle representing a back button, that will send the selected units back
        pygame.draw.rect(screen, (0, 0, 255), (menu_pos[0] - 45, menu_pos[1] - 15, 30, 30))

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
            show_main_menu = True
            reset_game()
            break
    for unit in enemy_unit_group:
        if unit.rect.x < alied_flag.rect.x + unit.rect.width:
            show_main_menu = True
            reset_game()
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