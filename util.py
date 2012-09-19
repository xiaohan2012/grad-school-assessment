import os
from config import *

def get_all_schools():
    return [l.split()[0] for l in open(os.path.join(PROJ_PATH , "usnew-urls.txt"),"r").readlines()]
