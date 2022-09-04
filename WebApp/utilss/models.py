from os import walk
from wsgiref.simple_server import sys_version
import cv2
import pandas as pd
import numpy as np
from PIL import Image
from utilss.BROIsExtractUtils import seperateBROIs
from utilss.roisExtractUtils import extractROI
import torch
import numpy as np
import utilss.predictBoneAge as predictBoneAge 
import pandas as pd
import sys

from app import *

def process_image(filename):
    imagePath = filename
    savePredictedBroiPath = "static/uploads"
    savePredictedRoiPath = "static/uploads"

    
    # Loading Yolo model for BROI detection
    BROImodel = torch.hub.load(f"models/yolov5", 'custom', path="models/broi.pt", source='local', force_reload=True)

    # Creating ROI extract instances
    roiExtrator = {
        'wrist': extractROI('wrist', save=True, savePath=savePredictedRoiPath),
        'thumb': extractROI('thumb', save=True, savePath=savePredictedRoiPath),
        'little': extractROI('little', save=True, savePath=savePredictedRoiPath),
        'middle': extractROI('middle', save=True, savePath=savePredictedRoiPath)
    }
    # The detected BROIs are saved and in variable
    BROIs = seperateBROIs(BROImodel, img_path=imagePath, image=None, save=True, savePath=savePredictedBroiPath)

    ROIs = {}
    for k, v in BROIs.items():
        if np.any(v) and k!="org":
            ROIs.update(roiExtrator[k].extract(imageName=None, image=v))

    predictedAge = predictBoneAge.predict(ROIs)

    csvData = pd.read_csv("static/csv/cleaned-training-dataset.csv")
    imageId = imagePath.split("/")[-1].split(".")[0]
    orgAge = csvData[csvData['id']==int(imageId)].boneage.values[0]

    broisPath = {}
    roisPaths = {}

    for k, v in BROIs.items():
        if np.any(v):
            broisPath[k] = f"{savePredictedBroiPath}/{k}.png"

    for k, v in ROIs.items():
        if np.any(v):
            broisPath[k] = f"{savePredictedRoiPath}/{k}.png"

    #print(predictedAge)
    #print(f"predicted median age : {np.median(predictedAge, axis=0)}\npredicted mean age : {}\nOriginal Age : {orgAge}")

    return broisPath, roisPaths, predictedAge.mean(), orgAge