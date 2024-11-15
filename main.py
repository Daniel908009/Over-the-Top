import pygame
import random


pygame.init()
pygame.display.set_caption("Over the Top")
screen = pygame.display.set_mode((1400, 700))
clock = pygame.time.Clock()

# functions
def update_offset():
    global x_offset
    # later here will be some code for the walls of the program

    # moving the objects
    for object in object_group:
        object.rect.x += x_offset
    for unit in unit_group:
        unit.rect.x += x_offset


# classes
class Unit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width*2
        self.rect.y = random.randint(100, 600 - self.rect.height/2)
        self.speed = random.randint(1, 3)
        self.in_trench = False
        self.left_trench = -1
        self.in_trench_id = -1
        self.direction = 1

    def move(self):
        if self.in_trench == False:
            self.rect.x += self.speed*self.direction

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

    def update(self):
        # checking if a unit is colliding with the trench, if yes, then the unit will stop moving
        global unit_group
        for unit in unit_group:
            if self.rect.colliderect(unit.rect) and unit.left_trench != self.id:
                unit.in_trench = True
                unit.in_trench_id = self.id
                unit.direction = 1
        # getting the number of units in the trench
        self.units_in_trench = 0
        for unit in unit_group:
            if unit.in_trench_id == self.id:
                self.units_in_trench += 1

    def commands(self):
        # if there is at least one unit in the trench, a button will appear above the trench
        if self.units_in_trench > 0:
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, 50, 50, 50))
            # if the button is clicked, the units will leave the trench
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x and pos[0] < self.rect.x + 50 and pos[1] > 50 and pos[1] < 100:
                    for unit in unit_group:
                        if unit.in_trench_id == self.id:
                            unit.in_trench = False
                            unit.in_trench_id = -1
                            unit.left_trench = self.id
            # creating a second button, that will send the units back
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, 0, 50, 50))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.rect.x and pos[0] < self.rect.x + 50 and pos[1] > 0 and pos[1] < 50:
                    for unit in unit_group:
                        if unit.in_trench_id == self.id:
                            unit.direction = -1
                            unit.in_trench = False
                            unit.in_trench_id = -1
                            unit.left_trench = self.id


# test unit group
unit_group = pygame.sprite.Group()
unit1 = Unit()
unit_group.add(unit1)

# test trench
object_group = pygame.sprite.Group()
number_of_trenches = 1
for i in range(int(10000/250)):
    trench = Trench(i*250)
    object_group.add(trench)

types_of_units = 3
x_offset = 0
# main loop
running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_offset += 50
            if event.key == pygame.K_d:
                x_offset -= 50
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                x_offset = 0
        # handling the buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if pos[1] > 600:
                    for i in range(types_of_units):
                        if pos[0] > i * 100 and pos[0] < (i + 1) * 100:
                            unit = Unit()
                            unit_group.add(unit)

    # drawing a line representing the ground
    pygame.draw.line(screen, (0, 255, 0), (0, 100), (10000, 100), 5)

    # updating the offset to applu to all the objects
    update_offset()

    # drawing the objects
    object_group.draw(screen)
    for object in object_group:
        object.update()
        object.commands()

    # drawing the units
    unit_group.draw(screen)

                       # UI
    # drawing buttons from the bottom left corner, based on the number of types of units
    for i in range(types_of_units):
        pygame.draw.rect(screen, (50, 50, 50), (i * 100, 600, 100, 100))

    # moving the units
    for unit in unit_group:
        unit.move()
    
    clock.tick(60)
    pygame.display.update()



pygame.quit()