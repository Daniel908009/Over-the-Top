import pygame
import random
import threading
import json
from classes import *
from pygame import mixer

pygame.init()
width, height = 1400, 700
pygame.display.set_caption("Over the Top")
screen = pygame.display.set_mode((width, height)) #, pygame.RESIZABLE) # resizability will be done later
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
clock = pygame.time.Clock()
level_width = None
base_size = int(width/28) # is used for scalability of the window
#print(base_size)
# important variables
allied_types_of_units = 0
enemy_types_of_units = 0
allied_types_of_special_actions = 0
enemy_types_of_special_actions = 0 # will be fully implemented later
types_of_special_actions = None
x_offset = 0
money = None
enemy_money = None
show_main_menu = True
shift = False
right_click_menu = False
menu_pos = (0, 0)
selected_units = []
allied_prices = []
enemy_prices = []
allied_units_stats= {
    "health": [],
    "damage": [],
    "speed": [],
    "range": [],
    "reload_time": []
}
enemy_units_stats= {
    "health": [],
    "damage": [],
    "speed": [],
    "range": [],
    "reload_time": []
}

# loading the data from the json file
def load_data_json(type, nation):
    global money, level_width, positions_of_trenches, alied, enemy, enemy_money, current_nation, current_level
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

# loading the images based on the nation
def load_units(nation, alied_or_enemy):
    global allied_troop_list , enemy_troop_list
    # loading the troop_types.json file and getting the specific images and stats for the nation
    with open("levels/troop_types.json", "r") as file:
        data = json.load(file)
        troop_types_data = data[nation]
    file.close()
    if alied_or_enemy == "alied":
        allied_troop_list = troop_types_data
        global allied_prices, allied_types_of_units, allied_types_of_special_actions, allied_units_stats
        for unit in allied_troop_list:
            if unit["type"] != "special":
                allied_prices.append(unit["cost"])
                allied_units_stats["health"].append(unit["health"])
                allied_units_stats["damage"].append(unit["damage"])
                allied_units_stats["speed"].append(unit["speed"])
                allied_units_stats["range"].append(unit["range"]*base_size) # has to be multiplied by the base size, because the range is in squares so it works in different sized windows
                allied_units_stats["reload_time"].append(unit["reload_time"])
            else:
                allied_types_of_special_actions = unit["special_actions"]
                # getting all the special actions prices
                prices = unit["prices"]
                for i in range(allied_types_of_special_actions):
                    allied_prices.append(prices[i]["price"])
        for unit in allied_troop_list:
            allied_types_of_units += 1
        allied_types_of_units -= 1
    elif alied_or_enemy == "enemy":
        enemy_troop_list = troop_types_data
        global enemy_prices, enemy_types_of_units, enemy_types_of_special_actions, enemy_units_stats
        for unit in enemy_troop_list:
            if unit["type"] != "special":
                enemy_prices.append(unit["cost"])
                enemy_units_stats["health"].append(unit["health"])
                enemy_units_stats["damage"].append(unit["damage"])
                enemy_units_stats["speed"].append(unit["speed"])
                enemy_units_stats["range"].append(unit["range"]*base_size)
                enemy_units_stats["reload_time"].append(unit["reload_time"])
            else:
                enemy_types_of_special_actions = unit["special_actions"]
                # getting all the special actions prices
                prices = unit["prices"]
                #print(prices[0]["price"])
                for i in range(enemy_types_of_special_actions):
                    enemy_prices.append(prices[i]["price"])
        for unit in enemy_troop_list:
            enemy_types_of_units += 1
        enemy_types_of_units -= 1

# loading the images based on the nation
def load_images(nation, alied_or_enemy):
    global base_size
    unit_size = base_size*1.2 # I will try to make the units the best size possible, so I will use this variable
    # getting the images from a json file
    with open("levels/troop_types.json", "r") as file:
        data = json.load(file)
        nation_data = data[nation]
    file.close()
    # now putting the images in their respective lists
    if alied_or_enemy == "alied":
        global unit_images_running_allies, unit_images_firing_allies, tank_images_allies
        for unit in nation_data:
            if unit["type"] != "special" and unit["type"] != "tank":
                #print(unit["running_image"][0])
                unit_images_running_allies.append([])
                #print(unit_images_running_allies)
                for i in range(len(unit["running_image"])):
                    unit_images_running_allies[int(unit["type"])].append(pygame.transform.scale(pygame.image.load(unit["running_image"][i]), (unit_size, unit_size)))
                unit_images_firing_allies.append(pygame.transform.scale(pygame.image.load(unit["firing_image"]), (unit_size, unit_size)))
            elif unit["type"] == "tank":
                tank_images_allies.append(pygame.transform.scale(pygame.image.load(unit["running_image"]), (base_size*2, base_size*2)))
            else:
                pass
                # will be done later, when I have some images for the special actions like the gas
    elif alied_or_enemy == "enemy":
        global unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies
        for unit in nation_data:
            if unit["type"] != "special" and unit["type"] != "tank":
                unit_images_running_enemies.append([])
                for i in range(len(unit["running_image"])):
                    unit_images_running_enemies[int(unit["type"])].append(pygame.transform.scale(pygame.image.load(unit["running_image"][i]), (unit_size, unit_size)))
                unit_images_firing_enemies.append(pygame.transform.scale(pygame.image.load(unit["firing_image"]), (unit_size, unit_size)))
            elif unit["type"] == "tank":
                tank_images_enemies.append(pygame.transform.scale(pygame.image.load(unit["running_image"]), (base_size*2, base_size*2)))
            else:
                pass
                # will be done later, when I have some images for the special actions like the gas

# function that loads the selected images and sets up the level, for now only flags
def setup_level():
    global alied_flag, enemy_flag, object_group, flags, positions_of_trenches, number_of_trenches, level_width, unit_images_running_allies, unit_images_firing_allies, tank_images_allies, unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies, base_size
    # loading the images, this will later be done based on who is fighting who, you can see this in the json file
    if alied == "default":
        alied_flag = Flag("alied", pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/default_flag1.png"), (base_size*2, base_size*2)), True, False), level_width, height)
        flags.add(alied_flag)
        # calling the load images function
        #print("loading images")
        load_units("default", "alied")
        load_images("default", "alied")# I will do the setup in two functions, like this, just to make it more simple to read 
        #unit_images_running_allies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_1.png"), (unit_size, unit_size)), pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_2.png"), (unit_size, unit_size))] # later more running images will be made
        #unit_images_firing_allies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1.png"), (unit_size, unit_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_2.png"), (unit_size, unit_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_3.png"), (unit_size, unit_size)), pygame.transform.scale(pygame.image.load("assets/default_unit_4.png"), (unit_size, unit_size))] # the firing images are the ones used in the trenches, maybe this will change later
        #tank_images_allies = [pygame.transform.scale(pygame.image.load("assets/tank.png"), (base_size*2, base_size*2))]
    elif alied == "british":
        pass
    elif alied == "germans":
        pass
    elif alied == "french": # this is currently here just for testing purposes, because I need to see how the flags on the units look and I will try to differentiate them somehow
        alied_flag = Flag("alied", pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/default_flag1.png"), (base_size*2, base_size*2)), True, False), level_width, height)
        flags.add(alied_flag)
        #unit_images_running_allies = [pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_1.png"), (unit_size, unit_size)), pygame.transform.scale(pygame.image.load("assets/default_unit_1_running_2.png"), (unit_size, unit_size))]
        #unit_images_firing_allies = [pygame.transform.scale(pygame.image.load("assets/french_unit_1.png"), (unit_size, unit_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_2.png"), (unit_size, unit_size)),pygame.transform.scale(pygame.image.load("assets/default_unit_3.png"), (unit_size, unit_size))]
        #tank_images_allies = [pygame.transform.scale(pygame.image.load("assets/tank.png"), (base_size*2, base_size*2))]
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
        load_units("default", "enemy")
        load_images("default", "enemy")
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
    # turning the enemy control on
    global enemy_running
    enemy_running = True

# main menu function
def main_menu_loop():
    global show_main_menu, font, running, base_size, clock, soldiers_image
    previous_button_position = 0
    difference_in_height = base_size*3
    buttons = pygame.sprite.Group()
    # creating the buttons
    button = Button(1, width/2 - base_size*5, height/2 - base_size*4, base_size*10, base_size*2, None, "Testing", (50, 50, 50))
    buttons.add(button)
    previous_button_position = height/2 - base_size*4
    button = Button(2, width/2 - base_size*5, previous_button_position + difference_in_height, base_size*10, base_size*2, None, "Campaign", (50, 50, 50))
    buttons.add(button)
    previous_button_position += difference_in_height
    button = Button(3, width/2 - base_size*5, previous_button_position + difference_in_height, base_size*10, base_size*2, None, "Settings", (50, 50, 50))
    buttons.add(button)# settings will be comming soon
    previous_button_position += difference_in_height
    button = Button(4, width/2 - base_size*5, previous_button_position +difference_in_height, base_size*10, base_size*2, None, "Exit", (50, 50, 50))
    buttons.add(button)
    previous_button_position += difference_in_height 
    while show_main_menu:
        screen.fill((255, 255, 255))
        # drawing three main buttons and their text
        buttons.draw(screen)
        for button in buttons:
            text = font.render(str(button.aliegance), True, (0, 0, 0))
            screen.blit(text, (button.rect.x + base_size*5 - text.get_width()/2, button.rect.y + base_size - text.get_height()/2))

        # comming soon sign over the settings button
        screen.blit(pygame.transform.scale(comming_soon, (base_size*4, base_size*2)), (width/2 - base_size*5, height/2 - base_size*4 + difference_in_height*2))

        # drawing the soldiers image, since I dont have any idea for a good background image
        screen.blit(soldiers_image, (width/2 - base_size*14, height/2 - base_size*2))
        screen.blit(soldiers_image, (width/2 + base_size*14-soldiers_image.get_width(), height/2 - base_size*2))

        # event handling
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
                            elif button.level == 2:
                                show_main_menu = False
                                nation_pick_menu()
                            elif button.level == 3:
                                print("settings") # later will be tkinter window
                            elif button.level == 4:
                                running = False
                                show_main_menu = False
        clock.tick(60)
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
        status_of_nations = data["status_of_nations"]
    file.close()
    number_of_nations = len(names_of_nations)
    # creating the buttons for each nation
    index = 0
    line_height = base_size*2
    previous_button_position = 0
    flags = []
    y_offset = 0
    for i in range(number_of_nations):
        if index == 5:
            index = 0
            line_height += base_size*6
            previous_button_position = 0
        if status_of_nations[i] == "Open":
            flags.append(pygame.transform.scale(pygame.image.load(flags_of_nations[i]), (base_size*4, base_size*2)))
        else:
            flags.append(pygame.transform.scale(comming_soon, (base_size*4, base_size*2)))
        button = Button(i+1, width/20 + previous_button_position+ width/10-base_size+int(base_size/10), line_height, base_size*4.2, base_size*4, buy_button, names_of_nations[i], None)
        nation_buttons.add(button)
        previous_button_position = button.rect.x + base_size
        index += 1
    while nation_pick_window:
        screen.fill((255, 255, 255))

        nation_buttons.draw(screen)
        for button in nation_buttons:
            button.y_offset(y_offset)

        #drawing the text on the buttons, later image will propably be enough
        for button in nation_buttons:
            text = font.render(str(button.aliegance), True, (0, 0, 0))
            screen.blit(text, (button.rect.x + base_size*2-text.get_width()/2, button.rect.y + base_size*3+int(base_size/2) - text.get_height()/2))
            # drawing the flag on the button
            screen.blit(flags[button.level-1], (button.rect.x+base_size/5-base_size/10, button.rect.y+base_size/2))
            # drawing rectangles around the flags, to make them better visible
            pygame.draw.rect(screen, (0, 0, 0), (button.rect.x+base_size/5-base_size/10, button.rect.y+base_size/2, base_size*4, base_size*2), 2)

        #drawing the return arrow
        screen.blit(return_arrow_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                nation_pick_window = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in nation_buttons:
                        if button.rect.collidepoint(pos) and status_of_nations[button.level-1] == "Open":
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
    global object_group, allied_unit_group, enemy_unit_group, bullets, flags, number_of_units, number_of_trenches, right_click_buttons, screen, aim_image
    object_group.empty()
    allied_unit_group.empty()
    enemy_unit_group.empty()
    right_click_buttons.empty()
    bullets.empty()
    flags.empty()
    number_of_units = 0
    number_of_trenches = 0
    # clearing image lists
    global unit_images_running_allies, unit_images_firing_allies, tank_images_allies, unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies
    unit_images_running_allies = []
    unit_images_firing_allies = []
    tank_images_allies = []
    unit_images_running_enemies = []
    unit_images_firing_enemies = []
    tank_images_enemies = []
    # clearing the stats
    global allied_units_stats, enemy_units_stats
    allied_units_stats = {
        "health": [],
        "damage": [],
        "speed": [],
        "range": [],
        "reload_time": []
    }
    enemy_units_stats = {
        "health": [],
        "damage": [],
        "speed": [],
        "range": [],
        "reload_time": []
    }
    global allied_prices, enemy_prices
    allied_prices = []
    enemy_prices = []
    global allied_types_of_units, enemy_types_of_units, allied_types_of_special_actions, enemy_types_of_special_actions
    allied_types_of_units = 0
    enemy_types_of_units = 0
    allied_types_of_special_actions = 0
    enemy_types_of_special_actions = 0

    # getting the new size and width of the window, and resizing the base_size and all the images
    #global width, height,base_size, back_button_image, down_arrow_image, forward_button_image, return_arrow_image, square_image, menu_button_image, buy_button
    #base_size = int(width/28) # will later have to be adjusted, since currently changing anything about this causes errors
    #menu_button_image = pygame.transform.scale(pygame.image.load("assets/menu.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
    #forward_button_image = pygame.transform.scale(pygame.image.load("assets/forward.png"), (base_size, base_size))
    #back_button_image = pygame.transform.scale(pygame.image.load("assets/back.png"), (base_size, base_size))
    #return_arrow_image = pygame.transform.scale(pygame.image.load("assets/back_arrow.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
    #down_arrow_image = pygame.transform.scale(pygame.image.load("assets/arrow_down.png"), (base_size, base_size))
    #square_image = pygame.transform.scale(pygame.image.load("assets/square.png"), (base_size, base_size))
    #buy_button = pygame.transform.scale(pygame.image.load("assets/buy_button.png"), (base_size*2, base_size))
    #aim_image = pygame.transform.scale(pygame.image.load("assets/aim.png"), (base_size*2, base_size*2))
    # resetting all the menus and screen, important variables
    #global show_game_menu, show_main_menu, right_click_menu, x_offset
    #right_click_menu = False
    #show_game_menu = False
    #if nation == None and level == None:
    #    show_main_menu = True
    #x_offset = 0
    # resizing the screen
    #if width != screen.get_width() or height != screen.get_height():
    #    width, height = screen.get_size()
    #    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    # if the reset comes from the game, then reloading the level
    #if nation != None and level != None:
    #    load_data_json(level, nation)
    #    setup_level()

# enemy control function this is a basic version of the enemy control, will be enhanced later, for now it works as intended
# is currently capable of winning the game
# I will later create different levels and different types of enemy control, this is currently the dummy version
def enemy_con():
    global running, object_group, allied_unit_group, enemy_unit_group, show_game_menu, show_main_menu, base_size, enemy_types_of_units, enemy_running
    can_buy = True
    # creating a 2d array that resembles the trench positions and who owns them
    trench_positions = []
    for trench in object_group:
        trench_positions.append([trench.rect.x, trench.current_owner, trench.id, trench.units_in_trench, trench.current_owner])
    # sorting the trench positions based on the id from the biggest to the smallest
    trench_positions = sorted(trench_positions, key=lambda x: x[2], reverse=True)
    while running:
        if show_game_menu == False and show_main_menu == False and enemy_running:
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
            if can_buy and enemy_running:
                buy(random.randint(0,enemy_types_of_units), "enemy")
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
                    send_units_forward(trench[2], "enemy", None,None)
                
                # checking if there is at least ten units in the enemy owned trenches, if not then sending all the units from the closest enemy owned trench
                if next_trench[1] == "enemy" and trench[1] == "enemy" and next_trench[3] < 10:
                    #print("sending units from trench " + str(trench[2]) + " to trench " + str(next_trench[2])+" because there are only " + str(next_trench[3]) + " units in the trench")
                    send_units_forward(trench[2], "enemy", None, None)
                
                # checking if the enemy has a number advantage compared to the alied trench, if so then sending all units to atack
                if next_trench[1] == "alied" and trench[1] == "enemy" and next_trench[3] < trench[3]:
                    #print("sending units from trench " + str(trench[2]) + " to trench " + str(next_trench[2])+" because the enemy has a number advantage")
                    send_units_forward(trench[2], "enemy", None, None)

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
    global money, allied_unit_group, enemy_money, enemy_unit_group, tank_images_allies, enemy_flag, alied_flag, number_of_units, unit_images_running_allies, unit_images_firing_allies, unit_images_running_enemies, unit_images_firing_enemies, tank_images_enemies, allied_prices, enemy_prices, allied_units_stats, enemy_units_stats, base_size, aiming
    number_of_units += 1
    if owner == "alied" and money >= allied_prices[unit_type]:
        if unit_type < allied_types_of_units- 1:
            #print(unit_images_firing_allies[unit_type])
            unit = Unit(unit_type, "alied", unit_images_running_allies[unit_type], unit_images_firing_allies[unit_type], enemy_flag, alied_flag, number_of_units, base_size, allied_units_stats["health"][unit_type], allied_units_stats["damage"][unit_type], allied_units_stats["range"][unit_type], allied_units_stats["reload_time"][unit_type], allied_units_stats["speed"][unit_type])
            allied_unit_group.add(unit)
            money -= allied_prices[unit_type]
        elif unit_type == allied_types_of_units-1 and money >= allied_prices[unit_type]:
            unit = tank("alied", allied_types_of_units, tank_images_allies, enemy_flag, alied_flag, number_of_units,base_size, allied_units_stats["health"][unit_type], allied_units_stats["damage"][unit_type], allied_units_stats["range"][unit_type], allied_units_stats["reload_time"][unit_type], allied_units_stats["speed"][unit_type])
            allied_unit_group.add(unit)
            money -= allied_prices[unit_type]
        # this will maybe be done some other way, because it depends on the fact that there is two of them, which might not be true in the future
        # will have to be reworked
        elif unit_type == allied_types_of_units+1 and money >= allied_prices[unit_type]:
            #special = Gas(x, y, image) # will be implemented later, when I have some image for it, and when I have some way of getting the x and y for destination
            #special_actions.add(special)
            money -= allied_prices[unit_type]
            print("gas")
            aiming = True
        elif unit_type == allied_types_of_units and money >= allied_prices[unit_type]:
            #special = Artillery( x, y, image)
            #special_actions.add(special)
            money -= allied_prices[unit_type]
            print("artillery")
            aiming = True
    elif owner == "enemy":
        if unit_type < enemy_types_of_units-1 and enemy_money >= enemy_prices[unit_type]:
            #print(unit_images_firing_enemies[unit_type])
            unit = Unit(unit_type, "enemy", unit_images_running_enemies[unit_type], unit_images_firing_enemies[unit_type], enemy_flag, alied_flag, number_of_units, base_size, enemy_units_stats["health"][unit_type], enemy_units_stats["damage"][unit_type], enemy_units_stats["range"][unit_type], enemy_units_stats["reload_time"][unit_type], enemy_units_stats["speed"][unit_type])
            enemy_unit_group.add(unit)
            enemy_money -= enemy_prices[unit_type]
        elif unit_type == enemy_types_of_units-1 and enemy_money >= enemy_prices[unit_type]:
            unit = tank("enemy", enemy_types_of_units, tank_images_enemies, enemy_flag, alied_flag, number_of_units, base_size, enemy_units_stats["health"][unit_type], enemy_units_stats["damage"][unit_type], enemy_units_stats["range"][unit_type], enemy_units_stats["reload_time"][unit_type], enemy_units_stats["speed"][unit_type])
            enemy_unit_group.add(unit)
            enemy_money -= enemy_prices[unit_type]
        # this will maybe be done some other way, because it depends on the fact that there is two of them, which might not be true in the future
        # will have to be reworked
        elif unit_type == enemy_types_of_units+1 and enemy_money >= enemy_prices[unit_type]:
            #special = Gas(x, y, image) # will be implemented later, when I have some image for it, and when I have some way of getting the x and y for destination
            #special_actions.add(special)
            enemy_money -= enemy_prices[unit_type]
            print("gas")
            # here will be some function that will find the best destination for the gas
        elif unit_type == enemy_types_of_units+2 and enemy_money >= enemy_prices[unit_type]:
            #special = Artillery( x, y, image)
            #special_actions.add(special)
            enemy_money -= enemy_prices[unit_type]
            print("artillery")
            # here will be some function that will find the best destination for the artillery

# function that sends the units back once a button is clicked or the enemy decides to send the units back
def send_units_back(trench_id, owner, unit_id):
    global allied_unit_group, enemy_unit_group
    if unit_id == None:
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
    else:
        # sending specific units back
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

# function that sends the units forward once a button is clicked or the enemy decides to send the units forward
def send_units_forward(trench_id, owner, type,unit_id):
    global allied_unit_group, enemy_unit_group
    if unit_id == None:
        if type == None:
            # sending all the units in a trench forward
            if owner == "alied":
                for unit in allied_unit_group:
                    if unit.in_trench_id == trench_id:
                        unit.direction = 1
                        unit.in_trench = False
                        unit.in_trench_id = -1
                        unit.left_trench = trench_id
            if owner == "enemy":
                for unit in enemy_unit_group:
                    if unit.in_trench_id == trench_id:
                        unit.direction = 1
                        unit.in_trench = False
                        unit.in_trench_id = -1
                        unit.left_trench = trench_id
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
    else:
        # sending specific units forward
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

# function that shows the trench menu
def show_trench_menu(trench_id, x, types):
    global font, clicking, square_image, unit_images_firing_allies, base_size
    # drawing the buttons for each unit type present
    for i in range(len(types)):
        # drawing the button
        screen.blit(square_image, (x + base_size, base_size*2 + base_size*i))
        # drawing the units image on the button
        if types[i] < len(unit_images_firing_allies):
            screen.blit(pygame.transform.scale(unit_images_firing_allies[types[i]], (base_size-int(base_size/10),base_size-int(base_size/10))), (x + base_size*2-base_size, base_size*2 + base_size*i))
            text = font.render(str(types[i]+1), True, (0, 0, 255))
        else:
            screen.blit(pygame.transform.scale(tank_images_allies[0], (base_size-int(base_size/10), base_size-int(base_size/10))), (x + base_size*2-base_size, base_size*2 + base_size*i))
            text = font.render(str(types[i]), True, (0, 0, 255))
        # drawing the text on the button
        screen.blit(text, (x + text.get_width()/2+base_size*2-int(base_size/2), base_size*2+int(base_size/2) + base_size*i ))
    # checking if the buttons are clicked
    if pygame.mouse.get_pressed()[0]: # the problem is that when the person clicks a button it will send not only the units of that type, but also the units next in line of types, its the basic button pressing problem, I will have to find a fix for it, but for now I dont have any ideas
        pos = pygame.mouse.get_pos()
        for i in range(len(types)):
            if pos[0] > x + base_size and pos[0] < x + base_size*2 and pos[1] > base_size*2 + base_size*i and pos[1] < base_size*3 + base_size*i and clicking == False:
                send_units_forward(trench_id, "alied", types[i], None)
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
                send_units_forward(trench.id, trench.current_owner, None, None)
        # creating a button, that will send the units back
        screen.blit(back_button_image, (trench.rect.x, 0))
        if pygame.mouse.get_pressed()[0] and show_game_menu == False:
            pos = pygame.mouse.get_pos()
            if pos[0] > trench.rect.x and pos[0] < trench.rect.x + base_size and pos[1] > 0 and pos[1] < base_size:
                send_units_back(trench.id, trench.current_owner, None)
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
unit_images_running_allies = []
unit_images_firing_allies = []
unit_images_running_enemies = []
unit_images_firing_enemies = []
# tank images
tank_images_allies = []
tank_images_enemies = []

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

# images used in the game and menus
menu_button_image = pygame.transform.scale(pygame.image.load("assets/menu.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
forward_button_image = pygame.transform.scale(pygame.image.load("assets/forward.png"), (base_size, base_size))
back_button_image = pygame.transform.scale(pygame.image.load("assets/back.png"), (base_size, base_size))
return_arrow_image = pygame.transform.scale(pygame.image.load("assets/back_arrow.png"), (base_size+int(base_size/2), base_size+int(base_size/2)))
down_arrow_image = pygame.transform.scale(pygame.image.load("assets/arrow_down.png"), (base_size, base_size))
square_image = pygame.transform.scale(pygame.image.load("assets/square.png"), (base_size, base_size))
buy_button = pygame.transform.scale(pygame.image.load("assets/buy_button.png"), (base_size*2, base_size*2))
soldiers_image = pygame.transform.scale(pygame.image.load("assets/icon.png"), (base_size*8, base_size*8))
gas = pygame.transform.scale(pygame.image.load("assets/gas.png"), (base_size, base_size))
bomb = pygame.transform.scale(pygame.image.load("assets/bomb.png"), (base_size, base_size))
aim_image = pygame.transform.scale(pygame.image.load("assets/aim.png"), (base_size*2, base_size*2))
comming_soon = pygame.transform.scale(pygame.image.load("assets/coming_soon.png"), (base_size*8, base_size*8))
actions = [bomb,gas ]
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
aiming = False # this is used for aiming, when a special action is selected
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
    pygame.draw.line(screen, (100, 100, 100), (0, base_size*2), (width, base_size*2), int(base_size/10))
    # drawing the ground, later it will be image instead of a pygame.draw.rect
    pygame.draw.rect(screen, ( 100, 25, 0 ), (0, base_size*2, width, height-base_size*2))

    # this is for testing, because the buying for the special doesnt work again
    # figured it out, the problem was that the types of units changed, now it works, but I will leave this code here, just in case
    #pos = pygame.mouse.get_pos()
    #for i in range(allied_types_of_special_actions):
    #    if pos[1] > height - base_size*2 - (base_size*2)*i and pos[1] < height - base_size*2 - (base_size*2)*i + base_size*2:
    #        print("on the spot"+ str(i))
    
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
                if aiming:
                    aiming = False
                    # here the special action will be called, and the destination will be set
                    break
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
                                    send_units_forward(unit.in_trench_id, "alied", None,unit.id)
                            if button.aliegance == "Send back":
                                for unit in selected_units:
                                    send_units_back(unit.in_trench_id, "alied", unit.id)
                # checking if the player clicked on a buy button
                if pos[1] > base_size*12 and show_game_menu == False:
                    for i in range(allied_types_of_units):
                        if pos[0] > i * base_size*2 and pos[0] < (i + 1) * base_size*2:
                            buy(i, "alied")
                # checking if the player clicked on one of the special action buttons in the bottom right corner, if so then calling the buy function, which should handle it correctly???
                if pos[0] > width - base_size*2 and show_game_menu == False:
                    if pos[1] > height - base_size*allied_types_of_special_actions*2:
                        # figuring out which button was clicked
                        for i in range(allied_types_of_special_actions):
                            if pos[1] > height - base_size*2 - (base_size*2)*i and pos[1] < height - base_size*2 - (base_size*2)*i + base_size*2:
                                #print("clicked on the special action button number " + str(i))
                                buy(allied_types_of_units+i, "alied")
                # checking if the drop down menu button in the top left corner is clicked
                if pos[0] < base_size*2+int(base_size/2) and pos[1] < base_size*2+int(base_size/2):
                    show_game_menu = True
                # checking if some game menu option is clicked
                if show_game_menu:
                    if pos[0] > width/2 - base_size*4 and pos[0] < width/2 + base_size*4 and pos[1] > height/2 - base_size and pos[1] < height/2 + base_size:
                        show_game_menu = False
                    if pos[0] > width/2 - base_size*4 and pos[0] < width/2 + base_size*4 and pos[1] > height/2 + base_size and pos[1] < height/2 + base_size*3:
                        show_main_menu = True
                        reset_game(None, None)
                        show_game_menu = False
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

    # drawing the special actions(gas, artillery, etc.)
    try:
        special_actions.draw(screen)
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
    # in case the right click menu is open, then showing the menu, will be enhanced later
    if right_click_menu:
        pygame.draw.circle(screen, (50, 50, 50), menu_pos, base_size)
        right_click_buttons.draw(screen)
    # drawing buttons from the bottom left corner, based on the number of types of units
    if running and not show_main_menu: # running has to be checked, otherwise the game ends with an error if player tries to exit from the main menu
        for i in range(allied_types_of_units):
            screen.blit(buy_button, (i * base_size*2, height-base_size*2))
            # drawing the image of the unit to which the button corresponds
            if i < len(allied_prices)-allied_types_of_special_actions-1:
                screen.blit(unit_images_firing_allies[i], (i * base_size*2 + int(base_size/2), base_size*12 + int(base_size/2)))
            elif i == len(allied_prices)-allied_types_of_special_actions-1:
                screen.blit(tank_images_allies[0], (i * base_size*2, base_size*12 ))
            # drawing the price of the unit on the bottom of the button
            text = font.render(str(allied_prices[i]), True, (0, 0, 200))
            screen.blit(text, (i * base_size*2 + int(base_size/2 + text.get_width()/2), base_size*13 + text.get_height()))

    # drawing a drop down menu icon
    screen.blit(menu_button_image, (0, 0))

    # drawing the special actions menu from the bottom right corner
    if not show_main_menu:
        temp_price_pos = len(allied_prices)-allied_types_of_special_actions # has to be here, because the order of the prices is different than it used to be, however this should work every time
        for i in range(allied_types_of_special_actions):
            screen.blit(buy_button, (width - base_size*2, height - base_size*2 - (base_size*2)*i))
            text = font.render(str(allied_prices[temp_price_pos+i]), True, (0, 0, 200))
            screen.blit(text, (width - base_size*2 + int(base_size/2 + text.get_width()/2), height -base_size - (base_size*2)*i + text.get_height()))
            screen.blit(actions[i], (width - base_size*2 + int(base_size/2), height - base_size*2 - (base_size*2)*i + int(base_size/2)))

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
    
    # if the player is aiming, than changing the cursor to a crosshair
    if aiming:
        pygame.mouse.set_visible(False)
        screen.blit(aim_image, pygame.mouse.get_pos())
    else:
        pygame.mouse.set_visible(True)

    # moving the units
    if show_game_menu == False:
        for unit in allied_unit_group:
            unit.move()
            #print(unit.time_since_last_fire)
            #print(unit.reload_time*frame_rate)
            # firing bug fix
            if unit.time_since_last_fire != 0:
                unit.firing = False
            # checking if the unit is ready to fire, if so than firing
            if unit.time_since_last_fire >= unit.reload_time*frame_rate:
                unit.fire(enemy_unit_group, allied_unit_group)
            else:
                unit.time_since_last_fire += 1
            # checking if the unit is firing, if so than spawning a bullet
            if unit.firing:
                bullet = Bullet("allied",unit_bullet, unit.rect.x, unit.rect.y, unit.fire_range)
                bullets.add(bullet)
                unit.firing = False
                shot_sound.play()
            if unit in selected_units:
                highlight_unit(unit)
        for unit in enemy_unit_group:
            unit.move()
            # firing bug fix
            if unit.time_since_last_fire != 0:
                unit.firing = False
            # checking if the unit is ready to fire, if so than firing
            if unit.time_since_last_fire >= unit.reload_time*frame_rate:
                unit.fire(enemy_unit_group, allied_unit_group)
            else:
                unit.time_since_last_fire += 1
            # checking if the unit is firing, if so than spawning a bullet
            if unit.firing:
                bullet = Bullet("enemy",unit_bullet, unit.rect.x, unit.rect.y, unit.fire_range)
                bullets.add(bullet)
                unit.firing = False
                shot_sound.play()
            if unit in selected_units:
                highlight_unit(unit)

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
            money += 6
            time_to_add_money = 1 * frame_rate
        enemy_time_to_add_money -= 1
        if enemy_time_to_add_money == 0:
            enemy_money += 3
            enemy_time_to_add_money = 1 * frame_rate

    clock.tick(frame_rate)
    pygame.display.update()

pygame.quit()