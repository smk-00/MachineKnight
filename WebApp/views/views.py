from flask import Flask, flash, redirect, render_template, request, url_for
from app import *



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
    rois = {}
    brois = {}

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
