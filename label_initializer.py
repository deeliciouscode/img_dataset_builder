from os import listdir
from os.path import isfile, join


def initialize():
    print("filepath?")
    #path = input()
    path = "../empty_wheelchairs"
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    return file_list, path
