import os
from PIL import Image
from helper_functions import get_ratios
import csv
import pandas as pd

def bound(source_path, coords):
    """crops the images down to the specified coordinates in the coords dict"""
    print("what label do you want?")
    label = input()
    csv_lines = []
    gs_directory = "gs://nemo_wheelchair_object_detection/"
    path_csv_temp = os.path.join(source_path, "bound", "google_import_temp.csv")
    path_csv = os.path.join(source_path, "bound", "google_import.csv")

    for key in coords:
        img = Image.open(os.path.join(source_path, key))
        ratio_x1, ratio_y1, ratio_x2, ratio_y2 = get_ratios(coords[key][0][0], coords[key][0][1],
                                                            coords[key][1][0], coords[key][1][1],
                                                            coords[key][2][0], coords[key][2][1])
        print(key)
        print(ratio_x1, ratio_y1, ratio_x2, ratio_y2)

        csv_lines.append(["", gs_directory+key, label, str(round(ratio_x1, 3)), str(round(ratio_y1, 3)), "", "",
                                                    str(round(ratio_x2, 3)), str(round(ratio_y2, 3)), "", ""])

        img.close()

    with open(path_csv_temp, 'w') as csv_file:
        for entry in csv_lines:
            file_writer = csv.writer(csv_file, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(entry)

    with open(path_csv_temp) as in_file:
        df = pd.read_csv(in_file, header=None)
        df.to_csv(path_csv, index=False, header=None)

    print(csv_lines)
