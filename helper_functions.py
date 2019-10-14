import os


def get_scaling(width, height, img_width, img_height):
    "scales the images so they fit in the window"
    scale_width = 0
    scale_height = 0
    if (width > img_width):
        scale_width = 1
    else: 
        scale_width = width/img_width
    if (height > img_height):
        scale_height = 1
    else:
        scale_height = height/img_height
    return scale_width, scale_height


def createFolders(folderPaths):
    "creates all the necessary folders for the programm to run if not already there"
    for path in folderPaths:       
        os.makedirs(path, exist_ok=True)