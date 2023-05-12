


################################# IMPORTS
#                               #
import pygame                   #
import numpy as np              #
import sys                      #
import random                   #
import os                       #
import math                     #
import HELLFIRE_CORTEX as hc    #
#                               #
#################################



class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Dot:
    def __init__(self, position, color, radius, speed):
        self.position = position
        self.color = color
        self.radius = radius
        self.speed = speed

class ScreenProps:
    def __init__(self, width, height,  color, position):
        self.width = width
        self.height = height
        self.color = color
        self.position = position



######################################################################### DECLARATIONS
#                                                                       #
ai_dot = Dot(Position(0.5,0.5),(255,0,0),5,0.006)                       # making the ai
destination = Dot(Position(0.8,0.8),(0,255,0),5,0.006)                  # making its "food"
screen_props = ScreenProps(600, 600, (0,0,0), (0,0))                    # properties of the screen (height, width, background color, position on monitor)
#                                                                       #
#-----------------------------------------------------------------------# neural network parts
#                                                                       #
number_of_inputs = 4                                                    #
number_of_neurons = [8,8,8,8]                                           #
number_of_outputs = 2                                                   #
#                                                                       #
#########################################################################





# FUNCTIONS

def draw_dot(input_dot, screen):    # displays the input Dot class object on the defined pygame screen
    # check if the dot is out of the screen, if not draw it to screen
    if screen_props.width > input_dot.position.x >= 0 and screen_props.height > input_dot.position.y >= 0:
        pygame.draw.circle(
            screen, 
            input_dot.color, 
            (int(screen_props.width * input_dot.position.x), int(screen_props.height * input_dot.position.y)), 
            input_dot.radius
            )
    


def calculate_movement():                       # add the outputs of the neural net outputs to the positions of the AI
    
    global nodes
    threshold = 0
    # applying change on the x axis
    if (threshold < nodes[len(nodes)-1][1]):
        ai_dot.position.x -= ai_dot.speed
    elif (threshold > nodes[len(nodes)-1][1]):
        ai_dot.position.x += ai_dot.speed
    
    # applying change on the y axis
    if (threshold < nodes[len(nodes)-1][2]):
        ai_dot.position.y -= ai_dot.speed
    elif (threshold > nodes[len(nodes)-1][2]):
        ai_dot.position.y += ai_dot.speed     

def randomize_position(input_dot):
    input_dot.position.x = np.float32(np.random.uniform(low=0.0, high=1.0, size=None))
    input_dot.position.y = np.float32(np.random.uniform(low=0.0, high=1.0, size=None))
    
last_distance = 666666
skip_next_training = False
def autotrain_network():
    global last_distance
    global training_counter
    global skip_next_training
    global weights
    global new_weights
    
    ai_dot_pos_x = int(screen_props.width * ai_dot.position.x)+1000
    ai_dot_pos_y = int(screen_props.height * ai_dot.position.y)+1000
    
    destination_pos_x = int(screen_props.width * destination.position.x)+1000
    destination_pos_y = int(screen_props.height * destination.position.y)+1000
    
    distance_x = abs(ai_dot_pos_x - destination_pos_x)
    distance_y = abs(ai_dot_pos_y - destination_pos_y)
    distance = math.sqrt(distance_x**2 + distance_y**2)
    
    if distance < last_distance:
        if skip_next_training:
            last_distance = distance
            skip_next_training = False
        else:
            weights = new_weights
            last_distance = distance
    if distance < 10:
        randomize_position(destination)
        last_distance = 666666
        skip_next_training = True
        training_counter = 0
    hc.add_mutation(new_weights)
    
    
    
def main_loop():

    global last_distance
    global skip_next_training
    global nodes
    global weights
    
    
    ##################################################################################### INITIALIZING PYGAME
    os.environ['SDL_VIDEO_WINDOW_POS'] = (                                              # set starting position of the screen on the monitor
        f"{screen_props.position[0]},{screen_props.position[1]}"                        #
    )                                                                                   #   
    pygame.init()                                                                       # initializing the engine
    screen = pygame.display.set_mode((screen_props.width, screen_props.height))         # defining the screen
    pygame.display.set_caption("Dot AI")                                                # set windows caption of the screen
    clock = pygame.time.Clock()                                                         # fps fixing / fps counter
    fps_font = pygame.font.Font(None, 36)                                               # fps display text font
    


    ############################### Just a bunch of booleans for controlling things inside the loop ##########################################
    move_up = False
    move_down = False
    move_left = False
    move_right = False
    quit_program = False
    running = True
    auto_train = True
    
    training_counter = 0
    training_interval = 5
    
    while running:
    
        r_pressed = False
        
        training_counter += 1
        if training_counter == training_interval:
            autotrain_network()
            training_counter = 0
        
        # EVENT HANDLERS
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    r_pressed = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_q:
                    running = False
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_r:
                    r_pressed = False
                    
        if move_up:
            destination.position.y = destination.position.y - destination.speed
        if move_down:
            destination.position.y = destination.position.y + destination.speed
        if move_left:
            destination.position.x = destination.position.x - destination.speed
        if move_right:
            destination.position.x = destination.position.x + destination.speed

        if r_pressed:
            randomize_position(ai_dot)
            randomize_position(destination)
            last_distance = 666666
            skip_next_training = True
            training_counter = 0
            continue
        

        # FPS CALCULATION
        
        clock.tick(60)
        fps = clock.get_fps()
        fps_text = fps_font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        text_bg_surface = pygame.Surface((160, 22))
        text_bg_surface.fill((0,0,255))

        
        # Add values to input layer elements
        
        nodes[0][1] = destination.position.x-ai_dot.position.x
        nodes[0][2] = destination.position.y-ai_dot.position.y
        nodes[0][3] = ai_dot.position.x-destination.position.x
        nodes[0][4] = ai_dot.position.y-destination.position.y
        
        
        
        # CALCULATING NEURONS & OUTPUTS
        hc.calculate_network(nodes, weights)
        calculate_movement()
        
        # DISPLAY
        
        print(nodes[len(nodes)-1])
        transparent_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 3))
        screen.blit(transparent_surface, (0, 0))
        draw_dot(ai_dot, screen)
        draw_dot(destination, screen)
        screen.blit(text_bg_surface, (10, 10))
        screen.blit(fps_text, (10, 10))
        pygame.display.flip()
        
        
        
    pygame.quit()



################################################### PROGRAM STARTS HERE

nodes = hc.generate_nodes(number_of_inputs, number_of_neurons, number_of_outputs)
weights = hc.generate_weights(nodes, -1, 1)
new_weights = weights

input()
"""
print(nodes)
hc.calculate_network(nodes, weights)
print()
print(weights)
print()
print(nodes)
input()
"""

randomize_position(ai_dot)
randomize_position(destination)
main_loop()
