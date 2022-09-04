from flask import Flask, flash, redirect, render_template, request, url_for
from app import *
from utils import *


import os
from os import walk
import cv2
import pandas as pd
import numpy as np
from PIL import Image


# Main Page
@app.route('/')
def home():
    return render_template('index.html')

#result Get
@app.route('/result', methods=['GET'])
def UplaodGet():
    return render_template('upload.html')

#result Post
@app.route('/result', methods=['POST'])
def UplaodPost():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)

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

        predict_data = loadData(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        df, row_id = preProcessDf(predict_data)
        final = predict(df)

        return render_template('result.html', final_pred=final, row_id=row_id)