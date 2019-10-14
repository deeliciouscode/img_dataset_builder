import pygame
import os
from PIL import Image

def crop(source_path, img_paths, coords):
    for i in range(len(img_paths)):

        img = Image.open(os.path.join(source_path, img_paths[i]))
        
        width, height = img.size
        crop_w1 = width * coords[0][0]
        crop_h1 = height * coords[0][1]
        crop_w2 = width * coords[0][2]
        crop_h2 = width * coords[0][3]
        crop_w1, crop_h1, crop_w2, crop_h2 = resize_crop_win(crop_w1, crop_h1, crop_w2, crop_h2)

        img = img.crop((crop_w1, crop_h1, crop_w2, crop_h2))
        width, height = img.size
        
        if (width > 300):
            img = img.resize(size=(360, 360), resample=1)
            img.save(os.path.join(source_path, 'cropped', img_paths[i]))
        else:
            pass
        
        img.close()


def resize_crop_win(crop_w1, crop_h1, crop_w2, crop_h2):
    d_width = int(crop_w2 - crop_w1)
    d_height = int(crop_h2 - crop_h1)

    if (d_width == d_height):
        pass

    elif (d_width > d_height):
        d_scale = d_width - d_height
        crop_h1 -= int(d_scale / 2)
        if ((d_scale % 2) == 1): 
            crop_h2 += int((d_scale / 2) + 1)
        else:
            crop_h2 += int((d_scale / 2))

    elif (d_height > d_width):
        d_scale = d_height - d_width
        crop_w1 -= int(d_scale / 2)
        if ((d_scale % 2) == 1): 
            crop_w2 += int((d_scale / 2) + 1)
        else:
            crop_w2 += int((d_scale / 2))

    return crop_w1, crop_h1, crop_w2, crop_h2