import os
import pickle
from os import listdir
from os.path import isfile, join


def get_scaling(width, height, img_width, img_height):
    """scales the images so they fit in the window"""
    scale_width = 0
    scale_height = 0
    if width >= img_width or height >= img_height:
        scale_width = 1
        scale_height = 1
    if width < img_width or height < img_height:
        scale_width = width/img_width
        scale_height = height/img_height
    return scale_width, scale_height


def create_folders(folder_paths):
    """creates all the necessary folders for the program to run if not already there"""
    for path in folder_paths:       
        os.makedirs(path, exist_ok=True)


def mouse_on_button(button_params, pos_mouse):
    """checks if mouse is in a specific area"""
    x = button_params[0]
    y = button_params[1]
    w = button_params[2]
    h = button_params[3]

    if x+w > pos_mouse[0] > x and y+h > pos_mouse[1] > y:
        return True
    else:
        return False


def save_obj(obj, name):
    """"safes the given object in binary in the obj folder in the same directory"""
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """loads a binary file by given name from obj folder"""
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def initialize():
    """initializes the program"""
    mode = ""
    print("filepath?")
    path = input()
    # path = "../people_in_wheelchairs"
    print("crop or bound?")
    incorrect_input = True
    while incorrect_input:
        mode = input().lower()
        if mode == "c" or mode == "crop":
            mode = "crop" 
            incorrect_input = False
        elif mode == "b" or mode == "bound":
            mode = "bound"
            incorrect_input = False      
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    return file_list, path, mode


def get_ratios(x1, y1, x2, y2, img_w, img_h):
    """"calculates the ratios between 4 given coordinates and image height and width"""
    rx1 = x1/img_w
    ry1 = y1/img_h
    rx2 = x2/img_w
    ry2 = y2/img_h

    rx1 = max(rx1, 0.0)
    ry1 = max(ry1, 0.0)
    rx2 = min(rx2, 1.0)
    ry2 = min(ry2, 1.0)

    return rx1, ry1, rx2, ry2


def delete_unused(source_path, all_images, used_images):
    """takes a source path, a list of all files and a list of used files and
    deletes all unsused files in the first list"""
    to_delete = []
    for img in all_images:
        not_used = True
        for used in used_images:
            print(img, used)
            if img == used:
                not_used = False
        if not_used:
            to_delete.append(img)

    delete_images(source_path, to_delete)


def delete_images(source_path, to_delete):
    """deletes all files in the list, given as the second argument"""
    for img in to_delete:
        os.remove(os.path.join(source_path, img))
