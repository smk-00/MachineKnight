# MachineKnight

All the Data analysis and model training are in ML folder. <br>
All the Frontend and Flask application are in WebApp folder.

The **prediction** for the **test data** are in the **/ML/submission.csv**.<br>

The Exploratory Data Analysis & Data Prepration are done in **EDA_DataPrep.ipynb** file.<br>

The model architecture and training are in **train.ipynb** file.


# MACHINE LEARNING APPROACH
It is a **regression** task. The features are in countinous and categorial.

## Pipeline for data prepration.
1. Converting a categorical to numerical data.
2. Removing the outliers.
3. The new features are added.
    i) No. of bathroom, balconies, cup_board per floor
    ii) Ratio of bathroom, balconies, cup_board with respect to property size
4. Then the data is normalized to certain range using RobustScaling methods.

## Model Training
1. The **deep neural network** model is trained using **K-Fold**.
2. The same data is used to train other 4 models BaggingRegressor, ExtraTreesRegressor, RandomForestRegressor, ExtraTreesRegressor.
3. All these models are ensembled for prediction.


# Frontend & Flask App
The API was developed in python FLASK.<br>

>> pip install -r requirements.py <br>
>> python WebApp/main.py<br>

Check the **www.localhost:5000** for the frontend.