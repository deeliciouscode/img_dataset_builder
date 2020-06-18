import os
from PIL import Image
from helper_functions import get_ratios


def crop(source_path, coords):
    """"crops the images down to the specified coordinates in the coords dict"""
    for key in coords:
        img = Image.open(os.path.join(source_path, key))
        ratio_x1, ratio_y1, ratio_x2, ratio_y2 = get_ratios(coords[key][0][0], coords[key][0][1],
                                                            coords[key][1][0], coords[key][1][1],
                                                            coords[key][2][0], coords[key][2][1])
        print(key)
        print(ratio_x1, ratio_y1, ratio_x2, ratio_y2)
        
        width, height = img.size
        crop_w1 = width * ratio_x1
        crop_h1 = height * ratio_y1
        crop_w2 = width * ratio_x2
        crop_h2 = height * ratio_y2
        print(width, height)
        print(crop_w1, crop_h1, crop_w2, crop_h2)
        
        crop_w1, crop_h1, crop_w2, crop_h2 = resize_crop_win(crop_w1, crop_h1, crop_w2, crop_h2)

        img_c = img.crop((crop_w1, crop_h1, crop_w2, crop_h2))
        width, height = img.size
            
        if width > 300:
            img_c = img_c.resize(size=(360, 360), resample=1)
            img_c.save(os.path.join(source_path, 'cropped', key))
        else:
            pass
        
        img.close()


def resize_crop_win(crop_w1, crop_h1, crop_w2, crop_h2):
    """resizes the crop window to a square shape"""
    d_width = int(crop_w2 - crop_w1)
    d_height = int(crop_h2 - crop_h1)

    if d_width == d_height:
        pass

    elif d_width > d_height:
        d_scale = d_width - d_height
        crop_h1 -= int(d_scale / 2)
        if (d_scale % 2) == 1:
            crop_h2 += int((d_scale / 2) + 1)
        else:
            crop_h2 += int((d_scale / 2))

    elif d_height > d_width:
        d_scale = d_height - d_width
        crop_w1 -= int(d_scale / 2)
        if (d_scale % 2) == 1:
            crop_w2 += int((d_scale / 2) + 1)
        else:
            crop_w2 += int((d_scale / 2))

    return crop_w1, crop_h1, crop_w2, crop_h2
