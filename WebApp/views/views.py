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
    return render_template('upload.html')

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
        
        final_csv = pd.DataFrame()
        final_csv['id'] = row_id
        final_csv['rent'] = final
        
        final_csv.to_csv('./static/uploads/result.csv', index=False)

        return render_template('result.html', final_pred=final, row_id=row_id, length=len(final), csv='./static/uploads/result.csv')

    else:
        flash('Allowed file types are -> csv')
        return redirect(request.url)