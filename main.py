import sys
import pygame
import helper_functions as hf
import os
import crop_imgs as ci
import bound_imgs as bi


file_list, source_path, mode = hf.initialize()
new_folders = [os.path.join(source_path, mode)]
hf.create_folders(new_folders)

print(pygame)
pygame.init()
size = width, height = 1000, 750
img_display = pygame.display.set_mode(size)

white = (255, 255, 255)
red = (220, 0, 0)
red_d = (190, 0, 0)
green = (0, 190, 0)
green_l = (0, 220, 0)
grey = (128, 128, 128)
grey_l = (160, 160, 160)
grey_d = (100, 100, 100)
grey_200 = (200, 200, 200)

clock = pygame.time.Clock()


def load_img(img_n):
    """"shows the given image"""
    img_display.blit(img_n, (0, 0))


def text_objects(text, font):
    """renders a text on a surface and returns it."""
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def button(msg, pos_tupel, ic, ac):
    """draws a button, color based on whether the mouse is hovering it or not."""
    mouse = pygame.mouse.get_pos()
    x = pos_tupel[0]
    y = pos_tupel[1]
    w = pos_tupel[2]
    h = pos_tupel[3]

    if hf.mouse_on_button(pos_tupel, mouse):
        pygame.draw.rect(img_display, ac, pos_tupel)
    else:
        pygame.draw.rect(img_display, ic, pos_tupel)

    small_text = pygame.font.Font("freesansbold.ttf", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    img_display.blit(text_surf, text_rect)
    return x, y, w, h


def check_round(cnt, len_fl):
    if cnt == (len_fl - 1):
        print("last round!")
        return False
    else:
        return True


counter = 0
more_images = True

red_button = (225, 620, 150, 50)
grey_button = (425, 620, 150, 50)
green_button = (625, 620, 150, 50)

pos_left_up = (0, 0)
pos_right_down = (0, 0)
img_width_height_current = (0, 0)

dict_name_pos = {}
down_on_button = False
fps = 35

# the following is the render loop, set fps variable
while more_images:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if hf.mouse_on_button(red_button, mouse_pos):
                down_on_button = True
            elif hf.mouse_on_button(grey_button, mouse_pos):
                down_on_button = True
            elif hf.mouse_on_button(green_button, mouse_pos):
                down_on_button = True
            else:
                pos_left_up = mouse_pos

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            print('pos_right_down ' + str(pos_right_down))
            print('img_width_height_current ' + str(img_width_height_current))
            if hf.mouse_on_button(red_button, mouse_pos) and down_on_button:
                counter += 1
                down_on_button = False
                pos_left_up = (0, 0)
                pos_right_down = (0, 0)
                more_images = check_round(counter, len(file_list))

            elif hf.mouse_on_button(grey_button, mouse_pos) and down_on_button:
                down_on_button = False
                more_images = False

            elif hf.mouse_on_button(green_button, mouse_pos) and (pos_left_up != 0) \
                    and (pos_right_down != 0) and down_on_button:

                dict_name_pos[file_list[counter]] = (pos_left_up, pos_right_down, img_width_height_current)
                print('counter --> ' + str(counter))
                print(file_list[counter])
                hf.save_obj(dict_name_pos, 'name_and_pos')
                counter += 1
                down_on_button = False
                pos_left_up = (0, 0)
                pos_right_down = (0, 0)
                more_images = check_round(counter, len(file_list))

            else:
                pos_right_down = mouse_pos

    try:
        img_display.fill(grey_d)
        img_n = pygame.image.load(os.path.join(source_path, file_list[counter]))
        img_width = img_n.get_width()
        img_height = img_n.get_height()
        scale_width, scale_height = hf.get_scaling(width, height, img_width, img_height)
        img_n = pygame.transform.scale(img_n, (int(width*scale_width), int(height*scale_height)))
        load_img(img_n)

        img_width_height_current = (img_n.get_width(), img_n.get_height())
    except:
        print("image format not supported or something, wtf" + "\n ---> " + file_list[counter])

    mouse = pygame.mouse.get_pos()
    pygame.draw.line(img_display, grey_200, (0, mouse[1]), (width, mouse[1]), 1)
    pygame.draw.line(img_display, grey_200, (mouse[0], 0), (mouse[0], height), 1)

    bounding_box_width = pos_right_down[0] - pos_left_up[0]
    bounding_box_height = pos_right_down[1] - pos_left_up[1]

    bounding_box = pygame.Rect(pos_left_up[0], pos_left_up[1], bounding_box_width, bounding_box_height)

    pygame.draw.rect(img_display, red, bounding_box, 2)

    button("Dismiss", red_button, red, red_d)
    button("Finish", grey_button, grey, grey_l)
    button("Submit", green_button, green, green_l)

    pygame.display.update()
    clock.tick(fps)

# print(mode)
if mode == "crop":
    ci.crop(source_path, dict_name_pos)
if mode == "bound":
    bi.bound(source_path, dict_name_pos)

print("delete unmarked images? [y | n]")
answer = "no"
incorrect_input = True
while incorrect_input:
    answer = input().lower()
    if answer == "y" or answer == "yes":
        answer = "yes"
        incorrect_input = False
    elif answer == "n" or answer == "no":
        answer = "no"
        incorrect_input = False

if answer == "yes":
    used_images = []
    for key in dict_name_pos:
        used_images.append(key)
    hf.delete_unused(source_path, file_list, used_images)
else:
    pass

sys.exit()
