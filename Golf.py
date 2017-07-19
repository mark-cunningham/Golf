#!/usr/bin/python
# Golf
# Code Angel


import sys
import os
import pygame
from pygame.locals import *
import random

# Define the colours
WHITE = (255, 255, 255)
GREY = (62, 87, 113)

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

SCOREBOARD_MARGIN = 4
SCOREBOARD_HEIGHT = 48
SCOREBOARD_LINE = 20
SCOREBOARD_COLUMNS = 10

HOLE_MESSAGE_Y = 60

METER_X = 25
METER_Y = SCOREBOARD_HEIGHT + 20

SLIDER_BORDER = 5
SLIDER_X = 35
SLIDER_TOP_PADDDING = 8

SLIDER_SPEED = 5
SLOW_SLIDER_SPEED = 20
SLOW_PUTT_RANGE = 3

MAX_POWER = 30
MIN_POWER = 1

START_BALL_X = 20
BALL_Y = 436
BALL_STEP = 3
BALL_DESCENT = 5

FLAG_Y = 244
RANDOM_FLAG_MIN = 10
RANDOM_FLAG_MAX = 30
FLAG_STEP = 18
HOLE_CENTRE = 8

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Golf')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)

# Load images
background_image = pygame.image.load('golf_background.png').convert()
power_meter_image = pygame.image.load('power_meter.png').convert()
slider_image = pygame.image.load('slider.png').convert_alpha()
ball_image = pygame.image.load('ball.png').convert_alpha()

flag_1_image = pygame.image.load('flag_1.png').convert_alpha()
flag_2_image = pygame.image.load('flag_2.png').convert_alpha()
flag_3_image = pygame.image.load('flag_3.png').convert_alpha()


def main():

    # Initialise variables
    slider_direction = 'up'
    slider_timer = SLOW_SLIDER_SPEED
    shot_power = 1
    meter_height = power_meter_image.get_rect().height - 2 * SLIDER_BORDER

    ball_x = START_BALL_X
    ball_distance = 0
    ball_direction = 'right'
    final_ball_location = 0
    moves_per_flag = FLAG_STEP / BALL_STEP

    flag_distance = random.randint(RANDOM_FLAG_MIN, RANDOM_FLAG_MAX)
    flag_x = flag_distance * FLAG_STEP + HOLE_CENTRE

    hole = 1

    hole_strokes = [0, 0, 0]
    round_strokes = 0
    best_round_strokes = 0

    in_the_hole = False

    # Main game loop
    while True:

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            # SPACE key pressed - hit shot
            if key_pressed[pygame.K_SPACE] and ball_distance == 0 and in_the_hole is False:
                slider_direction = 'none'
                ball_distance = shot_power * moves_per_flag

                hole_strokes[hole - 1] += 1

                if ball_direction == 'right':
                    final_ball_location += shot_power
                else:
                    final_ball_location -= shot_power

            # RETURN pressed when ball is in the hole - start new hole
            elif key_pressed[pygame.K_RETURN] and in_the_hole is True:

                if hole == 3:

                    if round_strokes < best_round_strokes or best_round_strokes == 0:
                        best_round_strokes = round_strokes

                    hole = 1
                    hole_strokes = [0, 0, 0]
                    round_strokes = 0

                else:
                    hole += 1

                in_the_hole = False
                shot_power = 1
                slider_direction = 'up'

                ball_x = START_BALL_X
                ball_direction = 'right'
                final_ball_location = 0

                flag_distance = random.randint(RANDOM_FLAG_MIN, RANDOM_FLAG_MAX)
                flag_x = flag_distance * FLAG_STEP + HOLE_CENTRE

                slider_timer = SLOW_SLIDER_SPEED

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Update slider
        slider_timer -= 1
        
        if slider_timer == 0:

            # Slider moving up, increase shot power
            if slider_direction == 'up':
                shot_power += 1
                if shot_power == MAX_POWER:
                    slider_direction = 'down'
                    
            # Slider moving down, decrease shot power
            elif slider_direction == 'down':
                shot_power -= 1
                if shot_power == MIN_POWER:
                    slider_direction = 'up'

            # New timer pause
            if shot_power <= SLOW_PUTT_RANGE:
                slider_timer = SLOW_SLIDER_SPEED
            else:
                slider_timer = SLIDER_SPEED

        # Update ball location
        if ball_distance > 0:
            
            if ball_direction == 'right':
                ball_x += BALL_STEP
            else:
                ball_x -= BALL_STEP
            
            # Ball gone off left or right hand edge of screen
            if ball_x > SCREEN_WIDTH or ball_x < 0:

                # Reset ball location at left of screen
                ball_x = START_BALL_X
                ball_distance = 0
                ball_direction = 'right'
                shot_power = 1

                # Reset slider at bottom of meter
                slider_direction = 'up'
                final_ball_location = 0
                slider_timer = SLOW_SLIDER_SPEED

            # Ball is still on screen so move ball closer to final_ball_position
            else:
                ball_distance -= 1

                # Ball has stopped rolling
                if ball_distance == 0:

                    # Ball in hole
                    if final_ball_location == flag_distance:
                        in_the_hole = True
                        round_strokes += hole_strokes[hole - 1]

                    # Ball missed hole
                    else:
                        if final_ball_location < flag_distance:
                            ball_direction = 'right'
                        else:
                            ball_direction = 'left'

                        # Reset slider at bottom of meter
                        shot_power = 1
                        slider_direction = 'up'
                        slider_timer = SLOW_SLIDER_SPEED

        # Draw background
        game_screen.blit(background_image, [0, 0])

        # Draw meter and slider
        if ball_distance == 0 and in_the_hole is False:
            game_screen.blit(power_meter_image, [METER_X, METER_Y])

            slider_step = (MAX_POWER - shot_power) * meter_height / MAX_POWER
            slider_y = METER_Y + SLIDER_BORDER + slider_step - SLIDER_TOP_PADDDING
            game_screen.blit(slider_image, [SLIDER_X, slider_y])

        # Draw flag
        if hole == 1:
            game_screen.blit(flag_1_image, [flag_x, FLAG_Y])
        elif hole == 2:
            game_screen.blit(flag_2_image, [flag_x, FLAG_Y])
        elif hole == 3:
            game_screen.blit(flag_3_image, [flag_x, FLAG_Y])

        # Draw ball
        if in_the_hole is False:
            game_screen.blit(ball_image, [ball_x, BALL_Y])
        else:
            game_screen.blit(ball_image, [ball_x, BALL_Y + BALL_DESCENT])

        # Display scoreboard
        display_scoreboard(hole_strokes, round_strokes, best_round_strokes)

        # In the hole messages
        if in_the_hole is True:
            in_hole_message(hole, hole_strokes[hole - 1], round_strokes)

        pygame.display.update()
        clock.tick(30)


# Display the scoreboard
def display_scoreboard(hole_strokes, round_strokes, best):

    scoreboard_background_rect = (0, 0, SCREEN_WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(game_screen, GREY, scoreboard_background_rect)

    # Display holes 1-3
    display_scoreboard_data('Hole:', 0, 0)

    for hole_number in range(1, 4):
        display_scoreboard_data(str(hole_number), hole_number, 0)

    # Display strokes on each of the 3 holes
    display_scoreboard_data('Strokes:', 0, 1)

    for hole_number in range(0, 3):
        if hole_strokes[hole_number] > 0:
            display_scoreboard_data(str(hole_strokes[hole_number]), hole_number + 1, 1)
        else:
            display_scoreboard_data(str('-'), hole_number + 1, 1)

    # Display total for round
    display_scoreboard_data('Total', 6, 0)

    if round_strokes > 0:
        display_scoreboard_data(str(round_strokes), 6, 1)
    else:
        display_scoreboard_data(str('-'), 6, 1)

    # Display best overall round
    display_scoreboard_data('Best', 7, 0)

    if best > 0:
        display_scoreboard_data(str(best), 7, 1)
    else:
        display_scoreboard_data(str('-'), 7, 1)


# Display scoreboard text items
def display_scoreboard_data(scoreboard_text, column, line):

    display_text = font.render(scoreboard_text, True, WHITE)

    text_x = SCREEN_WIDTH / SCOREBOARD_COLUMNS * column + SCOREBOARD_MARGIN
    text_y = SCOREBOARD_MARGIN + line * SCOREBOARD_LINE

    game_screen.blit(display_text, [text_x, text_y])


# Display message at the end of each hole
def in_hole_message(hole_number, hole_strokes, round_strokes):

    if hole_number == 3:
        message = 'Round completed in ' + str(round_strokes) + '. Press RETURN to play another round.'
        text = font.render(message, True, WHITE)
    else:
        message = 'In the hole in ' + str(hole_strokes) + '. Press RETURN to play next hole.'
        text = font.render(message, True, WHITE)

    background_x = SCOREBOARD_MARGIN * 4
    background_width = SCREEN_WIDTH - SCOREBOARD_MARGIN * 8
    background_height = 2 * SCOREBOARD_LINE
    message_background_rect = (background_x, HOLE_MESSAGE_Y, background_width, background_height)
    pygame.draw.rect(game_screen, GREY, message_background_rect)

    text_rect = text.get_rect()
    messsage_x = (SCREEN_WIDTH - text_rect.width) / 2
    message_y = HOLE_MESSAGE_Y + SCOREBOARD_LINE / 2
    game_screen.blit(text, [messsage_x, message_y])


if __name__ == '__main__':
    main()
