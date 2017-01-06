# Golf

import pygame, sys
from pygame.locals import *
import random

# Define the colours
WHITE = (255, 255, 255)
GREYBLUE = (62, 87, 113)

# Define constants
SCREENWIDTH = 400
SCREENHEIGHT = 300
SCOREBOARDMARGIN = 4
SCOREBOARDHEIGHT = 28
SLIDER_LEFT = 20
SLIDER_TOP = SLIDER_LEFT + SCOREBOARDHEIGHT
SLIDER_BOTTOM = SLIDER_TOP + 145
START_BALL_X = 20
BALL_Y = 288
FLAG_Y = 170




# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Golf")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)


# Load images
background_image = pygame.image.load("golf_background.png")
power_meter_image = pygame.image.load("power_meter.png")
slider_image = pygame.image.load("slider.png")
ball_image = pygame.image.load("ball.png")
flag_image = pygame.image.load("flag.png")
slider_image.set_colorkey(WHITE)


# Initialise variables
slider_x = 15
slider_y = SLIDER_BOTTOM
slider_direction = "UP"

ball_x = START_BALL_X
flag_distance = random.randint(10, 30)
flag_x = flag_distance * 10 + 15

ball_distance = 0
shot_power = 0
ball_direction = "RIGHT"
overall_ball_position = 0

hole = 1
hole_strokes = 0
round_strokes = 0
best_hole_strokes = 999
best_round_strokes = 999
in_the_hole = False



while True: # main game loop

    # Keypress events
    for event in pygame.event.get():
        key_pressed = pygame.key.get_pressed()

        # SPACE key pressed - hit shot
        if key_pressed[pygame.K_SPACE] and ball_distance == 0 and in_the_hole is False:
            slider_direction = "NONE"
            shot_power = 30 - ((slider_y - SLIDER_TOP)/5)
            ball_distance = shot_power * 2
            hole_strokes = hole_strokes + 1
            round_strokes = round_strokes + 1

            if ball_direction == "RIGHT":
                overall_ball_position = overall_ball_position + shot_power
            else:
                overall_ball_position = overall_ball_position - shot_power

        # Ball is in the hole - wait for RETURN key then start new hole
        elif key_pressed[pygame.K_RETURN] and in_the_hole is True:
            if hole_strokes < best_hole_strokes:
                best_hole_strokes = hole_strokes

            if hole == 3:
                if round_strokes < best_round_strokes:
                    best_round_strokes = round_strokes
                hole = 1
                round_strokes = 0
            else:
                hole = hole + 1
               
            hole_strokes = 0
            in_the_hole = False
            slider_y = SLIDER_BOTTOM
            slider_direction = "UP"

            ball_x = START_BALL_X
            ball_direction = "RIGHT"
            overall_ball_position = 0
                
            flag_distance = random.randint(10, 30)
            flag_x = flag_distance * 10 + 15

        
            

    if event.type == QUIT:
        pygame.quit()     
        sys.exit()

    game_screen.blit(background_image, [0,0])

    # Display scores and level
    scoreboard_background_rect = (0, 0, SCREENWIDTH, SCOREBOARDHEIGHT)
    pygame.draw.rect(game_screen, GREYBLUE, scoreboard_background_rect)
    
    hole_text = "Hole: " + str(hole)
    text = font.render(hole_text, True, (WHITE))
    game_screen.blit(text, [SCOREBOARDMARGIN, SCOREBOARDMARGIN])

    strokes_text = "Strokes: " + str(hole_strokes) + " [" + str(round_strokes) + "]"
    text = font.render(strokes_text, True, (WHITE))
    text_rect = text.get_rect()
    game_screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2, SCOREBOARDMARGIN])

    if best_hole_strokes == 999:
        display_best_hole_strokes = "-"
    else:
        display_best_hole_strokes = str(best_hole_strokes)

    if best_round_strokes == 999:
        display_best_round_strokes = "-"
    else:
        display_best_round_strokes = str(best_round_strokes)

    strokes_text = "Best: " + display_best_hole_strokes + " [" + display_best_round_strokes + "]"
    text = font.render(strokes_text, True, (WHITE))
    text_rect = text.get_rect()
    game_screen.blit(text, [SCREENWIDTH - text_rect.width - SCOREBOARDMARGIN, SCOREBOARDMARGIN])

    
    # In the hole messages
    if in_the_hole is True:
        if hole == 3:
            text = font.render("Round completed in " + str(round_strokes) + ". Press RETURN to play new round", True, (WHITE))
        else:
            text = font.render("In the hole in " + str(hole_strokes) + ". Press RETURN to play next hole", True, (WHITE))

        text_rect = text.get_rect()
        game_screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2, (SCREENHEIGHT - text_rect.height) / 2])
        
    
    # Move slider
    if slider_direction =="UP":
        slider_y = slider_y - 5
        if slider_y == SLIDER_TOP:
            slider_direction = "DOWN"  
    elif slider_direction == "DOWN":
        slider_y = slider_y + 5
        if slider_y == SLIDER_BOTTOM:
            slider_direction = "UP"


    # Move ball
    if ball_distance > 0:
        if ball_direction == "RIGHT":
            ball_x = ball_x + 5    
        else:
            ball_x = ball_x - 5

        if ball_x > 400 or ball_x < 0:
                ball_x = START_BALL_X
                ball_distance = 0
                ball_direction = "RIGHT"
                slider_y = SLIDER_BOTTOM
                slider_direction = "UP"
                overall_ball_position = 0
        else:      
            ball_distance = ball_distance - 1
            if ball_distance == 0:
                if overall_ball_position == flag_distance:
                    in_the_hole = True
                    
                else:
                    if overall_ball_position < flag_distance:
                        ball_direction = "RIGHT"
                    else:
                        ball_direction = "LEFT"
                    
                    slider_y = SLIDER_BOTTOM
                    slider_direction = "UP"


    # Display slider, flag and ball 
    if ball_distance == 0 and in_the_hole is False:
        game_screen.blit(power_meter_image, [SLIDER_LEFT, SLIDER_TOP])
        game_screen.blit(slider_image, [slider_x,slider_y])

    game_screen.blit(flag_image, [flag_x,FLAG_Y])

    if in_the_hole is False:
        game_screen.blit(ball_image, [ball_x,BALL_Y])
    else:
        game_screen.blit(ball_image, [ball_x,BALL_Y + 5])
    


    pygame.display.update()
    clock.tick(20)
