# MachineKnight 🤖

All the Data analysis and model training are in ML folder. <br>
All the Frontend and Flask application are in WebApp folder.<br>
**As the size of model are more than 20 MB the Model Weights are in drive. Download the model from GDRIVE the link is in WebApp/models/ .txt file and place them in same WebApp/models/ directory** <Br>

``` diff
- The **prediction** for the **test data** are in the **/ML/submission.csv**. 
```

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
1. The **deep neural network** model is trained using **K-Fold**.<br>
    i)  The **"Mean Absolute Error"** is used as loss function.<br>
    ii) The training **MAE loss** for the model is about **2700** and **RMSE** is about **3764**<br>
    iii) In each fold the model is trained for **100 epochs** with the **learning rate** of **1e-3**.<br>
2. The same data is used to train other 4 models BaggingRegressor, ExtraTreesRegressor, RandomForestRegressor, GradientBoostingRegressor at the end they are with the training RMSE loss of 3770, 3923, 3773, 3731.
3. All these models are ensembled for prediction.

# Frontend & Flask App
![image](https://user-images.githubusercontent.com/65153292/188326798-d6039c1c-2d37-4123-b277-4792807b6a69.png)
![image](https://user-images.githubusercontent.com/65153292/188326833-c7a8839c-2c46-49b1-b340-7e857682472f.png)

The API was developed in python FLASK.<br>

```diff
>> pip install -r requirements.py <br>
>> cd WebApp <br>
>> python main.py<br>
```

Check the **www.localhost:5000** for the frontend.
