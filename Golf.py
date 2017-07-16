# Golf

import pygame, sys
from pygame.locals import *
import random

# Define the colours
WHITE = (255, 255, 255)
GREYBLUE = (62, 87, 113)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
SCOREBOARDMARGIN = 4
SCOREBOARDHEIGHT = 48
SCOREBOARDLINE = 20
SCOREBOARDCOLUMNS = 10


SLIDERBORDER = 5
SLIDERLEFT = 20
METERLEFT = SLIDERLEFT + SLIDERBORDER
METERTOP = SCOREBOARDHEIGHT + 20
METERMAX = 30
METERMIN = 1

SLIDERSTEP = 10
SLIDERSPEED = 10
BOOSTSLIDERSPEED = 2
SLOWSLIDERSPEED = 50
SLOWPUTTRANGE = 2

STARTBALLX = 20
BALLY = 456
BALLDESCENT = 5

FLAGY = 264
RANDFLAGMIN = 10
RANDFLAGMAX = 30
FLAGSTEP = 18
FLAGPAD = 15
BALLSTEP = 3




# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Golf")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)


def main():

    # Load images
    background_image = pygame.image.load("golf background.png").convert()
    power_meter_image = pygame.image.load("power meter.png").convert()
    slider_image = pygame.image.load("slider.png").convert_alpha()
    ball_image = pygame.image.load("ball.png").convert_alpha()
    flag_1_image = pygame.image.load("flag 1.png").convert_alpha()
    flag_2_image = pygame.image.load("flag 2.png").convert_alpha()
    flag_3_image = pygame.image.load("flag 3.png").convert_alpha()


    # Initialise variables

    meter_rectangle = power_meter_image.get_rect()
    meter_bottom = METERTOP + meter_rectangle.height

    slider_direction = "UP"
    slider_timer = SLOWSLIDERSPEED
    shot_power = 1
    slider_speed_boost = False

    ball_x = STARTBALLX
    flag_distance = random.randint(RANDFLAGMIN, RANDFLAGMAX)
    flag_x = flag_distance * FLAGSTEP + FLAGPAD

    ball_distance = 0
    ball_direction = "RIGHT"
    overall_ball_position = 0

    hole = 1
    hole_1_strokes = 0
    hole_2_strokes = 0
    hole_3_strokes = 0
    round_strokes = 0
    best_round_strokes = 0
    in_the_hole = False



    while True: # main game loop

        # Keypress events
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            # SPACE key pressed - hit shot
            if key_pressed[pygame.K_SPACE] and ball_distance == 0 and in_the_hole is False:
                slider_direction = "NONE"
                ball_distance = shot_power * FLAGSTEP / BALLSTEP

                if hole == 1:
                    hole_1_strokes = hole_1_strokes + 1
                elif hole == 2:
                    hole_2_strokes = hole_2_strokes + 1
                else:
                    hole_3_strokes = hole_3_strokes + 1

                round_strokes = round_strokes + 1

                if ball_direction == "RIGHT":
                    overall_ball_position = overall_ball_position + shot_power
                else:
                    overall_ball_position = overall_ball_position - shot_power

            elif key_pressed[pygame.K_UP]:
                slider_speed_boost = True
                slider_timer = slider_speed_boost
            elif key_pressed[pygame.K_DOWN]:
                slider_speed_boost = False

            # Ball is in the hole - wait for RETURN key then start new hole
            elif key_pressed[pygame.K_RETURN] and in_the_hole is True:

                if hole == 3:
                    if round_strokes < best_round_strokes or best_round_strokes == 0:
                        best_round_strokes = round_strokes
                    hole = 1
                    hole_1_strokes = 0
                    hole_2_strokes = 0
                    hole_3_strokes = 0
                    round_strokes = 0

                else:
                    hole = hole + 1

                in_the_hole = False
                shot_power = 1
                slider_direction = "UP"

                ball_x = STARTBALLX
                ball_direction = "RIGHT"
                overall_ball_position = 0

                flag_distance = random.randint(RANDFLAGMIN, RANDFLAGMAX)
                flag_x = flag_distance * FLAGSTEP + FLAGPAD

                slider_timer = SLOWSLIDERSPEED
                slider_speed_boost = False




            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        game_screen.blit(background_image, [0,0])






        # In the hole messages
        if in_the_hole is True:
            if hole == 3:
                text = font.render("Round completed in " + str(round_strokes) + ". Press RETURN to play another round.", True, WHITE)
            else:
                text = font.render("In the hole. Press RETURN to play next hole.", True, WHITE)

            scoreboard_background_rect = (SCOREBOARDMARGIN * 4, SCREENHEIGHT / 2 - SCOREBOARDLINE, SCREENWIDTH - SCOREBOARDMARGIN * 8, 2 * SCOREBOARDLINE)
            pygame.draw.rect(game_screen, GREYBLUE, scoreboard_background_rect)
            text_rect = text.get_rect()
            game_screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2, (SCREENHEIGHT - text_rect.height) / 2])

        # Move slider
        slider_timer = slider_timer - 1
        if slider_timer == 0:

            if slider_direction =="UP":
                shot_power = shot_power + 1
                if shot_power == METERMAX:
                    slider_direction = "DOWN"
            elif slider_direction == "DOWN":
                shot_power = shot_power - 1
                if shot_power == METERMIN:
                    slider_direction = "UP"

            if slider_speed_boost is True:
                slider_timer = BOOSTSLIDERSPEED
            elif shot_power <= SLOWPUTTRANGE:
                slider_timer = SLOWSLIDERSPEED
            else:
                slider_timer = SLIDERSPEED



        # Move ball
        if ball_distance > 0:
            if ball_direction == "RIGHT":
                ball_x = ball_x + BALLSTEP
            else:
                ball_x = ball_x - BALLSTEP

            if ball_x > SCREENWIDTH or ball_x < 0:
                ball_x = STARTBALLX
                ball_distance = 0
                ball_direction = "RIGHT"
                shot_power = 1
                slider_direction = "UP"
                overall_ball_position = 0
                slider_timer = SLOWSLIDERSPEED
                slider_speed_boost = False
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

                        shot_power = 1
                        slider_direction = "UP"
                        slider_timer = SLOWSLIDERSPEED
                        slider_speed_boost = False

        # Display slider
        if ball_distance == 0 and in_the_hole is False:
            game_screen.blit(power_meter_image, [METERLEFT, METERTOP])

            slider_y = meter_bottom - shot_power * SLIDERSTEP - SLIDERBORDER - 1
            game_screen.blit(slider_image, [SLIDERLEFT, slider_y])

        # Display flag and ball
        if hole == 1:
            game_screen.blit(flag_1_image, [flag_x,FLAGY])
        elif hole == 2:
            game_screen.blit(flag_2_image, [flag_x, FLAGY])
        elif hole == 3:
            game_screen.blit(flag_3_image, [flag_x, FLAGY])

        if in_the_hole is False:
            game_screen.blit(ball_image, [ball_x,BALLY])
        else:
            game_screen.blit(ball_image, [ball_x,BALLY + BALLDESCENT])

        # Display scores and level
        display_scoreboard(hole_1_strokes, hole_2_strokes, hole_3_strokes, round_strokes, best_round_strokes)

        pygame.display.update()
        clock.tick(30)

def display_scoreboard(h1, h2, h3, round, best):
    scoreboard_background_rect = (0, 0, SCREENWIDTH, SCOREBOARDHEIGHT)
    pygame.draw.rect(game_screen, GREYBLUE, scoreboard_background_rect)

    display_scoreboard_data("Hole:", 0, 0)
    for hole_number in range(0, 3):
        display_scoreboard_data(str(hole_number + 1), hole_number + 1, 0)

    display_scoreboard_data("Total", 6, 0)
    display_scoreboard_data("Best", 7, 0)

    display_scoreboard_data("Strokes:", 0, 1)
    if h1 > 0:
        display_scoreboard_data(str(h1), 1, 1)
    else:
        display_scoreboard_data(str("-"), 1, 1)

    if h2 > 0:
        display_scoreboard_data(str(h2), 2, 1)
    else:
        display_scoreboard_data(str("-"), 2, 1)

    if h3 > 0:
        display_scoreboard_data(str(h3), 3, 1)
    else:
        display_scoreboard_data(str("-"), 3, 1)

    if round > 0:
        display_scoreboard_data(str(round), 6, 1)
    else:
        display_scoreboard_data(str("-"), 6, 1)

    if best > 0:
        display_scoreboard_data(str(best), 7, 1)
    else:
        display_scoreboard_data(str("-"), 7, 1)

def display_scoreboard_data(scoreboard_text, column, line):
    display_text = font.render(scoreboard_text, True, (WHITE))

    text_loc = [SCREENWIDTH / SCOREBOARDCOLUMNS * column + SCOREBOARDMARGIN, SCOREBOARDMARGIN + line * SCOREBOARDLINE]

    game_screen.blit(display_text, text_loc)


if __name__ == "__main__":
    main()


