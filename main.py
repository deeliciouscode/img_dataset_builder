import sys
import pygame
from label_initializer import *
from helper_functions import *
import os
from random import randint
from crop_imgs import *
import time


file_list, source_path = initialize()
file_list.sort()
new_folders = [os.path.join(source_path, "cropped")]
createFolders(new_folders)
print(file_list)

pygame.init()
size = width, height = 1000, 700
img_display = pygame.display.set_mode(size)

white = (255, 255, 255)
red = (220, 0, 0)
red_d = (190, 0, 0)
green = (0, 190, 0)
green_l = (0, 220, 0)
grey = (128, 128, 128)
grey_l = (160, 160, 160)

clock = pygame.time.Clock()


def load_img(img_n):
    img_display.blit(img_n, (0,0))

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,event=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.event.get()

    if (x+w > mouse[0] > x and y+h > mouse[1] > y):
        pygame.draw.rect(img_display, ac, (x, y, w, h))
        if (click[0] == 1 and event != None):
            event()
            time.sleep(1.0)
    else:
        pygame.draw.rect(img_display, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    img_display.blit(textSurf, textRect)

def lel():
    print("lel")
counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            print(event)

    # i = randint(0, 15)
    img_n = pygame.image.load(os.path.join(source_path, file_list[counter]))
    img_width = img_n.get_width()
    img_height = img_n.get_height()
    scale_width, scale_height = get_scaling(width, height, img_width, img_height)
    img_n = pygame.transform.scale(img_n, (int(width*scale_width), int(height*scale_height)))
    load_img(img_n)


    button("Dismiss", 225, 620, 150, 50, red, red_d, lel)
    button("Restart", 425, 620, 150, 50, grey, grey_l, lel)
    button("Submit", 625, 620, 150, 50, green, green_l, lel)

    mouse = pygame.mouse.get_pos()


    pygame.display.update()
    clock.tick(15)

coords = [(.15,.15,.7,.7)]
img_paths = file_list

crop(source_path, img_paths, coords)


