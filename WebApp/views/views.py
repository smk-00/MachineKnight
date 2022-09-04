from flask import Flask, flash, redirect, render_template, request, url_for
from app import *
from utilss.uploadCheck import *
from utilss.models import *


import os
from os import walk
import cv2
import pandas as pd
import numpy as np
from PIL import Image

# ---------------------------------------------------------- #
# Main Page
@app.route('/')
def home():
    #return render_template('index.html') # Landing Page If Required
    return render_template('upload.html')

# ---------------------------------------------------------- #
# Uplaod Get
@app.route('/upload', methods=['GET'])
def UplaodGet():
    return render_template('upload.html')

#Upload Post
@app.route('/upload', methods=['POST'])
def UplaodPost():
    rois = {}
    brois = {}

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        erase_dir()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        file_saver(file.filename)
        # Further Process can be done here #
        brois, rois, orginal_age, predicted_age = process_image("static/uploads/"+file.filename)
        print(brois,rois,orginal_age,predicted_age)
        #return render_template('result.html', orginal_path="static/uploads/"+file.filename, rois=rois, brois=brois, orginal_age=orginal_age, predicted_age=predicted_age)

    else:
        flash('Allowed image types are -> csv, xlsx')
        return redirect(request.url)
# ---------------------------------------------------------- #
# About an Contact Routes
@app.route('/about')
def about():
    return render_template('about.html')
