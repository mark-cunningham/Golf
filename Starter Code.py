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
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
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

# Load sounds
putt_sound = pygame.mixer.Sound('putt.ogg')
clap_sound = pygame.mixer.Sound('clap.ogg')