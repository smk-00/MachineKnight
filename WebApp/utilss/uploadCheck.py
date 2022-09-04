from os import walk
import cv2
import pandas as pd
import numpy as np
from PIL import Image

from app import *

# Helper Constant and Function
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

def file_saver(filename):
    file = os.path.splitext(filename)
    org = Image.open(os.path.join(
        app.config['UPLOAD_FOLDER'], filename))
    org.save(os.path.join(app.config['UPLOAD_FOLDER'], (file[0] + '.csv')))
    if file[1] != '.csv':
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return str(file[0] + '.csv')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def erase_dir():
    f = next(walk('static/uploads/'), (None, None, []))[2]
    for ele in f:
        os.remove('static/uploads/'+ele)